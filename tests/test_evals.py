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
                self.sections = {"postprocess_fix_count": "3"}
                self.dcf = None
                self.risks = []
                self.news = []
                self.peers = []

        payload = evaluate_report_with_metrics(FULL_REPORT, state=DummyState(), stock_code="600519", use_llm_judge=False)
        assert payload["postprocess_fix_count"] == 3

    def test_detects_report_state_inconsistency(self):
        state = SimpleNamespace(
            run_metrics={},
            sections={"rating": "推荐"},
            dcf=SimpleNamespace(per_share_value=555.57, current_price=1500.00, upside=-63.0),
            risks=[SimpleNamespace(description="监管或合规负面事件升温")],
            news=[{"title": "公司收到监管问询函"}],
            peers=[{"code": "000858"}],
        )
        report = "## 八、投资建议\n评级：推荐。"

        payload = evaluate_report_with_metrics(report, state=state, stock_code="600519", use_llm_judge=False)

        assert payload["consistency_passed"] is False
        assert payload["consistency_issue_count"] >= 1
        assert any("DCF 每股价值" in issue for issue in payload["consistency_issues"])
