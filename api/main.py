"""FastAPI application entry point."""

from __future__ import annotations

import time
from collections import defaultdict
from datetime import date

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes.video import router as video_router
from api.routes.config import router as config_router

DAILY_LIMIT = 20
_usage: dict[str, int] = defaultdict(int)
_usage_date: str = ""

app = FastAPI(
    title="NoteKing API",
    description=(
        "The ultimate video/blog to learning notes API. "
        "Supports 30+ platforms with 13 output templates."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Limit"],
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    global _usage, _usage_date

    today = date.today().isoformat()
    if _usage_date != today:
        _usage = defaultdict(int)
        _usage_date = today

    rate_limited_prefixes = ("/api/v1/summarize",)
    path = request.url.path
    is_limited = any(path.startswith(p) for p in rate_limited_prefixes)

    if is_limited and request.method == "POST":
        client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        if not client_ip:
            client_ip = request.client.host if request.client else "unknown"

        used = _usage[client_ip]
        remaining = max(0, DAILY_LIMIT - used)

        if used >= DAILY_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"今日免费次数已用完（{DAILY_LIMIT}次/天），明天再来吧~",
                    "limit": DAILY_LIMIT,
                    "remaining": 0,
                },
                headers={
                    "X-RateLimit-Limit": str(DAILY_LIMIT),
                    "X-RateLimit-Remaining": "0",
                },
            )

        _usage[client_ip] += 1
        remaining = max(0, DAILY_LIMIT - _usage[client_ip])

        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(DAILY_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

    return await call_next(request)


app.include_router(video_router)
app.include_router(config_router)


@app.get("/")
async def root():
    return {
        "name": "NoteKing API",
        "version": "0.1.0",
        "docs": "/docs",
        "templates": "/api/v1/templates",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


def start():
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
