"""顶部告警条与历史结果入口。"""
from __future__ import annotations

from app.evals.report_eval import EvalResult


def classify_run_error(message: str) -> dict[str, str]:
    text = (message or "").lower()
    if not text:
        return {"title": "运行失败", "hint": "请检查股票代码、网络和配置后重试。"}
    if "api" in text or "key" in text or "token" in text or "auth" in text:
        return {"title": "配置或鉴权异常", "hint": "请优先检查 API Key、Provider 配置与访问权限。"}
    if "timeout" in text or "timed out" in text or "connection" in text or "network" in text:
        return {"title": "网络或超时异常", "hint": "可能是外部接口波动，可稍后重试或检查网络连通性。"}
    if "stock" in text or "code" in text or "symbol" in text or "数据" in text:
        return {"title": "股票代码或数据异常", "hint": "请确认股票代码有效，且对应数据源当前可访问。"}
    return {"title": "运行失败", "hint": "请结合错误信息继续排查，优先检查配置、网络与输入参数。"}


def build_top_alerts(result: EvalResult) -> list[tuple[str, str]]:
    alerts: list[tuple[str, str]] = []
    if result.consistency_issue_count > 0:
        alerts.append(("warning", f"报告存在 {result.consistency_issue_count} 个一致性问题，建议优先查看核心摘要。"))
    if result.section_coverage < 0.875:
        alerts.append(("info", f"章节覆盖率为 {result.section_coverage:.0%}，仍可继续补强结构完整性。"))
    if result.data_gap_disclosure_count == 0:
        alerts.append(("warning", "本次报告未显式披露数据降级说明，请关注数据充分性。"))
    if result.risk_transmission_count == 0:
        alerts.append(("info", "风险传导路径较少，建议检查风险章节是否充分展开。"))
    if result.overall_score >= 80 and result.consistency_issue_count == 0:
        alerts.append(("success", "当前报告质量较稳定，可优先查看正文与估值结论。"))
    return alerts


def build_alert_summary(result: EvalResult) -> dict[str, str]:
    if result.consistency_issue_count > 0:
        return {
            "title": "建议先处理一致性风险",
            "body": "优先进入“核心摘要”查看一致性问题明细，再决定是否直接采信正文和估值结论。",
            "level": "warning",
        }
    if result.section_coverage < 0.875 or result.data_gap_disclosure_count == 0:
        return {
            "title": "建议先核对结构完整性与数据边界",
            "body": "可先查看质量诊断与自动评测，确认章节覆盖和数据降级披露是否充分。",
            "level": "info",
        }
    return {
        "title": "报告可优先进入结果浏览",
        "body": "建议先看结论摘要、估值模型和历史记录，再按需展开完整正文。",
        "level": "success",
    }


def render_top_alerts(result: EvalResult, *, st_module) -> None:
    summary = build_alert_summary(result)
    getattr(st_module, summary["level"])(f"**{summary['title']}** — {summary['body']}")
    for level, message in build_top_alerts(result):
        getattr(st_module, level)(message)


def render_recent_history_entry(history_records, *, st_module) -> None:
    if not history_records:
        return
    latest = history_records[0]
    st_module.markdown(
        f'<div class="result-card"><strong>最近一次历史结果</strong>'
        f'<div class="small-muted">{latest.stock_name} ({latest.stock_code}) | {latest.timestamp[:19]} | 评级 {latest.rating or "未知"} | 风险 {latest.risk_count}</div>'
        f'<div style="margin-top:0.45rem;">{(latest.conclusion or "暂无摘要")[:110]}</div></div>',
        unsafe_allow_html=True,
    )
