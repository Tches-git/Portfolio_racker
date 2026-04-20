"""杜邦分析模块 — ROE = 净利率 × 资产周转率 × 权益乘数"""
from __future__ import annotations
from app.models import FinancialMetrics, DuPontResult


def analyze_dupont(metrics: list[FinancialMetrics]) -> list[DuPontResult]:
    """对每个期间进行杜邦分解，返回 DuPontResult 列表。"""
    results: list[DuPontResult] = []
    for m in metrics:
        net_margin = 0.0
        asset_turnover = 0.0
        equity_multiplier = 0.0

        # 净利率
        if m.revenue > 0:
            net_margin = m.net_profit / m.revenue * 100

        # 资产周转率 & 权益乘数（直接计算路径）
        if m.total_assets > 0 and m.total_equity > 0:
            asset_turnover = m.revenue / m.total_assets
            equity_multiplier = m.total_assets / m.total_equity
            computed_roe = net_margin / 100 * asset_turnover * equity_multiplier * 100
        else:
            # 回退：使用 metrics 自带的 roe 估算
            computed_roe = m.roe

            # 通过 debt_ratio 估算权益乘数
            if m.debt_ratio < 100:
                equity_multiplier = 1 / (1 - m.debt_ratio / 100)

            # 已知 roe 和 net_margin，推算 asset_turnover * equity_multiplier
            if net_margin != 0 and equity_multiplier > 0:
                product = m.roe / net_margin  # roe(%) / net_margin(%) = AT * EM
                asset_turnover = product / equity_multiplier

        results.append(DuPontResult(
            period=m.period,
            roe=m.roe,
            net_margin=round(net_margin, 2),
            asset_turnover=round(asset_turnover, 4),
            equity_multiplier=round(equity_multiplier, 4),
            computed_roe=round(computed_roe, 2),
        ))
    return results


def format_dupont_table(results: list[DuPontResult]) -> str:
    """将杜邦分析结果格式化为 Markdown 表格。"""
    lines = [
        "| 期间 | ROE(%) | 净利率(%) | 资产周转率 | 权益乘数 | 分解ROE(%) |",
        "|------|--------|-----------|------------|----------|------------|",
    ]
    for r in results:
        lines.append(
            f"| {r.period} | {r.roe:.2f} | {r.net_margin:.2f} | "
            f"{r.asset_turnover:.4f} | {r.equity_multiplier:.4f} | {r.computed_roe:.2f} |"
        )
    return "\n".join(lines)


def dupont_summary(results: list[DuPontResult]) -> str:
    """对比各期间杜邦因子变化，输出文字摘要（含定性解读）。"""
    if not results:
        return "暂无杜邦分析数据。"

    latest = results[0]
    summary_parts = [
        f"最新期间 **{latest.period}**：ROE {latest.roe:.2f}%，"
        f"净利率 {latest.net_margin:.2f}%，资产周转率 {latest.asset_turnover:.4f}，"
        f"权益乘数 {latest.equity_multiplier:.4f}。",
    ]

    # 定性解读净利率水平
    if latest.net_margin > 20:
        summary_parts.append(f"净利率高达{latest.net_margin:.1f}%，表明公司拥有极强的定价权和品牌溢价能力。")
    elif latest.net_margin > 10:
        summary_parts.append(f"净利率{latest.net_margin:.1f}%处于较好水平，反映出一定的竞争壁垒和成本控制能力。")
    elif latest.net_margin > 0:
        summary_parts.append(f"净利率仅{latest.net_margin:.1f}%，利润空间较薄，公司在产业链中议价能力一般。")

    # 定性解读资产周转率
    if latest.asset_turnover > 1.0:
        summary_parts.append(f"资产周转率{latest.asset_turnover:.2f}倍，属于高周转商业模式，依靠规模和效率取胜。")
    elif latest.asset_turnover > 0.5:
        summary_parts.append(f"资产周转率{latest.asset_turnover:.2f}倍，运营效率处于中等水平。")
    else:
        summary_parts.append(f"资产周转率仅{latest.asset_turnover:.2f}倍，属于重资产模式或资产利用效率偏低。")

    # 定性解读权益乘数
    if latest.equity_multiplier > 3.0:
        summary_parts.append(f"权益乘数{latest.equity_multiplier:.2f}，财务杠杆较高，属于激进型财务策略。")
    elif latest.equity_multiplier > 1.5:
        summary_parts.append(f"权益乘数{latest.equity_multiplier:.2f}，杠杆水平适中。")
    else:
        summary_parts.append(f"权益乘数仅{latest.equity_multiplier:.2f}，财务策略保守，主要依靠自有资本驱动增长。")

    if len(results) < 2:
        summary_parts.append("仅有一期数据，无法进行趋势对比。")
        return "\n".join(summary_parts)

    prev = results[1]
    delta_margin = latest.net_margin - prev.net_margin
    delta_turnover = latest.asset_turnover - prev.asset_turnover
    delta_multiplier = latest.equity_multiplier - prev.equity_multiplier
    delta_roe = latest.roe - prev.roe

    direction = "提升" if delta_roe >= 0 else "下降"
    summary_parts.append(
        f"与上期 **{prev.period}** 相比，ROE {direction}了 {abs(delta_roe):.2f}个百分点。"
    )

    # 识别主要驱动因子
    changes = {
        "净利率": delta_margin,
        "资产周转率": delta_turnover,
        "权益乘数": delta_multiplier,
    }
    rel_changes: dict[str, float] = {}
    if prev.net_margin != 0:
        rel_changes["净利率"] = abs(delta_margin / prev.net_margin)
    if prev.asset_turnover != 0:
        rel_changes["资产周转率"] = abs(delta_turnover / prev.asset_turnover)
    if prev.equity_multiplier != 0:
        rel_changes["权益乘数"] = abs(delta_multiplier / prev.equity_multiplier)

    if rel_changes:
        driver = max(rel_changes, key=rel_changes.get)  # type: ignore[arg-type]
        raw_delta = changes[driver]
        move = "上升" if raw_delta >= 0 else "下降"

        driver_labels = {
            "净利率": ("盈利能力改善，可能源于产品提价、成本优化或规模效应释放",
                       "盈利能力减弱，可能受到成本上涨、竞争加剧或产品降价影响"),
            "资产周转率": ("运营效率提升，公司资产利用效率改善",
                          "运营效率下降，可能存在产能过剩或库存积压"),
            "权益乘数": ("财务杠杆增加，公司加大了债务融资力度",
                        "财务杠杆降低，公司在主动去杠杆或偿还债务"),
        }
        label = driver_labels[driver][0 if raw_delta >= 0 else 1]

        if delta_roe >= 0:
            summary_parts.append(f"ROE 提升主要由 **{driver}{move}** 驱动（{label}）。")
        else:
            summary_parts.append(f"ROE 下降主要因 **{driver}{move}**（{label}）。")

    # 多期趋势总结
    # results[0] 为最新期，results[-1] 为最早期
    # roe_values[0] 是最新值，roe_values[-1] 是最早值
    # 逐期递增（roe_values[i] <= roe_values[i+1] 即 新 <= 旧）表示 ROE 在下降
    # 逐期递减（roe_values[i] >= roe_values[i+1] 即 新 >= 旧）表示 ROE 在改善
    if len(results) >= 3:
        roe_values = [r.roe for r in results]
        if all(roe_values[i] >= roe_values[i+1] for i in range(len(roe_values)-1)):
            summary_parts.append("从多期数据看，ROE呈持续改善趋势，盈利能力不断增强。")
        elif all(roe_values[i] <= roe_values[i+1] for i in range(len(roe_values)-1)):
            summary_parts.append("从多期数据看，ROE呈持续下滑趋势，需关注盈利能力恶化的根本原因。")
        else:
            summary_parts.append("从多期数据看，ROE呈波动态势，盈利稳定性有待提升。")

    return "\n".join(summary_parts)
