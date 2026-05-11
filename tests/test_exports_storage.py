from __future__ import annotations

import json

from app.models import AnalysisState
from app.exports.storage import save_output_files


def test_save_output_files_exports_source_refs_json(tmp_path, monkeypatch):
    monkeypatch.setattr("app.exports.storage.OUTPUT_DIR", tmp_path)
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        final_report="# report\n\n正文",
        trace=["step1"],
        source_refs=[{"title": "公告A", "source": "东财", "provider": "eastmoney"}],
    )

    report_path, trace_path = save_output_files(state, timestamp="20260506_120000")

    sources_name = state.sections["source_refs_export"]
    sources_path = tmp_path / sources_name
    html_path = tmp_path / state.sections["report_html_export"]
    assert report_path.exists()
    assert trace_path.exists()
    assert sources_path.exists()
    assert html_path.exists()
    payload = json.loads(sources_path.read_text(encoding="utf-8"))
    assert payload[0]["title"] == "公告A"
    assert payload[0]["provider"] == "eastmoney"
    assert "贵州茅台" in html_path.read_text(encoding="utf-8")


def test_save_output_files_reuses_existing_exports(tmp_path, monkeypatch):
    monkeypatch.setattr("app.exports.storage.OUTPUT_DIR", tmp_path)
    report_path = tmp_path / "report_600519_20260506_120000.md"
    trace_path = tmp_path / "trace_600519_20260506_120000.log"
    html_path = tmp_path / "report_600519_20260506_120000.html"
    sources_path = tmp_path / "sources_600519_20260506_120000.json"
    report_path.write_text("# report", encoding="utf-8")
    trace_path.write_text("step1", encoding="utf-8")
    html_path.write_text("<html></html>", encoding="utf-8")
    sources_path.write_text("[]", encoding="utf-8")
    state = AnalysisState(
        stock_code="600519",
        sections={
            "report_export": report_path.name,
            "trace_export": trace_path.name,
            "report_html_export": html_path.name,
            "source_refs_export": sources_path.name,
        },
    )

    reused_report, reused_trace = save_output_files(state)

    assert reused_report == report_path
    assert reused_trace == trace_path
