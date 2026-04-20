"""Web 端输出文件存储。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR
from app.models import AnalysisState


def save_output_files(state: AnalysisState, *, root: Path | None = None) -> tuple[Path, Path]:
    del root
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_code = state.stock_code or "unknown"
    report_path = OUTPUT_DIR / f"report_{safe_code}_{timestamp}.md"
    trace_path = OUTPUT_DIR / f"trace_{safe_code}_{timestamp}.log"
    report_path.write_text(state.final_report, encoding="utf-8")
    trace_path.write_text("\n".join(state.trace), encoding="utf-8")
    return report_path, trace_path
