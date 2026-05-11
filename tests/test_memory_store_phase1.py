from __future__ import annotations

from app.memory.comparator import build_risk_evolution_summary, build_run_vs_last_comparison, build_valuation_rating_timeline
from app.memory.store import MemoryStore, StockMemorySnapshot
from app.models import AnalysisState


def test_save_analysis_records_source_reference_counts(tmp_path):
    store = MemoryStore(data_dir=tmp_path)
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        source_refs=[
            {"title": "公告A", "is_placeholder": False},
            {"title": "券商观点", "is_placeholder": True},
        ],
    )

    record = store.save_analysis(state)

    assert record.source_reference_count == 2
    assert record.placeholder_source_count == 1


def test_save_analysis_also_persists_stock_memory_snapshot(tmp_path):
    store = MemoryStore(data_dir=tmp_path)
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        analysis_payload={"research_conclusion": "盈利质量稳健，估值等待催化。"},
        sections={"research_conclusion": "盈利质量稳健，估值等待催化。", "rating": "推荐", "rating_detail": "综合评分 82/100"},
    )

    store.save_analysis(state)
    snapshots = store.get_stock_memory("600519")
    context = store.build_memory_context("600519")

    assert len(snapshots) == 1
    assert snapshots[0].rating == "推荐"
    assert "盈利质量稳健" in snapshots[0].thesis
    assert context["memory_hit_count"] == 1


def test_build_run_vs_last_comparison_and_timeline_rows():
    previous = StockMemorySnapshot(
        stock_code="600519",
        timestamp="2026-04-18T10:00:00",
        thesis="盈利稳健但估值偏贵，等待渠道改善。",
        rating="中性",
        target_range="1800-1900元",
        key_risks=["需求波动", "渠道调整"],
        catalysts=["旺季动销修复"],
        valuation_summary="DCF每股价值 1850.00元，上涨空间 +3.0%",
        confidence_signals={"rating_score": 76, "source_reference_count": 2, "placeholder_source_ratio": 0.5},
    )
    current = StockMemorySnapshot(
        stock_code="600519",
        timestamp="2026-04-21T10:00:00",
        thesis="盈利韧性延续，估值重估需等待新品放量与渠道修复。",
        rating="推荐",
        target_range="1950-2050元",
        key_risks=["需求波动", "新品投放节奏"],
        catalysts=["旺季动销修复", "新品放量"],
        valuation_summary="DCF每股价值 2010.00元，上涨空间 +9.0%",
        confidence_signals={"rating_score": 84, "source_reference_count": 5, "placeholder_source_ratio": 0.2},
        historical_delta="评级 中性→推荐；新增风险 新品投放节奏",
        conflict_flag=True,
        conflict_reason="评分变化 76.0→84.0；新增风险 新品投放节奏",
    )

    comparison = build_run_vs_last_comparison(current, previous)
    risk_rows = build_risk_evolution_summary([current, previous])
    valuation_rows = build_valuation_rating_timeline([current, previous])

    assert "中性 → 推荐" in comparison["rating_change"]
    assert "1800-1900元" in comparison["valuation_change"]
    assert "新品投放节奏" in comparison["risk_change"]
    assert "冲突原因" in comparison["confidence_change"]
    assert len(risk_rows) == 2
    assert risk_rows[-1]["冲突"] == "是"
    assert valuation_rows[-1]["评级"] == "推荐"
    assert valuation_rows[-1]["估值锚"] == "1950-2050元"


def test_memory_context_applies_dedupe_and_conflict_governance(tmp_path):
    store = MemoryStore(data_dir=tmp_path)
    store._stock_memory["600519"] = [
        StockMemorySnapshot(
            stock_code="600519",
            timestamp="2026-04-21T10:00:00",
            thesis="盈利韧性延续。",
            rating="推荐",
            target_range="1950-2050元",
            key_risks=["需求波动", "新品节奏"],
            catalysts=["渠道修复", "新品放量"],
            historical_delta="评级 中性→推荐",
            conflict_flag=True,
            conflict_reason="评分变化 76.0→84.0",
        ),
        StockMemorySnapshot(
            stock_code="600519",
            timestamp="2026-04-20T10:00:00",
            thesis="盈利韧性延续。",
            rating="推荐",
            target_range="1950-2050元",
            key_risks=["需求波动", "新品节奏"],
            catalysts=["渠道修复"],
        ),
        StockMemorySnapshot(
            stock_code="600519",
            timestamp="2025-01-01T10:00:00",
            thesis="盈利承压。",
            rating="中性",
            target_range="1800-1900元",
            key_risks=["渠道调整", "需求波动"],
            catalysts=["渠道修复"],
        ),
    ]

    ranked = store.get_ranked_stock_memory("600519", limit=6)
    context = store.build_memory_context("600519")

    assert len(ranked) == 2
    assert ranked[0].conflict_flag is True
    assert context["memory_hit_count"] == 2
    assert context["memory_conflict_count"] == 1
    assert "去重 1 条" in context["governance_notes"]
    assert "冲突原因" in context["summary"]
    assert context["repeated_risk_pattern_count"] == 1
    assert "需求波动" in context["repeated_risk_patterns"]
    assert context["repeated_catalyst_pattern_count"] == 1
    assert "渠道修复" in context["repeated_catalyst_patterns"]
    assert context["thesis_stability_score"] == 0.5
    assert context["rating_drift_count"] == 1
    assert "评级漂移" in context["memory_pattern_summary"]
