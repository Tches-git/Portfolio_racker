"""Streamlit 渲染函数。"""
from __future__ import annotations

import json

import pandas as pd

from app.models import AnalysisState


def render_data(state: AnalysisState, *, st_module) -> None:
    if state.profile:
        p = state.profile
        c1, c2, c3, c4 = st_module.columns(4)
        c1.metric("公司", f"{p.name} ({p.code})")
        c2.metric("行业", p.industry)
        c3.metric("市值", f"{p.market_cap:.0f}亿")
        c4.metric("PE / PB", f"{p.pe_ratio:.1f} / {p.pb_ratio:.1f}")

    if state.metrics:
        st_module.subheader("📊 多年财务指标")
        rows = []
        for m in state.metrics[:8]:
            rows.append({
                "期间": m.period,
                "营收(亿)": f"{m.revenue:.1f}",
                "净利润(亿)": f"{m.net_profit:.1f}",
                "营收增速": f"{m.revenue_yoy:+.1f}%",
                "利润增速": f"{m.profit_yoy:+.1f}%",
                "ROE": f"{m.roe:.1f}%",
                "毛利率": f"{m.gross_margin:.1f}%",
                "负债率": f"{m.debt_ratio:.1f}%",
                "总资产(亿)": f"{m.total_assets:.1f}",
                "净资产(亿)": f"{m.total_equity:.1f}",
            })
        st_module.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    if state.peers:
        st_module.subheader("🏢 同行业深度对比")
        rows = []
        for peer in state.peers[:5]:
            rows.append({
                "公司": peer.name,
                "市值(亿)": f"{peer.market_cap:.0f}",
                "PE": f"{peer.pe_ratio:.1f}",
                "PB": f"{peer.pb_ratio:.1f}",
                "ROE(%)": f"{peer.roe:.1f}",
                "毛利率(%)": f"{peer.gross_margin:.1f}",
                "净利率(%)": f"{peer.net_margin:.1f}",
                "营收(亿)": f"{peer.revenue:.1f}",
            })
        if state.profile and state.metrics:
            latest = state.metrics[0]
            net_margin = round(latest.net_profit / latest.revenue * 100, 1) if latest.revenue > 0 else 0
            rows.append({
                "公司": f"⭐{state.stock_name}",
                "市值(亿)": f"{state.profile.market_cap:.0f}",
                "PE": f"{state.profile.pe_ratio:.1f}",
                "PB": f"{state.profile.pb_ratio:.1f}",
                "ROE(%)": f"{latest.roe:.1f}",
                "毛利率(%)": f"{latest.gross_margin:.1f}",
                "净利率(%)": f"{net_margin}",
                "营收(亿)": f"{latest.revenue:.1f}",
            })
        st_module.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)


def render_dupont(state: AnalysisState, *, st_module) -> None:
    if not state.dupont:
        st_module.info("暂无杜邦分析数据")
        return
    st_module.subheader("🔬 杜邦分析: ROE = 净利率 × 资产周转率 × 权益乘数")
    rows = []
    for d in state.dupont:
        rows.append({
            "期间": d.period,
            "ROE(%)": f"{d.roe:.2f}",
            "净利率(%)": f"{d.net_margin:.2f}",
            "资产周转率": f"{d.asset_turnover:.4f}",
            "权益乘数": f"{d.equity_multiplier:.4f}",
            "分解ROE(%)": f"{d.computed_roe:.2f}",
        })
    st_module.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    if len(state.dupont) >= 2:
        periods = [d.period for d in reversed(state.dupont)]
        chart_df = pd.DataFrame({
            "期间": periods,
            "净利率(%)": [d.net_margin for d in reversed(state.dupont)],
            "资产周转率(×10)": [d.asset_turnover * 10 for d in reversed(state.dupont)],
            "权益乘数": [d.equity_multiplier for d in reversed(state.dupont)],
        }).set_index("期间")
        st_module.line_chart(chart_df)
    if state.sections.get("dupont_summary"):
        st_module.markdown(state.sections["dupont_summary"])


def render_valuation(state: AnalysisState, *, st_module) -> None:
    st_module.subheader("💰 估值分析")
    if state.dcf:
        st_module.markdown("### DCF 现金流折现估值")
        c1, c2, c3, c4 = st_module.columns(4)
        c1.metric("每股内在价值", f"{state.dcf.per_share_value:.2f}元")
        c2.metric("当前股价", f"{state.dcf.current_price:.2f}元")
        c3.metric("上涨空间", f"{state.dcf.upside:+.1f}%")
        c4.metric("WACC", f"{state.dcf.wacc:.1f}%")
        rows = [{"年份": f"第{p['year']}年", "自由现金流(亿)": f"{p['fcf']:.2f}", "现值(亿)": f"{p['pv']:.2f}"} for p in state.dcf.fcf_projections]
        st_module.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st_module.caption(f"终值: {state.dcf.terminal_value:.2f}亿 | 企业价值: {state.dcf.enterprise_value:.2f}亿 | 永续增长率: {state.dcf.terminal_growth:.1f}%")

        if state.dcf.monte_carlo_summary:
            mc = state.dcf.monte_carlo_summary
            st_module.markdown("### 🎲 蒙特卡洛 DCF 模拟")
            c1, c2, c3, c4 = st_module.columns(4)
            c1.metric("P50(中位数)", f"{mc.get('p50', 0):.2f}元")
            c2.metric("P10(悲观)", f"{mc.get('p10', 0):.2f}元")
            c3.metric("P90(乐观)", f"{mc.get('p90', 0):.2f}元")
            c4.metric("高于现价概率", f"{mc.get('prob_above_current', 0):.1f}%")
            st_module.caption(f"模拟 {mc.get('simulations', 0)} 次 | 均值 {mc.get('mean', 0):.2f}元 | 标准差 {mc.get('std', 0):.2f}元")
            st_module.warning("⚠️ 以上为情景模拟结果，基于 WACC 和增长率的随机采样，不构成投资建议。")

        if state.dcf.sensitivity_matrix:
            st_module.markdown("### 📊 敏感性分析 (每股价值)")
            sens_rows = []
            for i, wacc in enumerate(state.dcf.sensitivity_waccs):
                row = {"WACC": f"{wacc:.0f}%"}
                for j, growth in enumerate(state.dcf.sensitivity_growth_rates):
                    row[f"增长率{growth:.0f}%"] = f"{state.dcf.sensitivity_matrix[i][j]:.2f}"
                sens_rows.append(row)
            st_module.dataframe(pd.DataFrame(sens_rows), width="stretch", hide_index=True)
    else:
        st_module.info("DCF估值: 数据不足")

    if state.sections.get("comparable_summary"):
        st_module.markdown("### 可比公司估值")
        st_module.markdown(state.sections["comparable_summary"])


def render_trends(state: AnalysisState, *, st_module, get_chart_data_fn) -> None:
    if not state.trends:
        st_module.info("暂无趋势数据")
        return
    st_module.subheader("📈 多年趋势分析")
    chart_data = get_chart_data_fn(state.trends)
    rev_data = chart_data.get("营收")
    profit_data = chart_data.get("净利润")
    if rev_data and profit_data:
        st_module.markdown(f"**营收与净利润趋势** | 营收CAGR: {rev_data['cagr']:+.1f}% | 净利润CAGR: {profit_data['cagr']:+.1f}%")
        df = pd.DataFrame({"期间": rev_data["periods"], "营收(亿)": rev_data["values"], "净利润(亿)": profit_data["values"]}).set_index("期间")
        st_module.bar_chart(df)
    roe_data = chart_data.get("ROE")
    margin_data = chart_data.get("毛利率")
    if roe_data and margin_data:
        st_module.markdown("**ROE与毛利率趋势**")
        df2 = pd.DataFrame({"期间": roe_data["periods"], "ROE(%)": roe_data["values"], "毛利率(%)": margin_data["values"]}).set_index("期间")
        st_module.line_chart(df2)
    debt_data = chart_data.get("资产负债率")
    if debt_data:
        st_module.markdown("**资产负债率趋势**")
        df3 = pd.DataFrame({"期间": debt_data["periods"], "资产负债率(%)": debt_data["values"]}).set_index("期间")
        st_module.line_chart(df3)
    if state.sections.get("trend_summary"):
        st_module.info(f"📊 {state.sections['trend_summary']}")


def render_agent_trace(state: AnalysisState, engine=None, *, st_module) -> None:
    st_module.subheader("🤖 Agent 推理链 (Planning → Acting → Reflection)")
    if state.sections.get("research_plan"):
        with st_module.expander("📋 研究计划 (Planning)", expanded=True):
            for line in state.sections["research_plan"].split("\n"):
                if line.strip():
                    st_module.markdown(f"  {line}")

    st_module.caption("展示 Research Agent 的 Thought → Action → Observation 推理过程")

    if engine and engine.agent_trace:
        for i, step in enumerate(engine.agent_trace, 1):
            event = step.get("event", "")
            detail = step.get("detail", "")
            tool = step.get("tool", "")

            if event == "planning":
                st_module.markdown(f"**📋 规划阶段** — {detail}")
            elif event == "plan_ready":
                st_module.markdown("**📋 计划就绪** ✅")
            elif event == "thinking":
                st_module.markdown(f"**Step {step.get('step', i)}** 🧠 思考中...")
            elif event == "action":
                st_module.markdown(f"**Step {step.get('step', i)}** 🔧 调用工具: `{tool}`")
                if step.get("input"):
                    st_module.code(json.dumps(step["input"], ensure_ascii=False), language="json")
            elif event == "observation":
                with st_module.expander(f"📋 观察结果 (Step {step.get('step', i)})", expanded=False):
                    st_module.text(detail[:500])
            elif event == "reflecting":
                st_module.markdown(f"**🔍 反思阶段** — {detail}")
            elif event == "reflection_done":
                st_module.markdown(f"**🔍 反思完成** — {detail}")
            elif event == "final":
                st_module.success(f"✅ 最终结论: {detail[:200]}")
    else:
        for i, line in enumerate(state.trace, 1):
            if "❌" in line:
                st_module.markdown(f"`{i:02d}` :red[{line}]")
            elif "✅" in line:
                st_module.markdown(f"`{i:02d}` :green[{line}]")
            elif "🤖" in line:
                st_module.markdown(f"`{i:02d}` :blue[{line}]")
            elif "⚠️" in line:
                st_module.markdown(f"`{i:02d}` :orange[{line}]")
            else:
                st_module.markdown(f"`{i:02d}` {line}")

    if state.sections.get("research_reflection"):
        with st_module.expander("🔍 Agent 反思 (Reflection)", expanded=False):
            st_module.markdown(state.sections["research_reflection"])


def render_rag_trace(state: AnalysisState, engine=None, *, st_module) -> None:
    st_module.subheader("🧠 RAG 知识检索记录")
    st_module.caption("展示系统从金融知识库中检索到的相关知识及其相关度评分")

    if engine and engine.rag_trace:
        for i, hit in enumerate(engine.rag_trace, 1):
            query = hit.get("query", "")
            content = hit.get("content", hit.get("detail", ""))[:200]
            score = hit.get("score", 0)

            col1, col2 = st_module.columns([1, 4])
            with col1:
                if isinstance(score, (int, float)) and score > 0:
                    st_module.metric(f"命中 #{i}", f"{score:.3f}")
                else:
                    st_module.metric(f"命中 #{i}", "—")
            with col2:
                if query:
                    st_module.markdown(f"**查询**: {query}")
                st_module.caption(f"{content}...")
            st_module.divider()
    else:
        st_module.info(f"知识库文档: {state.sections.get('rag_hits', '0')} 条检索命中")


def render_history(state: AnalysisState, *, st_module, get_memory_store_fn, format_history_brief_fn) -> None:
    store = get_memory_store_fn()
    history = store.get_history(stock_code=state.stock_code, limit=5)
    if not history:
        st_module.info("暂无历史分析记录")
        return
    st_module.subheader("🕘 历史分析记录")
    for rec in history:
        st_module.markdown(format_history_brief_fn(rec))


def render_run_metrics(state: AnalysisState, engine=None, *, st_module, evaluate_report_fn) -> None:
    st_module.subheader("⚙️ 运行指标")
    metrics = dict(getattr(state, "run_metrics", {}) or {})
    if engine:
        metrics.setdefault("trace_id", engine.last_run_metrics.get("trace_id", ""))
    if not metrics:
        st_module.info("暂无运行指标")
        return
    c1, c2, c3, c4 = st_module.columns(4)
    c1.metric("总耗时", f"{metrics.get('duration_s', 0):.2f}s")
    c2.metric("LLM调用", str(metrics.get("llm_calls", 0)))
    c3.metric("工具调用", str(metrics.get("tool_calls", 0)))
    c4.metric("总Tokens", str(metrics.get("total_tokens", 0)))
    c5, c6, c7, c8 = st_module.columns(4)
    c5.metric("错误数", str(metrics.get("errors", 0)))
    c6.metric("Agent步数", state.sections.get("agent_steps", "0"))
    c7.metric("RAG命中", state.sections.get("rag_hits", "0"))
    c8.metric("自动修补", state.sections.get("postprocess_fix_count", "0"))
    if metrics.get("trace_id"):
        st_module.caption(f"trace_id: {metrics['trace_id']}")

    eval_result = evaluate_report_fn(state.final_report, state=state, use_llm_judge=False) if state.final_report else None
    if eval_result:
        st_module.markdown("### 🧪 质量诊断")
        d1, d2, d3, d4 = st_module.columns(4)
        d1.metric("一致性问题", str(eval_result.consistency_issue_count))
        d2.metric("风险证据", str(eval_result.risk_evidence_count))
        d3.metric("风险传导", str(eval_result.risk_transmission_count))
        d4.metric("数据降级披露", str(eval_result.data_gap_disclosure_count))

        data_gaps = [line for line in state.sections.get("data_gaps", "").split("\n") if line.strip()]
        if data_gaps:
            with st_module.expander("⚠️ 数据缺口与降级说明", expanded=False):
                for gap in data_gaps:
                    st_module.markdown(f"- {gap}")

        if eval_result.consistency_issues:
            with st_module.expander("🔎 报告一致性诊断", expanded=False):
                for issue in eval_result.consistency_issues:
                    st_module.markdown(f"- {issue}")

    fixes = [line for line in state.sections.get("postprocess_fixes", "").split("\n") if line.strip()]
    if fixes:
        with st_module.expander("🩹 报告自动修补记录", expanded=False):
            for fix in fixes:
                st_module.markdown(f"- `{fix}`")
    st_module.code(json.dumps(metrics, ensure_ascii=False, indent=2), language="json")
