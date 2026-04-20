"""Streamlit 页面级样式与摘要组件。"""
from __future__ import annotations

from app.models import AnalysisState

_WORKSPACE_CONFIG = {
    "home": {
        "label": "首页概览",
        "title": "首页概览",
        "description": "聚焦快速开始、流程说明与历史回看，不再把所有内容堆在同一屏。",
    },
    "run": {
        "label": "分析工作台",
        "title": "分析工作台",
        "description": "专注输入、运行进度、阶段指标与失败恢复。",
    },
    "result": {
        "label": "结果浏览",
        "title": "结果浏览",
        "description": "先看告警与核心摘要，再逐层展开正文、估值、Trace 与历史记录。",
    },
}


def build_workspace_options(has_result: bool) -> list[dict[str, str]]:
    options = [
        {"key": "home", **_WORKSPACE_CONFIG["home"]},
        {"key": "run", **_WORKSPACE_CONFIG["run"]},
    ]
    if has_result:
        options.append({"key": "result", **_WORKSPACE_CONFIG["result"]})
    return options


def resolve_workspace_view(requested: str, *, has_result: bool, running: bool) -> str:
    if running:
        return "run"
    allowed = {item["key"] for item in build_workspace_options(has_result)}
    if requested in allowed:
        return requested
    return "result" if has_result else "home"


def render_workspace_nav(st_module, *, has_result: bool, running: bool, session_state) -> str:
    options = build_workspace_options(has_result)
    current_view = resolve_workspace_view(
        str(session_state.get("workspace_view", "") or ""),
        has_result=has_result,
        running=running,
    )
    labels = [item["label"] for item in options]
    label_to_key = {item["label"]: item["key"] for item in options}
    current_label = next(item["label"] for item in options if item["key"] == current_view)
    selected_label = st_module.radio("工作区", labels, index=labels.index(current_label), horizontal=True, label_visibility="collapsed")
    selected_view = label_to_key[selected_label]
    session_state["workspace_view"] = selected_view
    meta = next(item for item in options if item["key"] == selected_view)
    st_module.markdown(
        f'<div class="tip-card"><strong>{meta["title"]}</strong><div class="small-muted">{meta["description"]}</div></div>',
        unsafe_allow_html=True,
    )
    return selected_view


def inject_page_style(st_module) -> None:
    st_module.markdown(
        """
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px;}
[data-testid="stAppViewContainer"] {background: linear-gradient(180deg, #f8fbff 0%, #ffffff 18%);}
[data-testid="stMetric"] {background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.75rem;}
[data-testid="stSidebar"] {border-right: 1px solid #e2e8f0;}
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {border-radius: 10px; padding: 0.5rem 0.9rem; background: #f8fafc;}
div[role="radiogroup"] {gap: 0.5rem; margin-bottom: 0.8rem;}
div[role="radiogroup"] label {background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 999px; padding: 0.2rem 0.6rem;}
.hero-card {padding: 1.35rem 1.4rem; border: 1px solid #dbeafe; border-radius: 20px; background: linear-gradient(135deg, #f8fbff 0%, #eef6ff 100%); margin-bottom: 1.2rem; box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);}
.tip-card {padding: 1rem 1.1rem; border: 1px solid #e2e8f0; border-radius: 16px; background: #ffffff; margin-bottom: 1rem; box-shadow: 0 8px 24px rgba(15, 23, 42, 0.03);}
.result-card {padding: 1rem 1.1rem; border: 1px solid #dbeafe; border-radius: 16px; background: #f8fbff; margin-bottom: 1rem; box-shadow: 0 10px 24px rgba(37, 99, 235, 0.05);}
.panel-card {padding: 1rem 1.1rem; border: 1px solid #e2e8f0; border-radius: 18px; background: #ffffff; margin-bottom: 1rem;}
.section-kicker {color: #2563eb; font-size: 0.82rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 0.25rem;}
.section-title {font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 0.2rem;}
.section-desc {color: #64748b; font-size: 0.92rem; margin-bottom: 0.9rem;}
.badge-row {display:flex; gap:0.5rem; flex-wrap:wrap; margin:0.4rem 0 0.2rem 0;}
.badge {display:inline-block; padding:0.25rem 0.55rem; border-radius:999px; font-size:0.85rem; border:1px solid #dbeafe; background:#eff6ff; color:#1d4ed8;}
.small-muted {color: #64748b; font-size: 0.92rem;}
.placeholder-card {padding: 1rem 1.1rem; border: 1px dashed #cbd5e1; border-radius: 16px; background: linear-gradient(90deg, #f8fafc 0%, #ffffff 50%, #f8fafc 100%); color: #94a3b8; margin-bottom: 0.8rem;}
</style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(st_module) -> None:
    st_module.markdown(
        """
<div class="hero-card">
  <h1 style="margin:0 0 0.4rem 0;">金融研报智能分析系统</h1>
  <div class="small-muted">输入股票代码后，系统会依次完成知识准备、Agent 研究、RAG 写作与质量诊断。</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(st_module, kicker: str, title: str, description: str) -> None:
    st_module.markdown(
        f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div><div class="section-desc">{description}</div>',
        unsafe_allow_html=True,
    )


def render_overview_cards(st_module) -> None:
    render_section_intro(st_module, "Home", "从首页开始工作", "先快速选择股票、看历史与流程，再进入分析工作台，避免所有信息同时出现。")
    left, right = st_module.columns([3, 2])
    with left:
        st_module.markdown(
            """
<div class="tip-card">
  <strong>分析流程</strong><br/>
  1. 初始化知识与数据<br/>
  2. Agent 自主研究<br/>
  3. RAG 增强写作<br/>
  4. 输出报告与质量诊断
</div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st_module.markdown(
            """
<div class="tip-card">
  <strong>使用提示</strong><br/>
  • 首次运行会更慢<br/>
  • 生成中请勿重复点击<br/>
  • 完成后可在结果浏览页分层查看明细
</div>
            """,
            unsafe_allow_html=True,
        )


def build_result_summary(state: AnalysisState, run_metrics: dict) -> dict[str, str]:
    return {
        "stock": f"{state.stock_name} ({state.stock_code})",
        "agent_steps": str(state.sections.get("agent_steps", "?")),
        "rag_hits": str(state.sections.get("rag_hits", "?")),
        "duration": f"{run_metrics.get('duration_s', 0):.2f}s",
        "tokens": str(run_metrics.get("total_tokens", 0)),
    }


def render_result_summary(state: AnalysisState, run_metrics: dict, *, st_module) -> None:
    summary = build_result_summary(state, run_metrics)
    badges = []
    if state.sections.get("rating"):
        badges.append(f"评级：{state.sections['rating']}")
    if state.sections.get("postprocess_fix_count"):
        badges.append(f"自动修补：{state.sections['postprocess_fix_count']}")
    badge_html = "".join(f'<span class="badge">{item}</span>' for item in badges)
    st_module.markdown(
        '<div class="result-card"><strong>结果摘要</strong><div class="small-muted">本次生成已完成，可直接进入下方标签页查看细节。</div>'
        + (f'<div class="badge-row">{badge_html}</div>' if badge_html else '')
        + '</div>',
        unsafe_allow_html=True,
    )
    s1, s2, s3, s4, s5 = st_module.columns(5)
    s1.metric("股票", summary["stock"])
    s2.metric("Agent步数", summary["agent_steps"])
    s3.metric("RAG命中", summary["rag_hits"])
    s4.metric("耗时", summary["duration"])
    s5.metric("Tokens", summary["tokens"])
