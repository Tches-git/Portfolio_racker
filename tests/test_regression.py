from __future__ import annotations

import json

import run_regression


def test_build_regression_checks_and_summary_section():
    rows = [
        {
            "success": True,
            "overall_score": 82.0,
            "section_coverage": 1.0,
            "investment_anchor_present": True,
        },
        {
            "success": True,
            "overall_score": 78.0,
            "section_coverage": 0.875,
            "investment_anchor_present": True,
        },
    ]

    regression = run_regression.build_regression_checks(
        rows,
        min_success_rate=100.0,
        min_avg_score=75.0,
        min_avg_section_coverage=0.85,
        min_anchor_coverage=100.0,
    )
    summary = run_regression.append_regression_section("# 汇总", regression)

    assert regression["overall_pass"] is True
    assert regression["checks"]["avg_score"]["actual"] == 80.0
    assert "黄金集回归判定" in summary
    assert "平均评分" in summary
    assert "估值锚覆盖率" in summary


def test_build_regression_checks_handles_empty_rows():
    regression = run_regression.build_regression_checks(
        [],
        min_success_rate=100.0,
        min_avg_score=70.0,
        min_avg_section_coverage=0.875,
        min_anchor_coverage=100.0,
    )

    assert regression["overall_pass"] is False
    assert regression["samples"] == 0
    assert regression["checks"]["success_rate"]["actual"] == 0.0


def test_regression_main_writes_outputs_and_returns_zero(monkeypatch, tmp_path):
    monkeypatch.setattr(run_regression.run_ablation, "RUNNERS", {"baseline": lambda stock_code: {"state": stock_code}})
    monkeypatch.setattr(run_regression.run_ablation, "evaluate_state", lambda state, experiment, stock_code, use_llm_judge, output_dir: {
        "success": True,
        "overall_score": 80.0,
        "section_coverage": 1.0,
        "investment_anchor_present": True,
        "stock_code": stock_code,
    })
    monkeypatch.setattr(run_regression.run_ablation, "summarize_results", lambda rows, use_llm_judge=False, previous_aggregate=None: ("# 汇总", {"experiments": {"baseline": {"avg_score": 80.0, "avg_duration_s": 1.0}}, "experiment_contracts": {}, "history_summary": {}}))

    result = run_regression.main(["--stocks", "600519", "000858", "--output-dir", str(tmp_path)])

    assert result == 0
    summary_path = tmp_path / "regression_summary.md"
    payload_path = tmp_path / "regression_summary.json"
    assert summary_path.exists()
    assert payload_path.exists()
    assert "黄金集回归判定" in summary_path.read_text(encoding="utf-8")
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    assert payload["aggregate"]["baseline"]["avg_score"] == 80.0
    assert payload["regression"]["overall_pass"] is True
    assert payload["artifact_index"]["summary_json_path"].endswith("regression_summary.json")


def test_parse_args_accepts_custom_summary_name():
    args = run_regression.parse_args(["--summary-name", "nightly_regression"])

    assert args.summary_name == "nightly_regression"


def test_regression_main_uses_custom_summary_name(monkeypatch, tmp_path):
    monkeypatch.setattr(run_regression.run_ablation, "RUNNERS", {"baseline": lambda stock_code: {"state": stock_code}})
    monkeypatch.setattr(run_regression.run_ablation, "evaluate_state", lambda state, experiment, stock_code, use_llm_judge, output_dir: {
        "success": True,
        "overall_score": 80.0,
        "section_coverage": 1.0,
        "investment_anchor_present": True,
        "stock_code": stock_code,
    })
    monkeypatch.setattr(run_regression.run_ablation, "summarize_results", lambda rows, use_llm_judge=False, previous_aggregate=None: ("# 汇总", {"experiments": {"baseline": {"avg_score": 80.0, "avg_duration_s": 1.0}}, "experiment_contracts": {}, "history_summary": {}}))

    result = run_regression.main([
        "--stocks", "600519",
        "--output-dir", str(tmp_path),
        "--summary-name", "nightly_regression",
    ])

    assert result == 0
    assert (tmp_path / "nightly_regression.md").exists()
    assert (tmp_path / "nightly_regression.json").exists()


def test_regression_main_returns_nonzero_when_threshold_fails(monkeypatch, tmp_path):
    monkeypatch.setattr(run_regression.run_ablation, "RUNNERS", {"baseline": lambda stock_code: {"state": stock_code}})
    monkeypatch.setattr(run_regression.run_ablation, "evaluate_state", lambda state, experiment, stock_code, use_llm_judge, output_dir: {
        "success": True,
        "overall_score": 60.0,
        "section_coverage": 0.5,
        "investment_anchor_present": False,
        "stock_code": stock_code,
    })
    monkeypatch.setattr(run_regression.run_ablation, "summarize_results", lambda rows, use_llm_judge=False, previous_aggregate=None: ("# 汇总", {"experiments": {"baseline": {"avg_score": 80.0, "avg_duration_s": 1.0}}, "experiment_contracts": {}, "history_summary": {}}))

    result = run_regression.main(["--stocks", "600519", "--output-dir", str(tmp_path)])

    assert result == 1
    payload = json.loads((tmp_path / "regression_summary.json").read_text(encoding="utf-8"))
    assert payload["regression"]["overall_pass"] is False
    assert payload["regression"]["checks"]["avg_score"]["passed"] is False


def test_regression_main_skips_empty_rows_in_aggregate(monkeypatch, tmp_path):
    monkeypatch.setattr(run_regression.run_ablation, "RUNNERS", {"baseline": lambda stock_code: {"state": stock_code}})
    rows = iter([
        None,
        {"success": True, "overall_score": 80.0, "section_coverage": 1.0, "investment_anchor_present": True, "stock_code": "000858"},
    ])
    monkeypatch.setattr(run_regression.run_ablation, "evaluate_state", lambda state, experiment, stock_code, use_llm_judge, output_dir: next(rows))
    monkeypatch.setattr(run_regression.run_ablation, "summarize_results", lambda rows, use_llm_judge=False, previous_aggregate=None: ("# 汇总", {"experiments": {"baseline": {"avg_score": 80.0, "avg_duration_s": 1.0}}, "experiment_contracts": {}, "history_summary": {}}))

    result = run_regression.main(["--stocks", "600519", "000858", "--output-dir", str(tmp_path)])

    assert result == 0
    payload = json.loads((tmp_path / "regression_summary.json").read_text(encoding="utf-8"))
    assert len(payload["rows"]) == 1
    assert payload["aggregate"]["baseline"]["avg_score"] == 80.0


def test_append_regression_section_formats_section_coverage_as_percent():
    summary = run_regression.append_regression_section("# 汇总", {
        "overall_pass": False,
        "checks": {
            "avg_section_coverage": {"actual": 0.875, "threshold": 0.9, "passed": False},
        },
    })

    assert "87.5%" in summary
    assert "90.0%" in summary
