"""历史对比分析逻辑"""
from __future__ import annotations

from datetime import datetime

from app.memory.store import AnalysisRecord


# ---------------------------------------------------------------------------
# 内部工具函数
# ---------------------------------------------------------------------------

def _pct_change(old: float, new: float) -> float | None:
    """计算百分比变化，处理除零"""
    if old == 0:
        return None
    return (new - old) / abs(old) * 100


def _direction_emoji(pct: float | None) -> str:
    """根据变化幅度返回方向 emoji"""
    if pct is None:
        return "➡️"
    if pct > 2:
        return "📈"
    if pct < -2:
        return "📉"
    return "➡️"


def _fmt_value(value: float, fmt: str) -> str:
    """按照格式化规则输出数值字符串"""
    if fmt == "int":
        return f"{value:.0f}"
    if fmt == "pct":
        return f"{value:.1f}%"
    if fmt == "f1":
        return f"{value:.1f}"
    if fmt == "f2":
        return f"{value:.2f}"
    return f"{value}"


def _change_str(pct: float | None) -> str:
    """格式化变化幅度"""
    if pct is None:
        return "N/A"
    return f"{pct:+.1f}%"


# ---------------------------------------------------------------------------
# 核心指标定义：(显示名, 字段名, 格式)
# ---------------------------------------------------------------------------

_CORE_METRICS: list[tuple[str, str, str]] = [
    ("市值(亿)", "market_cap", "int"),
    ("PE", "pe_ratio", "f1"),
    ("PB", "pb_ratio", "f1"),
    ("营收(亿)", "revenue", "f1"),
    ("净利润(亿)", "net_profit", "f1"),
    ("ROE", "roe", "pct"),
    ("毛利率", "gross_margin", "pct"),
    ("负债率", "debt_ratio", "pct"),
    ("现金流(亿)", "cash_flow", "f1"),
]

_VALUATION_METRICS: list[tuple[str, str, str]] = [
    ("DCF每股价值", "dcf_per_share", "f2"),
    ("上涨空间", "dcf_upside", "pct"),
    ("当前价格", "current_price", "f2"),
]

# 评级等级序（用于判断上调 / 下调）
_RATING_ORDER = ["卖出", "减持", "中性", "推荐", "强烈推荐"]


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def compare_with_history(current: AnalysisRecord, previous: AnalysisRecord) -> str:
    """对比当前和历史分析结果，生成 Markdown 格式的对比摘要"""

    parts: list[str] = []

    # ---- 1. 时间跨度 ----
    ts_cur = datetime.fromisoformat(current.timestamp)
    ts_prev = datetime.fromisoformat(previous.timestamp)
    delta_days = abs((ts_cur - ts_prev).days)
    parts.append(
        f"### 🔄 历史对比分析：{current.stock_name}（{current.stock_code}）\n"
        f"> 上次分析：{ts_prev.strftime('%Y-%m-%d')}　｜　"
        f"本次分析：{ts_cur.strftime('%Y-%m-%d')}　｜　"
        f"间隔 **{delta_days}** 天\n"
    )

    # ---- 2. 核心指标变化表格 ----
    parts.append("#### 📊 核心指标变化\n")
    parts.append("| 指标 | 上次值 | 本次值 | 变化 | 方向 |")
    parts.append("|------|--------|--------|------|------|")
    for label, attr, fmt in _CORE_METRICS:
        old_val = getattr(previous, attr, 0.0)
        new_val = getattr(current, attr, 0.0)
        pct = _pct_change(old_val, new_val)
        parts.append(
            f"| {label} | {_fmt_value(old_val, fmt)} | {_fmt_value(new_val, fmt)} "
            f"| {_change_str(pct)} | {_direction_emoji(pct)} |"
        )
    parts.append("")

    # ---- 3. 估值变化 ----
    parts.append("#### 💰 估值变化\n")
    parts.append("| 指标 | 上次值 | 本次值 | 变化 | 方向 |")
    parts.append("|------|--------|--------|------|------|")
    for label, attr, fmt in _VALUATION_METRICS:
        old_val = getattr(previous, attr, 0.0)
        new_val = getattr(current, attr, 0.0)
        pct = _pct_change(old_val, new_val)
        parts.append(
            f"| {label} | {_fmt_value(old_val, fmt)} | {_fmt_value(new_val, fmt)} "
            f"| {_change_str(pct)} | {_direction_emoji(pct)} |"
        )
    parts.append("")

    # ---- 4. 评级变化 ----
    if current.rating != previous.rating:
        old_idx = _RATING_ORDER.index(previous.rating) if previous.rating in _RATING_ORDER else -1
        new_idx = _RATING_ORDER.index(current.rating) if current.rating in _RATING_ORDER else -1
        if old_idx >= 0 and new_idx >= 0:
            direction = "上调" if new_idx > old_idx else "下调"
        else:
            direction = "变更"
        parts.append(
            f"#### ⭐ 评级变化\n"
            f"> 评级从【{previous.rating}】**{direction}**至【{current.rating}】"
            f"（评分 {previous.rating_score:.1f} → {current.rating_score:.1f}）\n"
        )
    else:
        parts.append(
            f"#### ⭐ 评级变化\n"
            f"> 评级维持【{current.rating}】不变"
            f"（评分 {previous.rating_score:.1f} → {current.rating_score:.1f}）\n"
        )

    # ---- 5. 定性解读 ----
    insights: list[str] = []

    rev_chg = _pct_change(previous.revenue, current.revenue)
    profit_chg = _pct_change(previous.net_profit, current.net_profit)
    roe_chg = _pct_change(previous.roe, current.roe)
    debt_chg = _pct_change(previous.debt_ratio, current.debt_ratio)
    margin_chg = _pct_change(previous.gross_margin, current.gross_margin)
    upside_chg = _pct_change(previous.dcf_upside, current.dcf_upside)
    cf_chg = _pct_change(previous.cash_flow, current.cash_flow)

    # 营收 + 利润双增
    if rev_chg is not None and profit_chg is not None and rev_chg > 2 and profit_chg > 2:
        insights.append("公司经营状况持续向好，营收与净利润实现双增长。")
    elif rev_chg is not None and rev_chg > 2 and (profit_chg is None or profit_chg <= 2):
        insights.append("营收保持增长，但利润增速放缓，需关注成本控制情况。")
    elif rev_chg is not None and profit_chg is not None and rev_chg < -2 and profit_chg < -2:
        insights.append("营收与利润双双下滑，公司经营面临压力。")

    # ROE
    if roe_chg is not None and roe_chg > 2:
        insights.append("资本回报效率改善，ROE 呈上升趋势。")
    elif roe_chg is not None and roe_chg < -2:
        insights.append("资本回报效率下降，ROE 出现回落，需关注盈利质量。")

    # 负债率
    if debt_chg is not None and debt_chg < -2:
        insights.append("财务结构更加稳健，资产负债率有所下降。")
    elif debt_chg is not None and debt_chg > 5:
        insights.append("负债率上升明显，需关注偿债风险。")

    # 毛利率
    if margin_chg is not None and margin_chg > 2:
        insights.append("毛利率提升，产品盈利能力增强。")
    elif margin_chg is not None and margin_chg < -2:
        insights.append("毛利率下滑，可能面临成本上升或竞争加剧压力。")

    # 估值空间
    if upside_chg is not None and upside_chg < -10:
        insights.append("当前估值已部分反映基本面改善，上涨空间有所收窄。")
    elif upside_chg is not None and upside_chg > 10:
        insights.append("估值上涨空间扩大，当前价格可能被低估。")

    # 现金流
    if cf_chg is not None and cf_chg > 5:
        insights.append("经营现金流改善，企业造血能力增强。")
    elif cf_chg is not None and cf_chg < -5:
        insights.append("经营现金流恶化，需警惕资金链风险。")

    # 保证至少 2 条，最多 4 条
    if not insights:
        insights.append("整体指标变化不大，公司基本面保持平稳。")
    insights = insights[:4]

    parts.append("#### 📝 定性解读\n")
    for item in insights:
        parts.append(f"- {item}")
    parts.append("")

    return "\n".join(parts)


def format_history_brief(records: list[AnalysisRecord]) -> str:
    """格式化历史记录列表为简洁的 Markdown 摘要"""

    if not records:
        return "### 📚 历史分析记录\n\n暂无历史记录。\n"

    lines: list[str] = [
        "### 📚 历史分析记录\n",
        "| 日期 | 股票 | 评级 | ROE | PE | 市值(亿) |",
        "|------|------|------|-----|----|---------| ",
    ]

    for r in records:
        ts = datetime.fromisoformat(r.timestamp)
        date_str = ts.strftime("%Y-%m-%d")
        lines.append(
            f"| {date_str} | {r.stock_name} | {r.rating} "
            f"| {r.roe:.1f}% | {r.pe_ratio:.1f} | {r.market_cap:.0f} |"
        )

    lines.append("")
    return "\n".join(lines)


def find_peer_from_history(
    records: list[AnalysisRecord],
    industry: str,
    exclude_code: str = "",
) -> list[AnalysisRecord]:
    """从历史记录中找到同行业的其他股票最新分析结果

    对同一 stock_code 仅保留最新（timestamp 最大）的记录。
    """
    # 按 stock_code 分组，取最新
    latest: dict[str, AnalysisRecord] = {}
    for r in records:
        if r.industry != industry:
            continue
        if r.stock_code == exclude_code:
            continue
        existing = latest.get(r.stock_code)
        if existing is None or r.timestamp > existing.timestamp:
            latest[r.stock_code] = r

    # 按市值降序排列
    return sorted(latest.values(), key=lambda r: r.market_cap, reverse=True)
