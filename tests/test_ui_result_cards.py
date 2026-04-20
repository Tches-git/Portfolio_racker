from __future__ import annotations

from app.evals.report_eval import EvalResult
from app.models import AnalysisState
from app.ui.result_cards import build_quality_guidance, build_quality_highlights, build_report_brief, build_result_dashboard_bars, build_result_overview_cards
from app.ui.tabs import get_tab_labels


def test_build_quality_highlights_flags_consistency_issue():
    result = EvalResult(overall_score=82.0, section_coverage=1.0, consistency_issue_count=2, data_gap_disclosure_count=1)

    cards = build_quality_highlights(result)

    assert cards[0]["label"] == "综合评分"
    assert any(card["label"] == "一致性问题" and card["tone"] == "bad" for card in cards)


def test_get_tab_labels_includes_core_summary():
    labels = get_tab_labels()

    assert labels[0] == "核心摘要"
    assert "研报正文" in labels
    assert "运行指标" in labels


def test_build_report_brief_extracts_non_heading_lines():
    state = AnalysisState(final_report="# 标题\n\n## 一、投资要点\n公司盈利能力稳健。\n估值具备一定安全边际。\n建议继续跟踪。")

    brief = build_report_brief(state)

    assert "盈利能力稳健" in brief
    assert "建议继续跟踪" in brief


def test_build_quality_guidance_prioritizes_consistency_and_data_checks():
    result = EvalResult(
        overall_score=72.0,
        section_coverage=0.75,
        consistency_issue_count=2,
        data_gap_disclosure_count=0,
        risk_transmission_count=0,
    )

    guidance = build_quality_guidance(result)

    assert any("一致性" in item for item in guidance)
    assert any("数据降级" in item for item in guidance)


def test_build_result_overview_cards_summarizes_key_result_layers():
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        final_report="# 标题\n盈利能力稳健。\n估值仍需跟踪。",
        sections={"rating": "推荐"},
    )
    result = EvalResult(overall_score=81.0, section_coverage=1.0, consistency_issue_count=1, risk_transmission_count=2)

    cards = build_result_overview_cards(state, result)

    assert len(cards) == 4
    assert cards[0]["title"] == "结论摘要"
    assert "评级" in cards[1]["value"]


def test_build_result_dashboard_bars_outputs_normalized_values():
    result = EvalResult(overall_score=80.0, section_coverage=0.875, consistency_issue_count=1, risk_transmission_count=2, data_gap_disclosure_count=1)

    bars = build_result_dashboard_bars(result)

    assert len(bars) == 5
    assert all(0.0 <= float(item["value"]) <= 1.0 for item in bars)
    assert bars[0]["label"] == "质量评分"
