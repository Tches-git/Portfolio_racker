from __future__ import annotations

from app.evals.human_rubric import (
    RUBRIC_DIMENSIONS,
    build_manual_review_payload,
    format_manual_review_markdown,
)


def test_build_manual_review_payload_contains_rubric_and_metrics():
    report = "# 测试研报\n\n## 一、投资要点\n营收100亿。目标价120元。"
    payload = build_manual_review_payload(
        report,
        "600519",
        benchmark_entry={"stock_name": "贵州茅台", "review_focus": ["估值锚"]},
    )

    assert payload["stock_code"] == "600519"
    assert len(payload["manual_rubric"]) == len(RUBRIC_DIMENSIONS)
    assert "automated_metrics" in payload


def test_format_manual_review_markdown_renders_sections():
    payload = {
        "stock_code": "600519",
        "benchmark": {"stock_name": "贵州茅台", "industry": "白酒", "review_focus": ["估值锚"], "key_risks": ["需求波动"]},
        "automated_metrics": {"overall_score": 80, "section_coverage": 1.0, "risk_evidence_count": 2, "risk_transmission_count": 2, "investment_anchor_present": True, "data_gap_disclosure_count": 1},
        "manual_rubric": [
            {"title": "结构完整性", "scale": "1-5", "question": "是否完整", "score": None, "comment": ""}
        ],
        "overall_comment": "整体质量较好。",
    }
    md = format_manual_review_markdown(payload)

    assert "# 人工评审表 — 600519" in md
    assert "## 自动指标参考" in md
    assert "## 人工 Rubric（1-5）" in md
    assert "整体质量较好。" in md
