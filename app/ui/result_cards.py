"""结果摘要、下载和质量高亮卡。"""
from __future__ import annotations

from app.evals.report_eval import EvalResult
from app.models import AnalysisState


def build_result_dashboard_bars(result: EvalResult) -> list[dict[str, float | str]]:
    consistency_score = max(0.0, 1.0 - min(result.consistency_issue_count, 5) / 5)
    risk_score = min(1.0, result.risk_transmission_count / 3) if result.risk_transmission_count >= 0 else 0.0
    disclosure_score = 1.0 if result.data_gap_disclosure_count > 0 else 0.25
    return [
        {"label": "质量评分", "value": min(1.0, max(0.0, result.overall_score / 100))},
        {"label": "章节覆盖", "value": min(1.0, max(0.0, result.section_coverage))},
        {"label": "一致性稳定度", "value": consistency_score},
        {"label": "风险展开度", "value": risk_score},
        {"label": "数据边界披露", "value": disclosure_score},
    ]


def build_result_overview_cards(state: AnalysisState, result: EvalResult) -> list[dict[str, str]]:
    rating = state.sections.get("rating", "未给出")
    upside = "--"
    if state.dcf:
        upside = f"{state.dcf.upside:+.1f}%"
    return [
        {"title": "结论摘要", "value": build_report_brief(state), "caption": "先读核心结论，再决定是否展开全文。"},
        {"title": "评级与估值", "value": f"评级 {rating} | DCF空间 {upside}", "caption": "快速确认结论方向与估值口径。"},
        {"title": "风险与可信度", "value": f"风险传导 {result.risk_transmission_count} | 一致性问题 {result.consistency_issue_count}", "caption": "优先关注风险链条和一致性诊断。"},
        {"title": "质量完成度", "value": f"综合 {result.overall_score:.1f} / 覆盖 {result.section_coverage:.0%}", "caption": "用评测指标判断是否适合直接使用。"},
    ]


def build_quality_highlights(result: EvalResult) -> list[dict[str, str]]:
    items = [
        {
            "label": "综合评分",
            "value": f"{result.overall_score:.1f}",
            "tone": "good" if result.overall_score >= 75 else "warn",
        },
        {
            "label": "章节覆盖",
            "value": f"{result.section_coverage:.0%}",
            "tone": "good" if result.section_coverage >= 0.875 else "warn",
        },
        {
            "label": "一致性问题",
            "value": str(result.consistency_issue_count),
            "tone": "good" if result.consistency_issue_count == 0 else "bad",
        },
        {
            "label": "数据降级披露",
            "value": str(result.data_gap_disclosure_count),
            "tone": "good" if result.data_gap_disclosure_count > 0 else "warn",
        },
    ]
    return items


def build_quality_guidance(result: EvalResult) -> list[str]:
    guidance: list[str] = []
    if result.consistency_issue_count > 0:
        guidance.append("优先查看一致性问题明细，先确认评级、估值和正文表述是否互相吻合。")
    if result.section_coverage < 0.875:
        guidance.append("章节覆盖仍不完整，建议先补齐缺失章节，再判断结论是否可直接使用。")
    if result.data_gap_disclosure_count == 0:
        guidance.append("当前未显式披露数据降级说明，建议核对数据充分性与结论边界。")
    if result.risk_transmission_count == 0:
        guidance.append("风险传导链条较弱，可重点复核风险章节是否写清影响路径和落点。")
    if not guidance:
        guidance.append("当前诊断较稳定，可优先阅读正文、估值模型与历史对比信息。")
    return guidance[:3]


def build_report_brief(state: AnalysisState) -> str:
    report = (state.final_report or "").strip()
    if not report:
        return "暂无报告摘要。"
    lines = [line.strip() for line in report.splitlines() if line.strip()]
    body_lines = [line for line in lines if not line.startswith("#")][:3]
    if not body_lines:
        return "暂无报告摘要。"
    return " ".join(body_lines)[:220]


def render_download_actions(state: AnalysisState, report_path, trace_path, *, st_module) -> None:
    left, right = st_module.columns(2)
    with left:
        st_module.download_button(
            label="下载研报 Markdown",
            data=(state.final_report or "").encode("utf-8"),
            file_name=report_path.name,
            mime="text/markdown",
            use_container_width=True,
        )
    with right:
        st_module.download_button(
            label="下载追踪日志",
            data="\n".join(state.trace).encode("utf-8"),
            file_name=trace_path.name,
            mime="text/plain",
            use_container_width=True,
        )


def render_result_overview(state: AnalysisState, result: EvalResult, *, st_module) -> None:
    st_module.markdown("### 结果总览")
    cards = build_result_overview_cards(state, result)
    cols = st_module.columns(2)
    for index, item in enumerate(cards):
        col = cols[index % 2]
        with col:
            st_module.markdown(
                f'<div class="panel-card"><strong>{item["title"]}</strong><div style="margin-top:0.35rem;">{item["value"]}</div><div class="small-muted" style="margin-top:0.45rem;">{item["caption"]}</div></div>',
                unsafe_allow_html=True,
            )
    st_module.markdown("### 质量与可靠性仪表板")
    for item in build_result_dashboard_bars(result):
        st_module.progress(float(item["value"]), text=f'{item["label"]} · {float(item["value"]) * 100:.0f}%')


def render_quality_highlights(result: EvalResult, *, st_module) -> None:
    st_module.markdown("### 关键质量诊断")
    cards = build_quality_highlights(result)
    cols = st_module.columns(len(cards))
    for col, item in zip(cols, cards):
        delta = None
        if item["label"] == "一致性问题" and item["value"] != "0":
            delta = "需检查"
        if item["label"] == "数据降级披露" and item["value"] == "0":
            delta = "建议补充"
        col.metric(item["label"], item["value"], delta=delta)
    if result.consistency_issues:
        st_module.warning("发现报告一致性问题，建议优先查看“核心摘要”页中的诊断提示。")


def render_report_brief(state: AnalysisState, *, st_module) -> None:
    st_module.markdown(
        f'<div class="result-card"><strong>结论摘要</strong><div class="small-muted">{build_report_brief(state)}</div></div>',
        unsafe_allow_html=True,
    )


def render_core_summary(state: AnalysisState, result: EvalResult, *, st_module) -> None:
    render_report_brief(state, st_module=st_module)
    render_quality_highlights(result, st_module=st_module)
    st_module.markdown("### 建议优先查看")
    for item in build_quality_guidance(result):
        st_module.markdown(f"- {item}")
    if result.consistency_issues:
        st_module.markdown("### 一致性问题明细")
        for issue in result.consistency_issues:
            st_module.markdown(f"- {issue}")
