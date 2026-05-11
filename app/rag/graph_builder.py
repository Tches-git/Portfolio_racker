"""轻量 graph 摘要构建。"""
from __future__ import annotations

import re

from app.models import AnalysisState
from app.rag.graph_schema import GraphEdge, GraphNode, GraphSummary


def _analysis_value(state: AnalysisState, key: str, default: str = "") -> str:
    return str((getattr(state, "analysis_payload", {}) or {}).get(key, state.sections.get(key, default)) or default)


def build_graph_summary(state: AnalysisState) -> GraphSummary:
    stock_label = state.stock_name or state.stock_code or "目标公司"
    if not stock_label:
        return GraphSummary()

    nodes: dict[str, GraphNode] = {}
    edges: list[GraphEdge] = []

    def add_node(node_id: str, node_type: str, label: str) -> None:
        if node_id not in nodes:
            nodes[node_id] = GraphNode(node_id=node_id, node_type=node_type, label=label)

    def add_edge(source: str, relation: str, target: str, evidence: str = "") -> None:
        edges.append(GraphEdge(source=source, relation=relation, target=target, evidence=evidence[:120]))

    company_id = f"company:{state.stock_code or stock_label}"
    add_node(company_id, "Company", stock_label)

    if state.profile and state.profile.industry:
        industry_id = f"industry:{state.profile.industry}"
        add_node(industry_id, "Industry", state.profile.industry)
        add_edge(stock_label, "belongs_to_industry", state.profile.industry)

    for peer in state.peers[:3]:
        add_node(f"peer:{peer.code}", "Peer", peer.name)
        add_edge(stock_label, "compares_with", peer.name, evidence=f"PE {peer.pe_ratio:.1f} | ROE {peer.roe:.1f}%")

    for risk in state.risks[:4]:
        risk_label = risk.description[:40]
        add_node(f"risk:{risk_label}", "Risk", risk_label)
        add_edge(stock_label, "causes_risk", risk_label, evidence=risk.evidence or risk.source or "")
        if risk.impact:
            metric_label = risk.impact[:30]
            add_node(f"metric:{metric_label}", "Metric", metric_label)
            add_edge(risk_label, "affects_metric", metric_label, evidence=risk.transmission_path or "")

    conclusion = _analysis_value(state, "research_conclusion", "")
    for snippet in _extract_catalyst_snippets(conclusion):
        add_node(f"catalyst:{snippet}", "Catalyst", snippet)
        add_edge(stock_label, "triggers_catalyst", snippet)
    for ref in getattr(state, "source_refs", [])[:4]:
        title = ref.get("title", "")
        if not title:
            continue
        add_node(f"source:{title}", "News", title[:40])
        add_edge(title[:40], "mentions_company", stock_label, evidence=ref.get("source", ""))
        if conclusion:
            add_edge(title[:40], "supports_thesis", (conclusion[:40] + "...") if len(conclusion) > 40 else conclusion, evidence=ref.get("summary", ""))

    graph_hit_count = len(edges)
    relationship_coverage = round(min(graph_hit_count, 8) / 8, 4) if graph_hit_count else 0.0
    risk_path_edges = [edge for edge in edges if edge.relation in {"causes_risk", "affects_metric"}]
    risk_path_completeness = round(min(len(risk_path_edges), 6) / 6, 4) if risk_path_edges else 0.0
    summary = _build_summary_text(stock_label, edges)
    return GraphSummary(
        nodes=list(nodes.values()),
        edges=edges,
        summary=summary,
        graph_hit_count=graph_hit_count,
        relationship_coverage=relationship_coverage,
        risk_path_completeness=risk_path_completeness,
        query_focus="通用关系",
    )


def _extract_catalyst_snippets(text: str) -> list[str]:
    snippets: list[str] = []
    for chunk in re.split(r"[。；\n]", text):
        clean = chunk.strip()
        if clean and any(keyword in clean for keyword in ("催化", "修复", "增长", "扩张", "改善")):
            snippets.append(clean[:40])
    return snippets[:3]


def _build_summary_text(stock_label: str, edges: list[GraphEdge]) -> str:
    if not edges:
        return "暂无关系图摘要"
    relation_counts: dict[str, int] = {}
    for edge in edges:
        relation_counts[edge.relation] = relation_counts.get(edge.relation, 0) + 1
    ordered = sorted(relation_counts.items(), key=lambda item: (-item[1], item[0]))
    top_relations = "；".join(f"{relation}×{count}" for relation, count in ordered[:4])
    return f"{stock_label} 关系图摘要：已提取 {len(edges)} 条关系，主要包括 {top_relations}。"
