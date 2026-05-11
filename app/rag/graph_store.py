"""轻量 graph store。"""
from __future__ import annotations

import re
from typing import cast

from app.rag.graph_schema import GraphEdge, GraphSummary


_RELATION_QUERY_HINTS = {
    "belongs_to_industry": {"label": "行业归属", "keywords": ("行业", "industry", "产业", "赛道")},
    "compares_with": {"label": "同行对比", "keywords": ("同行", "可比", "对比", "竞争", "peer")},
    "affects_metric": {"label": "指标影响", "keywords": ("指标", "metric", "估值", "利润", "收入", "传导")},
    "causes_risk": {"label": "风险传导", "keywords": ("风险", "risk", "传导", "下行", "波动")},
    "triggers_catalyst": {"label": "催化因素", "keywords": ("催化", "catalyst", "修复", "改善", "增长")},
    "mentions_company": {"label": "来源证据", "keywords": ("公告", "新闻", "来源", "公司", "证据")},
    "supports_thesis": {"label": "论点支撑", "keywords": ("论点", "thesis", "支持", "证据", "结论")},
}


class GraphStore:
    def __init__(self) -> None:
        self._summaries: dict[str, GraphSummary] = {}

    def save_summary(self, key: str, summary: GraphSummary) -> None:
        self._summaries[key] = summary

    def get_summary(self, key: str) -> GraphSummary | None:
        return self._summaries.get(key)

    def query(self, key: str, query_text: str, *, limit: int = 6) -> list[GraphEdge]:
        return [item["edge"] for item in self.query_scored(key, query_text, limit=limit)]

    def query_scored(self, key: str, query_text: str, *, limit: int = 6) -> list[dict[str, int | str | GraphEdge]]:
        summary = self._summaries.get(key)
        if summary is None:
            return []
        query_tokens = _tokenize(query_text)
        if not query_tokens:
            return []
        scored: list[dict[str, int | str | GraphEdge]] = []
        for edge in summary.edges:
            haystack = f"{edge.source} {edge.relation} {edge.target} {edge.evidence}".lower()
            score = 0
            matched_tokens = 0
            for token in query_tokens:
                if token in haystack:
                    matched_tokens += 1
                    score += 2 if len(token) >= 3 else 1
            relation_boost, relation_reason = _relation_intent_score(edge.relation, query_tokens)
            score += relation_boost
            if score > 0:
                scored.append({
                    "edge": edge,
                    "score": score,
                    "matched_tokens": matched_tokens,
                    "reason": relation_reason,
                })
        scored.sort(
            key=lambda item: (
                int(item["score"]),
                int(item["matched_tokens"]),
                len(cast(GraphEdge, item["edge"]).evidence),
            ),
            reverse=True,
        )
        return scored[:limit]


def _tokenize(text: str) -> list[str]:
    raw_tokens = re.split(r"[\s,，。；;：:、/|()\[\]{}]+", text.lower())
    tokens: list[str] = []
    seen: set[str] = set()
    for token in raw_tokens:
        clean = token.strip()
        if len(clean) < 2 or clean in seen:
            continue
        seen.add(clean)
        tokens.append(clean)
    return tokens[:24]


def _relation_intent_score(relation: str, query_tokens: list[str]) -> tuple[int, str]:
    hint = _RELATION_QUERY_HINTS.get(relation)
    if not hint:
        return 0, "文本命中"
    score = 0
    for token in query_tokens:
        if any(token in keyword or keyword in token for keyword in hint["keywords"]):
            score += 3
    if score > 0:
        return score, f"关系意图={hint['label']}"
    return 0, "文本命中"
