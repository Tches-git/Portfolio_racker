"""首页历史结果面板。"""
from __future__ import annotations


def filter_history_records(records, keyword: str) -> list:
    query = keyword.strip().lower()
    if not query:
        return list(records[:5])
    matched = []
    for record in records:
        haystack = f"{record.stock_name} {record.stock_code} {record.rating or ''} {record.conclusion or ''}".lower()
        if query in haystack:
            matched.append(record)
    return matched[:5]


def build_recent_history_rows(records) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in records[:5]:
        rows.append({
            "股票": f"{record.stock_name} ({record.stock_code})",
            "时间": record.timestamp[:19].replace("T", " "),
            "评级": record.rating or "未知",
            "风险数": str(record.risk_count),
            "结论摘要": (record.conclusion or "暂无摘要")[:60],
        })
    return rows


def build_history_detail(record) -> dict[str, str]:
    return {
        "title": f"{record.stock_name} ({record.stock_code})",
        "meta": f"{record.timestamp[:19].replace('T', ' ')} | 评级 {record.rating or '未知'} | 风险 {record.risk_count}",
        "conclusion": record.conclusion or "暂无摘要",
        "risk_summary": record.risk_summary or "暂无风险摘要",
    }


def build_history_focus_options(records) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []
    seen_codes: set[str] = set()
    for record in records:
        if record.stock_code in seen_codes:
            continue
        seen_codes.add(record.stock_code)
        options.append({
            "label": f"{record.stock_name} ({record.stock_code}) · {record.timestamp[:10]}",
            "code": record.stock_code,
        })
    return options[:5]


def render_recent_history_panel(records, *, st_module) -> None:
    keyword = st_module.text_input("筛选历史", value="", placeholder="按股票、代码、评级或结论关键词筛选")
    filtered_records = filter_history_records(records, keyword)
    rows = build_recent_history_rows(filtered_records)
    if not rows:
        st_module.info("当前筛选条件下暂无历史记录。")
        return
    st_module.markdown("### 最近分析历史")
    selected_index = st_module.radio(
        "历史记录",
        options=list(range(len(filtered_records[:5]))),
        format_func=lambda idx: f"{filtered_records[idx].stock_name} ({filtered_records[idx].stock_code}) · {filtered_records[idx].timestamp[:10]}",
        horizontal=True,
        label_visibility="collapsed",
    )
    left, right = st_module.columns([3, 2])
    with left:
        st_module.dataframe(rows, width="stretch", hide_index=True)
    with right:
        detail = build_history_detail(filtered_records[selected_index])
        st_module.markdown(
            f'<div class="panel-card"><strong>{detail["title"]}</strong><div class="small-muted" style="margin-top:0.35rem;">{detail["meta"]}</div><div style="margin-top:0.65rem;">{detail["conclusion"]}</div><div class="small-muted" style="margin-top:0.65rem;">主要风险：{detail["risk_summary"]}</div></div>',
            unsafe_allow_html=True,
        )
    focus_options = build_history_focus_options(filtered_records)
    if focus_options:
        st_module.caption("可直接选择一只最近分析过的股票重新载入到输入框，便于继续回看或重跑。")
        labels = [item["label"] for item in focus_options]
        selected_label = st_module.selectbox("基于历史继续查看", labels, index=None, placeholder="选择最近分析过的股票")
        if selected_label:
            selected = next(item for item in focus_options if item["label"] == selected_label)
            st_module.session_state["stock_code_input"] = selected["code"]
    st_module.caption("展示最近 5 次已落库的分析记录，便于快速回看项目产出。")
