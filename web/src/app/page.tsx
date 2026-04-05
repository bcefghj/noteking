"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import ReactMarkdown from "react-markdown";

const TEMPLATES = [
  { name: "brief", label: "简要总结", icon: "⚡" },
  { name: "detailed", label: "详细学习笔记", icon: "📝" },
  { name: "mindmap", label: "思维导图", icon: "🧠" },
  { name: "flashcard", label: "闪卡 (Anki)", icon: "🃏" },
  { name: "quiz", label: "测验题", icon: "❓" },
  { name: "timeline", label: "时间线笔记", icon: "⏱️" },
  { name: "exam", label: "考试复习笔记", icon: "📚" },
  { name: "tutorial", label: "教程步骤", icon: "🛠️" },
  { name: "news", label: "新闻速览", icon: "📰" },
  { name: "podcast", label: "播客摘要", icon: "🎙️" },
  { name: "xhs_note", label: "小红书笔记", icon: "📕" },
  { name: "latex_pdf", label: "LaTeX PDF", icon: "📄" },
  { name: "custom", label: "自定义", icon: "✏️" },
];

const API_BASE =
  typeof window !== "undefined"
    ? `${window.location.protocol}//${window.location.hostname}:8000`
    : "http://api:8000";

const HISTORY_KEY = "noteking_history";
const MAX_HISTORY = 50;

type Result = {
  title: string;
  content: string;
  template: string;
  source: string;
  platform: string;
  duration: number;
  frames_b64?: Record<string, string>;
};

type HistoryItem = {
  id: string;
  url: string;
  title: string;
  template: string;
  contentPreview: string;
  content: string;
  source: string;
  platform: string;
  duration: number;
  timestamp: number;
};

function loadHistory(): HistoryItem[] {
  if (typeof window === "undefined") return [];
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveHistory(items: HistoryItem[]) {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(items.slice(0, MAX_HISTORY)));
}

function addToHistory(result: Result, url: string) {
  const items = loadHistory();
  const item: HistoryItem = {
    id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    url,
    title: result.title,
    template: result.template,
    contentPreview: result.content.slice(0, 120).replace(/\n/g, " "),
    content: result.content,
    source: result.source,
    platform: result.platform,
    duration: result.duration,
    timestamp: Date.now(),
  };
  items.unshift(item);
  saveHistory(items);
}

export default function Home() {
  const [url, setUrl] = useState("");
  const [template, setTemplate] = useState("detailed");
  const [customPrompt, setCustomPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [streamContent, setStreamContent] = useState("");
  const [streamStage, setStreamStage] = useState("");
  const [streamTitle, setStreamTitle] = useState("");
  const [remaining, setRemaining] = useState<number | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [copied, setCopied] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    setHistory(loadHistory());
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!url.trim() || loading) return;
    setLoading(true);
    setError("");
    setResult(null);
    setStreamContent("");
    setStreamStage("正在连接...");
    setStreamTitle("");

    abortRef.current = new AbortController();

    try {
      const resp = await fetch(`${API_BASE}/api/v1/summarize/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: url.trim(),
          template,
          custom_prompt: customPrompt,
        }),
        signal: abortRef.current.signal,
      });

      if (resp.status === 429) {
        const errData = await resp.json().catch(() => ({}));
        setRemaining(0);
        throw new Error(errData.detail || "今日免费次数已用完（20次/天），明天再来吧~");
      }

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || `HTTP ${resp.status}`);
      }

      const limitHeader = resp.headers.get("X-RateLimit-Remaining");
      if (limitHeader !== null) setRemaining(parseInt(limitHeader, 10));

      const reader = resp.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";
      let accumulated = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const jsonStr = line.slice(6).trim();
          if (!jsonStr) continue;

          try {
            const event = JSON.parse(jsonStr);
            switch (event.stage) {
              case "info":
                setStreamStage(event.message || "获取视频信息...");
                if (event.title) setStreamTitle(event.title);
                break;
              case "subtitle":
                setStreamStage(event.message || "提取字幕...");
                break;
              case "generating":
                setStreamStage("AI 正在生成笔记...");
                if (event.content) {
                  accumulated += event.content;
                  setStreamContent(accumulated);
                }
                break;
              case "done": {
                const finalResult: Result = {
                  title: event.title || streamTitle,
                  content: event.content || accumulated,
                  template: event.template || template,
                  source: event.source || "",
                  platform: event.platform || "",
                  duration: event.duration || 0,
                  frames_b64: event.frames_b64 || {},
                };
                setResult(finalResult);
                addToHistory(finalResult, url.trim());
                setHistory(loadHistory());
                break;
              }
              case "error":
                throw new Error(event.message || "生成失败");
            }
          } catch (parseErr: any) {
            if (parseErr.message && !parseErr.message.includes("JSON"))
              throw parseErr;
          }
        }
      }
    } catch (e: any) {
      if (e.name !== "AbortError") {
        setError(e.message || "生成失败，请重试");
      }
    } finally {
      setLoading(false);
      setStreamStage("");
      abortRef.current = null;
    }
  }, [url, template, customPrompt, loading, streamTitle]);

  const handleCancel = () => {
    abortRef.current?.abort();
    setLoading(false);
    setStreamStage("");
  };

  const handleCopy = () => {
    const text = result?.content || streamContent;
    if (text) {
      navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    const content = result?.content;
    if (!content) return;
    const isLatex = template === "latex_pdf";
    const ext = isLatex ? ".tex" : ".md";
    const mime = isLatex ? "application/x-tex" : "text/markdown";
    const blob = new Blob([content], { type: mime });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${result.title || "notes"}_${template}${ext}`;
    a.click();
  };

  const [pdfCompiling, setPdfCompiling] = useState(false);

  const handleDownloadPDF = async () => {
    const content = result?.content;
    if (!content) return;
    const title = result?.title || "NoteKing 笔记";
    const isLatex = result?.template === "latex_pdf" || template === "latex_pdf";

    if (isLatex) {
      setPdfCompiling(true);
      try {
        const resp = await fetch(`${API_BASE}/api/v1/compile-latex`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            tex_content: content,
            filename: title,
            frames_b64: result?.frames_b64 || {},
          }),
        });
        if (!resp.ok) {
          const errData = await resp.json().catch(() => ({}));
          throw new Error(errData.detail || `PDF 编译失败 (${resp.status})`);
        }
        const blob = await resp.blob();
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `${title}.pdf`;
        a.click();
        URL.revokeObjectURL(a.href);
      } catch (e: any) {
        alert(e.message || "PDF 编译失败");
      } finally {
        setPdfCompiling(false);
      }
      return;
    }

    const win = window.open("", "_blank");
    if (!win) return;
    win.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8">
<title>${title} - NoteKing</title>
<style>
  @media print { body { margin: 0; } @page { margin: 1.5cm 2cm; } }
  body { font-family: -apple-system, "Microsoft YaHei", sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #1a1a1a; line-height: 1.8; font-size: 14px; }
  h1 { font-size: 22px; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; }
  h2 { font-size: 18px; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-top: 24px; }
  h3 { font-size: 16px; margin-top: 18px; }
  code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
  pre { background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; }
  pre code { background: none; color: inherit; padding: 0; }
  blockquote { border-left: 3px solid #3b82f6; padding: 8px 16px; margin: 12px 0; background: #f8fafc; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; }
  th, td { border: 1px solid #e5e7eb; padding: 8px 12px; text-align: left; }
  th { background: #f8fafc; font-weight: 600; }
  strong { color: #3b82f6; }
  .header { text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #3b82f6; }
  .header h1 { border: none; margin: 0; }
  .header p { color: #64748b; margin: 4px 0; font-size: 12px; }
  .footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid #e5e7eb; text-align: center; color: #94a3b8; font-size: 11px; }
</style>
</head><body>
<div class="header">
  <h1>${title}</h1>
  <p>\u5e73\u53f0: ${result?.platform || ""} | \u5b57\u5e55: ${result?.source || ""} | \u65f6\u957f: ${result?.duration ? Math.round(result.duration / 60) + " \u5206\u949f" : ""}</p>
  <p>\u7531 NoteKing \u7b14\u8bb0\u4e4b\u738b \u81ea\u52a8\u751f\u6210 | github.com/bcefghj/noteking</p>
</div>
<div id="content"></div>
<div class="footer">NoteKing \u7b14\u8bb0\u4e4b\u738b | GitHub: github.com/bcefghj/noteking | \u5c0f\u7ea2\u4e66: bcefghj</div>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"><\/script>
<script>
  document.getElementById("content").innerHTML = marked.parse(${JSON.stringify(content)});
  setTimeout(() => { window.print(); }, 500);
<\/script>
</body></html>`);
    win.document.close();
  };

  const handleHistoryClick = (item: HistoryItem) => {
    setResult({
      title: item.title,
      content: item.content,
      template: item.template,
      source: item.source,
      platform: item.platform,
      duration: item.duration,
    });
    setTemplate(item.template);
    setUrl(item.url);
    setShowHistory(false);
  };

  const clearHistory = () => {
    localStorage.removeItem(HISTORY_KEY);
    setHistory([]);
  };

  const displayContent = result?.content || streamContent;

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]">
        {/* Header */}
        <header className="border-b border-[var(--border)] bg-[var(--bg-secondary)]">
          <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-3xl">👑</span>
              <div>
                <h1 className="text-xl font-bold">NoteKing 笔记之王</h1>
                <p className="text-xs text-[var(--text-secondary)]">
                  视频一键生成学习笔记 | 支持 B站、YouTube 等 30+ 平台
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {remaining !== null && (
                <span className="text-xs text-[var(--text-secondary)] px-2 py-1 rounded border border-[var(--border)]">
                  今日剩余 {remaining} 次
                </span>
              )}
              <button
                onClick={() => { setShowHistory(!showHistory); setResult(null); }}
                className="px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-primary)] transition text-sm"
              >
                📋 历史
              </button>
              <button
                onClick={() => setDarkMode(!darkMode)}
                className="px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-primary)] transition text-sm"
              >
                {darkMode ? "☀️" : "🌙"}
              </button>
            </div>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-4 py-8">
          {/* Input */}
          <div className="bg-[var(--bg-secondary)] rounded-2xl p-6 border border-[var(--border)] mb-8">
            <div className="flex gap-3 mb-4">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="粘贴视频链接... (B站、YouTube、抖音、小红书等)"
                className="flex-1 px-4 py-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)] text-base"
                onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
              />
              {loading ? (
                <button
                  onClick={handleCancel}
                  className="px-6 py-3 bg-red-500 text-white rounded-xl font-medium hover:opacity-90 transition whitespace-nowrap"
                >
                  取消
                </button>
              ) : (
                <button
                  onClick={handleSubmit}
                  disabled={!url.trim()}
                  className="px-6 py-3 bg-[var(--accent)] text-white rounded-xl font-medium hover:opacity-90 transition disabled:opacity-50 whitespace-nowrap"
                >
                  生成笔记
                </button>
              )}
            </div>

            <div className="flex flex-wrap gap-2">
              {TEMPLATES.map((t) => (
                <button
                  key={t.name}
                  onClick={() => setTemplate(t.name)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition ${
                    template === t.name
                      ? "bg-[var(--accent)] text-white"
                      : "bg-[var(--bg-primary)] border border-[var(--border)] hover:border-[var(--accent)]"
                  }`}
                >
                  {t.icon} {t.label}
                </button>
              ))}
            </div>

            {template === "custom" && (
              <textarea
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                placeholder="输入自定义 Prompt..."
                className="w-full mt-3 px-4 py-3 rounded-xl bg-[var(--bg-primary)] border border-[var(--border)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)] min-h-[80px] text-sm"
              />
            )}
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 rounded-xl p-4 mb-6">
              {error}
            </div>
          )}

          {/* Streaming progress */}
          {loading && (
            <div className="bg-[var(--bg-secondary)] rounded-2xl border border-[var(--border)] mb-6">
              <div className="px-6 py-4 border-b border-[var(--border)] flex items-center gap-3">
                <div className="w-5 h-5 border-2 border-[var(--accent)] border-t-transparent rounded-full animate-spin" />
                <span className="text-sm font-medium">{streamStage}</span>
                {streamTitle && (
                  <span className="text-xs text-[var(--text-secondary)] ml-auto truncate max-w-[300px]">
                    {streamTitle}
                  </span>
                )}
              </div>
              {streamContent && (
                <div className="p-6 note-content prose prose-slate dark:prose-invert max-w-none max-h-[60vh] overflow-y-auto">
                  <ReactMarkdown>{streamContent}</ReactMarkdown>
                </div>
              )}
            </div>
          )}

          {/* Result */}
          {result && !loading && (
            <div className="bg-[var(--bg-secondary)] rounded-2xl border border-[var(--border)]">
              <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)]">
                <div>
                  <h2 className="font-semibold text-lg">{result.title}</h2>
                  <div className="flex gap-3 text-xs text-[var(--text-secondary)] mt-1">
                    <span>平台: {result.platform}</span>
                    <span>字幕: {result.source}</span>
                    {result.duration > 0 && (
                      <span>时长: {Math.round(result.duration / 60)} 分钟</span>
                    )}
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={handleCopy}
                    className="px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-primary)] transition text-sm"
                  >
                    {copied ? "已复制!" : "复制"}
                  </button>
                  <button
                    onClick={handleDownloadPDF}
                    disabled={pdfCompiling}
                    className="px-3 py-1.5 rounded-lg bg-[var(--accent)] text-white hover:opacity-90 transition text-sm disabled:opacity-60"
                  >
                    {pdfCompiling ? "编译中..." : "下载 PDF"}
                  </button>
                  <button
                    onClick={handleDownload}
                    className="px-3 py-1.5 rounded-lg border border-[var(--border)] hover:bg-[var(--bg-primary)] transition text-sm"
                  >
                    下载 {template === "latex_pdf" ? ".tex" : ".md"}
                  </button>
                </div>
              </div>
              <div className="p-6 note-content prose prose-slate dark:prose-invert max-w-none">
                <ReactMarkdown>{result.content}</ReactMarkdown>
              </div>
            </div>
          )}

          {/* History panel */}
          {showHistory && !loading && !result && (
            <div className="bg-[var(--bg-secondary)] rounded-2xl border border-[var(--border)]">
              <div className="flex items-center justify-between px-6 py-4 border-b border-[var(--border)]">
                <h2 className="font-semibold">历史记录 ({history.length})</h2>
                {history.length > 0 && (
                  <button onClick={clearHistory} className="text-xs text-red-500 hover:underline">
                    清空
                  </button>
                )}
              </div>
              {history.length === 0 ? (
                <div className="p-8 text-center text-[var(--text-secondary)]">暂无记录</div>
              ) : (
                <div className="divide-y divide-[var(--border)]">
                  {history.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => handleHistoryClick(item)}
                      className="w-full text-left px-6 py-4 hover:bg-[var(--bg-primary)] transition"
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-sm truncate max-w-[70%]">{item.title}</span>
                        <span className="text-xs text-[var(--text-secondary)]">
                          {new Date(item.timestamp).toLocaleDateString("zh-CN", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
                        </span>
                      </div>
                      <div className="flex gap-2 text-xs text-[var(--text-secondary)]">
                        <span>{TEMPLATES.find(t => t.name === item.template)?.icon} {TEMPLATES.find(t => t.name === item.template)?.label}</span>
                        <span>| {item.platform}</span>
                      </div>
                      <p className="text-xs text-[var(--text-secondary)] mt-1 line-clamp-1">{item.contentPreview}</p>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Features */}
          {!result && !loading && !showHistory && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
              <FC icon="🌐" title="30+ 平台" desc="B站、YouTube、抖音、小红书、TikTok 等 1800+ 平台" />
              <FC icon="📋" title="13 种模板" desc="笔记、思维导图、闪卡、测验、考试复习等" />
              <FC icon="🎯" title="智能字幕提取" desc="三级回退：CC字幕 -> ASR语音识别 -> 视觉模式" />
              <FC icon="📄" title="LaTeX PDF 讲义" desc="自动生成带目录、代码块的 PDF 图文讲义" />
              <FC icon="📦" title="批量处理" desc="支持整个播放列表和 50+ 集课程批量生成" />
              <FC icon="⚡" title="流式输出" desc="实时看到 AI 生成过程，无需等待" />
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-[var(--border)] mt-16">
          <div className="max-w-6xl mx-auto px-4 py-6">
            <div className="flex flex-col md:flex-row items-center justify-between gap-4">
              <div className="text-sm text-[var(--text-secondary)]">
                NoteKing 笔记之王 - 开源视频学习笔记工具 | 每日免费 20 次
              </div>
              <div className="flex items-center gap-4 text-sm">
                <a href="https://github.com/bcefghj/noteking" target="_blank"
                  className="text-[var(--accent)] hover:underline flex items-center gap-1">
                  <svg className="w-4 h-4" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
                  GitHub
                </a>
                <a href="https://www.xiaohongshu.com/user/profile/bcefghj" target="_blank"
                  className="text-[var(--accent)] hover:underline flex items-center gap-1">
                  📕 小红书: bcefghj
                </a>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

function FC({ icon, title, desc }: { icon: string; title: string; desc: string }) {
  return (
    <div className="bg-[var(--bg-secondary)] rounded-xl p-5 border border-[var(--border)]">
      <span className="text-2xl">{icon}</span>
      <h3 className="font-semibold mt-2">{title}</h3>
      <p className="text-sm text-[var(--text-secondary)] mt-1">{desc}</p>
    </div>
  );
}
