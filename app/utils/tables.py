"""研报表格构建工具"""
from __future__ import annotations

from app.models import AnalysisState


def build_metrics_table(state: AnalysisState) -> str:
    """构建多期财务指标 Markdown 表格"""
    if not state.metrics:
        return "暂无数据"
    annual_metrics = [m for m in state.metrics if str(m.period).endswith("12-31")]
    display_metrics = annual_metrics[:5] if annual_metrics else state.metrics[:8]
    show_balance = any(m.total_assets > 0 or m.total_equity > 0 for m in display_metrics)
    if show_balance:
        lines = [
            "| 期间 | 营收(亿) | 净利润(亿) | 营收增速 | 利润增速 | ROE | 毛利率 | 负债率 | 总资产(亿) | 净资产(亿) |",
            "|------|---------|-----------|---------|---------|-----|-------|-------|----------|----------|",
        ]
        for m in display_metrics:
            lines.append(
                f"| {m.period} | {m.revenue:.1f} | {m.net_profit:.1f} | "
                f"{m.revenue_yoy:+.1f}% | {m.profit_yoy:+.1f}% | "
                f"{m.roe:.1f}% | {m.gross_margin:.1f}% | {m.debt_ratio:.1f}% | "
                f"{m.total_assets:.1f} | {m.total_equity:.1f} |"
            )
        return "\n".join(lines)

    lines = [
        "| 期间 | 营收(亿) | 净利润(亿) | 营收增速 | 利润增速 | ROE | 毛利率 | 负债率 |",
        "|------|---------|-----------|---------|---------|-----|-------|-------|",
    ]
    for m in display_metrics:
        lines.append(
            f"| {m.period} | {m.revenue:.1f} | {m.net_profit:.1f} | "
            f"{m.revenue_yoy:+.1f}% | {m.profit_yoy:+.1f}% | "
            f"{m.roe:.1f}% | {m.gross_margin:.1f}% | {m.debt_ratio:.1f}% |"
        )
    return "\n".join(lines)


def build_peers_table(state: AnalysisState) -> str:
    """构建同行业对比 Markdown 表格"""
    if not state.peers:
        return "暂无数据"
    lines = ["| 公司 | 市值(亿) | PE | PB | ROE(%) | 毛利率(%) | 净利率(%) | 营收(亿) |",
             "|------|---------|-----|-----|--------|----------|----------|---------|"]
    for p in state.peers[:5]:
        lines.append(
            f"| {p.name} | {p.market_cap:.0f} | {p.pe_ratio:.1f} | {p.pb_ratio:.1f} | "
            f"{p.roe:.1f} | {p.gross_margin:.1f} | {p.net_margin:.1f} | {p.revenue:.1f} |"
        )
    if state.profile and state.metrics:
        m = state.metrics[0]
        net_margin = round(m.net_profit / m.revenue * 100, 1) if m.revenue > 0 else 0
        lines.append(
            f"| **{state.stock_name}** | **{state.profile.market_cap:.0f}** | **{state.profile.pe_ratio:.1f}** | **{state.profile.pb_ratio:.1f}** | "
            f"**{m.roe:.1f}** | **{m.gross_margin:.1f}** | **{net_margin}** | **{m.revenue:.1f}** |"
        )
    return "\n".join(lines)
