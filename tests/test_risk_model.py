from __future__ import annotations

from app.finance.risk_model import _sanitize_external_text, assess_financial_risks, assess_news_risks
from app.models import FinancialMetrics, StockProfile


def test_sanitize_external_text_removes_control_chars_and_truncates():
    text = "hello\x00world\n" + "a" * 300
    cleaned = _sanitize_external_text(text, max_len=20)
    assert "\x00" not in cleaned
    assert "\n" not in cleaned
    assert len(cleaned) == 20


def test_assess_financial_risks_contains_evidence_and_path():
    profile = StockProfile(code="600519", name="茅台", industry="白酒", pe_ratio=90)
    metrics = [FinancialMetrics(code="600519", period="2025-12-31", debt_ratio=75, profit_yoy=-35, cash_flow=-10, roe=2)]

    risks = assess_financial_risks(profile, metrics)

    assert risks
    assert any(r.evidence for r in risks)
    assert any(r.transmission_path for r in risks)
    assert any(r.impact for r in risks)


def test_assess_news_risks_extracts_rule_based_risk():
    news = [{
        "title": "公司收到监管问询函",
        "content": "涉及信息披露与经营波动事项",
        "source": "东财",
        "time": "2026-01-02",
    }]

    risks = assess_news_risks(news, "茅台")

    assert len(risks) == 1
    assert risks[0].category == "news"
    assert "监管" in risks[0].description
    assert risks[0].evidence
    assert risks[0].transmission_path
