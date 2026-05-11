from __future__ import annotations

from app.rag.graph_schema import GraphEdge, GraphSummary
from app.rag.graph_store import GraphStore
from app.rag.hybrid_retriever import build_hybrid_context


def test_graph_store_query_matches_edges_by_tokens():
    store = GraphStore()
    summary = GraphSummary(
        edges=[
            GraphEdge(source="贵州茅台", relation="causes_risk", target="需求波动", evidence="渠道调研"),
            GraphEdge(source="贵州茅台", relation="compares_with", target="五粮液", evidence="PE 25"),
        ],
        summary="关系图摘要",
    )
    store.save_summary("600519", summary)

    edges = store.query("600519", "causes_risk 渠道", limit=3)

    assert len(edges) == 1
    assert edges[0].relation == "causes_risk"


def test_build_hybrid_context_falls_back_when_no_graph_match():
    store = GraphStore()
    summary = GraphSummary(summary="暂无关系图摘要")

    payload = build_hybrid_context(
        store,
        graph_key="600519",
        graph_summary=summary,
        query_text="无匹配",
        vector_context="向量上下文",
    )

    assert payload["graph_hit_count"] == 0
    assert payload["hybrid_retrieval_hit_rate"] == 1.0
    assert payload["graph_query_focus"] == "通用关系"
    assert payload["graph_focus_coverage"] == 0.0
    assert payload["section_graph_hit_count"] == 0
    assert payload["section_graph_focus_coverage"] == 0.0
    assert "风险章节=未命中" in str(payload["section_graph_summary"])
    assert "风险章节 Graph Context：" in str(payload["section_graph_context_map"]["risk"])
    assert "Query Focus：通用关系" in str(payload["graph_context"])
    assert "多焦点关系摘要" in str(payload["graph_context"])
    assert "向量上下文" in str(payload["hybrid_context"])


def test_build_hybrid_context_prefers_graph_hits_when_available():
    store = GraphStore()
    summary = GraphSummary(
        edges=[GraphEdge(source="贵州茅台", relation="triggers_catalyst", target="渠道修复", evidence="研究结论")],
        summary="贵州茅台 关系图摘要：已提取 1 条关系。",
    )

    payload = build_hybrid_context(
        store,
        graph_key="600519",
        graph_summary=summary,
        query_text="茅台 渠道 修复",
        vector_context="向量上下文",
    )

    assert payload["graph_hit_count"] == 1
    assert payload["hybrid_retrieval_hit_rate"] == 1.0
    assert payload["graph_query_focus"] == "催化因素"
    assert payload["graph_focus_coverage"] > 0
    assert payload["section_graph_hit_count"] > 0
    assert payload["section_graph_focus_coverage"] > 0
    assert "triggers_catalyst" in str(payload["section_graph_context_map"]["valuation"])
    assert "图关系命中" in str(payload["graph_context"])
    assert "命中原因 关系意图=催化因素" in str(payload["graph_context"])
    assert "多焦点关系摘要" in str(payload["graph_context"])
    assert "催化因素：贵州茅台 --triggers_catalyst--> 渠道修复" in str(payload["graph_context"])
    assert "风险章节" in str(payload["section_graph_context"])
    assert "向量上下文" in str(payload["hybrid_context"])


def test_graph_store_query_scored_prefers_relation_intent_matches():
    store = GraphStore()
    summary = GraphSummary(
        edges=[
            GraphEdge(source="贵州茅台", relation="causes_risk", target="需求波动", evidence="渠道反馈"),
            GraphEdge(source="贵州茅台", relation="compares_with", target="五粮液", evidence="PE 25"),
        ],
        summary="关系图摘要",
    )
    store.save_summary("600519", summary)

    hits = store.query_scored("600519", "风险 传导", limit=2)

    assert len(hits) == 1
    assert hits[0]["edge"].relation == "causes_risk"
    assert hits[0]["reason"] == "关系意图=风险传导"


def test_build_hybrid_context_exposes_multi_focus_summary():
    store = GraphStore()
    summary = GraphSummary(
        edges=[
            GraphEdge(source="贵州茅台", relation="causes_risk", target="需求波动", evidence="渠道反馈"),
            GraphEdge(source="贵州茅台", relation="triggers_catalyst", target="渠道修复", evidence="研究结论"),
            GraphEdge(source="贵州茅台", relation="compares_with", target="五粮液", evidence="PE 25"),
            GraphEdge(source="贵州茅台", relation="belongs_to_industry", target="白酒", evidence="公司资料"),
            GraphEdge(source="需求波动", relation="affects_metric", target="收入增速", evidence="动销走弱"),
        ],
        summary="贵州茅台 关系图摘要：已提取 5 条关系。",
    )

    payload = build_hybrid_context(
        store,
        graph_key="600519",
        graph_summary=summary,
        query_text="茅台 风险 传导 催化 同行 行业 指标",
        vector_context="",
        section_query_overrides={
            "risk": "茅台 需求波动 风险 传导 指标 下行",
            "industry": "茅台 五粮液 同行 可比 行业 竞争 格局",
            "valuation": "茅台 估值 DCF 收入增速 催化 修复",
        },
    )

    assert payload["graph_query_focus"] == "风险传导"
    assert payload["graph_focus_coverage"] == 1.0
    assert payload["section_graph_hit_count"] == 3
    assert payload["section_graph_focus_coverage"] == 1.0
    assert "风险传导=命中(causes_risk)" in str(payload["graph_focus_summary"])
    assert "催化因素=命中(triggers_catalyst)" in str(payload["graph_focus_summary"])
    assert "同行对比=命中(compares_with)" in str(payload["graph_focus_summary"])
    assert "风险章节=命中(causes_risk)" in str(payload["section_graph_summary"])
    assert "行业章节=命中(compares_with)" in str(payload["section_graph_summary"])
    assert "估值章节=命中(affects_metric)" in str(payload["section_graph_summary"])
    assert "需求波动 风险 传导 指标 下行" in str(payload["section_graph_query_summary"])
    assert "五粮液 同行 可比 行业 竞争 格局" in str(payload["section_graph_query_summary"])
    assert "风险章节 Graph Context：" in str(payload["section_graph_context_map"]["risk"])
    assert "行业章节 Graph Context：" in str(payload["section_graph_context_map"]["industry"])
    assert "估值章节 Graph Context：" in str(payload["section_graph_context_map"]["valuation"])


def test_build_hybrid_context_exposes_refinement_summary_when_feedback_requests_tighter_queries():
    store = GraphStore()
    summary = GraphSummary(
        edges=[
            GraphEdge(source="贵州茅台", relation="causes_risk", target="需求波动", evidence="渠道反馈"),
            GraphEdge(source="贵州茅台", relation="compares_with", target="五粮液", evidence="份额对比"),
            GraphEdge(source="贵州茅台", relation="affects_metric", target="收入增速", evidence="盈利预测"),
        ],
        summary="贵州茅台 关系图摘要：已提取 3 条关系。",
    )

    payload = build_hybrid_context(
        store,
        graph_key="600519",
        graph_summary=summary,
        query_text="茅台 风险 同行 估值",
        vector_context="",
        section_query_overrides={
            "risk": "茅台 需求波动 风险",
            "industry": "茅台 五粮液 同行",
            "valuation": "茅台 DCF 估值",
        },
        section_query_refinements={
            "risk": "低吸收 风险事件 证据",
            "industry": "低吸收 竞争格局 市占率",
            "valuation": "低吸收 估值锚 目标价",
        },
    )

    assert payload["section_graph_query_refined_count"] == 3
    assert payload["section_graph_refinement_improved_count"] >= 0
    assert "风险章节=低吸收 风险事件 证据" in str(payload["section_graph_query_refinement_summary"])
    assert "行业章节=低吸收 竞争格局 市占率" in str(payload["section_graph_query_refinement_summary"])
    assert "估值章节=低吸收 估值锚 目标价" in str(payload["section_graph_query_refinement_summary"])
    assert "[Refined: 低吸收 风险事件 证据" in str(payload["section_graph_query_summary"])
    assert "风险章节=" in str(payload["section_graph_refinement_comparison_summary"])


def test_build_hybrid_context_exposes_before_after_hit_delta_for_refinement():
    store = GraphStore()
    summary = GraphSummary(
        edges=[
            GraphEdge(source="贵州茅台", relation="causes_risk", target="需求波动", evidence="渠道反馈"),
            GraphEdge(source="需求波动", relation="affects_metric", target="收入增速", evidence="动销走弱"),
        ],
        summary="贵州茅台 关系图摘要：已提取 2 条关系。",
    )

    payload = build_hybrid_context(
        store,
        graph_key="600519",
        graph_summary=summary,
        query_text="茅台 风险",
        vector_context="",
        section_query_overrides={"risk": "茅台 风险"},
        section_query_refinements={"risk": "风险事件 证据 传导路径 指标 下行"},
    )

    assert "风险章节=1->2 (Δ1)" in str(payload["section_graph_refinement_comparison_summary"])
    assert payload["section_graph_refinement_improved_count"] >= 1
