from __future__ import annotations

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
