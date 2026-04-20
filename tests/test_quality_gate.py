from __future__ import annotations

import run_quality_gate


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
