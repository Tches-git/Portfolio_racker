from __future__ import annotations

import run_ablation


def test_summarize_results_includes_postprocess_metrics():
    rows = [
        {
            "stock_code": "600519",
            "label": "baseline",
            "success": True,
            "overall_score": 85.0,
            "duration_s": 10.0,
            "total_tokens": 1000,
            "llm_calls": 5,
            "tool_calls": 8,
            "agent_steps": 6,
            "rag_hits": 3,
            "news_count": 4,
            "risk_count": 2,
            "risk_evidence_count": 2,
            "risk_transmission_count": 2,
            "investment_anchor_present": True,
            "postprocess_fix_count": 1,
            "report_length": 5000,
            "numeric_references": 20,
            "errors": 0,
        },
        {
            "stock_code": "600519",
            "label": "no_rag",
            "success": True,
            "overall_score": 80.0,
            "duration_s": 9.0,
            "total_tokens": 900,
            "llm_calls": 4,
            "tool_calls": 7,
            "agent_steps": 5,
            "rag_hits": 0,
            "news_count": 4,
            "risk_count": 2,
            "risk_evidence_count": 1,
            "risk_transmission_count": 1,
            "investment_anchor_present": False,
            "postprocess_fix_count": 3,
            "report_length": 4500,
            "numeric_references": 15,
            "errors": 0,
        },
    ]

    summary_md, aggregate = run_ablation.summarize_results(rows, use_llm_judge=False)

    assert "自动修补" in summary_md
    assert "平均自动修补次数" in summary_md
    assert aggregate["baseline"]["avg_postprocess_fix_count"] == 1.0
    assert aggregate["no_rag"]["avg_postprocess_fix_count"] == 3.0
