from __future__ import annotations

from app.ui.stock_insights import build_stock_insight_rows


def test_build_stock_insight_rows_formats_summary():
    stocks = [
        {"code": "600519", "name": "贵州茅台", "count": 3, "latest": "2026-04-19T13:00:00"},
        {"code": "300750", "name": "宁德时代", "count": 2, "latest": "2026-04-18T10:30:00"},
    ]

    rows = build_stock_insight_rows(stocks)

    assert rows[0]["股票"] == "贵州茅台 (600519)"
    assert rows[0]["分析次数"] == "3"
    assert rows[0]["最近分析"] == "2026-04-19 13:00:00"
