from __future__ import annotations

from app.finance.valuation import run_monte_carlo_dcf
from app.models import FinancialMetrics, StockProfile


def test_run_monte_carlo_dcf_returns_distribution():
    metrics = [
        FinancialMetrics(
            code="600519",
            period="2024-12-31",
            revenue=1000,
            net_profit=300,
            revenue_yoy=12,
            profit_yoy=10,
            cash_flow=260,
            total_liability=100,
            cash_and_equivalents=40,
        )
    ]
    profile = StockProfile(
        code="600519",
        name="Test",
        industry="饮料",
        market_cap=2000,
        pe_ratio=20,
        pb_ratio=5,
        total_shares=10,
    )

    result = run_monte_carlo_dcf(metrics, profile, simulations=200)

    assert result
    assert result["simulations"] > 0
    assert len(result["values"]) == result["simulations"]
    assert result["p10"] <= result["p50"] <= result["p90"]
    assert 0 <= result["prob_above_current"] <= 100
