"""report_eval 的辅助逻辑。"""
from __future__ import annotations

import re


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


def check_report_consistency(report: str, state) -> list[str]:
    issues: list[str] = []
    if state is None:
        return issues

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
    }


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
