"""Streamlit 回调函数。"""
from __future__ import annotations

from app.models import AnalysisState

_STAGE_CONFIG = {
    "rag_init": {"icon": "🧠", "label": "知识库初始化", "progress": 0.10, "status": "running", "stage": "knowledge"},
    "rag_ready": {"icon": "🧠", "label": "知识库就绪", "progress": 0.22, "status": "done", "stage": "knowledge"},
    "prefetch_done": {"icon": "📦", "label": "数据预取完成", "progress": 0.35, "status": "done", "stage": "data"},
    "research_start": {"icon": "🤖", "label": "Research Agent 自主研究", "progress": 0.42, "status": "running", "stage": "research"},
    "research_done": {"icon": "🤖", "label": "Research Agent 完成", "progress": 0.70, "status": "done", "stage": "research"},
    "writer_start": {"icon": "✍️", "label": "Report Agent RAG增强写作", "progress": 0.82, "status": "running", "stage": "write"},
    "writer_done": {"icon": "✍️", "label": "研报撰写完成", "progress": 1.00, "status": "done", "stage": "write"},
}

_STAGE_LABELS = {
    "knowledge": "知识准备",
    "data": "数据就绪",
    "research": "Agent研究",
    "write": "报告写作",
}

_STATUS_LABELS = {
    "pending": "⏳ 待开始",
    "running": "🔄 进行中",
    "done": "✅ 已完成",
}


def get_progress_state(event: str) -> dict | None:
    cfg = _STAGE_CONFIG.get(event)
    if not cfg:
        return None
    return dict(cfg)


def build_stage_overview(stage_statuses: dict[str, str]) -> str:
    lines = [
        "### 阶段状态",
        "| 阶段 | 状态 |",
        "|---|---|",
    ]
    for key, label in _STAGE_LABELS.items():
        lines.append(f"| {label} | {_STATUS_LABELS.get(stage_statuses.get(key, 'pending'), '⏳ 待开始')} |")
    return "\n".join(lines)


def make_callback(*, progress_bar, status_placeholder, log_placeholder, metrics_placeholder, stage_placeholder):
    """创建步骤回调，实时渲染到 Streamlit。"""
    logs: list[str] = []
    stage_statuses = {key: "pending" for key in _STAGE_LABELS}
    stage_placeholder.markdown(build_stage_overview(stage_statuses))

    def render_logs() -> None:
        if not logs:
            return
        rendered = "\n".join(f"- {item}" for item in logs[-10:])
        log_placeholder.markdown(f"### 实时进展\n{rendered}")

    def render_metrics(state: AnalysisState) -> None:
        metrics = getattr(state, "run_metrics", {}) or {}
        metrics_placeholder.caption(
            f"阶段步数: {state.sections.get('agent_steps', '0')} | "
            f"RAG命中: {state.sections.get('rag_hits', '0')} | "
            f"LLM调用: {metrics.get('llm_calls', 0)} | "
            f"工具调用: {metrics.get('tool_calls', 0)}"
        )

    def on_step(event: str, detail: str, state: AnalysisState):
        progress_state = get_progress_state(event)
        if progress_state:
            progress_bar.progress(progress_state["progress"])
            stage_statuses[progress_state["stage"]] = progress_state["status"]
            stage_placeholder.markdown(build_stage_overview(stage_statuses))
            status_text = f"{progress_state['icon']} {progress_state['label']}"
            if progress_state["status"] == "done":
                status_placeholder.success(f"{status_text}：{detail}")
            else:
                status_placeholder.info(f"{status_text}：{detail}")
            logs.append(f"{status_text} — {detail}")
            render_logs()
            render_metrics(state)
            return
        if "thinking" in event or "action" in event or "observation" in event:
            logs.append(f"🔗 {detail[:180]}")
            render_logs()
            render_metrics(state)

    return on_step
