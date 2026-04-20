from __future__ import annotations

from types import SimpleNamespace

from app.evals.report_eval import EvalResult
from app.ui.alerts import build_alert_summary, build_top_alerts, classify_run_error


def test_build_top_alerts_contains_consistency_warning():
    result = EvalResult(overall_score=78.0, section_coverage=1.0, consistency_issue_count=2, data_gap_disclosure_count=1)

    alerts = build_top_alerts(result)

    assert any(level == "warning" and "一致性问题" in message for level, message in alerts)


def test_build_top_alerts_contains_success_when_stable():
    result = EvalResult(overall_score=82.0, section_coverage=1.0, consistency_issue_count=0, data_gap_disclosure_count=1, risk_transmission_count=1)

    alerts = build_top_alerts(result)

    assert any(level == "success" for level, _ in alerts)


def test_build_top_alerts_contains_risk_path_info():
    result = EvalResult(overall_score=70.0, section_coverage=1.0, consistency_issue_count=0, data_gap_disclosure_count=1, risk_transmission_count=0)

    alerts = build_top_alerts(result)

    assert any("风险传导路径" in message for _, message in alerts)


def test_build_alert_summary_prioritizes_consistency():
    result = EvalResult(overall_score=84.0, section_coverage=1.0, consistency_issue_count=1, data_gap_disclosure_count=1)

    summary = build_alert_summary(result)

    assert summary["level"] == "warning"
    assert "一致性风险" in summary["title"]


def test_classify_run_error_detects_api_configuration_issue():
    classified = classify_run_error("API key invalid")

    assert classified["title"] == "配置或鉴权异常"
    assert "API Key" in classified["hint"]
