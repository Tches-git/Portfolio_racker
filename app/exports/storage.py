"""输出文件存储。"""
from __future__ import annotations

import json
from datetime import datetime
from html import escape
from pathlib import Path

from app.config import OUTPUT_DIR
from app.models import AnalysisState

_EXPORT_KEYS = {
    "report": "report_export",
    "trace": "trace_export",
    "sources": "source_refs_export",
    "html": "report_html_export",
    "pdf": "report_pdf_export",
}


def _resolve_existing_export_paths(state: AnalysisState) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for kind, key in _EXPORT_KEYS.items():
        name = str(state.sections.get(key, "") or "").strip()
        if not name:
            continue
        path = OUTPUT_DIR / name
        if path.exists():
            paths[kind] = path
    return paths


def _build_html_report(state: AnalysisState) -> str:
    try:
        from markdown import markdown as markdown_to_html
    except Exception:
        body = "\n".join(f"<p>{escape(line)}</p>" for line in (state.final_report or "").splitlines() if line.strip())
    else:
        body = markdown_to_html(state.final_report or "", extensions=["tables", "fenced_code"])
    title = f"{state.stock_name or '研报'} ({state.stock_code or 'unknown'})"
    trace_items = "".join(f"<li>{escape(line)}</li>" for line in state.trace[:12])
    source_items = "".join(
        f"<li><strong>{escape(str(ref.get('title', '未命名来源')))}</strong>：{escape(str(ref.get('summary', '')))}</li>"
        for ref in state.source_refs[:8]
    )
    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <title>{escape(title)} - 深度研究报告</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif; margin: 0; background: #f8fbff; color: #0f172a; }}
    .page {{ max-width: 960px; margin: 0 auto; padding: 32px 24px 48px; }}
    .hero, .card {{ background: #fff; border: 1px solid #dbeafe; border-radius: 18px; padding: 20px 22px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04); }}
    .hero h1 {{ margin: 0 0 6px; font-size: 30px; }}
    .meta {{ color: #475569; font-size: 14px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .report {{ line-height: 1.75; }}
    .report table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
    .report th, .report td {{ border: 1px solid #cbd5e1; padding: 8px 10px; text-align: left; }}
    .report code {{ background: #eff6ff; padding: 2px 4px; border-radius: 6px; }}
    .report blockquote {{ margin: 16px 0; padding: 12px 16px; background: #f8fafc; border-left: 4px solid #60a5fa; }}
    ul {{ margin: 10px 0 0 18px; }}
  </style>
</head>
<body>
  <div class=\"page\">
    <div class=\"hero\">
      <h1>{escape(title)} 深度研究报告</h1>
      <div class=\"meta\">导出格式：HTML 展示版 | 来源数 {len(state.source_refs)} | Trace {len(state.trace)} 条</div>
    </div>
    <div class=\"grid\">
      <div class=\"card\"><strong>报告正文</strong><div class=\"report\">{body}</div></div>
      <div>
        <div class=\"card\"><strong>来源摘要</strong><ul>{source_items or '<li>暂无补充来源</li>'}</ul></div>
        <div class=\"card\"><strong>运行追踪摘要</strong><ul>{trace_items or '<li>暂无 Trace</li>'}</ul></div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def _register_pdf_font() -> str | None:
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except Exception:
        return None
    font_candidates = [
        ("MicrosoftYaHei", Path("C:/Windows/Fonts/msyh.ttc")),
        ("SimSun", Path("C:/Windows/Fonts/simsun.ttc")),
        ("NotoSansCJK", Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")),
    ]
    for font_name, font_path in font_candidates:
        if not font_path.exists():
            continue
        try:
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            return font_name
        except Exception:
            continue
    return None


def _write_pdf_report(state: AnalysisState, path: Path) -> Path | None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except Exception:
        return None
    font_name = _register_pdf_font()
    if not font_name:
        return None
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("ReportTitle", parent=styles["Heading1"], fontName=font_name, fontSize=18, leading=24)
    body_style = ParagraphStyle("ReportBody", parent=styles["BodyText"], fontName=font_name, fontSize=10.5, leading=16)
    story = [
        Paragraph(f"{escape(state.stock_name or '研报')}（{escape(state.stock_code or 'unknown')}）深度研究报告", title_style),
        Spacer(1, 12),
    ]
    for raw_line in (state.final_report or "").splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        normalized = line.lstrip("#").lstrip("-*0123456789. ").strip()
        story.append(Paragraph(escape(normalized), body_style))
        story.append(Spacer(1, 4))
    doc.build(story)
    return path


def save_output_files(state: AnalysisState, *, root: Path | None = None, timestamp: str | None = None) -> tuple[Path, Path]:
    del root
    existing_paths = _resolve_existing_export_paths(state)
    if "report" in existing_paths and "trace" in existing_paths:
        return existing_paths["report"], existing_paths["trace"]

    OUTPUT_DIR.mkdir(exist_ok=True)
    export_timestamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_code = state.stock_code or "unknown"
    report_path = OUTPUT_DIR / f"report_{safe_code}_{export_timestamp}.md"
    trace_path = OUTPUT_DIR / f"trace_{safe_code}_{export_timestamp}.log"
    sources_path = OUTPUT_DIR / f"sources_{safe_code}_{export_timestamp}.json"
    html_path = OUTPUT_DIR / f"report_{safe_code}_{export_timestamp}.html"
    pdf_path = OUTPUT_DIR / f"report_{safe_code}_{export_timestamp}.pdf"

    report_path.write_text(state.final_report, encoding="utf-8")
    trace_path.write_text("\n".join(state.trace), encoding="utf-8")
    sources_path.write_text(json.dumps(list(state.source_refs), ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(_build_html_report(state), encoding="utf-8")
    generated_pdf = _write_pdf_report(state, pdf_path)

    state.sections[_EXPORT_KEYS["report"]] = report_path.name
    state.sections[_EXPORT_KEYS["trace"]] = trace_path.name
    state.sections[_EXPORT_KEYS["sources"]] = sources_path.name
    state.sections[_EXPORT_KEYS["html"]] = html_path.name
    if generated_pdf is not None:
        state.sections[_EXPORT_KEYS["pdf"]] = generated_pdf.name
    else:
        state.sections.pop(_EXPORT_KEYS["pdf"], None)
    return report_path, trace_path
