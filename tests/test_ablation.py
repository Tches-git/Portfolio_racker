from __future__ import annotations

import json

import run_ablation
from app.models import AblationConfig


def test_summarize_results_includes_postprocess_metrics():
    rows = [
        {
            "stock_code": "600519",
            "label": "baseline",
            "success": True,
            "overall_score": 85.0,
            "duration_s": 10.0,
            "total_tokens": 1000,
            "llm_calls": 5,
            "tool_calls": 8,
            "agent_steps": 6,
            "rag_hits": 3,
            "news_count": 4,
            "risk_count": 2,
            "risk_evidence_count": 2,
            "risk_transmission_count": 2,
            "investment_anchor_present": True,
            "postprocess_fix_count": 1,
            "report_length": 5000,
            "numeric_references": 20,
            "errors": 0,
        },
        {
            "stock_code": "600519",
            "label": "no_rag",
            "success": True,
            "overall_score": 80.0,
            "duration_s": 9.0,
            "total_tokens": 900,
            "llm_calls": 4,
            "tool_calls": 7,
            "agent_steps": 5,
            "rag_hits": 0,
            "news_count": 4,
            "risk_count": 2,
            "risk_evidence_count": 1,
            "risk_transmission_count": 1,
            "investment_anchor_present": False,
            "postprocess_fix_count": 3,
            "report_length": 4500,
            "numeric_references": 15,
            "errors": 0,
        },
    ]

    summary_md, aggregate = run_ablation.summarize_results(rows, use_llm_judge=False)

    assert "自动修补" in summary_md
    assert "平均自动修补次数" in summary_md
    assert aggregate["experiments"]["baseline"]["avg_postprocess_fix_count"] == 1.0
    assert aggregate["experiments"]["no_rag"]["avg_postprocess_fix_count"] == 3.0
    assert aggregate["experiment_contracts"]["baseline"]["banner"] == "Baseline（完整系统）"
    assert aggregate["history_summary"] == {}


def test_build_ablation_config_maps_experiment_flags():
    baseline = run_ablation._build_ablation_config("baseline")
    no_reflection = run_ablation._build_ablation_config("no_reflection")
    no_rag = run_ablation._build_ablation_config("no_rag")

    assert baseline == AblationConfig(label="baseline")
    assert no_reflection == AblationConfig(label="no_reflection", enable_reflection=False)
    assert no_rag == AblationConfig(label="no_rag", enable_rag=False)


def test_build_experiment_returns_explicit_contract():
    experiment = run_ablation._build_experiment("no_rag")

    assert experiment.label == "no_rag"
    assert experiment.banner == "-RAG（移除知识库检索）"
    assert experiment.config == AblationConfig(label="no_rag", enable_rag=False)


def test_run_experiment_passes_ablation_config_to_engine(monkeypatch):
    captured = {}

    class DummyEngine:
        def __init__(self, on_step=None, *, ablation_config=None):
            captured["config"] = ablation_config

        def run(self, stock_code):
            captured["stock_code"] = stock_code
            return {"stock_code": stock_code}

    monkeypatch.setattr("app.engine.ReportEngine", DummyEngine)

    result = run_ablation._run_experiment("600519", label="no_reflection", banner="Banner")

    assert result == {"stock_code": "600519"}
    assert captured["stock_code"] == "600519"
    assert captured["config"] == AblationConfig(label="no_reflection", enable_reflection=False)


def test_evaluate_state_exposes_ablation_contract_in_row(monkeypatch, tmp_path):
    state = type("State", (), {
        "final_report": "# report",
        "run_metrics": {"duration_s": 1.2, "llm_calls": 2, "tool_calls": 3, "total_tokens": 100, "errors": 0, "trace_id": "t1"},
        "sections": {"agent_steps": "4", "rag_hits": "0"},
        "news": [],
        "risks": [],
    })()

    class EvalResult:
        overall_score = 80.0
        section_coverage = 1.0
        has_tables = True
        has_numbers = True
        completeness = 4
        data_support = 4
        reasoning_quality = 4
        readability = 4
        report_length = 1000
        numeric_references = 10
        risk_evidence_count = 0
        risk_transmission_count = 0
        investment_anchor_present = True
        postprocess_fix_count = 0

    monkeypatch.setattr("app.evals.report_eval.evaluate_report", lambda *args, **kwargs: EvalResult())
    monkeypatch.setattr("app.evals.report_eval.evaluate_report_with_metrics", lambda *args, **kwargs: {"run_metrics": state.run_metrics})
    monkeypatch.setattr("app.evals.report_eval.format_eval_report", lambda result: "eval")

    row = run_ablation.evaluate_state(state, "no_reflection", "600519", use_llm_judge=False, output_dir=tmp_path)

    assert row["experiment_banner"] == "-Reflection（移除反思阶段）"
    assert row["ablation_config"] == {"label": "no_reflection", "enable_reflection": False, "enable_rag": True}


def test_ablation_main_writes_experiment_contracts_json(monkeypatch, tmp_path):
    monkeypatch.setattr(run_ablation, "RUNNERS", {
        "baseline": lambda stock_code: {"state": stock_code},
        "no_reflection": lambda stock_code: {"state": stock_code},
        "no_rag": lambda stock_code: {"state": stock_code},
    })
    monkeypatch.setattr(run_ablation, "evaluate_state", lambda state, label, stock_code, use_llm_judge, output_dir: {
        "label": label,
        "stock_code": stock_code,
        "success": True,
        "overall_score": 80.0,
        "duration_s": 1.0,
        "total_tokens": 100,
        "llm_calls": 1,
        "tool_calls": 1,
        "agent_steps": 1,
        "rag_hits": 1,
        "news_count": 0,
        "risk_count": 0,
        "risk_evidence_count": 0,
        "risk_transmission_count": 0,
        "investment_anchor_present": True,
        "postprocess_fix_count": 0,
        "report_length": 100,
        "numeric_references": 1,
        "errors": 0,
        "experiment_banner": "Baseline（完整系统）",
        "ablation_config": {"label": "baseline", "enable_reflection": True, "enable_rag": True},
    })
    (tmp_path / "ablation_summary.json").write_text(json.dumps({"aggregate": {"baseline": {"avg_score": 70.0, "avg_duration_s": 2.0, "avg_tokens": 90.0}}}, ensure_ascii=False), encoding="utf-8")

    assert run_ablation.main(["--stocks", "600519", "--output-dir", str(tmp_path)]) == 0
    payload = json.loads((tmp_path / "ablation_summary.json").read_text(encoding="utf-8"))

    assert payload["aggregate"]["baseline"]["avg_score"] == 80.0
    assert payload["experiment_contracts"]["baseline"]["banner"] == "Baseline（完整系统）"
    assert payload["experiment_contracts"]["baseline"]["ablation_config"]["enable_rag"] is True
    assert payload["history_summary"]["baseline"]["score_delta"] == 10.0
    assert payload["artifact_index"]["summary_json_path"].endswith("ablation_summary.json")
