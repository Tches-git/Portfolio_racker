"""研报评测框架 — 规则型 + LLM-as-Judge 评估"""
from __future__ import annotations
import logging
from dataclasses import asdict, dataclass, field

from app.evals.report_eval_helpers import (
    build_judge_prompt,
    check_report_consistency,
    collect_rule_metrics,
    format_eval_markdown,
)

logger = logging.getLogger("fin.evals")


@dataclass
class EvalResult:
    """评测结果"""
    stock_code: str = ""
    # 规则型指标
    section_coverage: float = 0.0      # 章节覆盖率 (0-1)
    has_tables: bool = False            # 是否包含表格
    has_numbers: bool = False           # 是否引用数据
    missing_sections: list[str] = field(default_factory=list)
    # 一致性指标
    rating_consistent: bool = False     # 评级与估值方向一致
    consistency_passed: bool = True
    consistency_issue_count: int = 0
    consistency_issues: list[str] = field(default_factory=list)
    # LLM 评分
    completeness: int = 0              # 完整性 (1-5)
    data_support: int = 0              # 数据支撑 (1-5)
    reasoning_quality: int = 0         # 推理质量 (1-5)
    readability: int = 0               # 可读性 (1-5)
    overall_score: float = 0.0         # 综合评分 (0-100)
    report_length: int = 0
    numeric_references: int = 0
    covered_sections: int = 0
    llm_judge_enabled: bool = True
    risk_evidence_count: int = 0
    risk_transmission_count: int = 0
    investment_anchor_present: bool = False
    postprocess_fix_count: int = 0
    data_gap_disclosure_count: int = 0

    def summary(self) -> str:
        return (
            f"章节覆盖: {self.section_coverage:.0%} | "
            f"表格: {'✅' if self.has_tables else '❌'} | "
            f"数据引用: {'✅' if self.has_numbers else '❌'} | "
            f"评级一致: {'✅' if self.rating_consistent else '❌'} | "
            f"LLM评分: 完整{self.completeness} 数据{self.data_support} "
            f"推理{self.reasoning_quality} 可读{self.readability} | "
            f"综合: {self.overall_score:.1f}/100"
        )


def evaluate_report(report: str, state=None, stock_code: str = "", *, use_llm_judge: bool = True) -> EvalResult:
    """评测研报质量"""
    result = EvalResult(stock_code=stock_code, llm_judge_enabled=use_llm_judge)
    result.report_length = len(report)

    # 1. 规则型指标
    rule_metrics = collect_rule_metrics(report)
    result.covered_sections = rule_metrics["covered_sections"]
    result.section_coverage = rule_metrics["section_coverage"]
    result.missing_sections = rule_metrics["missing_sections"]
    result.has_tables = rule_metrics["has_tables"]
    result.numeric_references = rule_metrics["numeric_references"]
    result.has_numbers = rule_metrics["has_numbers"]
    result.risk_evidence_count = rule_metrics["risk_evidence_count"]
    result.risk_transmission_count = rule_metrics["risk_transmission_count"]
    result.investment_anchor_present = rule_metrics["investment_anchor_present"]
    result.data_gap_disclosure_count = rule_metrics["data_gap_disclosure_count"]

    # 4. 评级一致性
    if state:
        result.postprocess_fix_count = int(state.sections.get("postprocess_fix_count", "0") or 0)
        result.consistency_issues = check_report_consistency(report, state)
        result.consistency_issue_count = len(result.consistency_issues)
        result.consistency_passed = result.consistency_issue_count == 0
        rating = state.sections.get("rating", "")
        dcf = state.dcf
        if dcf and rating:
            if dcf.upside > 0 and rating in ("强烈推荐", "推荐"):
                result.rating_consistent = True
            elif dcf.upside < 0 and rating in ("谨慎", "回避"):
                result.rating_consistent = True
            elif rating == "中性":
                result.rating_consistent = True

    # 5. LLM-as-Judge
    if use_llm_judge:
        try:
            from app.llm import chat_json

            scores = chat_json(build_judge_prompt(report), temperature=0.1, max_tokens=512)
            if isinstance(scores, dict) and "completeness" in scores:
                result.completeness = min(5, max(1, int(scores.get("completeness", 3))))
                result.data_support = min(5, max(1, int(scores.get("data_support", 3))))
                result.reasoning_quality = min(5, max(1, int(scores.get("reasoning_quality", 3))))
                result.readability = min(5, max(1, int(scores.get("readability", 3))))
        except Exception as e:
            logger.warning(f"LLM 评分失败: {e}")
            result.completeness = 3
            result.data_support = 3
            result.reasoning_quality = 3
            result.readability = 3
    else:
        result.completeness = 0
        result.data_support = 0
        result.reasoning_quality = 0
        result.readability = 0

    # 6. 综合评分
    rule_score = (
        result.section_coverage * 30 +
        (10 if result.has_tables else 0) +
        (10 if result.has_numbers else 0) +
        (5 if result.rating_consistent else 0)
    )
    llm_score = 0.0
    if use_llm_judge:
        llm_score = (
            result.completeness + result.data_support +
            result.reasoning_quality + result.readability
        ) / 20 * 45  # 最高 45 分
    result.overall_score = round(rule_score + llm_score, 1)

    return result


def evaluate_report_with_metrics(report: str, state=None, stock_code: str = "", *, use_llm_judge: bool = True) -> dict:
    result = evaluate_report(report, state=state, stock_code=stock_code, use_llm_judge=use_llm_judge)
    payload = asdict(result)
    payload["summary"] = result.summary()
    if state is not None and getattr(state, "run_metrics", None):
        payload["run_metrics"] = dict(state.run_metrics)
    return payload


def format_eval_report(result: EvalResult) -> str:
    """格式化评测报告为 Markdown"""
    return format_eval_markdown(result)
