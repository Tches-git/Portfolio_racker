"""DCF估值与可比公司估值模块"""
from __future__ import annotations

import numpy as np

from app.config import (
    DCF_DEFAULT_TERMINAL_GROWTH,
    DCF_DEFAULT_WACC,
    MC_MAX_GROWTH,
    MC_MAX_WACC,
    MC_MIN_GROWTH,
    MC_MIN_WACC,
)
from app.models import DCFResult, FinancialMetrics, PeerCompany, StockProfile


def dcf_valuation(
    metrics: list[FinancialMetrics],
    profile: StockProfile,
    wacc: float = DCF_DEFAULT_WACC,
    terminal_growth: float = DCF_DEFAULT_TERMINAL_GROWTH,
    growth_rate: float | None = None,
    projection_years: int = 5,
) -> DCFResult | None:
    """DCF现金流折现估值"""
    if not metrics or not profile:
        return None

    latest = metrics[0]
    base_fcf = latest.cash_flow if latest.cash_flow > 0 else latest.net_profit * 0.7
    if base_fcf <= 0:
        return None

    if growth_rate is None:
        yoy_vals = [m.revenue_yoy for m in metrics if m.revenue_yoy != 0]
        growth_rate = sum(yoy_vals) / len(yoy_vals) if yoy_vals else 5.0
        growth_rate = max(3.0, min(growth_rate, 30.0))

    wacc_dec = wacc / 100
    tg_dec = terminal_growth / 100

    fcf_projections: list[dict] = []
    pv_sum = 0.0
    prev_fcf = base_fcf

    for yr in range(1, projection_years + 1):
        if projection_years > 1:
            yr_growth = growth_rate - (growth_rate - terminal_growth) * (yr - 1) / (projection_years - 1)
        else:
            yr_growth = growth_rate
        fcf = prev_fcf * (1 + yr_growth / 100)
        pv = fcf / (1 + wacc_dec) ** yr
        fcf_projections.append({
            "year": yr,
            "fcf": round(fcf, 2),
            "pv": round(pv, 2),
        })
        pv_sum += pv
        prev_fcf = fcf

    last_fcf = prev_fcf
    terminal_value = last_fcf * (1 + tg_dec) / (wacc_dec - tg_dec)
    pv_terminal = terminal_value / (1 + wacc_dec) ** projection_years
    enterprise_value = pv_sum + pv_terminal

    net_debt = 0.0
    if latest.total_liability > 0:
        cash = latest.cash_and_equivalents if latest.cash_and_equivalents > 0 else max(latest.cash_flow, 0)
        net_debt = max(latest.total_liability - cash, 0)
    equity_value = enterprise_value - net_debt

    if profile.total_shares > 0 and equity_value > 0:
        per_share_value = equity_value / profile.total_shares
    else:
        per_share_value = 0.0

    current_price = 0.0
    if profile.total_shares > 0 and profile.market_cap > 0:
        current_price = profile.market_cap / profile.total_shares

    upside = 0.0
    if current_price > 0:
        upside = (per_share_value / current_price - 1) * 100

    return DCFResult(
        wacc=wacc,
        terminal_growth=terminal_growth,
        fcf_projections=fcf_projections,
        terminal_value=round(terminal_value, 2),
        enterprise_value=round(enterprise_value, 2),
        equity_value=round(equity_value, 2),
        per_share_value=round(per_share_value, 2),
        current_price=round(current_price, 2),
        upside=round(upside, 1),
    )


def comparable_valuation(
    profile: StockProfile,
    peers: list[PeerCompany],
) -> dict:
    """可比公司估值"""
    pe_vals = [p.pe_ratio for p in peers if 0 < p.pe_ratio <= 200]
    pb_vals = [p.pb_ratio for p in peers if p.pb_ratio > 0]

    peer_avg_pe = float(np.median(pe_vals)) if pe_vals else 0.0
    peer_avg_pb = float(np.median(pb_vals)) if pb_vals else 0.0

    current_mc = profile.market_cap
    pe = profile.pe_ratio
    pb = profile.pb_ratio

    if pe > 0 and current_mc > 0:
        earnings = current_mc / pe
        implied_value_pe = earnings * peer_avg_pe
    else:
        implied_value_pe = 0.0

    if pb > 0 and current_mc > 0:
        book_value = current_mc / pb
        implied_value_pb = book_value * peer_avg_pb
    else:
        implied_value_pb = 0.0

    pe_upside = (implied_value_pe / current_mc - 1) * 100 if current_mc > 0 and implied_value_pe > 0 else 0.0
    pb_upside = (implied_value_pb / current_mc - 1) * 100 if current_mc > 0 and implied_value_pb > 0 else 0.0

    lines = [f"可比公司平均PE: {peer_avg_pe:.1f}，平均PB: {peer_avg_pb:.1f}"]
    if implied_value_pe > 0:
        lines.append(f"PE估值隐含市值 {implied_value_pe:.1f}亿，相对当前{'溢价' if pe_upside > 0 else '折价'} {abs(pe_upside):.1f}%")
    if implied_value_pb > 0:
        lines.append(f"PB估值隐含市值 {implied_value_pb:.1f}亿，相对当前{'溢价' if pb_upside > 0 else '折价'} {abs(pb_upside):.1f}%")

    return {
        "peer_avg_pe": round(peer_avg_pe, 2),
        "peer_avg_pb": round(peer_avg_pb, 2),
        "implied_value_pe": round(implied_value_pe, 2),
        "implied_value_pb": round(implied_value_pb, 2),
        "current_market_cap": current_mc,
        "pe_upside": round(pe_upside, 1),
        "pb_upside": round(pb_upside, 1),
        "summary": "\n".join(lines),
    }


def format_dcf_table(result: DCFResult) -> str:
    """将DCF结果格式化为Markdown表格"""
    lines = [
        "| 年份 | 自由现金流(亿) | 现值(亿) |",
        "|------|---------------|---------|",
    ]
    for p in result.fcf_projections:
        lines.append(f"| 第{p['year']}年 | {p['fcf']:.2f} | {p['pv']:.2f} |")

    pv_fcf_total = sum(p["pv"] for p in result.fcf_projections)
    lines.append("")
    lines.append(f"- **终值**: {result.terminal_value:.2f} 亿元")
    lines.append(f"- **预测期现值合计**: {pv_fcf_total:.2f} 亿元")
    lines.append(f"- **企业价值**: {result.enterprise_value:.2f} 亿元")
    lines.append(f"- **每股内在价值**: {result.per_share_value:.2f} 元")
    lines.append(f"- **当前股价**: {result.current_price:.2f} 元")
    lines.append(f"- **上涨空间**: {result.upside:+.1f}%")
    return "\n".join(lines)


def valuation_summary(dcf: DCFResult | None, comparable: dict | None) -> str:
    """综合估值摘要"""
    parts: list[str] = ["## 估值分析"]

    if dcf:
        parts.append("\n### DCF现金流折现")
        parts.append(f"WACC={dcf.wacc:.1f}%，永续增长率={dcf.terminal_growth:.1f}%")
        parts.append(
            f"每股内在价值 **{dcf.per_share_value:.2f}元**，当前股价 {dcf.current_price:.2f}元，"
            f"{'上涨' if dcf.upside >= 0 else '下跌'}空间 **{dcf.upside:+.1f}%**"
        )
        parts.append("")
        parts.append(format_dcf_table(dcf))
    else:
        parts.append("\nDCF估值：数据不足，无法计算。")

    if comparable:
        parts.append("\n### 可比公司估值")
        parts.append(comparable.get("summary", ""))
    else:
        parts.append("\n可比公司估值：无可用同行数据。")

    return "\n".join(parts)


def run_monte_carlo_dcf(
    metrics: list[FinancialMetrics],
    profile: StockProfile,
    simulations: int = 1000,
    wacc_mean: float = DCF_DEFAULT_WACC,
    wacc_std: float = 1.5,
    growth_mean: float | None = None,
    growth_std: float = 3.0,
    terminal_growth: float = DCF_DEFAULT_TERMINAL_GROWTH,
) -> dict:
    """蒙特卡洛 DCF 模拟 — 随机采样 WACC 和增长率，输出概率分布"""
    if not metrics or not profile:
        return {}

    latest = metrics[0]
    base_fcf = latest.cash_flow if latest.cash_flow > 0 else latest.net_profit * 0.7
    if base_fcf <= 0:
        return {}

    if growth_mean is None:
        yoy_vals = [m.revenue_yoy for m in metrics if m.revenue_yoy != 0]
        growth_mean = sum(yoy_vals) / len(yoy_vals) if yoy_vals else 8.0
        growth_mean = max(3.0, min(growth_mean, 25.0))

    current_price = 0.0
    if profile.total_shares > 0 and profile.market_cap > 0:
        current_price = profile.market_cap / profile.total_shares
    if profile.total_shares <= 0:
        return {}

    rng = np.random.default_rng()
    projection_years = 5
    wacc_samples = np.clip(rng.normal(wacc_mean, wacc_std, simulations), MC_MIN_WACC, MC_MAX_WACC)
    growth_samples = np.clip(rng.normal(growth_mean, growth_std, simulations), MC_MIN_GROWTH, MC_MAX_GROWTH)

    wacc_dec = wacc_samples / 100
    tg_dec = terminal_growth / 100
    valid_mask = wacc_dec > tg_dec
    if not np.any(valid_mask):
        return {}

    wacc_dec = wacc_dec[valid_mask]
    growth_samples = growth_samples[valid_mask]

    year_index = np.arange(projection_years)
    growth_matrix = growth_samples[:, None] - (growth_samples[:, None] - terminal_growth) * year_index / (projection_years - 1)
    fcf_matrix = base_fcf * np.cumprod(1 + growth_matrix / 100, axis=1)
    discount_factors = (1 + wacc_dec[:, None]) ** np.arange(1, projection_years + 1)
    pv_sum = np.sum(fcf_matrix / discount_factors, axis=1)

    last_fcf = fcf_matrix[:, -1]
    terminal_values = last_fcf * (1 + tg_dec) / (wacc_dec - tg_dec)
    pv_terminal = terminal_values / ((1 + wacc_dec) ** projection_years)
    equity_values = pv_sum + pv_terminal

    if latest.total_liability > 0:
        cash = latest.cash_and_equivalents if latest.cash_and_equivalents > 0 else max(latest.cash_flow, 0)
        net_debt = max(latest.total_liability - cash, 0)
        equity_values = equity_values - net_debt

    per_share_values = equity_values / profile.total_shares
    if current_price > 0:
        valid_price_mask = (per_share_values > 0.01 * current_price) & (per_share_values < 100 * current_price)
    else:
        valid_price_mask = per_share_values > 0
    values = np.round(per_share_values[valid_price_mask], 2).tolist()

    if not values:
        return {}

    arr = np.array(values)
    return {
        "simulations": len(values),
        "values": values,
        "mean": round(float(np.mean(arr)), 2),
        "median": round(float(np.median(arr)), 2),
        "std": round(float(np.std(arr)), 2),
        "p10": round(float(np.percentile(arr, 10)), 2),
        "p25": round(float(np.percentile(arr, 25)), 2),
        "p50": round(float(np.percentile(arr, 50)), 2),
        "p75": round(float(np.percentile(arr, 75)), 2),
        "p90": round(float(np.percentile(arr, 90)), 2),
        "current_price": round(current_price, 2),
        "prob_above_current": round(float(np.mean(arr > current_price) * 100), 1) if current_price > 0 else 0.0,
    }


def build_sensitivity_table(
    metrics: list[FinancialMetrics],
    profile: StockProfile,
    wacc_range: list[float] | None = None,
    growth_range: list[float] | None = None,
) -> dict:
    """敏感性分析 — WACC × 增长率 网格"""
    if wacc_range is None:
        wacc_range = [8.0, 9.0, 10.0, 11.0, 12.0]
    if growth_range is None:
        growth_range = [3.0, 5.0, 8.0, 10.0, 15.0]

    matrix: list[list[float]] = []
    for wacc in wacc_range:
        row: list[float] = []
        for growth in growth_range:
            result = dcf_valuation(metrics, profile, wacc=wacc, growth_rate=growth)
            row.append(round(result.per_share_value if result else 0.0, 2))
        matrix.append(row)

    header = "| WACC \\ 增长率 | " + " | ".join(f"{g:.0f}%" for g in growth_range) + " |"
    sep = "|" + "|".join(["---"] * (len(growth_range) + 1)) + "|"
    rows = []
    for i, wacc in enumerate(wacc_range):
        vals = " | ".join(f"{v:.2f}" for v in matrix[i])
        rows.append(f"| {wacc:.0f}% | {vals} |")

    table_md = "\n".join([header, sep, *rows])
    return {
        "waccs": wacc_range,
        "growth_rates": growth_range,
        "matrix": matrix,
        "table_md": table_md,
    }


def format_monte_carlo_summary(mc_result: dict) -> str:
    """格式化蒙特卡洛模拟结果为 Markdown"""
    if not mc_result:
        return "蒙特卡洛模拟: 数据不足"
    return (
        f"### 蒙特卡洛 DCF 模拟 ({mc_result['simulations']} 次)\n\n"
        f"| 统计量 | 每股价值(元) |\n"
        f"|--------|-------------|\n"
        f"| 均值 | {mc_result['mean']:.2f} |\n"
        f"| 中位数(P50) | {mc_result['p50']:.2f} |\n"
        f"| P10(悲观) | {mc_result['p10']:.2f} |\n"
        f"| P25 | {mc_result['p25']:.2f} |\n"
        f"| P75 | {mc_result['p75']:.2f} |\n"
        f"| P90(乐观) | {mc_result['p90']:.2f} |\n"
        f"| 标准差 | {mc_result['std']:.2f} |\n"
        f"| 当前股价 | {mc_result['current_price']:.2f} |\n"
        f"| **高于现价概率** | **{mc_result['prob_above_current']:.1f}%** |\n\n"
        f"> ⚠️ 以上为情景模拟结果，基于 WACC 和增长率的随机采样，不构成投资建议。"
    )
