"""研报评测模块单元测试"""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.evals.report_eval import evaluate_report, evaluate_report_with_metrics, EvalResult, format_eval_report


# 构造一个包含所有必备章节的模拟研报
FULL_REPORT = """
# 贵州茅台 深度研究报告

## 一、投资要点
1. 营收稳定增长，2024年营收1505亿元
2. ROE持续保持25%以上高水平

## 二、公司概况
贵州茅台是中国白酒行业龙头企业。

## 三、杜邦分析
ROE分解：净利率52% × 资产周转率0.4 × 权益乘数1.3

| 期间 | ROE | 净利率 |
|------|-----|--------|
| 2024 | 25% | 52%    |

## 四、财务分析
营收1505亿元，同比增长15.7%。毛利率91.5%。

## 五、估值分析
DCF现金流折现估值：每股内在价值2100元。

## 六、行业分析
白酒行业CR5集中度持续提升。竞争格局稳定。

## 七、风险提示
1. 消费降级风险
2. 政策监管风险

## 八、投资建议
评级：强烈推荐。目标价2200元。
"""

MINIMAL_REPORT = "这是一份很简短的报告，没有任何结构。"


class TestEvaluateReport:
    """evaluate_report 函数测试"""

    def test_full_report_high_coverage(self):
        result = evaluate_report(FULL_REPORT, stock_code="600519", use_llm_judge=False)
        assert result.section_coverage >= 0.875  # 至少7/8章节

    def test_minimal_report_low_coverage(self):
        result = evaluate_report(MINIMAL_REPORT, stock_code="000001", use_llm_judge=False)
        assert result.section_coverage < 0.5

    def test_has_tables_detection(self):
        result = evaluate_report(FULL_REPORT, stock_code="600519", use_llm_judge=False)
        assert result.has_tables is True

    def test_no_tables_detection(self):
        result = evaluate_report(MINIMAL_REPORT, stock_code="000001", use_llm_judge=False)
        assert result.has_tables is False

    def test_has_numbers(self):
        report_with_numbers = "营收100亿 利润20亿 增速15% PE30倍 市值500亿 ROE25% 毛利率50% 负债率30% 现金流10亿 PB5倍 目标价100元"
        result = evaluate_report(report_with_numbers, use_llm_judge=False)
        assert result.has_numbers is True
        assert result.numeric_references >= 10

    def test_missing_sections_listed(self):
        result = evaluate_report(MINIMAL_REPORT, stock_code="000001", use_llm_judge=False)
        assert len(result.missing_sections) > 0

    def test_overall_score_range(self):
        result = evaluate_report(FULL_REPORT, stock_code="600519", use_llm_judge=False)
        assert 0 <= result.overall_score <= 100
        assert result.llm_judge_enabled is False


class TestFormatEvalReport:
    """format_eval_report 格式化测试"""

    def test_contains_markdown(self):
        result = EvalResult(
            stock_code="600519",
            section_coverage=0.875,
            has_tables=True,
            has_numbers=True,
            completeness=4,
            data_support=4,
            reasoning_quality=4,
            readability=4,
            overall_score=85.0,
        )
        md = format_eval_report(result)
        assert "# 研报评测报告" in md
        assert "600519" in md
        assert "85.0" in md


class TestEvaluateReportWithMetrics:
    def test_includes_run_metrics(self):
        class DummyState:
            def __init__(self):
                self.run_metrics = {"duration_s": 1.23, "total_tokens": 456}
                self.sections = {}
                self.dcf = None
                self.risks = []
                self.news = []
                self.peers = []
                self.source_refs = []

        payload = evaluate_report_with_metrics(FULL_REPORT, state=DummyState(), stock_code="600519", use_llm_judge=False)
        assert payload["report_length"] == len(FULL_REPORT)
        assert payload["numeric_references"] >= 1
        assert payload["run_metrics"]["total_tokens"] == 456

    def test_extracts_risk_and_anchor_metrics(self):
        report = FULL_REPORT + "\n风险事件：监管问询。证据：收到交易所问询函。传导路径：监管整改→利润率承压。目标价2200元。数据降级说明：新闻数据不足。"
        payload = evaluate_report_with_metrics(report, stock_code="600519", use_llm_judge=False)

        assert payload["risk_evidence_count"] >= 1
        assert payload["risk_transmission_count"] >= 1
        assert payload["investment_anchor_present"] is True
        assert payload["data_gap_disclosure_count"] >= 1

    def test_reads_postprocess_fix_count_from_state(self):
        class DummyState:
            def __init__(self):
                self.run_metrics = {}
                self.run_payload = {"postprocess": {"fix_count": 4, "fixes": ["a"]}}
                self.sections = {"postprocess_fix_count": "3"}
                self.dcf = None
                self.risks = []
                self.news = []
                self.peers = []
                self.source_refs = []

        payload = evaluate_report_with_metrics(FULL_REPORT, state=DummyState(), stock_code="600519", use_llm_judge=False)
        assert payload["postprocess_fix_count"] == 4

    def test_detects_report_state_inconsistency(self):
        state = SimpleNamespace(
            run_metrics={},
            sections={"rating": "推荐"},
            dcf=SimpleNamespace(per_share_value=555.57, current_price=1500.00, upside=-63.0),
            risks=[SimpleNamespace(description="监管或合规负面事件升温")],
            news=[{"title": "公司收到监管问询函"}],
            peers=[{"code": "000858"}],
            source_refs=[],
        )
        report = "## 八、投资建议\n评级：推荐。"

        payload = evaluate_report_with_metrics(report, state=state, stock_code="600519", use_llm_judge=False)

        assert payload["consistency_passed"] is False
        assert payload["consistency_issue_count"] >= 1
        assert any("DCF 每股价值" in issue for issue in payload["consistency_issues"])

    def test_collects_phase1_source_metrics_from_state(self):
        state = SimpleNamespace(
            run_metrics={},
            runtime_input_payload={
                "documents": {
                    "parse_success_rate": "0.50",
                    "table_extraction_success_rate": "0.25",
                },
                "live_tools": {"success_rate": "0.75"},
            },
            memory_payload={
                "memory_hit_count": 3,
                "historical_delta_coverage": 1.0,
                "duplicate_memory_injection_rate": 0.25,
                "repeated_risk_pattern_count": 2,
                "repeated_catalyst_pattern_count": 1,
                "thesis_stability_score": 0.6,
                "rating_drift_count": 1,
            },
            graph_payload={
                "graph_hit_count": 6,
                "hybrid_retrieval_hit_rate": 0.8,
                "relationship_coverage": 0.75,
                "risk_path_completeness": 0.5,
                "graph_query_focus": "风险传导",
                "graph_focus_coverage": 0.8,
                "graph_focus_summary": "风险传导=命中(causes_risk)；催化因素=命中(triggers_catalyst)",
                "section_graph_hit_count": 3,
                "section_graph_focus_coverage": 1.0,
                "section_graph_summary": "风险章节=命中(causes_risk)；行业章节=命中(compares_with)；估值章节=命中(affects_metric)",
                "section_graph_context_map": {
                    "risk": "风险章节 Graph Context：\n- 贵州茅台 --causes_risk--> 需求波动",
                    "industry": "行业章节 Graph Context：\n- 贵州茅台 --compares_with--> 五粮液",
                    "valuation": "估值章节 Graph Context：\n- 需求波动 --affects_metric--> 收入增速",
                },
                "section_graph_query_summary": "风险章节=贵州茅台 需求波动 风险 传导 指标 下行；行业章节=贵州茅台 五粮液 同行 可比 行业 竞争 格局；估值章节=贵州茅台 估值 DCF 2010.00元 上涨空间 +9.0% 催化 修复 利润 收入",
                "section_graph_refinement_comparison_summary": "风险章节=1->1 (Δ0)；行业章节=1->1 (Δ0)；估值章节=1->1 (Δ0)",
                "section_graph_refinement_improved_count": 0,
            },
            sections={
                "document_parse_success_rate": "0.40",
                "table_extraction_success_rate": "0.20",
                "live_tool_success_rate": "0.70",
                "memory_hit_count": "1",
                "historical_delta_coverage": "0.5",
                "duplicate_memory_injection_rate": "0.5",
                "repeated_risk_pattern_count": "1",
                "repeated_catalyst_pattern_count": "0",
                "thesis_stability_score": "0.3",
                "rating_drift_count": "0",
                "graph_hit_count": "1",
                "hybrid_retrieval_hit_rate": "0.2",
                "relationship_coverage": "0.1",
                "risk_path_completeness": "0.1",
                "graph_query_focus": "通用关系",
                "graph_focus_coverage": "0.1",
                "graph_focus_summary": "旧摘要",
                "section_graph_hit_count": "1",
                "section_graph_focus_coverage": "0.3",
                "section_graph_summary": "旧章节摘要",
                "section_graph_context_risk": "旧风险上下文",
                "section_graph_context_industry": "旧行业上下文",
                "section_graph_context_valuation": "旧估值上下文",
                "section_graph_query_summary": "旧 query",
                "section_graph_refinement_comparison_summary": "旧对比",
                "section_graph_refinement_improved_count": "2",
            },
            dcf=None,
            risks=[],
            news=[],
            peers=[],
            source_refs=[
                {"title": "公告1", "source": "东财"},
                {"title": "文档1", "source": "upload"},
            ],
        )

        payload = evaluate_report_with_metrics(FULL_REPORT, state=state, stock_code="600519", use_llm_judge=False)

        assert payload["source_reference_count"] == 2
        assert payload["source_provenance_coverage"] == 1.0
        assert payload["document_parse_success_rate"] == 0.5
        assert payload["live_tool_success_rate"] == 0.75
        assert payload["memory_hit_count"] == 3
        assert payload["historical_delta_coverage"] == 1.0
        assert payload["duplicate_memory_injection_rate"] == 0.25
        assert payload["repeated_risk_pattern_count"] == 2
        assert payload["repeated_catalyst_pattern_count"] == 1
        assert payload["thesis_stability_score"] == 0.6
        assert payload["rating_drift_count"] == 1
        assert payload["graph_hit_count"] == 6
        assert payload["hybrid_retrieval_hit_rate"] == 0.8
        assert payload["relationship_coverage"] == 0.75
        assert payload["risk_path_completeness"] == 0.5
        assert payload["graph_query_focus"] == "风险传导"
        assert payload["graph_focus_coverage"] == 0.8
        assert payload["section_graph_hit_count"] == 3
        assert payload["section_graph_focus_coverage"] == 1.0
        assert payload["section_graph_prompt_injection_present"] is True
        assert "贵州茅台" in payload["section_graph_query_summary"]
        assert payload["section_graph_absorption_count"] == 1
        assert payload["section_graph_absorption_rate"] == 0.3333
        assert payload["section_graph_low_absorption_count"] == 2
        assert payload["section_graph_low_absorption_sections"] == "风险章节、行业章节"
        assert payload["section_graph_refinement_triggered"] is False
        assert payload["section_graph_refinement_coverage"] == 0.0
        assert payload["section_graph_refinement_improved_count"] == 0
        assert payload["section_graph_refinement_improvement_rate"] == 0.0
        assert payload["section_graph_no_hit_count"] == 0
        assert payload["section_graph_no_gain_count"] == 2
        assert payload["section_graph_low_absorption_only_count"] == 0
        assert "风险章节=有命中但无增量" in payload["section_graph_low_improvement_summary"]
        assert "风险章节=1->1 (Δ0)" in payload["section_graph_refinement_comparison_summary"]
        assert "风险章节=注入是/吸收否" in payload["section_graph_feedback_summary"]
        assert "估值章节=注入是/吸收是" in payload["section_graph_feedback_summary"]
        assert "风险传导=命中(causes_risk)" in payload["graph_focus_summary"]
        assert "风险章节=命中(causes_risk)" in payload["section_graph_summary"]

    def test_detects_missing_memory_reference_when_history_exists(self):
        state = SimpleNamespace(
            run_metrics={},
            memory_payload={
                "memory_hit_count": 2,
                "comparison_rating": "中性 → 推荐",
                "comparison_risk": "风险变化：新增 新品投放节奏",
                "comparison_valuation": "1800-1900元 → 1950-2050元",
                "historical_delta_coverage": 1.0,
                "duplicate_memory_injection_rate": 0.0,
                "governance_notes": "去重 1 条；衰减低权重 0 条；保留冲突 1 条",
            },
            sections={
                "rating": "推荐",
                "memory_hit_count": "1",
                "memory_comparison_rating": "旧评级变化",
                "memory_comparison_risk": "旧风险变化",
                "memory_comparison_valuation": "旧估值变化",
                "historical_delta_coverage": "0.0",
                "duplicate_memory_injection_rate": "1.0",
                "memory_governance_notes": "旧治理说明",
                "graph_hit_count": "4",
            },
            dcf=None,
            risks=[],
            news=[],
            peers=[],
            source_refs=[],
        )

        payload = evaluate_report_with_metrics("## 八、投资建议\n评级：推荐。", state=state, stock_code="600519", use_llm_judge=False)

        assert payload["memory_reference_present"] is False
        assert payload["memory_reference_coverage"] == 0.0
        assert any("长期记忆" in issue for issue in payload["consistency_issues"])

    def test_marks_memory_reference_present_when_report_mentions_history_changes(self):
        state = SimpleNamespace(
            run_metrics={},
            memory_payload={
                "memory_hit_count": 2,
                "comparison_rating": "中性 → 推荐",
                "comparison_risk": "风险变化：新增 新品投放节奏",
                "comparison_valuation": "1800-1900元 → 1950-2050元",
                "historical_delta_coverage": 1.0,
                "duplicate_memory_injection_rate": 0.0,
                "governance_notes": "去重 1 条；衰减低权重 0 条；保留冲突 1 条",
            },
            sections={
                "rating": "推荐",
                "memory_hit_count": "1",
                "memory_comparison_rating": "旧评级变化",
                "memory_comparison_risk": "旧风险变化",
                "memory_comparison_valuation": "旧估值变化",
                "historical_delta_coverage": "0.0",
                "duplicate_memory_injection_rate": "1.0",
                "memory_governance_notes": "旧治理说明",
                "graph_hit_count": "4",
            },
            dcf=None,
            risks=[],
            news=[],
            peers=[],
            source_refs=[],
        )
        report = "## 一、投资要点\n相较上次覆盖，中性→推荐，且风险变化聚焦新品投放节奏，估值演变由1800-1900元抬升至1950-2050元。"

        payload = evaluate_report_with_metrics(report, state=state, stock_code="600519", use_llm_judge=False)

        assert payload["memory_reference_present"] is True
        assert payload["memory_reference_coverage"] == 1.0

    def test_computes_refinement_effectiveness_metrics_when_refinement_exists(self):
        state = SimpleNamespace(
            run_metrics={},
            sections={
                "section_graph_context_risk": "风险章节 Graph Context：\n- 贵州茅台 --causes_risk--> 需求波动",
                "section_graph_context_industry": "行业章节 Graph Context：\n- 贵州茅台 --compares_with--> 五粮液",
                "section_graph_context_valuation": "估值章节 Graph Context：\n- 未命中",
                "section_graph_query_refined_count": "1",
                "section_graph_refinement_improved_count": "1",
                "section_graph_refinement_comparison_summary": "风险章节=1->2 (Δ1)；行业章节=1->1 (Δ0)；估值章节=0->0 (Δ0)",
            },
            dcf=None,
            risks=[],
            news=[],
            peers=[],
            source_refs=[],
        )
        report = "## 六、行业格局与可比公司对比\n行业竞争格局清晰。\n\n## 七、核心风险与跟踪指标\n公司经营稳健，但相关不确定性仍需跟踪。"

        payload = evaluate_report_with_metrics(report, state=state, stock_code="600519", use_llm_judge=False)

        assert payload["section_graph_low_absorption_count"] == 1
        assert payload["section_graph_low_absorption_sections"] == "风险章节"
        assert payload["section_graph_refinement_triggered"] is True
        assert payload["section_graph_refinement_coverage"] == 1.0
        assert payload["section_graph_refinement_improved_count"] == 1
        assert payload["section_graph_refinement_improvement_rate"] == 1.0
        assert payload["section_graph_no_hit_count"] == 0
        assert payload["section_graph_no_gain_count"] == 0
        assert payload["section_graph_low_absorption_only_count"] == 0
        assert payload["section_graph_low_improvement_summary"] == ""
        assert "风险章节=1->2 (Δ1)" in payload["section_graph_refinement_comparison_summary"]

    def test_detects_missing_graph_reference_when_graph_hits_exist(self):
        state = SimpleNamespace(
            run_metrics={},
            sections={
                "graph_hit_count": "3",
                "graph_query_focus": "风险传导",
                "graph_focus_summary": "风险传导=命中(causes_risk)；催化因素=命中(triggers_catalyst)",
                "section_graph_summary": "风险章节=命中(causes_risk)；行业章节=命中(compares_with)",
                "section_graph_context_risk": "风险章节 Graph Context：\n- 贵州茅台 --causes_risk--> 需求波动",
                "section_graph_context_industry": "行业章节 Graph Context：\n- 贵州茅台 --compares_with--> 五粮液",
                "section_graph_context_valuation": "估值章节 Graph Context：\n- 未命中",
            },
            dcf=None,
            risks=[],
            news=[],
            peers=[],
            source_refs=[],
        )

        payload = evaluate_report_with_metrics("## 一、投资要点\n公司盈利稳健。", state=state, stock_code="600519", use_llm_judge=False)

        assert payload["section_graph_absorption_count"] == 0
        assert payload["section_graph_absorption_rate"] == 0.0
        assert payload["section_graph_low_absorption_count"] == 2
        assert payload["section_graph_low_absorption_sections"] == "风险章节、行业章节"
        assert payload["section_graph_refinement_triggered"] is False
        assert payload["section_graph_refinement_coverage"] == 0.0
        assert payload["section_graph_refinement_improved_count"] == 0
        assert payload["section_graph_refinement_improvement_rate"] == 0.0
        assert payload["section_graph_no_hit_count"] == 0
        assert payload["section_graph_no_gain_count"] == 0
        assert payload["section_graph_low_absorption_only_count"] == 2
        assert "风险章节=低吸收" in payload["section_graph_low_improvement_summary"]
        assert "行业章节=低吸收" in payload["section_graph_low_improvement_summary"]
        assert "风险章节=注入是/吸收否" in payload["section_graph_feedback_summary"]
        assert any("图查询焦点：风险传导" in issue for issue in payload["consistency_issues"])
        assert any("多焦点摘要" in issue for issue in payload["consistency_issues"])
        assert any("章节定向摘要" in issue for issue in payload["consistency_issues"])
        assert any("已注入章节Graph=风险,行业,估值" in issue for issue in payload["consistency_issues"])
        assert any("风险章节存在章节级 Graph 注入" in issue for issue in payload["consistency_issues"])
