from __future__ import annotations

import json
import subprocess

import run_quality_gate
from app.utils.tracer import Tracer


def test_build_gate_commands_and_format_results():
    args = run_quality_gate.parse_args([
        "--skip-tests",
        "--stocks",
        "600519",
        "000858",
        "--min-avg-score",
        "75",
    ])

    commands = run_quality_gate.build_gate_commands(args)
    assert len(commands) == 1
    name, cmd = commands[0]
    assert name == "golden_regression"
    assert cmd[1].endswith("main.py")
    assert cmd[2] == "regression"
    assert "--stocks" in cmd
    assert "600519" in cmd
    assert "000858" in cmd

    summary = run_quality_gate.format_results([
        {"name": "pytest", "passed": True, "returncode": 0},
        {"name": "golden_regression", "passed": False, "returncode": 1},
    ])
    assert "Overall: FAIL" in summary
    assert "pytest: PASS" in summary
    assert "golden_regression: FAIL" in summary


def test_write_summary_persists_markdown_and_json(tmp_path, monkeypatch):
    monkeypatch.setattr(run_quality_gate, "QUALITY_GATE_OUTPUT_DIR", tmp_path)
    regression_dir = tmp_path / "regression"
    regression_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(run_quality_gate, "DEFAULT_REGRESSION_OUTPUT_DIR", regression_dir)
    (regression_dir / "regression_summary.json").write_text(
        json.dumps({
            "aggregate": {"count": 1},
            "regression": {"overall_pass": True, "samples": 1, "checks": {"avg_score": {"passed": True}}},
        }, ensure_ascii=False),
        encoding="utf-8",
    )

    summary_path = run_quality_gate.write_summary(
        "# Quality Gate Summary\n",
        [{"name": "pytest", "command": ["python", "-m", "pytest"], "returncode": 0, "passed": True}],
    )

    assert summary_path == tmp_path / "quality_gate_summary.md"
    assert summary_path.read_text(encoding="utf-8") == "# Quality Gate Summary\n"
    payload = json.loads((tmp_path / "quality_gate_summary.json").read_text(encoding="utf-8"))
    assert payload["overall_pass"] is True
    assert payload["results"][0]["name"] == "pytest"
    assert payload["artifacts"]["step_count"] == 1
    assert payload["artifacts"]["step_categories"]["pytest"] == "verification"
    assert payload["artifacts"]["regression_overall_pass"] is True
    assert payload["artifacts"]["regression_aggregate"] == {"count": 1}
    assert payload["artifacts"]["regression_history_summary"] is None
    assert payload["artifacts"]["regression_artifact_index"] is None


def test_build_gate_commands_includes_llm_judge_and_thresholds():
    args = run_quality_gate.parse_args([
        "--skip-tests",
        "--llm-judge",
        "--min-success-rate",
        "95",
        "--min-anchor-coverage",
        "80",
    ])

    commands = run_quality_gate.build_gate_commands(args)
    _, cmd = commands[0]

    assert "--llm-judge" in cmd
    assert "--min-success-rate" in cmd
    assert "95.0" in cmd
    assert "--min-anchor-coverage" in cmd
    assert "80.0" in cmd


def test_build_gate_commands_keeps_custom_pytest_args():
    args = run_quality_gate.parse_args([
        "--skip-regression",
        "--pytest-args",
        "-q",
        "tests/test_main_cli.py",
    ])

    commands = run_quality_gate.build_gate_commands(args)
    name, cmd = commands[0]

    assert name == "pytest"
    assert cmd[-2:] == ["-q", "tests/test_main_cli.py"]


def test_run_gate_and_main_cover_success_path(monkeypatch, tmp_path):
    monkeypatch.setattr(run_quality_gate, "QUALITY_GATE_OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(run_quality_gate, "run_gate", lambda commands: [{"name": name, "command": cmd, "returncode": 0, "passed": True} for name, cmd in commands])

    result = run_quality_gate.main(["--skip-regression"])

    assert result == 0
    summary_path = tmp_path / "quality_gate_summary.md"
    assert summary_path.exists()
    assert "Overall: PASS" in summary_path.read_text(encoding="utf-8")
    payload = json.loads((tmp_path / "quality_gate_summary.json").read_text(encoding="utf-8"))
    assert payload["overall_pass"] is True



def test_quality_gate_main_returns_nonzero_when_gate_fails(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(run_quality_gate, "QUALITY_GATE_OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(run_quality_gate, "run_gate", lambda commands: [{"name": "pytest", "command": ["python", "-m", "pytest"], "returncode": 1, "passed": False}])

    result = run_quality_gate.main(["--skip-regression"])

    assert result == 1
    summary_text = (tmp_path / "quality_gate_summary.md").read_text(encoding="utf-8")
    assert "Overall: FAIL" in summary_text
    payload = json.loads((tmp_path / "quality_gate_summary.json").read_text(encoding="utf-8"))
    assert payload["overall_pass"] is False
    assert "质量门禁汇总已保存到" in capsys.readouterr().out



def test_quality_gate_main_returns_nonzero_when_all_steps_skipped(capsys):
    result = run_quality_gate.main(["--skip-tests", "--skip-regression"])

    assert result == 1
    assert "未选择任何质量门禁步骤" in capsys.readouterr().out



def test_run_gate_captures_return_codes(monkeypatch):
    calls = []

    def fake_run(cmd, cwd=None):
        calls.append((cmd, cwd))
        return subprocess.CompletedProcess(cmd, 1)

    monkeypatch.setattr(run_quality_gate.subprocess, "run", fake_run)

    results = run_quality_gate.run_gate([("pytest", ["python", "-m", "pytest"])])

    assert calls[0][0] == ["python", "-m", "pytest"]
    assert results[0]["passed"] is False
    assert results[0]["returncode"] == 1


def test_format_results_handles_empty_result_list():
    summary = run_quality_gate.format_results([])

    assert "Overall: FAIL" in summary


def test_extract_gate_artifacts_tracks_failed_steps(tmp_path, monkeypatch):
    regression_dir = tmp_path / "regression"
    regression_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(run_quality_gate, "DEFAULT_REGRESSION_OUTPUT_DIR", regression_dir)
    (regression_dir / "regression_summary.json").write_text(
        json.dumps({
            "aggregate": {"count": 2},
            "regression": {"overall_pass": False, "samples": 2, "checks": {"avg_score": {"passed": False}}},
            "history_summary": {"score_delta": -1.0},
            "artifact_index": {"summary_json_path": "regression_summary.json"},
        }, ensure_ascii=False),
        encoding="utf-8",
    )

    artifacts = run_quality_gate._extract_gate_artifacts([
        {"name": "pytest", "passed": True},
        {"name": "golden_regression", "passed": False},
    ])

    assert artifacts["step_count"] == 2
    assert artifacts["passed_steps"] == ["pytest"]
    assert artifacts["failed_steps"] == ["golden_regression"]
    assert artifacts["step_categories"]["golden_regression"] == "regression"
    assert artifacts["regression_overall_pass"] is False
    assert artifacts["regression_samples"] == 2
    assert artifacts["regression_history_summary"] == {"score_delta": -1.0}
    assert artifacts["regression_artifact_index"] == {"summary_json_path": "regression_summary.json"}


def test_tracer_summary_includes_phase_breakdown_and_failed_phases():
    tracer = Tracer()
    with tracer.span("data_prefetch", "phase"):
        pass
    try:
        with tracer.span("write_report", "phase"):
            raise RuntimeError("boom")
    except RuntimeError:
        pass

    summary = tracer.summary()

    assert summary["phases"] == 2
    assert summary["phase_total_ms"] >= 0
    assert summary["phase_breakdown"][0]["name"] == "data_prefetch"
    assert any(item["name"] == "write_report" and item["status"] == "error" for item in summary["phase_breakdown"])
    assert summary["failed_phases"][0]["name"] == "write_report"
    assert summary["errors"] >= 1
