"""report_eval 的辅助逻辑。"""
from __future__ import annotations

import re


def _pick_state_value(primary, fallback, default=""):
    if primary not in (None, ""):
        return primary
    if fallback not in (None, ""):
        return fallback
    return default


REQUIRED_SECTIONS = [
    ("投资要点", ["投资要点", "核心结论", "投资亮点"]),
    ("公司概况", ["公司概况", "公司简介", "企业概况"]),
    ("杜邦分析", ["杜邦分析", "杜邦", "ROE分解"]),
    ("财务分析", ["财务分析", "财务指标", "盈利分析"]),
    ("估值分析", ["估值分析", "DCF", "现金流折现", "可比估值"]),
    ("行业分析", ["行业分析", "竞争格局", "同行对比"]),
    ("风险提示", ["风险提示", "风险分析", "风险评估"]),
    ("投资建议", ["投资建议", "评级", "目标价"]),
]

_SECTION_GRAPH_RULES = {
    "risk": {
        "heading": "## 七、核心风险与跟踪指标",
        "keywords": ("风险", "传导", "波动", "下行", "影响指标"),
        "label": "风险章节",
    },
    "industry": {
        "heading": "## 六、行业格局与可比公司对比",
        "keywords": ("行业", "同行", "可比", "竞争", "格局"),
        "label": "行业章节",
    },
    "valuation": {
        "heading": "## 五、估值分析",
        "keywords": ("估值", "指标", "利润", "收入", "催化"),
        "label": "估值章节",
    },
}


def collect_section_graph_feedback(report: str, state) -> dict[str, dict[str, str | bool]]:
    feedback: dict[str, dict[str, str | bool]] = {}
    if state is None:
        return feedback
    graph_payload = getattr(state, "graph_payload", {}) or {}
    section_graph_context_map = graph_payload.get("section_graph_context_map", {}) if isinstance(graph_payload.get("section_graph_context_map", {}), dict) else {}
    for section_id, meta in _SECTION_GRAPH_RULES.items():
        graph_context = str(_pick_state_value(section_graph_context_map.get(section_id), state.sections.get(f"section_graph_context_{section_id}", ""), "") or "")
        injected = bool(graph_context and "未命中" not in graph_context)
        section_body = _extract_section_body(report, meta["heading"])
        absorbed = bool(section_body and any(keyword in section_body for keyword in meta["keywords"]))
        feedback[section_id] = {
            "label": meta["label"],
            "injected": injected,
            "absorbed": absorbed,
            "section_body": section_body,
        }
    return feedback


def check_report_consistency(report: str, state) -> list[str]:
    issues: list[str] = []
    if state is None:
        return issues

    runtime_payload = getattr(state, "runtime_input_payload", {}) or {}
    memory_payload = getattr(state, "memory_payload", {}) or {}
    graph_payload = getattr(state, "graph_payload", {}) or {}

    rating = state.sections.get("rating", "")
    if rating and rating not in report:
        issues.append(f"报告正文未显式包含 state 中的评级：{rating}")

    if state.dcf:
        dcf = state.dcf
        if dcf.per_share_value > 0:
            per_share_rounded = f"{dcf.per_share_value:.2f}"
            if per_share_rounded not in report:
                issues.append(f"报告正文未引用 state 中的 DCF 每股价值：{per_share_rounded}元")
        if dcf.current_price > 0:
            current_price_rounded = f"{dcf.current_price:.2f}"
            if current_price_rounded not in report:
                issues.append(f"报告正文未引用 state 中的当前股价：{current_price_rounded}元")

    if state.risks:
        risk_descriptions = [risk.description for risk in state.risks if risk.description]
        if not any(desc in report for desc in risk_descriptions):
            issues.append("报告正文未覆盖 state 中已识别的核心风险描述")

    if state.news and "新闻" not in report and "舆情" not in report:
        issues.append("存在新闻数据，但报告正文未明显体现新闻/舆情信息")

    if state.peers and ("同行" not in report and "可比" not in report):
        issues.append("存在同行数据，但报告正文未明显体现同行/可比分析")

    graph_hit_count = int(float(_pick_state_value(graph_payload.get("graph_hit_count"), state.sections.get("graph_hit_count", "0"), 0) or 0))
    graph_query_focus = str(_pick_state_value(graph_payload.get("graph_query_focus"), state.sections.get("graph_query_focus", "通用关系"), "通用关系") or "通用关系")
    graph_focus_summary = str(_pick_state_value(graph_payload.get("graph_focus_summary"), state.sections.get("graph_focus_summary", ""), "") or "")
    section_graph_summary = str(_pick_state_value(graph_payload.get("section_graph_summary"), state.sections.get("section_graph_summary", ""), "") or "")
    focus_keywords = {
        "风险传导": ("风险", "传导"),
        "催化因素": ("催化", "修复", "改善"),
        "同行对比": ("同行", "可比", "竞争"),
        "行业归属": ("行业", "赛道"),
        "指标影响": ("指标", "利润", "收入", "估值"),
    }
    focus_matched = any(keyword in report for keyword in focus_keywords.get(graph_query_focus, ()))
    multi_focus_matched = any(focus in report for focus in ("风险传导", "催化因素", "同行对比", "行业归属", "指标影响"))
    if graph_hit_count > 0 and all(keyword not in report for keyword in ("关系", "传导", "催化", "同行", "行业")) and not focus_matched and not multi_focus_matched:
        issue = f"存在关系图摘要，但报告正文未明显吸收关系信息（当前图查询焦点：{graph_query_focus}）"
        if graph_focus_summary:
            issue += f"；多焦点摘要：{graph_focus_summary}"
        if section_graph_summary:
            issue += f"；章节定向摘要：{section_graph_summary}"
        injected_sections = []
        section_graph_context_map = graph_payload.get("section_graph_context_map", {}) if isinstance(graph_payload.get("section_graph_context_map", {}), dict) else {}
        if _pick_state_value(section_graph_context_map.get("risk"), state.sections.get("section_graph_context_risk", ""), ""):
            injected_sections.append("风险")
        if _pick_state_value(section_graph_context_map.get("industry"), state.sections.get("section_graph_context_industry", ""), ""):
            injected_sections.append("行业")
        if _pick_state_value(section_graph_context_map.get("valuation"), state.sections.get("section_graph_context_valuation", ""), ""):
            injected_sections.append("估值")
        if injected_sections:
            issue += f"；已注入章节Graph={','.join(injected_sections)}"
        issues.append(issue)

    memory_hit_count = int(float(_pick_state_value(memory_payload.get("memory_hit_count"), state.sections.get("memory_hit_count", "0"), 0) or 0))
    if memory_hit_count > 0:
        memory_checks = {
            "评级变化": _pick_state_value(memory_payload.get("comparison_rating"), state.sections.get("memory_comparison_rating", ""), ""),
            "风险演化": _pick_state_value(memory_payload.get("comparison_risk"), state.sections.get("memory_comparison_risk", ""), ""),
            "估值演变": _pick_state_value(memory_payload.get("comparison_valuation"), state.sections.get("memory_comparison_valuation", ""), ""),
        }
        matched_memory = 0
        history_cues = ("上次", "本次", "历史", "变化", "演变", "vs")
        report_has_history_cue = any(cue in report for cue in history_cues)
        for label, source_text in memory_checks.items():
            if not source_text:
                continue
            tokens = [token.strip() for token in re.split(r"[→；：:，,\s]+", source_text) if token.strip() and len(token.strip()) >= 2]
            if report_has_history_cue and (label in report or any(token in report for token in tokens[:4])):
                matched_memory += 1
        if matched_memory == 0:
            issues.append("存在长期记忆，但报告正文未显式覆盖评级变化、风险演化或估值演变")

    section_graph_feedback = collect_section_graph_feedback(report, state)
    for section_id, meta in _SECTION_GRAPH_RULES.items():
        section_feedback = section_graph_feedback.get(section_id, {})
        if not section_feedback.get("injected"):
            continue
        if not section_feedback.get("absorbed"):
            issues.append(f"{meta['label']}存在章节级 Graph 注入，但正文未明显吸收对应关系线索")

    return issues


def collect_rule_metrics(report: str) -> dict:
    missing_sections: list[str] = []
    covered = 0
    for section_name, keywords in REQUIRED_SECTIONS:
        found = any(keyword in report for keyword in keywords)
        if found:
            covered += 1
        else:
            missing_sections.append(section_name)
    numbers = re.findall(r"\d+\.?\d*[%亿元倍]", report)
    section_graph_absorption_count = 0
    for meta in _SECTION_GRAPH_RULES.values():
        section_body = _extract_section_body(report, meta["heading"])
        if section_body and any(keyword in section_body for keyword in meta["keywords"]):
            section_graph_absorption_count += 1
    return {
        "covered_sections": covered,
        "section_coverage": covered / len(REQUIRED_SECTIONS),
        "missing_sections": missing_sections,
        "has_tables": "|" in report and "---" in report,
        "numeric_references": len(numbers),
        "has_numbers": len(numbers) >= 10,
        "risk_evidence_count": len(re.findall(r"证据[：:]", report)),
        "risk_transmission_count": len(re.findall(r"传导路径[：:]", report)),
        "investment_anchor_present": any(keyword in report for keyword in ["目标价", "估值区间", "估值锚", "合理估值区间"]),
        "data_gap_disclosure_count": len(re.findall(r"数据降级说明[：:]|数据降级说明", report)),
        "section_graph_absorption_count": section_graph_absorption_count,
    }


def _extract_section_body(report: str, heading: str) -> str:
    pattern = rf"{re.escape(heading)}\s*(.*?)(?=\n## |\Z)"
    match = re.search(pattern, report, flags=re.S)
    if not match:
        return ""
    return match.group(1).strip()


def build_judge_prompt(report: str) -> str:
    if len(report) <= 4000:
        report_excerpt = report
    else:
        report_excerpt = report[:2000] + "\n\n[...中间部分省略...]\n\n" + report[-2000:]
    return f"""请评估以下金融研报的质量，按 1-5 分评分。

## 研报内容（截取）
{report_excerpt}

请严格以 JSON 格式输出：
```json
{{
  \"completeness\": 4,
  \"completeness_reason\": \"原因\",
  \"data_support\": 3,
  \"data_support_reason\": \"原因\",
  \"reasoning_quality\": 4,
  \"reasoning_quality_reason\": \"原因\",
  \"readability\": 5,
  \"readability_reason\": \"原因\"
}}
```

评分标准：
- completeness: 报告结构是否完整（投资要点/财务/估值/风险/建议）
- data_support: 分析是否有具体数据支撑（数字/表格/图表）
- reasoning_quality: 推理逻辑是否合理（因果关系/对比分析/趋势判断）
- readability: 语言是否专业流畅（结构清晰/用词准确/排版合理）"""


def format_eval_markdown(result) -> str:
    lines = [
        f"# 研报评测报告 — {result.stock_code}",
        "",
        "## 规则型指标",
        f"- 章节覆盖率: **{result.section_coverage:.0%}** (8个必备章节)",
        f"- 缺失章节: {', '.join(result.missing_sections) if result.missing_sections else '无'}",
        f"- 包含数据表格: {'✅' if result.has_tables else '❌'}",
        f"- 数据引用充分: {'✅' if result.has_numbers else '❌'}",
        f"- 评级与估值一致: {'✅' if result.rating_consistent else '❌'}",
        f"- 报告-状态一致性: {'✅' if result.consistency_passed else '❌'} ({result.consistency_issue_count} 项)",
        f"- 风险证据条目: **{result.risk_evidence_count}**",
        f"- 风险传导路径条目: **{result.risk_transmission_count}**",
        f"- 投资建议估值锚: {'✅' if result.investment_anchor_present else '❌'}",
        f"- 数据降级披露次数: **{result.data_gap_disclosure_count}**",
        f"- 来源引用条目: **{result.source_reference_count}**",
        f"- 来源覆盖率: **{result.source_provenance_coverage:.0%}**",
        f"- 文档解析成功率: **{result.document_parse_success_rate:.0%}**",
        f"- 表格抽取成功率: **{result.table_extraction_success_rate:.0%}**",
        f"- 在线工具成功率: **{result.live_tool_success_rate:.0%}**",
        f"- 报告后处理修补次数: **{result.postprocess_fix_count}**",
        "",
        "## LLM 评分 (1-5)",
        f"- 完整性: **{result.completeness}**/5",
        f"- 数据支撑: **{result.data_support}**/5",
        f"- 推理质量: **{result.reasoning_quality}**/5",
        f"- 可读性: **{result.readability}**/5",
        "",
        f"## 综合评分: **{result.overall_score:.1f}**/100",
    ]
    if result.consistency_issues:
        lines.extend(["", "## 一致性诊断"])
        for issue in result.consistency_issues:
            lines.append(f"- {issue}")
    return "\n".join(lines)
