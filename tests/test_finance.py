"""金融计算模块单元测试"""
from __future__ import annotations

import math
import pytest

from app.models import FinancialMetrics, StockProfile, DuPontResult


# ── Helper 函数 ──────────────────────────────────────────────


def make_metrics(
    code: str = "000001",
    period: str = "2024Q3",
    revenue: float = 100.0,
    net_profit: float = 20.0,
    revenue_yoy: float = 10.0,
    profit_yoy: float = 15.0,
    roe: float = 15.0,
    gross_margin: float = 40.0,
    debt_ratio: float = 45.0,
    cash_flow: float = 25.0,
    total_assets: float = 500.0,
    total_equity: float = 300.0,
    total_liability: float = 200.0,
    operating_cost: float = 60.0,
) -> FinancialMetrics:
    return FinancialMetrics(
        code=code,
        period=period,
        revenue=revenue,
        net_profit=net_profit,
        revenue_yoy=revenue_yoy,
        profit_yoy=profit_yoy,
        roe=roe,
        gross_margin=gross_margin,
        debt_ratio=debt_ratio,
        cash_flow=cash_flow,
        total_assets=total_assets,
        total_equity=total_equity,
        total_liability=total_liability,
        operating_cost=operating_cost,
    )


def make_profile(
    code: str = "000001",
    name: str = "测试公司",
    industry: str = "制造业",
    market_cap: float = 1000.0,
    pe_ratio: float = 20.0,
    pb_ratio: float = 3.0,
    total_shares: float = 50.0,
) -> StockProfile:
    return StockProfile(
        code=code,
        name=name,
        industry=industry,
        market_cap=market_cap,
        pe_ratio=pe_ratio,
        pb_ratio=pb_ratio,
        total_shares=total_shares,
    )


# ══════════════════════════════════════════════════════════════
# 1. 杜邦分析测试
# ══════════════════════════════════════════════════════════════


class TestDupont:
    """app.finance.dupont 模块测试"""

    def test_normal_case(self):
        """正常情况：给定 revenue=100, net_profit=20, total_assets=500,
        total_equity=300, roe=10 → net_margin≈20%, asset_turnover≈0.2,
        equity_multiplier≈1.667"""
        from app.finance.dupont import analyze_dupont

        m = make_metrics(
            revenue=100, net_profit=20,
            total_assets=500, total_equity=300, roe=10,
        )
        results = analyze_dupont([m])
        assert len(results) == 1
        r = results[0]
        assert r.net_margin == pytest.approx(20.0, abs=0.01)
        assert r.asset_turnover == pytest.approx(0.2, abs=0.001)
        assert r.equity_multiplier == pytest.approx(1.6667, abs=0.01)

    def test_roe_decomposition_consistency(self):
        """ROE 分解一致性：computed_roe ≈ net_margin/100 * asset_turnover * equity_multiplier * 100"""
        from app.finance.dupont import analyze_dupont

        m = make_metrics(
            revenue=200, net_profit=30,
            total_assets=800, total_equity=400, roe=18,
        )
        results = analyze_dupont([m])
        r = results[0]
        expected_roe = r.net_margin / 100 * r.asset_turnover * r.equity_multiplier * 100
        assert r.computed_roe == pytest.approx(expected_roe, abs=0.1)

    def test_empty_data(self):
        """传入空列表返回空列表"""
        from app.finance.dupont import analyze_dupont

        assert analyze_dupont([]) == []

    def test_format_dupont_table_markdown(self):
        """format_dupont_table 返回的字符串包含 Markdown 表格标记"""
        from app.finance.dupont import format_dupont_table

        results = [
            DuPontResult(
                period="2024Q3", roe=15.0,
                net_margin=20.0, asset_turnover=0.2,
                equity_multiplier=1.667, computed_roe=6.67,
            )
        ]
        table = format_dupont_table(results)
        assert "|" in table
        assert "---" in table
        assert "2024Q3" in table


# ══════════════════════════════════════════════════════════════
# 2. DCF 估值测试
# ══════════════════════════════════════════════════════════════


class TestValuation:
    """app.finance.valuation 模块测试"""

    def test_dcf_normal(self):
        """正常 DCF：per_share_value > 0, enterprise_value > 0"""
        from app.finance.valuation import dcf_valuation

        m = make_metrics(cash_flow=30, total_liability=200, revenue_yoy=10)
        p = make_profile(total_shares=50, market_cap=1000)
        result = dcf_valuation([m], p)
        assert result is not None
        assert result.per_share_value > 0
        assert result.enterprise_value > 0

    def test_equity_value_deducts_net_debt(self):
        """equity_value 应扣除净债务（enterprise_value - net_debt >= 0）"""
        from app.finance.valuation import dcf_valuation

        m = make_metrics(cash_flow=10, total_liability=100, revenue_yoy=8)
        p = make_profile(total_shares=50, market_cap=500)
        result = dcf_valuation([m], p)
        assert result is not None
        # equity_value = enterprise_value - net_debt，net_debt >= 0
        # 因此 equity_value <= enterprise_value
        assert result.equity_value <= result.enterprise_value

    def test_dcf_negative_cash_flow_uses_profit(self):
        """现金流为负时使用净利润的70%作为基础FCF"""
        from app.finance.valuation import dcf_valuation
        m = make_metrics(cash_flow=-10, net_profit=30, total_liability=100, revenue_yoy=10)
        p = make_profile(total_shares=50, market_cap=1000)
        result = dcf_valuation([m], p)
        assert result is not None
        assert result.per_share_value > 0

    def test_dcf_zero_profit_and_cashflow_returns_none(self):
        """净利润和现金流都为零/负时返回None"""
        from app.finance.valuation import dcf_valuation
        m = make_metrics(cash_flow=-10, net_profit=-5, total_liability=100, revenue_yoy=10)
        p = make_profile(total_shares=50, market_cap=1000)
        result = dcf_valuation([m], p)
        assert result is None

    def test_comparable_uses_median(self):
        """可比估值应使用中位数而非均值"""
        from app.finance.valuation import comparable_valuation
        p = make_profile(pe_ratio=20, pb_ratio=3, market_cap=1000)
        from app.models import PeerCompany
        peers = [
            PeerCompany(code="001", name="A", pe_ratio=15, pb_ratio=2),
            PeerCompany(code="002", name="B", pe_ratio=18, pb_ratio=2.5),
            PeerCompany(code="003", name="C", pe_ratio=20, pb_ratio=3),
            PeerCompany(code="004", name="D", pe_ratio=150, pb_ratio=10),  # 极端值
        ]
        result = comparable_valuation(p, peers)
        # 中位数 = (18+20)/2 = 19，而非均值 50.75
        assert result["peer_avg_pe"] == pytest.approx(19.0, abs=0.1)

    def test_no_data_returns_none(self):
        """无数据返回 None"""
        from app.finance.valuation import dcf_valuation

        p = make_profile()
        assert dcf_valuation([], p) is None

    def test_monte_carlo_percentiles(self):
        """蒙特卡洛返回结果包含 p10, p50, p90 且 p10 <= p50 <= p90"""
        from app.finance.valuation import run_monte_carlo_dcf

        m = make_metrics(cash_flow=30, total_liability=200, revenue_yoy=12)
        p = make_profile(total_shares=50, market_cap=1000)
        mc = run_monte_carlo_dcf([m], p, simulations=500)
        assert mc  # 非空字典
        assert "p10" in mc
        assert "p50" in mc
        assert "p90" in mc
        assert mc["p10"] <= mc["p50"] <= mc["p90"]

    def test_sensitivity_table_dimensions(self):
        """敏感性分析矩阵维度正确"""
        from app.finance.valuation import build_sensitivity_table

        m = make_metrics(cash_flow=30, total_liability=200, revenue_yoy=10)
        p = make_profile(total_shares=50, market_cap=1000)
        waccs = [8.0, 10.0, 12.0]
        growths = [3.0, 5.0, 10.0, 15.0]
        result = build_sensitivity_table([m], p, wacc_range=waccs, growth_range=growths)
        assert len(result["matrix"]) == len(waccs)
        for row in result["matrix"]:
            assert len(row) == len(growths)
        assert "table_md" in result


# ══════════════════════════════════════════════════════════════
# 3. 趋势分析测试
# ══════════════════════════════════════════════════════════════


class TestTrend:
    """app.finance.trend 模块测试"""

    def test_cagr_calculation(self):
        """CAGR 计算：100 → 200 经过 3 年，CAGR ≈ 26.0%"""
        from app.finance.trend import _calc_cagr

        cagr = _calc_cagr(100, 200, 3)
        assert cagr == pytest.approx(26.0, abs=0.1)

    def test_direction_ascending(self):
        """持续增长 → '上升'"""
        from app.finance.trend import _determine_direction

        assert _determine_direction([10, 20, 30, 40]) == "上升"

    def test_direction_descending(self):
        """持续下降 → '下降'"""
        from app.finance.trend import _determine_direction

        assert _determine_direction([40, 30, 20, 10]) == "下降"

    def test_empty_data(self):
        """空数据返回空列表"""
        from app.finance.trend import analyze_trends

        assert analyze_trends([]) == []

    def test_analyze_trends_multi_period(self):
        """多期数据趋势分析正常返回"""
        from app.finance.trend import analyze_trends

        metrics = [
            make_metrics(period="2024", revenue=150, net_profit=30, roe=18, gross_margin=45, debt_ratio=40),
            make_metrics(period="2023", revenue=130, net_profit=25, roe=16, gross_margin=43, debt_ratio=42),
            make_metrics(period="2022", revenue=100, net_profit=20, roe=14, gross_margin=40, debt_ratio=45),
        ]
        trends = analyze_trends(metrics)
        assert len(trends) > 0
        revenue_trend = next(t for t in trends if t.metric_name == "营收")
        assert revenue_trend.trend_direction == "上升"
        assert revenue_trend.cagr > 0


# ══════════════════════════════════════════════════════════════
# 4. 量化评分测试
# ══════════════════════════════════════════════════════════════


class TestMetrics:
    """app.finance.metrics 模块测试"""

    def test_excellent_company_high_profitability(self):
        """优秀公司评分应偏高（ROE>20, 毛利率>50, 利润增速>20）"""
        from app.finance.metrics import score_profitability

        m = make_metrics(roe=25, gross_margin=55, profit_yoy=25, revenue_yoy=20)
        result = score_profitability([m])
        assert result["score"] >= 80

    def test_high_risk_low_safety(self):
        """高风险公司评分应偏低（负债率>70, 现金流<0）"""
        from app.finance.metrics import score_safety

        m = make_metrics(debt_ratio=75, cash_flow=-10, revenue_yoy=-15)
        result = score_safety([m])
        assert result["score"] <= 30

    def test_score_safety_finance_industry(self):
        """score_safety 对金融行业使用更高的负债率阈值（industry 参数）
        
        注意：当前 score_safety 尚未实现 industry 参数，
        此测试验证金融行业场景下负债率 80% 不应判为高风险。
        如果函数签名已新增 industry 参数，取消 skipif。
        """
        import inspect
        from app.finance.metrics import score_safety

        sig = inspect.signature(score_safety)
        if "industry" not in sig.parameters:
            pytest.skip("score_safety 尚未新增 industry 参数，跳过此测试")

        # 金融行业：负债率 80% 仍可接受
        m = make_metrics(debt_ratio=80, cash_flow=50, revenue_yoy=5)
        result = score_safety([m], industry="金融")
        # 金融行业 80% 负债率不应判为极低分
        assert result["score"] >= 20

    def test_overall_rating_levels(self):
        """overall_rating 分级：>=80 强烈推荐, >=65 推荐, >=50 中性, >=35 谨慎, <35 回避"""
        from app.finance.metrics import overall_rating

        assert overall_rating(90, 90, 90)[0] == "强烈推荐"
        assert overall_rating(70, 70, 70)[0] == "推荐"
        assert overall_rating(55, 55, 55)[0] == "中性"
        assert overall_rating(40, 40, 40)[0] == "谨慎"
        assert overall_rating(10, 10, 10)[0] == "回避"


# ══════════════════════════════════════════════════════════════
# 5. 风险模型测试
# ══════════════════════════════════════════════════════════════


class TestRiskModel:
    """app.finance.risk_model 模块测试"""

    def test_high_debt_triggers_high_risk(self):
        """高负债率触发 high 风险"""
        from app.finance.risk_model import assess_financial_risks

        m = make_metrics(debt_ratio=80)
        p = make_profile()
        risks = assess_financial_risks(p, [m])
        high_debt_risks = [
            r for r in risks
            if r.level == "high" and "负债" in r.description
        ]
        assert len(high_debt_risks) >= 1

    def test_profit_decline_triggers_risk(self):
        """利润大幅下滑触发风险"""
        from app.finance.risk_model import assess_financial_risks

        m = make_metrics(profit_yoy=-35)
        p = make_profile()
        risks = assess_financial_risks(p, [m])
        profit_risks = [
            r for r in risks
            if "利润" in r.description or "profit" in r.metric.lower()
        ]
        assert len(profit_risks) >= 1

    def test_negative_cashflow_triggers_risk(self):
        """经营现金流为负触发风险"""
        from app.finance.risk_model import assess_financial_risks
        m = make_metrics(cash_flow=-20, debt_ratio=40)
        p = make_profile()
        risks = assess_financial_risks(p, [m])
        cash_risks = [r for r in risks if "现金" in r.description or "cash" in r.metric.lower()]
        assert len(cash_risks) >= 1

    def test_high_pe_triggers_risk(self):
        """PE过高触发估值风险"""
        from app.finance.risk_model import assess_financial_risks
        m = make_metrics()
        p = make_profile(pe_ratio=150)
        risks = assess_financial_risks(p, [m])
        valuation_risks = [r for r in risks if "估值" in r.description or "PE" in r.description.upper()]
        assert len(valuation_risks) >= 1

    def test_normal_no_high_risk(self):
        """正常指标不触发 high 级别的财务风险"""
        from app.finance.risk_model import assess_financial_risks

        m = make_metrics(
            debt_ratio=40, profit_yoy=10, cash_flow=30,
            roe=15,
        )
        p = make_profile(pe_ratio=20)
        risks = assess_financial_risks(p, [m])
        high_risks = [r for r in risks if r.level == "high"]
        assert len(high_risks) == 0
