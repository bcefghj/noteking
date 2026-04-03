"""Download engine: yt-dlp wrapper with proxy, cookie, and batch support."""

from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator

from .config import AppConfig


@dataclass
class VideoMeta:
    title: str = ""
    description: str = ""
    duration: float = 0.0
    uploader: str = ""
    upload_date: str = ""
    thumbnail: str = ""
    webpage_url: str = ""
    chapters: list[dict] = field(default_factory=list)
    subtitles: dict = field(default_factory=dict)
    entries: list[dict] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    @property
    def has_subtitles(self) -> bool:
        return bool(self.subtitles)

    @property
    def is_playlist(self) -> bool:
        return bool(self.entries)

    @property
    def entry_count(self) -> int:
        return len(self.entries) if self.entries else 1


BILIBILI_COOKIES_FILE = Path("/app/bilibili_cookies.txt")


def _base_cmd(config: AppConfig) -> list[str]:
    import os
    from urllib.parse import unquote

    cmd = ["yt-dlp", "--no-warnings"]

    # 代理：配置优先，其次读环境变量
    proxy = config.proxy.for_ytdlp or os.environ.get("NOTEKING_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        cmd += ["--proxy", proxy]

    # B站 cookies：文件优先，其次用 SESSDATA 生成临时文件
    if BILIBILI_COOKIES_FILE.exists():
        cmd += ["--cookies", str(BILIBILI_COOKIES_FILE)]
    else:
        sessdata = config.bilibili_sessdata or os.environ.get("BILIBILI_SESSDATA", "")
        if sessdata:
            decoded = unquote(sessdata)
            tmp = Path(tempfile.mktemp(suffix="_bili_cookies.txt"))
            tmp.write_text(
                f"# Netscape HTTP Cookie File\n"
                f".bilibili.com\tTRUE\t/\tTRUE\t9999999999\tSESSDATA\t{decoded}\n"
            )
            cmd += ["--cookies", str(tmp)]

    return cmd


def get_video_info(url: str, config: AppConfig) -> VideoMeta:
    """Fetch metadata without downloading."""
    cmd = _base_cmd(config) + [
        "--dump-json",
        "--flat-playlist",
        "--no-download",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp info failed: {result.stderr[:500]}")

    lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
    if not lines:
        raise RuntimeError("yt-dlp returned no data")

    entries = []
    first = json.loads(lines[0])

    if len(lines) > 1:
        for line in lines:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return VideoMeta(
        title=first.get("title", ""),
        description=first.get("description", ""),
        duration=first.get("duration", 0) or 0,
        uploader=first.get("uploader", ""),
        upload_date=first.get("upload_date", ""),
        thumbnail=first.get("thumbnail", ""),
        webpage_url=first.get("webpage_url", url),
        chapters=first.get("chapters") or [],
        subtitles=first.get("subtitles") or {},
        entries=entries if len(entries) > 1 else [],
        extra={"id": first.get("id", "")},
    )


def download_subtitles(
    url: str,
    output_dir: Path,
    config: AppConfig,
    langs: str = "zh-Hans,zh-CN,zh,ai-zh,en",
) -> list[Path]:
    """Download subtitles using yt-dlp."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = _base_cmd(config) + [
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", langs,
        "--convert-subs", "srt",
        "--skip-download",
        "-o", str(output_dir / "%(title)s.%(ext)s"),
        url,
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return list(output_dir.glob("*.srt"))


def download_audio(
    url: str,
    output_dir: Path,
    config: AppConfig,
) -> Path:
    """Extract audio from video for ASR."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "audio.wav"
    cmd = _base_cmd(config) + [
        "-x",
        "--audio-format", "wav",
        "--audio-quality", "0",
        "-o", str(output_path),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        raise RuntimeError(f"Audio download failed: {result.stderr[:500]}")

    wavs = list(output_dir.glob("*.wav"))
    if wavs:
        return wavs[0]
    raise FileNotFoundError("No WAV file produced")


def download_video(
    url: str,
    output_dir: Path,
    config: AppConfig,
    quality: str = "best",
) -> Path:
    """Download video file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = _base_cmd(config) + [
        "-f", quality,
        "-o", str(output_dir / "%(title)s.%(ext)s"),
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if result.returncode != 0:
        raise RuntimeError(f"Video download failed: {result.stderr[:500]}")

    for ext in ("mp4", "mkv", "webm", "flv"):
        vids = list(output_dir.glob(f"*.{ext}"))
        if vids:
            return vids[0]
    raise FileNotFoundError("No video file produced")


def download_thumbnail(
    url: str,
    output_dir: Path,
    config: AppConfig,
) -> Path | None:
    """Download video thumbnail/cover image."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = _base_cmd(config) + [
        "--write-thumbnail",
        "--skip-download",
        "--convert-thumbnails", "jpg",
        "-o", str(output_dir / "thumbnail"),
        url,
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    for ext in ("jpg", "png", "webp"):
        thumbs = list(output_dir.glob(f"thumbnail*.{ext}"))
        if thumbs:
            return thumbs[0]
    return None


def list_playlist_entries(url: str, config: AppConfig) -> list[dict]:
    """List all entries in a playlist/collection."""
    cmd = _base_cmd(config) + [
        "--flat-playlist",
        "--dump-json",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    entries = []
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries
