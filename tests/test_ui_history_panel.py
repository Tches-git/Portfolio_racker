from __future__ import annotations

from types import SimpleNamespace

from app.ui.history_panel import build_history_detail, build_history_focus_options, build_recent_history_rows, filter_history_records


def test_build_recent_history_rows_formats_core_fields():
    records = [
        SimpleNamespace(stock_name="贵州茅台", stock_code="600519", timestamp="2026-04-19T12:34:56", rating="推荐", risk_count=2, conclusion="品牌力强，盈利能力稳健。"),
        SimpleNamespace(stock_name="宁德时代", stock_code="300750", timestamp="2026-04-18T08:00:00", rating="中性", risk_count=1, conclusion="需求波动需继续观察。"),
    ]

    rows = build_recent_history_rows(records)

    assert rows[0]["股票"] == "贵州茅台 (600519)"
    assert rows[0]["时间"] == "2026-04-19 12:34:56"
    assert rows[0]["评级"] == "推荐"
    assert rows[0]["风险数"] == "2"
    assert "盈利能力稳健" in rows[0]["结论摘要"]


def test_build_history_focus_options_deduplicates_by_stock_code():
    records = [
        SimpleNamespace(stock_name="贵州茅台", stock_code="600519", timestamp="2026-04-19T12:34:56", rating="推荐", risk_count=2, conclusion="A"),
        SimpleNamespace(stock_name="贵州茅台", stock_code="600519", timestamp="2026-04-18T08:00:00", rating="中性", risk_count=1, conclusion="B"),
        SimpleNamespace(stock_name="宁德时代", stock_code="300750", timestamp="2026-04-17T08:00:00", rating="中性", risk_count=1, conclusion="C"),
    ]

    options = build_history_focus_options(records)

    assert len(options) == 2
    assert options[0]["code"] == "600519"
    assert "贵州茅台" in options[0]["label"]


def test_build_history_detail_extracts_master_detail_payload():
    record = SimpleNamespace(
        stock_name="贵州茅台",
        stock_code="600519",
        timestamp="2026-04-19T12:34:56",
        rating="推荐",
        risk_count=2,
        conclusion="品牌力强，盈利能力稳健。",
        risk_summary="需求波动；渠道调整",
    )

    detail = build_history_detail(record)

    assert detail["title"] == "贵州茅台 (600519)"
    assert "评级 推荐" in detail["meta"]
    assert "渠道调整" in detail["risk_summary"]


def test_filter_history_records_supports_keyword_search():
    records = [
        SimpleNamespace(stock_name="贵州茅台", stock_code="600519", timestamp="2026-04-19T12:34:56", rating="推荐", conclusion="品牌力强"),
        SimpleNamespace(stock_name="宁德时代", stock_code="300750", timestamp="2026-04-18T12:34:56", rating="中性", conclusion="需求波动"),
    ]

    filtered = filter_history_records(records, "茅台")

    assert len(filtered) == 1
    assert filtered[0].stock_code == "600519"
