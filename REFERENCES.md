# 参考项目与致谢

NoteKing 的开发过程中参考了大量优秀的开源项目和同类产品，在此表示感谢。

---

## 核心依赖

NoteKing 基于以下开源工具构建，感谢所有贡献者的辛勤工作：

| 项目 | 用途 | 许可证 |
|------|------|--------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | 视频下载核心引擎，支持 1800+ 网站 | Unlicense |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | LLM API 统一接口 | Apache 2.0 |
| [FastAPI](https://github.com/tiangolo/fastapi) | 高性能 REST API 框架 | MIT |
| [Next.js](https://github.com/vercel/next.js) | React 全栈 Web 框架 | MIT |
| [React](https://github.com/facebook/react) | 前端 UI 库 | MIT |
| [Tailwind CSS](https://github.com/tailwindlabs/tailwindcss) | 原子化 CSS 框架 | MIT |
| [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | 视频场景检测与关键帧提取 | BSD 3-Clause |
| [OpenCV](https://github.com/opencv/opencv-python) | 计算机视觉库 | Apache 2.0 |
| [Pillow](https://github.com/python-pillow/Pillow) | 图像处理 | HPND |
| [ImageHash](https://github.com/JohannesBuchner/imagehash) | 感知哈希去重 | BSD 2-Clause |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | 高性能 ASR 语音识别 | MIT |
| [Whisper](https://github.com/openai/whisper) | OpenAI 语音识别模型 | MIT |
| [LaTeX / tcolorbox](https://ctan.org/pkg/tcolorbox) | 专业 PDF 排版与彩色知识框 | LPPL |
| [react-markdown](https://github.com/remarkjs/react-markdown) | Markdown 渲染组件 | MIT |
| [Pydantic](https://github.com/pydantic/pydantic) | 数据验证 | MIT |
| [Uvicorn](https://github.com/encode/uvicorn) | ASGI 服务器 | BSD 3-Clause |
| [Docker](https://www.docker.com/) | 容器化部署 | Apache 2.0 |

---

## 同类产品调研

在设计 NoteKing 的功能和架构时，我们调研了以下同类产品和项目，从中汲取了灵感：

### 商业产品

| 产品 | 简介 | 特色 |
|------|------|------|
| [NoteGPT](https://notegpt.io/) | AI 视频笔记工具 | 支持多种视频平台，提供 Chrome 扩展 |
| [Glarity](https://glarity.app/) | YouTube/Google AI 摘要 | 浏览器扩展，实时生成摘要 |
| [BibiGPT](https://bibigpt.co/) | B站/YouTube AI 摘要 | 专注中文视频摘要 |
| [Summarize.tech](https://www.summarize.tech/) | AI 视频摘要 | 简洁的 Web 界面 |
| [NotebookLM](https://notebooklm.google.com/) | Google AI 笔记工具 | 多源知识整合、AI 对话 |
| [Notion AI](https://www.notion.so/product/ai) | AI 写作助手 | 集成在 Notion 中的 AI 功能 |
| [Otter.ai](https://otter.ai/) | AI 会议记录 | 实时语音转文字 |
| [Fireflies.ai](https://fireflies.ai/) | AI 会议记录 | 自动会议总结和行动项 |
| [Descript](https://www.descript.com/) | 音视频编辑 | 基于文本的视频编辑 |
| [Recall.ai](https://recall.ai/) | AI 知识管理 | 视频/播客/文章自动总结 |

### 浏览器扩展

| 扩展 | 简介 |
|------|------|
| [YouTube Summary with ChatGPT](https://glasp.co/youtube-summary) | Chrome 扩展，一键生成 YouTube 视频摘要 |
| [Glasp](https://glasp.co/) | 社交化高亮和笔记工具 |
| [Eightify](https://eightify.app/) | YouTube 视频 AI 总结扩展 |
| [Notta](https://www.notta.ai/) | 实时语音转文字 Chrome 扩展 |

### 开源项目

| 项目 | 简介 | GitHub |
|------|------|--------|
| [VideoSummary](https://github.com/matthayas/VideoSummary) | 开源视频摘要工具 | Python |
| [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) | YouTube 字幕提取 API | Python |
| [bilibili-api](https://github.com/Nemo2011/bilibili-api) | B站 API 封装 | Python |
| [whisper.cpp](https://github.com/ggerganov/whisper.cpp) | Whisper 的 C++ 移植版本 | C++ |
| [markmap](https://github.com/markmap/markmap) | Markdown 思维导图可视化 | TypeScript |
| [Quivr](https://github.com/QuivrHQ/quivr) | AI 第二大脑 | Python |
| [tldraw/make-real](https://github.com/tldraw/make-real) | AI 生成 UI | TypeScript |
| [langchain](https://github.com/langchain-ai/langchain) | LLM 应用开发框架 | Python |

### AI Agent 与 Skill 生态

| 项目 | 简介 |
|------|------|
| [OpenClaw](https://openclaw.ai/) | 开源 AI Agent 平台 |
| [Claude Code](https://docs.anthropic.com/claude/docs/claude-code) | Anthropic 编程 Agent |
| [Cursor](https://cursor.com/) | AI 编程 IDE |
| [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 自主 AI Agent |

---

## NoteKing 的差异化

NoteKing 在调研以上产品后，重点在以下方面做出差异化：

1. **图文并茂的 LaTeX PDF 讲义** - 不只是文字摘要，而是带关键帧截图、结构化章节、高亮知识框的专业讲义
2. **13 种输出模板** - 覆盖学习笔记、闪卡、测验、考试复习等多种场景
3. **30+ 平台支持** - 通过 yt-dlp 支持几乎所有视频网站
4. **批量处理** - 支持整个课程合集一键处理
5. **多种部署方式** - CLI、Web、Docker、MCP、OpenClaw Skill、桌面应用
6. **完全开源** - MIT 许可证，可自由使用和修改
7. **流式输出** - 实时展示 AI 生成过程

---

## 声明

NoteKing 是一个独立开发的开源项目。以上所列产品和项目的名称、商标归各自所有者所有。本项目与上述任何产品和项目不存在合作或从属关系，列出它们仅为致谢和参考说明。
