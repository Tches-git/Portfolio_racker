"""首页股票历史洞察。"""
from __future__ import annotations


def build_stock_insight_rows(stocks: list[dict]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in stocks[:5]:
        rows.append({
            "股票": f"{item['name']} ({item['code']})",
            "分析次数": str(item["count"]),
            "最近分析": str(item["latest"])[:19].replace("T", " "),
        })
    return rows


def render_stock_insight_panel(stocks: list[dict], *, st_module) -> None:
    rows = build_stock_insight_rows(stocks)
    if not rows:
        return
    st_module.markdown("### 已分析股票概览")
    st_module.dataframe(rows, width="stretch", hide_index=True)
