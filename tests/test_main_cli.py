from __future__ import annotations

import json
import types

import app.config as app_config
import main


def test_main_defaults_to_analysis(monkeypatch):
    called = {}

    def fake_run_analysis(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_analysis", fake_run_analysis)

    assert main.main(["600519", "--eval"]) == 0
    assert called["argv"] == ["600519", "--eval"]


def test_main_dispatches_analyze_subcommand(monkeypatch):
    called = {}

    def fake_run_analysis(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_analysis", fake_run_analysis)

    assert main.main(["analyze", "000858"]) == 0
    assert called["argv"] == ["000858"]


def test_main_dispatches_script_subcommand(monkeypatch):
    monkeypatch.setattr(main, "_dispatch_script", lambda module_name, argv: 0 if module_name == "scripts.regression" and argv == ["--llm-judge"] else 1)

    assert main.main(["regression", "--llm-judge"]) == 0


def test_main_dispatches_quality_gate_subcommand(monkeypatch):
    called = {}

    def fake_dispatch(module_name, argv):
        called["module_name"] = module_name
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_dispatch_script", fake_dispatch)

    assert main.main(["quality-gate", "--skip-regression"]) == 0
    assert called == {"module_name": "scripts.quality_gate", "argv": ["--skip-regression"]}


def test_main_prints_root_help(monkeypatch, capsys):
    monkeypatch.setattr(main, "print_root_help", lambda: print("ROOT_HELP"))

    assert main.main(["--help"]) == 0
    assert "ROOT_HELP" in capsys.readouterr().out


def test_main_dispatches_api(monkeypatch):
    called = {}

    def fake_run_api(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_api", fake_run_api)

    assert main.main(["api", "--reload"]) == 0
    assert called["argv"] == ["--reload"]


def test_main_falls_back_to_analysis_for_unknown_command(monkeypatch):
    called = {}

    def fake_run_analysis(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_analysis", fake_run_analysis)

    assert main.main(["unknown-cmd", "--flag"]) == 0
    assert called["argv"] == ["unknown-cmd", "--flag"]


def test_dispatch_script_calls_module_main(monkeypatch):
    module = types.SimpleNamespace(main=lambda argv: 7)
    monkeypatch.setattr(main.importlib, "import_module", lambda name: module)

    assert main._dispatch_script("scripts.ablation", ["--stocks", "600519"]) == 7


def test_dispatch_script_normalizes_none_return(monkeypatch):
    module = types.SimpleNamespace(main=lambda argv: None)
    monkeypatch.setattr(main.importlib, "import_module", lambda name: module)

    assert main._dispatch_script("scripts.regression", []) == 0


def test_analyze_parser_accepts_legacy_and_optional_flags():
    args = main.build_analyze_parser().parse_args(["600519", "--eval", "--mc-sims", "500", "--doc", "memo.txt"])

    assert args.code == "600519"
    assert args.eval is True
    assert args.mc_sims == 500
    assert args.doc_paths == ["memo.txt"]


def test_load_uploaded_items_reads_relative_paths(tmp_path, monkeypatch):
    doc_path = tmp_path / "memo.txt"
    doc_path.write_text("hello", encoding="utf-8")
    monkeypatch.setattr(main, "ROOT", tmp_path)

    items = main._load_uploaded_items(["memo.txt"])

    assert items[0]["name"] == "memo.txt"
    assert items[0]["content"] == b"hello"
    assert items[0]["content_type"] == "text/plain"


def test_load_uploaded_items_rejects_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "ROOT", tmp_path)

    try:
        main._load_uploaded_items(["missing.txt"])
    except FileNotFoundError as exc:
        assert "补充文档不存在" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")


def test_run_analysis_returns_failure_when_doc_missing(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(main, "ROOT", tmp_path)

    result = main._run_analysis(["600519", "--doc", "missing.txt"])

    assert result == 1
    assert "补充文档不存在" in capsys.readouterr().out


def test_run_analysis_passes_uploaded_items_to_engine(monkeypatch, tmp_path):
    doc_path = tmp_path / "memo.txt"
    doc_path.write_text("hello", encoding="utf-8")
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path / "output")

    class DummyEngine:
        def __init__(self, on_step=None):
            self.on_step = on_step

        def run(self, code, *, uploaded_items=None):
            test_run_analysis_passes_uploaded_items_to_engine.called = {"code": code, "uploaded_items": uploaded_items}
            return types.SimpleNamespace(final_report="# report", trace=[], stock_code=code, sections={})

    monkeypatch.setattr(main, "ROOT", tmp_path)
    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)
    monkeypatch.setattr("app.exports.storage.save_output_files", lambda state, root=None, timestamp=None: (tmp_path / "output" / "report_600519.md", tmp_path / "output" / "trace_600519.log"))

    result = main._run_analysis(["600519", "--doc", str(doc_path)])

    assert result == 0
    assert test_run_analysis_passes_uploaded_items_to_engine.called["code"] == "600519"
    assert test_run_analysis_passes_uploaded_items_to_engine.called["uploaded_items"][0]["name"] == "memo.txt"


def test_run_analysis_updates_mc_simulations_runtime(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(main, "ROOT", tmp_path)

    class DummyEngine:
        def __init__(self, on_step=None):
            self.on_step = on_step

        def run(self, code, *, uploaded_items=None):
            return types.SimpleNamespace(final_report="# report", trace=[], stock_code=code, sections={})

    original_value = app_config.MC_SIMULATIONS
    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)
    monkeypatch.setattr("app.exports.storage.save_output_files", lambda state, root=None, timestamp=None: (tmp_path / "output" / "report_600519.md", tmp_path / "output" / "trace_600519.log"))

    try:
        result = main._run_analysis(["600519", "--mc-sims", "321"])
        assert result == 0
        assert app_config.MC_SIMULATIONS == 321
    finally:
        app_config.MC_SIMULATIONS = original_value



def test_run_analysis_rebuilds_kb_and_exits_when_no_code(monkeypatch):
    called = {"rebuild": 0, "engine": 0}

    monkeypatch.setattr(main, "_rebuild_knowledge_base", lambda: called.__setitem__("rebuild", called["rebuild"] + 1))

    class DummyEngine:
        def __init__(self, on_step=None):
            called["engine"] += 1

        def run(self, code, *, uploaded_items=None):
            return types.SimpleNamespace(final_report="# report", trace=[], stock_code=code, sections={})

    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)

    result = main._run_analysis(["--rebuild-kb"])

    assert result == 0
    assert called["rebuild"] == 1
    assert called["engine"] == 0


def test_run_analysis_writes_eval_markdown_and_json(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(main, "ROOT", tmp_path)
    monkeypatch.setattr(main, "EVAL_DIR", tmp_path / "evals")

    class DummyEngine:
        def __init__(self, on_step=None):
            self.on_step = on_step

        def run(self, code, *, uploaded_items=None):
            return types.SimpleNamespace(final_report="# report", trace=[], stock_code=code, sections={})

    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)
    monkeypatch.setattr("app.exports.storage.save_output_files", lambda state, root=None, timestamp=None: (tmp_path / "output" / f"report_{state.stock_code}_{timestamp}.md", tmp_path / "output" / f"trace_{state.stock_code}_{timestamp}.log"))
    monkeypatch.setattr(
        "app.evals.report_eval.evaluate_report_with_metrics",
        lambda report, state, stock_code: {
            "stock_code": stock_code,
            "section_coverage": 1.0,
            "has_tables": True,
            "has_numbers": True,
            "missing_sections": [],
            "rating_consistent": True,
            "consistency_passed": True,
            "consistency_issue_count": 0,
            "consistency_issues": [],
            "completeness": 5,
            "data_support": 5,
            "reasoning_quality": 5,
            "readability": 5,
            "overall_score": 90.0,
            "report_length": 100,
            "numeric_references": 10,
            "covered_sections": 8,
            "llm_judge_enabled": True,
            "risk_evidence_count": 1,
            "risk_transmission_count": 1,
            "investment_anchor_present": True,
            "postprocess_fix_count": 0,
            "data_gap_disclosure_count": 0,
            "source_reference_count": 0,
            "source_provenance_coverage": 0.0,
            "document_parse_success_rate": 1.0,
            "table_extraction_success_rate": 0.0,
            "live_tool_success_rate": 1.0,
            "memory_hit_count": 0,
            "memory_usefulness_score": 0.0,
            "historical_delta_coverage": 0.0,
            "duplicate_memory_injection_rate": 0.0,
            "memory_reference_present": True,
            "memory_reference_coverage": 1.0,
            "repeated_risk_pattern_count": 0,
            "repeated_catalyst_pattern_count": 0,
            "thesis_stability_score": 0.0,
            "rating_drift_count": 0,
            "graph_hit_count": 0,
            "hybrid_retrieval_hit_rate": 0.0,
            "relationship_coverage": 0.0,
            "risk_path_completeness": 0.0,
            "graph_query_focus": "通用关系",
            "graph_focus_coverage": 0.0,
            "graph_focus_summary": "",
            "section_graph_hit_count": 0,
            "section_graph_focus_coverage": 0.0,
            "section_graph_summary": "",
            "section_graph_prompt_injection_present": False,
            "section_graph_absorption_count": 0,
            "section_graph_absorption_rate": 0.0,
            "section_graph_query_summary": "",
            "section_graph_feedback_summary": "",
            "section_graph_query_refinement_summary": "",
            "section_graph_query_refined_count": 0,
            "section_graph_low_absorption_count": 0,
            "section_graph_low_absorption_sections": "",
            "section_graph_refinement_triggered": False,
            "section_graph_refinement_coverage": 0.0,
            "section_graph_refinement_comparison_summary": "",
            "section_graph_refinement_improved_count": 0,
            "section_graph_refinement_improvement_rate": 0.0,
            "section_graph_low_improvement_summary": "",
            "section_graph_no_hit_count": 0,
            "section_graph_no_gain_count": 0,
            "section_graph_low_absorption_only_count": 0,
            "section_graph_refinement_strategy_summary": "",
            "summary": "章节覆盖: 100%",
            "run_metrics": {"duration_s": 1.2},
        },
    )
    monkeypatch.setattr("app.evals.report_eval.format_eval_report", lambda result: "# 评测报告")

    result = main._run_analysis(["600519", "--eval"])

    assert result == 0
    eval_dir = tmp_path / "evals"
    md_files = list(eval_dir.glob("eval_600519_*.md"))
    json_files = list(eval_dir.glob("eval_600519_*.json"))
    assert len(md_files) == 1
    assert len(json_files) == 1
    assert md_files[0].read_text(encoding="utf-8") == "# 评测报告"
    payload = json.loads(json_files[0].read_text(encoding="utf-8"))
    assert payload["summary"] == "章节覆盖: 100%"
    assert payload["run_metrics"]["duration_s"] == 1.2


def test_run_analysis_returns_failure_when_report_missing(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(main, "OUTPUT_DIR", tmp_path / "output")
    monkeypatch.setattr(main, "ROOT", tmp_path)

    class DummyEngine:
        def __init__(self, on_step=None):
            self.on_step = on_step

        def run(self, code, *, uploaded_items=None):
            return types.SimpleNamespace(final_report="", trace=["failed"], stock_code=code, sections={})

    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)

    result = main._run_analysis(["600519"])

    assert result == 1
    assert "分析失败" in capsys.readouterr().out
