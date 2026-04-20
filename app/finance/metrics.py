"""财务指标分析模块 — 多维度量化评分"""
from __future__ import annotations
from app.models import FinancialMetrics, StockProfile

def score_profitability(metrics: list[FinancialMetrics]) -> dict:
    """盈利能力评分 (0-100)"""
    if not metrics:
        return {"score": 0, "details": "无数据"}
    latest = metrics[0]
    score = 0
    details = []
    # ROE
    if latest.roe > 20:
        score += 30; details.append(f"ROE {latest.roe:.1f}% 优秀(>20%)")
    elif latest.roe > 10:
        score += 20; details.append(f"ROE {latest.roe:.1f}% 良好(>10%)")
    elif latest.roe > 0:
        score += 10; details.append(f"ROE {latest.roe:.1f}% 一般")
    else:
        details.append(f"ROE {latest.roe:.1f}% 亏损")
    # 毛利率
    if latest.gross_margin > 50:
        score += 30; details.append(f"毛利率 {latest.gross_margin:.1f}% 高壁垒")
    elif latest.gross_margin > 30:
        score += 20; details.append(f"毛利率 {latest.gross_margin:.1f}% 中等")
    else:
        score += 5; details.append(f"毛利率 {latest.gross_margin:.1f}% 偏低")
    # 净利润增速
    if latest.profit_yoy > 20:
        score += 25; details.append(f"利润增速 {latest.profit_yoy:+.1f}% 高增长")
    elif latest.profit_yoy > 0:
        score += 15; details.append(f"利润增速 {latest.profit_yoy:+.1f}% 正增长")
    else:
        score += 0; details.append(f"利润增速 {latest.profit_yoy:+.1f}% 下滑")
    # 营收增速
    if latest.revenue_yoy > 15:
        score += 15; details.append(f"营收增速 {latest.revenue_yoy:+.1f}% 良好")
    elif latest.revenue_yoy > 0:
        score += 10; details.append(f"营收增速 {latest.revenue_yoy:+.1f}% 平稳")
    else:
        details.append(f"营收增速 {latest.revenue_yoy:+.1f}% 下滑")
    return {"score": min(score, 100), "details": "; ".join(details)}

def score_safety(metrics: list[FinancialMetrics], industry: str = "") -> dict:
    """安全性评分 (0-100)"""
    if not metrics:
        return {"score": 0, "details": "无数据"}
    latest = metrics[0]
    score = 0
    details = []
    # 资产负债率（区分行业）
    is_financial = any(kw in industry for kw in ("银行", "保险", "证券", "金融"))
    debt_thresholds = (60, 80, 90) if is_financial else (30, 50, 70)
    if latest.debt_ratio < debt_thresholds[0]:
        score += 40; details.append(f"负债率 {latest.debt_ratio:.1f}% 很安全")
    elif latest.debt_ratio < debt_thresholds[1]:
        score += 30; details.append(f"负债率 {latest.debt_ratio:.1f}% 适中")
    elif latest.debt_ratio < debt_thresholds[2]:
        score += 15; details.append(f"负债率 {latest.debt_ratio:.1f}% 偏高")
    else:
        score += 0; details.append(f"负债率 {latest.debt_ratio:.1f}% 高风险")
    # 现金流
    if latest.cash_flow > 0:
        score += 35; details.append(f"经营现金流 {latest.cash_flow:.1f}亿 为正")
    else:
        score += 0; details.append(f"经营现金流 {latest.cash_flow:.1f}亿 为负⚠️")
    # 增长稳定性（看多期）
    if len(metrics) >= 2:
        growth_stable = all(m.revenue_yoy > -10 for m in metrics[:3])
        if growth_stable:
            score += 25; details.append("近几期营收稳定")
        else:
            score += 5; details.append("营收波动较大")
    return {"score": min(score, 100), "details": "; ".join(details)}

def score_valuation(profile: StockProfile) -> dict:
    """估值评分 (0-100)"""
    score = 0
    details = []
    pe = profile.pe_ratio
    pb = profile.pb_ratio
    if pe <= 0:
        score += 0; details.append(f"PE {pe:.1f} 亏损或无意义")
    elif pe < 15:
        score += 45; details.append(f"PE {pe:.1f} 低估")
    elif pe < 30:
        score += 30; details.append(f"PE {pe:.1f} 合理")
    elif pe < 60:
        score += 15; details.append(f"PE {pe:.1f} 偏高")
    else:
        score += 0; details.append(f"PE {pe:.1f} 高估⚠️")
    if pb <= 0:
        details.append(f"PB {pb:.1f} 无效")
    elif pb < 2:
        score += 35; details.append(f"PB {pb:.1f} 低估")
    elif pb < 5:
        score += 20; details.append(f"PB {pb:.1f} 合理")
    else:
        score += 5; details.append(f"PB {pb:.1f} 偏高")
    cap = profile.market_cap
    if cap > 0:
        if cap > 5000:
            details.append(f"市值 {cap:.0f}亿 超大盘")
        elif cap > 1000:
            details.append(f"市值 {cap:.0f}亿 大盘")
        elif cap > 200:
            details.append(f"市值 {cap:.0f}亿 中盘")
        else:
            details.append(f"市值 {cap:.0f}亿 小盘")
    return {"score": min(score, 100), "details": "; ".join(details)}

def overall_rating(profitability: int, safety: int, valuation: int) -> tuple[str, str]:
    """综合评级"""
    total = profitability * 0.4 + safety * 0.3 + valuation * 0.3
    if total >= 80:
        return "强烈推荐", f"综合评分 {total:.0f}/100"
    elif total >= 65:
        return "推荐", f"综合评分 {total:.0f}/100"
    elif total >= 50:
        return "中性", f"综合评分 {total:.0f}/100"
    elif total >= 35:
        return "谨慎", f"综合评分 {total:.0f}/100"
    else:
        return "回避", f"综合评分 {total:.0f}/100"
