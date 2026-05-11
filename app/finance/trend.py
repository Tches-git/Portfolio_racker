"""多年趋势分析模块 — 营收/利润/ROE等关键指标的多期趋势与CAGR"""
from __future__ import annotations
import math
from app.models import FinancialMetrics, TrendResult

# 百分比类指标（使用算术变化而非CAGR）
_PCT_METRICS = {"ROE", "毛利率", "资产负债率"}

# 指标配置: (显示名, 取值属性)
_METRIC_DEFS: list[tuple[str, str]] = [
    ("营收", "revenue"),
    ("净利润", "net_profit"),
    ("ROE", "roe"),
    ("毛利率", "gross_margin"),
    ("资产负债率", "debt_ratio"),
]


def _calc_cagr(first: float, last: float, n_periods: int) -> float:
    """计算CAGR(%)，n_periods为间隔数（期数-1）"""
    if n_periods <= 0 or first <= 0:
        return 0.0
    return (math.pow(last / first, 1 / n_periods) - 1) * 100


def _determine_direction(values: list[float]) -> str:
    """判断趋势方向"""
    if len(values) < 2:
        return "波动"
    first, last = values[0], values[-1]
    increases = sum(1 for i in range(1, len(values)) if values[i] >= values[i - 1])
    decreases = sum(1 for i in range(1, len(values)) if values[i] <= values[i - 1])
    threshold = (len(values) - 1) / 2
    if last > first and increases > threshold:
        return "上升"
    if last < first and decreases > threshold:
        return "下降"
    return "波动"


# ── 主分析函数 ──────────────────────────────────────────────


def analyze_trends(metrics: list[FinancialMetrics]) -> list[TrendResult]:
    """对多期财务数据做趋势分析，metrics 按 period 降序排列（最新在前）"""
    if not metrics:
        return []
    # 转为时间正序
    ordered = list(reversed(metrics))
    periods = [m.period for m in ordered]
    results: list[TrendResult] = []
    for name, attr in _METRIC_DEFS:
        vals = [getattr(m, attr) for m in ordered]
        n = len(vals)
        if name in _PCT_METRICS:
            cagr = vals[-1] - vals[0] if n >= 2 else 0.0
        else:
            cagr = _calc_cagr(vals[0], vals[-1], n - 1) if n >= 2 else 0.0
        results.append(TrendResult(
            metric_name=name,
            periods=list(periods),
            values=list(vals),
            cagr=round(cagr, 2),
            trend_direction=_determine_direction(vals),
        ))
    return results


# ── Markdown 表格 ───────────────────────────────────────────


def format_trend_table(trends: list[TrendResult]) -> str:
    """生成 Markdown 趋势表格"""
    if not trends:
        return ""
    periods = trends[0].periods
    header = "| 指标 | " + " | ".join(periods) + " | CAGR/变化 | 趋势 |"
    sep = "|" + "|".join(["---"] * (len(periods) + 3)) + "|"
    rows: list[str] = []
    for t in trends:
        vals_str = " | ".join(f"{v:.2f}" for v in t.values)
        unit = "pp" if t.metric_name in _PCT_METRICS else "%"
        rows.append(f"| {t.metric_name} | {vals_str} | {t.cagr:+.2f}{unit} | {t.trend_direction} |")
    return "\n".join([header, sep, *rows])


# ── 文本摘要 ─────────────────────────────────────────────────


def trend_summary(trends: list[TrendResult]) -> str:
    """返回趋势概述文字（含定性解读）"""
    if not trends:
        return "暂无趋势数据。"
    parts: list[str] = []
    n_years = len(trends[0].periods) - 1 if trends[0].periods else 0
    for t in trends:
        if t.metric_name in _PCT_METRICS:
            first_val = t.values[0] if t.values else 0
            last_val = t.values[-1] if t.values else 0
            change_dir = '上升' if last_val >= first_val else '下降'
            parts.append(
                f"{t.metric_name}从{first_val:.1f}%{change_dir}至{last_val:.1f}%"
            )
        else:
            direction = "保持稳定增长" if t.trend_direction == "上升" else (
                "呈下降趋势" if t.trend_direction == "下降" else "有所波动"
            )
            parts.append(f"{t.metric_name}{n_years}年CAGR为{t.cagr:+.1f}%，{direction}")

    summary = "；".join(parts) + "。"

    # 综合定性判断
    rev_trend = next((t for t in trends if t.metric_name == "营收"), None)
    profit_trend = next((t for t in trends if t.metric_name == "净利润"), None)
    roe_trend = next((t for t in trends if t.metric_name == "ROE"), None)

    insights: list[str] = []
    if rev_trend and profit_trend:
        if rev_trend.cagr > 0 and profit_trend.cagr > rev_trend.cagr:
            insights.append("利润增速快于营收增速，说明公司具备经营杠杆优势或盈利能力在提升")
        elif rev_trend.cagr > 0 and profit_trend.cagr < rev_trend.cagr:
            insights.append("利润增速慢于营收增速，可能面临成本上升压力或费用率扩张")
        elif rev_trend.cagr < 0:
            insights.append("营收处于负增长通道，需关注行业需求萎缩或市场份额流失风险")

    if roe_trend and roe_trend.values:
        latest_roe = roe_trend.values[-1]
        if latest_roe > 15:
            insights.append(f"最新ROE达{latest_roe:.1f}%，资本回报率优秀")
        elif latest_roe < 5:
            insights.append(f"最新ROE仅{latest_roe:.1f}%，资本使用效率偏低")

    if insights:
        summary += "\n" + "；".join(insights) + "。"

    return summary


# ── 图表数据 ─────────────────────────────────────────────────


def get_chart_data(trends: list[TrendResult]) -> dict[str, dict]:
    """返回供前端渲染的图表数据"""
    return {
        t.metric_name: {
            "periods": list(t.periods),
            "values": list(t.values),
            "cagr": t.cagr,
        }
        for t in trends
    }
