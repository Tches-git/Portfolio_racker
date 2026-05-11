from __future__ import annotations

from app.models import AnalysisState, PeerCompany, RiskItem, StockProfile
from app.rag.graph_builder import build_graph_summary


def test_build_graph_summary_extracts_core_relations():
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        profile=StockProfile(code="600519", name="贵州茅台", industry="白酒"),
        peers=[PeerCompany(code="000858", name="五粮液", pe_ratio=25, roe=18)],
        risks=[
            RiskItem(
                category="news",
                level="high",
                description="需求波动可能压制动销与价格体系",
                evidence="渠道调研显示旺季动销波动",
                transmission_path="动销走弱→收入增速放缓→估值承压",
                impact="收入增速、估值中枢",
            )
        ],
        source_refs=[{"title": "渠道调研纪要", "source": "中信", "summary": "提到旺季动销和渠道修复"}],
        analysis_payload={"research_conclusion": "若渠道修复与新品放量兑现，将形成估值修复催化。"},
        sections={"research_conclusion": "若渠道修复与新品放量兑现，将形成估值修复催化。"},
    )

    summary = build_graph_summary(state)

    assert summary.graph_hit_count >= 5
    assert summary.relationship_coverage > 0
    assert summary.risk_path_completeness > 0
    assert any(edge.relation == "belongs_to_industry" for edge in summary.edges)
    assert any(edge.relation == "causes_risk" for edge in summary.edges)
    assert any(edge.relation == "affects_metric" for edge in summary.edges)
    assert any(edge.relation == "triggers_catalyst" for edge in summary.edges)
    assert "关系图摘要" in summary.summary
