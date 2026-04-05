"""Video processing API routes."""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Generator

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel

from api.models.schemas import (
    VideoRequest, VideoResponse, BatchRequest, BatchResponse,
    TemplateInfo, ErrorResponse,
)
from core.config import AppConfig, LLMConfig
from core import summarize
from core.templates import TEMPLATE_LIST

router = APIRouter(prefix="/api/v1", tags=["video"])


def _load_config() -> AppConfig:
    """Load config from environment variables (called on each request)."""
    cfg = AppConfig()
    if os.environ.get("NOTEKING_LLM_API_KEY"):
        cfg.llm.api_key = os.environ["NOTEKING_LLM_API_KEY"]
    if os.environ.get("NOTEKING_LLM_BASE_URL"):
        cfg.llm.base_url = os.environ["NOTEKING_LLM_BASE_URL"]
    if os.environ.get("NOTEKING_LLM_MODEL"):
        cfg.llm.model = os.environ["NOTEKING_LLM_MODEL"]
    if os.environ.get("BILIBILI_SESSDATA"):
        cfg.bilibili_sessdata = os.environ["BILIBILI_SESSDATA"]
    if os.environ.get("NOTEKING_PROXY"):
        cfg.proxy.enabled = True
        cfg.proxy.http = os.environ["NOTEKING_PROXY"]
        cfg.proxy.https = os.environ["NOTEKING_PROXY"]
    if not cfg.llm.api_key:
        raise RuntimeError(
            "No LLM API key configured. Set it via config file, "
            "environment variable NOTEKING_LLM_API_KEY, or --api-key flag."
        )
    return cfg


def _sse_event(stage: str, **kwargs) -> str:
    data = {"stage": stage, **kwargs}
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/summarize", response_model=VideoResponse)
async def summarize_video(req: VideoRequest):
    """Process a single video and generate notes."""
    try:
        cfg = _load_config()
        result = summarize(
            url=req.url,
            template=req.template,
            config=cfg,
            custom_prompt=req.custom_prompt,
            use_cache=req.use_cache,
        )
        return VideoResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
            template=result.get("template", req.template),
            source=result.get("source", ""),
            platform=result.get("platform", ""),
            url=result.get("url", req.url),
            duration=result.get("duration", 0),
            output_file=result.get("output_file", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize/stream")
async def summarize_video_stream(req: VideoRequest):
    """Process a video with SSE streaming progress."""

    def generate() -> Generator[str, None, None]:
        try:
            cfg = _load_config()

            yield _sse_event("info", message="正在获取视频信息...")
            from core.parser import parse_link, Platform, is_batch
            from core.downloader import get_video_info, VideoMeta
            from core.subtitle import extract_subtitles, SubtitleResult
            from core.llm import chat_stream
            from core.templates import get_template, TemplateContext
            from core.cache import Cache

            parsed = parse_link(req.url)
            meta = get_video_info(req.url, cfg)

            yield _sse_event("info", message=f"视频: {meta.title}",
                             title=meta.title, duration=meta.duration,
                             platform=parsed.platform.value)

            cache = Cache(cfg)
            cached = cache.get(req.url, req.template)
            if cached and req.use_cache:
                content = cached.get("content", "")
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                yield _sse_event("done",
                                 title=cached.get("title", ""),
                                 content=content,
                                 template=req.template,
                                 source=cached.get("source", ""),
                                 platform=parsed.platform.value,
                                 duration=meta.duration)
                return

            yield _sse_event("subtitle", message="正在提取字幕...")
            work_dir = Path(tempfile.mkdtemp(prefix="noteking_"))
            subs = extract_subtitles(parsed, work_dir, cfg, skip_asr=True)

            if not subs.segments and subs.source == "visual":
                subs = SubtitleResult(
                    segments=[], source="visual",
                    raw_text=f"标题:{meta.title}\n简介:{meta.description[:800]}",
                )

            yield _sse_event("subtitle",
                             message=f"字幕来源: {subs.source}",
                             source=subs.source)

            # ── 关键帧提取（仅 latex_pdf 模板）──────────────────────────────
            frames_b64: dict[str, str] = {}   # {"frame_00.jpg": "<base64>", ...}
            frames_info: list[dict] = []       # [{"name": "...", "ts": 12.5}, ...]
            if req.template == "latex_pdf":
                try:
                    from core.downloader import download_video
                    from core.frames import extract_keyframes
                    import base64

                    yield _sse_event("info", message="正在下载视频提取截图（约1-3分钟）...")
                    frames_dir = work_dir / "frames"
                    frames_dir.mkdir(exist_ok=True)

                    video_path = download_video(req.url, work_dir / "video", cfg,
                                                quality="bestvideo[height<=720]+bestaudio/best[height<=720]/best")
                    yield _sse_event("info", message="正在提取关键帧...")
                    kframes = extract_keyframes(video_path, frames_dir, max_frames=12)

                    for i, f in enumerate(kframes):
                        name = f"frame_{i:02d}.jpg"
                        dst = frames_dir / name
                        if not dst.exists() and f.path.exists():
                            dst = f.path
                        if dst.exists():
                            frames_b64[name] = base64.b64encode(dst.read_bytes()).decode()
                            frames_info.append({"name": name, "ts": f.timestamp,
                                                "ts_str": f.timestamp_str})
                    yield _sse_event("info",
                                     message=f"已提取 {len(frames_info)} 张关键帧")
                except Exception as fe:
                    yield _sse_event("info", message=f"截图提取跳过: {fe}")
            # ────────────────────────────────────────────────────────────────

            yield _sse_event("generating", message="AI 正在生成笔记...")
            tmpl = get_template(req.template, user_prompt=req.custom_prompt)
            ctx = TemplateContext(
                meta=meta, subtitles=subs, config=cfg,
                extra={"custom_prompt": req.custom_prompt,
                       "frames_info": frames_info},
            )
            prompt = tmpl.build_prompt(ctx)
            system = tmpl.system_prompt(ctx)

            full_content = ""
            in_think = False
            for chunk in chat_stream(prompt, cfg, system=system):
                full_content += chunk
                if "<think>" in chunk:
                    in_think = True
                if "</think>" in chunk:
                    in_think = False
                    continue
                if not in_think:
                    yield _sse_event("generating", content=chunk)

            content = re.sub(r"<think>.*?</think>", "", full_content, flags=re.DOTALL).strip()
            content = tmpl.post_process(content, ctx)

            result = {
                "title": meta.title,
                "content": content,
                "template": req.template,
                "source": subs.source,
                "url": req.url,
                "platform": parsed.platform.value,
                "duration": meta.duration,
                "frames_b64": frames_b64,   # 传给前端，下载 PDF 时回传给编译服务
            }
            cache.set(req.url, req.template, result)

            yield _sse_event("done", **result)

        except Exception as e:
            yield _sse_event("error", message=str(e))

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/batch", response_model=BatchResponse)
async def batch_summarize(req: BatchRequest):
    """Process a playlist/collection."""
    try:
        cfg = _load_config()
        result = summarize(
            url=req.url,
            template=req.template,
            config=cfg,
        )
        return BatchResponse(
            title=result.get("title", ""),
            content=result.get("content", ""),
            template=result.get("template", req.template),
            total=result.get("total", 1),
            completed=result.get("completed", 1),
            failed=result.get("failed", []),
            output_file=result.get("output_file", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates", response_model=list[TemplateInfo])
async def list_templates():
    """List all available output templates."""
    return [TemplateInfo(**t) for t in TEMPLATE_LIST]


@router.get("/info")
async def get_video_info_endpoint(url: str):
    """Get video metadata without processing."""
    from core.downloader import get_video_info as fetch_info
    try:
        cfg = _load_config()
        meta = fetch_info(url, cfg)
        return {
            "title": meta.title,
            "uploader": meta.uploader,
            "duration": meta.duration,
            "thumbnail": meta.thumbnail,
            "has_subtitles": meta.has_subtitles,
            "is_playlist": meta.is_playlist,
            "entry_count": meta.entry_count,
            "chapters": meta.chapters,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/transcript")
async def get_transcript(url: str):
    """Get only the transcript text."""
    from core import get_transcript as fetch_transcript
    try:
        cfg = _load_config()
        text = fetch_transcript(url, cfg)
        return {"url": url, "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


LATEX_COMPILER_URL = os.environ.get("LATEX_COMPILER_URL", "http://host.docker.internal:9090")


class LatexCompileRequest(BaseModel):
    tex_content: str
    filename: str = "noteking_notes"


@router.post("/compile-latex")
async def compile_latex(req: LatexCompileRequest):
    """Proxy LaTeX compilation to the host-side compiler service."""
    safe_name = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', req.filename)[:80]
    try:
        transport = httpx.AsyncHTTPTransport()
        async with httpx.AsyncClient(timeout=180, transport=transport) as client:
            resp = await client.post(
                f"{LATEX_COMPILER_URL}/compile",
                json={"tex_content": req.tex_content, "filename": req.filename},
            )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="LaTeX 编译服务未启动，请联系管理员")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LaTeX 编译超时（>180秒）")

    if resp.status_code != 200:
        detail = "LaTeX 编译失败"
        try:
            detail = resp.json().get("error", detail)
        except Exception:
            pass
        raise HTTPException(status_code=resp.status_code, detail=detail)

    from urllib.parse import quote
    encoded_name = quote(f"{safe_name}.pdf")
    return Response(
        content=resp.content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}",
        },
    )
