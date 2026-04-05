"""LaTeX PDF lecture notes template with keyframe screenshots."""

from .base import BaseTemplate, TemplateContext, _truncate_transcript


class LaTeXPDFTemplate(BaseTemplate):
    name = "latex_pdf"
    display_name = "LaTeX PDF 讲义"
    description = "Professional LaTeX lecture notes compiled to PDF"
    file_extension = ".tex"

    def build_prompt(self, ctx: TemplateContext) -> str:
        transcript = _truncate_transcript(ctx.transcript)
        chapters_info = ""
        if ctx.has_chapters:
            chapters_info = "\n视频章节:\n"
            for ch in ctx.meta.chapters:
                t = ch.get("title", "")
                s = ch.get("start_time", 0)
                chapters_info += f"- [{s:.0f}s] {t}\n"

        # 关键帧信息
        frames_info: list[dict] = ctx.extra.get("frames_info", [])
        frames_section = ""
        frames_usage = ""
        if frames_info:
            frames_section = "\n已提取的视频关键帧（按时间顺序）:\n"
            for f in frames_info:
                frames_section += f"- 文件名: {f['name']}  时间戳: {f['ts_str']} ({f['ts']:.1f}s)\n"
            frames_usage = """
图片使用规则（非常重要）:
- 在讲解某个概念时，如果有对应时间段的截图，必须插入该截图
- 插入格式（每张图片完整代码）:
  \\begin{{figure}}[H]
  \\centering
  \\includegraphics[width=0.85\\textwidth]{{frame_XX.jpg}}
  \\caption{{时间戳 MM:SS - 对该截图内容的简短描述}}
  \\label{{fig:frameXX}}
  \\end{{figure}}
- 根据截图时间戳，判断该帧对应哪个知识点，选择合适的位置插入
- 每个主要 section 至少插入 1 张截图（如果有对应时段的帧）
- 截图数量占全部提取帧的 80% 以上（尽量都用上）"""
        else:
            frames_usage = "- 本次未提取到截图，不要插入任何 \\includegraphics 命令"

        return f"""请根据以下视频内容，生成一份完整的 LaTeX 讲义文档。

视频标题: {ctx.meta.title}
作者: {ctx.meta.uploader}
时长: {ctx.meta.duration:.0f} 秒
{chapters_info}
{frames_section}
视频内容转录:
{transcript}

要求:
1. 生成完整的 .tex 文档，从 \\documentclass 到 \\end{{document}}
2. 使用 ctexart 文档类（支持中文）
3. 按教学逻辑重组内容，而非简单按字幕时间顺序排列
4. 每个主要章节结构:
   - 动机: 为什么要学这个
   - 核心概念: 主要思想
   - 机制/方法: 如何工作
   - 示例: 具体案例
   - 小结: 本节要点
5. 公式使用 $$...$$ 或 \\begin{{equation}}，并解释每个符号
6. 代码使用 \\begin{{lstlisting}} 环境
7. 重要概念用 \\textbf{{}} 强调
8. 每个主要 section 结尾加 \\subsection{{本章小结}}
9. 文档最后加 \\section{{总结与延伸}}
{frames_usage}

LaTeX 文档头部必须包含以下所有包:
\\documentclass[12pt,a4paper]{{ctexart}}
\\usepackage{{amsmath,amssymb,listings,xcolor,geometry,hyperref}}
\\usepackage{{graphicx,float}}
\\geometry{{margin=2.5cm}}
\\lstset{{basicstyle=\\ttfamily\\small,breaklines=true,frame=single}}
\\title{{{ctx.meta.title}}}
\\author{{笔记整理自 {ctx.meta.uploader} 的视频}}
\\date{{}}

请直接输出完整的 .tex 文档:"""
