from __future__ import annotations

import types

import main


def test_run_analysis_prints_additional_export_paths(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(main, "ROOT", tmp_path)

    class DummyEngine:
        def __init__(self, on_step=None):
            self.on_step = on_step

        def run(self, code, *, uploaded_items=None):
            return types.SimpleNamespace(
                final_report="# report",
                trace=["step1"],
                stock_code=code,
                sections={
                    "report_html_export": "report_600519_demo.html",
                    "report_pdf_export": "report_600519_demo.pdf",
                    "source_refs_export": "sources_600519_demo.json",
                },
            )

    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)
    monkeypatch.setattr(
        "app.exports.storage.save_output_files",
        lambda state, root=None, timestamp=None: (tmp_path / "output" / "report_600519_demo.md", tmp_path / "output" / "trace_600519_demo.log"),
    )

    result = main._run_analysis(["600519"])

    out = capsys.readouterr().out
    assert result == 0
    assert "HTML 展示版: output\\report_600519_demo.html" in out
    assert "PDF 展示版: output\\report_600519_demo.pdf" in out
    assert "来源索引: output\\sources_600519_demo.json" in out
