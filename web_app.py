"""金融研报智能分析系统 — Agent + RAG 架构"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.engine import ReportEngine
from app.evals.report_eval import evaluate_report, format_eval_report
from app.finance.trend import get_chart_data
from app.memory.comparator import format_history_brief
from app.memory.store import get_memory_store
from app.ui.alerts import render_recent_history_entry, render_top_alerts
from app.ui.history_panel import render_recent_history_panel
from app.ui.stock_insights import render_stock_insight_panel
from app.ui.callbacks import build_stage_overview, make_callback
from app.ui.renderers import (
    render_agent_trace as _render_agent_trace,
    render_data as _render_data,
    render_dupont as _render_dupont,
    render_history as _render_history,
    render_rag_trace as _render_rag_trace,
    render_run_metrics as _render_run_metrics,
    render_trends as _render_trends,
    render_valuation as _render_valuation,
)
from app.ui.landing import render_empty_state, render_failure_state, render_loading_placeholders, render_quick_start, render_sidebar_controls
from app.ui.session_state import clear_result_state, consume_queued_run, make_retry_callback, set_workspace_view
from app.ui.page import inject_page_style, render_hero, render_overview_cards, render_result_summary, render_section_intro, render_workspace_nav
from app.ui.result_cards import render_core_summary, render_download_actions, render_quality_highlights, render_report_brief, render_result_overview
from app.ui.tabs import get_result_groups
from app.ui.storage import save_output_files

ROOT = Path(__file__).parent

POPULAR_STOCKS = {
    "贵州茅台": "600519",
    "宁德时代": "300750",
    "招商银行": "600036",
    "比亚迪": "002594",
    "恒瑞医药": "600276",
    "中芯国际": "688981",
    "美的集团": "000333",
    "中国平安": "601318",
    "万科A": "000002",
    "隆基绿能": "601012",
}


def render_data(state):
    return _render_data(state, st_module=st)


def render_dupont(state):
    return _render_dupont(state, st_module=st)


def render_valuation(state):
    return _render_valuation(state, st_module=st)


def render_trends(state):
    return _render_trends(state, st_module=st, get_chart_data_fn=get_chart_data)


def render_agent_trace(state, engine=None):
    return _render_agent_trace(state, engine, st_module=st)


def render_rag_trace(state, engine=None):
    return _render_rag_trace(state, engine, st_module=st)


def render_history(state):
    return _render_history(state, st_module=st, get_memory_store_fn=get_memory_store, format_history_brief_fn=format_history_brief)


def render_run_metrics(state, engine=None):
    return _render_run_metrics(state, engine, st_module=st, evaluate_report_fn=evaluate_report)


def main():
    st.set_page_config(page_title="金融研报智能分析系统", layout="wide")
    inject_page_style(st)
    render_hero(st)

    running = bool(st.session_state.get("running", False))
    has_result = bool(getattr(st.session_state.get("state"), "final_report", ""))
    workspace_view = render_workspace_nav(st, has_result=has_result, running=running, session_state=st.session_state)
    queued_stock_code = consume_queued_run(st.session_state)
    default_input = st.session_state.get("stock_code_input", "")
    if queued_stock_code:
        default_input = queued_stock_code
    stock_code, run_clicked = render_sidebar_controls(
        st,
        POPULAR_STOCKS,
        disabled=running,
        initial_stock_code=default_input,
        workspace_view=workspace_view,
    )
    if queued_stock_code and not run_clicked:
        stock_code = queued_stock_code
        run_clicked = True
    if stock_code:
        st.session_state["stock_code_input"] = stock_code

    memory_store = get_memory_store()
    history_records = memory_store.get_history(limit=5)
    stock_overview = memory_store.get_all_stocks()

    if workspace_view == "home":
        render_overview_cards(st)
        render_quick_start(st, session_state=st.session_state, rerun_fn=st.rerun, disabled=running)
        render_recent_history_entry(history_records[:1], st_module=st)
        if history_records:
            continue_cols = st.columns([3, 1])
            with continue_cols[0]:
                st.info(f"可继续查看最近一次分析：{history_records[0].stock_name} ({history_records[0].stock_code})")
            with continue_cols[1]:
                if st.button("继续查看最近结果", use_container_width=True):
                    st.session_state["stock_code_input"] = history_records[0].stock_code
                    set_workspace_view(st.session_state, "result")
                    st.rerun()
        left_panel, right_panel = st.columns([3, 2])
        with left_panel:
            render_recent_history_panel(history_records, st_module=st)
        with right_panel:
            render_stock_insight_panel(stock_overview, st_module=st)
    elif workspace_view == "run":
        render_section_intro(st, "Run", "进入分析工作台", "这里仅保留输入、进度、日志和失败恢复，减少视觉噪音。")
        render_loading_placeholders(st)

    progress_section = st.container() if workspace_view == "run" or running or run_clicked else None
    if progress_section is not None:
        with progress_section:
            st.subheader("🚦 运行进度")
            progress_bar = st.progress(0.0)
            status_placeholder = st.empty()
            metrics_placeholder = st.empty()
            stage_placeholder = st.empty()
            log_placeholder = st.empty()
            status_placeholder.info("等待开始分析")
            stage_placeholder.markdown(build_stage_overview({
                "knowledge": "pending",
                "data": "pending",
                "research": "pending",
                "write": "pending",
            }))
            log_placeholder.markdown("### 实时进展\n- 暂无任务")
    else:
        progress_bar = None
        status_placeholder = None
        metrics_placeholder = None
        stage_placeholder = None
        log_placeholder = None

    if run_clicked and stock_code:
        clear_result_state(st.session_state)
        st.session_state["running"] = True
        st.session_state["last_stock_code"] = stock_code.strip()
        if workspace_view != "run":
            set_workspace_view(st.session_state, "run")
        engine = ReportEngine(on_step=make_callback(
            progress_bar=progress_bar,
            status_placeholder=status_placeholder,
            log_placeholder=log_placeholder,
            metrics_placeholder=metrics_placeholder,
            stage_placeholder=stage_placeholder,
        ))
        try:
            state = engine.run(stock_code.strip())
        except Exception as exc:
            st.session_state["running"] = False
            st.session_state["run_error"] = str(exc)
            state = None
            engine = None
        else:
            st.session_state["state"] = state
            st.session_state["engine"] = engine
            st.session_state["running"] = False

        if state and state.final_report:
            set_workspace_view(st.session_state, "result")
            progress_bar.progress(1.0)
            stage_placeholder.markdown(build_stage_overview({
                "knowledge": "done",
                "data": "done",
                "research": "done",
                "write": "done",
            }))
            status_placeholder.success("✅ 研报已生成，可在下方标签页查看全文、数据与诊断结果")
            report_path, trace_path = save_output_files(state, root=ROOT)
            run_metrics = state.run_metrics or engine.last_run_metrics
            eval_result = evaluate_report(state.final_report, state=state, use_llm_judge=False)
            if workspace_view == "run":
                render_result_summary(state, run_metrics, st_module=st)
                render_report_brief(state, st_module=st)
                render_quality_highlights(eval_result, st_module=st)
                render_download_actions(state, report_path, trace_path, st_module=st)
                st.success(
                    f"✅ 深度研报生成完成！{state.stock_name} ({state.stock_code}) | "
                    f"Tokens {run_metrics.get('total_tokens', 0)}"
                )
                st.caption(f"已保存报告: {report_path.name} | 追踪日志: {trace_path.name}")
        else:
            st.session_state["running"] = False
            if status_placeholder is not None:
                status_placeholder.error("❌ 生成失败，请检查股票代码或配置")
            st.error("生成失败，请检查股票代码是否正确")

    state = st.session_state.get("state")
    engine = st.session_state.get("engine")
    run_error = st.session_state.get("run_error", "")
    has_result = bool(state and state.final_report)
    if workspace_view == "run" and not has_result:
        if run_error:
            render_failure_state(
                st,
                st.session_state.get("last_stock_code", ""),
                retry_fn=lambda: (make_retry_callback(st.session_state, st.session_state.get("last_stock_code", ""))(), st.rerun()),
                error_message=run_error,
            )
            st.caption(run_error)
        else:
            render_empty_state(st)
    if workspace_view == "result" and has_result:
        st.markdown("---")
        render_section_intro(st, "Result", "先总览，再下钻", "先确认结论、估值、风险与质量，再进入分组标签查看细节。")
        eval_result = evaluate_report(state.final_report, state=state)
        run_metrics = state.run_metrics or getattr(engine, "last_run_metrics", {})
        render_top_alerts(eval_result, st_module=st)
        render_result_summary(state, run_metrics, st_module=st)
        render_result_overview(state, eval_result, st_module=st)
        render_download_actions(state, *save_output_files(state, root=ROOT), st_module=st)
        group_specs = get_result_groups()
        group_labels = [label for label, _ in group_specs]
        active_group = st.radio("结果分区", group_labels, horizontal=True, label_visibility="collapsed")
        group_map = {label: items for label, items in group_specs}
        tabs = st.tabs([label for label, _ in group_map[active_group]])
        for tab, (label, key) in zip(tabs, group_map[active_group]):
            with tab:
                if key == "summary":
                    render_core_summary(state, eval_result, st_module=st)
                elif key == "report":
                    st.markdown(state.final_report)
                elif key == "data":
                    render_data(state)
                    render_dupont(state)
                elif key == "valuation":
                    render_valuation(state)
                elif key == "trends":
                    render_trends(state)
                elif key == "metrics":
                    render_run_metrics(state, engine)
                elif key == "agent":
                    render_agent_trace(state, engine)
                elif key == "rag":
                    render_rag_trace(state, engine)
                elif key == "history":
                    render_history(state)
        st.caption("如需进一步核对质量，可展开下方自动评测报告查看完整规则与诊断明细。")
        with st.expander("自动评测", expanded=False):
            st.code(format_eval_report(eval_result))


if __name__ == "__main__":
    main()
