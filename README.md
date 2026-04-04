# NoteKing 笔记之王

> **一键把视频变成精美图文 PDF 讲义 —— 全网最强视频笔记工具**

[![GitHub](https://img.shields.io/badge/GitHub-bcefghj%2Fnoteking-blue?logo=github)](https://github.com/bcefghj/noteking)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![小红书](https://img.shields.io/badge/小红书-bcefghj-red)](https://www.xiaohongshu.com/user/profile/bcefghj)

---

## 🚀 升级版来了 → NoteKing Pro

> 本仓库是 **NoteKing v1（视频笔记）**，专注在线视频转 PDF 讲义。
>
> 如果你还需要处理**本地录音/会议**，请移步升级版：

| | NoteKing（本仓库） | [NoteKing Pro](https://github.com/bcefghj/noteking-pro) |
|--|--|--|
| 在线视频转笔记 | ✅ | ✅ |
| 本地录音/会议处理 | ❌ | ✅ |
| 说话人分离（多人会议） | ❌ | ✅ |
| 降噪增强 | ❌ | ✅ |
| 多文件合并 | ❌ | ✅ |
| 输出模板数量 | 13 种 | 23 种 |
| MCP Server 工具 | 基础 | 扩展版 |
| 案例演示 | MiniMind 课程 | OpenClaw 圆桌会议 |

**👉 [点击进入 NoteKing Pro →](https://github.com/bcefghj/noteking-pro)**

---

### 在线体验

**[http://150.158.123.30:3000](http://150.158.123.30:3000)** - 无需安装，直接使用（每日免费 20 次）

---

## 这是什么？

你有没有遇到过这些情况：

- B站收藏了几十个课程合集，但根本没时间看？
- YouTube 上有很好的教程，但看视频效率太低？
- 想把一个 3 小时的课程变成可以打印、可以复习的讲义？

**NoteKing** 就是来解决这些问题的。给它一个视频链接，它就能自动：

```
视频链接 → 下载视频 → 智能截取关键帧 → 提取字幕/语音 → AI生成笔记 → 输出精美PDF讲义
```

---

## 核心卖点：图文并茂的 PDF 讲义

这不是简单的"视频转文字"，而是 **带关键帧截图、结构化章节、高亮知识框** 的专业讲义：

| 功能 | 说明 |
|------|------|
| 🎯 智能关键帧提取 | 场景检测 + 信息密度评分 + 感知哈希去重，自动挑选最有价值的画面 |
| 📐 专业 LaTeX 排版 | tcolorbox 高亮框、代码高亮、数学公式、封面、目录、页眉页脚 |
| 📚 13 种输出模板 | 详细笔记、简要总结、思维导图、闪卡、测验题、考试复习、时间线…… |
| 🌍 30+ 平台支持 | B站、YouTube、抖音、小红书、快手、TikTok、Twitter 等 |
| 🔄 批量处理 | 整个课程合集（比如 26 集的课）一键全部处理 |
| 🔁 字幕三级回退 | 平台字幕 → Whisper ASR → 纯视觉模式 |

---

## 实际效果展示

> 以下全部是 NoteKing 自动生成的真实结果，源文件在 [`demos/minimind/`](demos/minimind/) 目录。

### 案例：MiniMind 课程（B站 26 集完整合集）

原始视频：[【2025/Minimind】Only三小时！Pytorch从零手敲大模型](https://www.bilibili.com/video/BV1T2k6BaEeC/)

NoteKing 把这个 26 集、3.3 小时的完整课程，自动处理成了 **31.3 MB 的图文 PDF 讲义合集**。

#### PDF 讲义效果（LaTeX 专业排版）

每一集都包含：

- **封面页**：课程标题、视频信息、NoteKing 品牌
- **自动目录**：根据章节结构自动生成
- **关键帧截图**：智能选取的视频画面，插入在对应知识点旁边
- **高亮知识框**：
  - 🟡 重点提示框（黄色）—— 核心知识点
  - 🔵 背景知识框（蓝色）—— 补充说明
  - 🔴 注意事项框（红色）—— 易错点警告
  - 🟢 总结框（绿色）—— 章节小结
- **代码块**：深色主题 + 语法高亮 + 行号
- **数学公式**：原生 LaTeX 渲染
- **页眉页脚**：NoteKing 品牌 + 页码 + 社交链接

#### 26 集完整 PDF 列表

| 集数 | 标题 | PDF 大小 |
|------|------|----------|
| P01 | 开篇 | 863 KB |
| P02 | 前言 | 1.1 MB |
| P03 | 必看：前言补充 | 1.4 MB |
| P04 | 前置知识 | 850 KB |
| P05 | 架构图解读 | 1.1 MB |
| P06 | 初始化项目 | 1.2 MB |
| P07 | 理论：RMSNorm | 1.0 MB |
| P08 | 代码：RMSNorm | 1.2 MB |
| P09 | 理论：RoPE & YaRN | 1.0 MB |
| P10 | 代码：RoPE & YaRN | 1.4 MB |
| P11 | 理论：GQA | 953 KB |
| P12 | 代码：GQA 上 | 1.3 MB |
| P13 | 代码：GQA 下 | 1.3 MB |
| P14 | 理论：FFN | 1.0 MB |
| P15 | 代码：FFN | 1.3 MB |
| P16 | 拼接 Block | 1.3 MB |
| P17 | 组装 Model | 1.4 MB |
| P18 | 封装 CausalLM | 1.4 MB |
| P19 | 回顾与知识检验 | 1.3 MB |
| P20 | 必看：纠错补充 | 1.1 MB |
| P21 | 重制 Dataset 理论 | 1.2 MB |
| P22 | 重制 Dataset 代码 | 1.2 MB |
| P23 | 重制 Pretrain 理论 | 1.4 MB |
| P24 | 重制 Pretrain 代码 | 1.5 MB |
| P25 | 训练，启动！ | 803 KB |
| P26 | Eval 完结！ | 1.2 MB |
| **合集** | **全 26 集合并** | **31.3 MB** |

> 💡 合并版 PDF 太大无法直接放在 GitHub 仓库，已上传到 [Releases 页面](https://github.com/bcefghj/noteking/releases) 供下载。

---

### 13 种模板效果展示

> 下面展示的是同一个视频（第 7 集：理论 RMSNorm），分别用不同模板生成的结果。
> 完整文件见 [`demos/minimind/templates_demo/`](demos/minimind/templates_demo/)

#### 1. 详细笔记（`detailed`）—— 系统学习用

> 带完整目录、分章节、代码示例、数学公式的学习笔记

```
# MiniMind 第7集学习笔记：RMSNorm（理论）

## 目录
1. 层归一化概述
2. LayerNorm 详解
3. RMSNorm 详解
4. 数学推导与对比
5. 代码实现
```

#### 2. 简要总结（`brief`）—— 快速了解

> 3-5 段话概括整个视频核心内容

```
层归一化（Layer Normalization）是Transformer架构中稳定训练的关键技术。
RMSNorm移除了中心化操作，仅保留缩放操作，降低约7%-64%的计算开销。
公式：y = x / RMS(x) ⊙ g
```

#### 3. 思维导图（`mindmap`）—— 知识结构一目了然

```
# RMSNorm
## 层归一化基础原理
  - 定义：将一层神经元的输出进行标准化
  - 目的：稳定训练、加速收敛
## LayerNorm vs RMSNorm
  - LayerNorm：减均值 + 除标准差
  - RMSNorm：仅除以均方根
## 数学推导
  - RMS(x) = sqrt(1/n * Σxᵢ²)
```

#### 4. 闪卡 / Anki（`flashcard`）—— 间隔复习

```
Q1: 什么是层归一化(Layer Normalization)？
A1: 层归一化是一种归一化技术，对单个样本的所有特征进行归一化，
    使输出均值为0、方差为1。

Q2: RMSNorm 和 LayerNorm 的核心区别？
A2: RMSNorm 省略了均值计算（去中心化），只保留缩放操作。
```

#### 5. 测验题（`quiz`）—— 自测掌握程度

```
一、选择题（共7题，每题10分）

1. LayerNorm 计算过程中需要哪两个统计量？
   A. 均值和方差  B. 中位数和标准差  C. 最大值和最小值  D. 偏度和峰度
```

#### 6. 考试复习（`exam`）—— 公式速查 + 真题

```
核心概念速查表：
| 概念     | 定义                        | 关键特点         |
|----------|----------------------------|-----------------|
| LayerNorm | 对单个样本所有特征做归一化   | 计算均值μ和方差σ² |
| RMSNorm  | 仅使用均方根进行归一化       | 省略均值计算      |
```

#### 7. 时间线（`timeline`）—— 按时间戳整理

```
[00:00] 开场引入 - 本集内容概览
[00:30] 层归一化（LayerNorm）原理讲解
[01:15] RMSNorm 对比分析
[02:00] 数学推导
[03:30] 总结与下集预告
```

#### 8. 教程步骤（`tutorial`）—— 跟着做

```
Step 1: 理解层归一化基础原理
Step 2: 对比 LayerNorm 和 RMSNorm
Step 3: 手推 RMSNorm 公式
Step 4: 用 PyTorch 实现 RMSNorm
```

#### 9. 新闻简报（`news`）—— 媒体报道风格

```
MiniMind开源系列第7集发布：深入解析RMSNorm归一化技术

MiniMind项目于本周发布第7集技术教学视频，时长4分6秒，聚焦Transformer
架构中的核心归一化技术——RMSNorm。
```

#### 10. 播客摘要（`podcast`）—— 音频内容整理

```
🎙️ 播客风格摘要
时长: 4分6秒
主题: 层归一化原理与RMSNorm数学推导
```

#### 11. 小红书笔记（`xhs_note`）—— 社交分享

```
🚀 RMSNorm终于搞懂了！比LayerNorm更简洁的归一化神器

姐妹们！今天挖到宝了～MiniMind第7集把RMSNorm讲得明明白白，4分钟通透理解！✨
```

#### 12. 自定义提示（`custom`）—— 想怎么生成就怎么生成

```
Q&A 问答格式（示例）：

Q1: 什么是层归一化（Layer Normalization）？
A: 层归一化是一种在神经网络的每一层内部对特征向量进行归一化的技术...
```

---

## 快速开始

### 方式一：命令行（最灵活）

```bash
# 1. 安装依赖
pip install yt-dlp openai httpx pillow imagehash scenedetect opencv-python-headless

# 2. 设置 API Key（支持 MiniMax / DeepSeek / OpenAI 等任何兼容接口）
export NOTEKING_LLM_API_KEY="你的API密钥"
export NOTEKING_LLM_BASE_URL="https://api.minimax.chat/v1"
export NOTEKING_LLM_MODEL="MiniMax-M2.7"

# 3. 生成笔记
python -m noteking.cli run "https://www.bilibili.com/video/BV1T2k6BaEeC?p=7" --template detailed
```

### 方式二：Docker 一键部署（最简单）

```bash
git clone https://github.com/bcefghj/noteking.git
cd noteking
echo "NOTEKING_LLM_API_KEY=你的API密钥" > .env
docker compose up -d
# 打开浏览器访问 http://localhost:3000
```

### 方式三：OpenClaw 小龙虾

直接对话：
> 请帮我安装 NoteKing 视频笔记技能

然后：
> 帮我总结这个视频 https://www.bilibili.com/video/BVxxx

---

## 13 种输出模板一览

| 模板 | 名称 | 适用场景 | 命令 |
|------|------|----------|------|
| `brief` | 简要总结 | 快速了解视频讲了什么 | `-t brief` |
| `detailed` | 详细笔记 | 系统学习，带章节目录 | `-t detailed` |
| `mindmap` | 思维导图 | 画出知识结构 | `-t mindmap` |
| `flashcard` | 闪卡/Anki | 间隔复习背诵 | `-t flashcard` |
| `quiz` | 测验题 | 自测掌握程度 | `-t quiz` |
| `timeline` | 时间线 | 按时间戳整理要点 | `-t timeline` |
| `exam` | 考试复习 | 公式速查 + 练习题 | `-t exam` |
| `tutorial` | 教程步骤 | 跟着视频一步步做 | `-t tutorial` |
| `news` | 新闻速览 | 媒体报道风格 | `-t news` |
| `podcast` | 播客摘要 | 音频/访谈内容整理 | `-t podcast` |
| `xhs_note` | 小红书笔记 | 社交平台分享 | `-t xhs_note` |
| `latex_pdf` | LaTeX PDF | 专业打印讲义 | `-t latex_pdf` |
| `custom` | 自定义 | 自己写提示词 | `-t custom` |

---

## 支持的平台

| 平台 | 状态 | 特色功能 |
|------|------|----------|
| **哔哩哔哩** | ✅ 完整支持 | 单视频、合集、多P、SESSDATA高清 |
| **YouTube** | ✅ 完整支持 | 单视频、播放列表、频道（支持代理翻墙） |
| **抖音** | ✅ 支持 | 短视频 |
| **小红书** | ✅ 支持 | 自动解析短链接 |
| **快手** | ✅ 支持 | 短视频 |
| **TikTok** | ✅ 支持 | 国际版 |
| **Twitter/X** | ✅ 支持 | 视频推文 |
| **本地文件** | ✅ 支持 | MP4/MP3/WAV/FLAC |
| **其他 1800+** | ✅ 通过 yt-dlp | 几乎所有视频网站 |

---

## 部署教程（保姆级）

我们准备了超级详细的教程，完全不懂编程的小白也能跟着做：

| 教程 | 说明 |
|------|------|
| 📖 [**中文保姆级入门教程**](docs/beginner-guide-cn.md) | 从零开始，每一步都有截图和解释 |
| 📖 [English Beginner Guide](docs/beginner-guide-en.md) | Step-by-step guide for English users |
| 🐳 [Docker 部署教程](docs/deploy-docker.md) | 一行命令搞定 |
| ☁️ [阿里云部署教程](docs/deploy-aliyun.md) | 部署到云服务器 |
| ☁️ [腾讯云部署教程](docs/deploy-tencent.md) | 部署到腾讯云 |
| 🌐 [Vercel 部署教程](docs/deploy-vercel.md) | 免费部署到网上 |
| 🦞 [OpenClaw 安装教程](docs/openclaw-install.md) | 用小龙虾直接对话使用 |
| 🌏 [YouTube 代理配置](docs/youtube-proxy.md) | 在国内访问 YouTube |

---

## 项目结构

```
noteking/
  core/
    __init__.py      # 主流水线：summarize()
    config.py        # 配置管理
    parser.py        # URL 解析（30+ 平台）
    downloader.py    # yt-dlp 下载器
    subtitle.py      # 字幕三级回退
    transcriber.py   # ASR 语音识别引擎
    frames.py        # 智能关键帧提取
    pdf_engine.py    # PDF 生成引擎
    llm.py           # LLM 接口（兼容 OpenAI）
    templates/       # 13 种输出模板
  cli/               # 命令行工具
  api/               # FastAPI REST API
  mcp/               # MCP 服务器（Cursor/Claude）
  skill/             # AI Agent 技能定义
  assets/            # LaTeX 模板
  demos/             # 示例输出
  docs/              # 部署教程
```

---

## 常见问题

**Q: 需要什么 API？**

A: 任何兼容 OpenAI 接口的大模型 API 都行。推荐：
- **MiniMax**（国产，性价比高，推荐 M2.7 模型）
- **DeepSeek**（国产，便宜好用）
- **OpenAI**（效果最好但贵）
- **Qwen / 通义千问**（阿里出品）

**Q: 处理一个视频要多久？**

A: 通常 30 秒到 2 分钟，取决于视频长度和 API 速度。

**Q: 可以处理整个课程合集吗？**

A: 当然！直接给合集链接，NoteKing 会自动批量处理所有视频。比如上面的 MiniMind 26 集就是一键处理的。

**Q: YouTube 在国内打不开怎么办？**

A: 配置代理即可，详见 [YouTube 代理配置教程](docs/youtube-proxy.md)。

**Q: LaTeX PDF 需要装什么？**

A: 需要安装 TinyTeX（很小，5分钟搞定）：
```bash
# macOS / Linux
curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh
tlmgr install ctex tcolorbox listings booktabs float fancyhdr xcolor enumitem etoolbox
```

---

## 参考与致谢

NoteKing 的开发参考了大量优秀的开源项目和同类产品，详见 [REFERENCES.md](REFERENCES.md)。

---

## License

MIT

---

**GitHub**: [github.com/bcefghj/noteking](https://github.com/bcefghj/noteking) · **小红书**: bcefghj

---

> 🔺 **需要处理本地录音/会议？** 升级到 [NoteKing Pro](https://github.com/bcefghj/noteking-pro)，支持说话人分离、降噪、23 种模板。
