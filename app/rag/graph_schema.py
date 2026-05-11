"""轻量关系图数据结构。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GraphNode:
    node_id: str
    node_type: str
    label: str


@dataclass
class GraphEdge:
    source: str
    relation: str
    target: str
    evidence: str = ""


@dataclass
class GraphSummary:
    nodes: list[GraphNode] = field(default_factory=list)
    edges: list[GraphEdge] = field(default_factory=list)
    summary: str = "暂无关系图摘要"
    graph_hit_count: int = 0
    relationship_coverage: float = 0.0
    risk_path_completeness: float = 0.0
    hybrid_retrieval_hit_rate: float = 0.0
    query_focus: str = "通用关系"

    def to_prompt_text(self) -> str:
        if not self.edges:
            return self.summary
        lines = [self.summary, "", "关系边摘要："]
        for edge in self.edges[:8]:
            evidence = f" | 证据 {edge.evidence}" if edge.evidence else ""
            lines.append(f"- {edge.source} --{edge.relation}--> {edge.target}{evidence}")
        return "\n".join(lines)
