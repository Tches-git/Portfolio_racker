"""graph + vector 的轻量混合检索。"""
from __future__ import annotations

from app.rag.graph_schema import GraphSummary
from app.rag.graph_store import GraphStore


_GRAPH_FOCUS_QUERIES = {
    "风险传导": "风险 传导 下行 波动",
    "催化因素": "催化 修复 改善 增长",
    "同行对比": "同行 可比 竞争 对比",
    "行业归属": "行业 赛道 产业",
    "指标影响": "指标 估值 利润 收入",
}

_SECTION_GRAPH_QUERIES = {
    "risk": {"label": "风险章节", "query": "风险 传导 下行 波动 指标"},
    "industry": {"label": "行业章节", "query": "同行 可比 行业 竞争 格局"},
    "valuation": {"label": "估值章节", "query": "估值 指标 催化 修复 利润 收入"},
}

_SECTION_GRAPH_REFINEMENT_HINTS = {
    "risk": "风险事件 证据 传导路径 经营 财务 指标 下行",
    "industry": "同行 可比 竞争格局 市占率 龙头 份额",
    "valuation": "估值锚 DCF 目标价 上涨空间 催化 修复 利润 收入",
}


def build_hybrid_context(
    graph_store: GraphStore,
    *,
    graph_key: str,
    graph_summary: GraphSummary,
    query_text: str,
    vector_context: str,
    section_query_overrides: dict[str, str] | None = None,
    section_query_refinements: dict[str, str] | None = None,
) -> dict[str, str | int | float]:
    graph_store.save_summary(graph_key, graph_summary)
    scored_hits = graph_store.query_scored(graph_key, query_text, limit=6)
    graph_edges = [item["edge"] for item in scored_hits]
    query_focus = _infer_query_focus(query_text)
    focus_hits = _build_focus_hits(graph_store, graph_key, base_query_text=query_text)
    focus_coverage = round(sum(1 for hits in focus_hits.values() if hits) / len(_GRAPH_FOCUS_QUERIES), 4)
    graph_context = graph_summary.summary
    if graph_edges:
        lines = [graph_summary.summary, "", f"Query Focus：{query_focus}", "图关系命中："]
        for item in scored_hits:
            edge = item["edge"]
            evidence = f" | 证据 {edge.evidence}" if edge.evidence else ""
            reason = f" | 命中原因 {item['reason']}" if item.get("reason") else ""
            lines.append(f"- {edge.source} --{edge.relation}--> {edge.target}{evidence}{reason}")
        graph_context = "\n".join(lines)
    elif graph_context:
        graph_context = f"{graph_context}\n\nQuery Focus：{query_focus}"
    graph_context = _append_multi_focus_summary(graph_context, focus_hits)
    hybrid_text = vector_context.strip()
    if graph_context:
        hybrid_text = f"{graph_context}\n\n---\n\n{vector_context}".strip()
    graph_hit_count = len(graph_edges)
    available_channels = int(bool(graph_summary.edges)) + int(bool(vector_context.strip()))
    hit_channels = int(bool(graph_edges)) + int(bool(vector_context.strip()))
    hit_rate = round(hit_channels / available_channels, 4) if available_channels else 0.0
    section_queries = _build_section_queries(
        query_text,
        section_query_overrides=section_query_overrides,
        section_query_refinements=section_query_refinements,
    )
    section_hits = _build_section_hits(graph_store, graph_key, section_queries=section_queries)
    section_refinement_map = _build_section_refinement_map(section_query_refinements)
    section_refinement_comparison = _build_section_refinement_comparison(
        graph_store,
        graph_key,
        base_query_text=query_text,
        section_query_overrides=section_query_overrides,
        section_refinement_map=section_refinement_map,
        refined_hits=section_hits,
    )
    return {
        "graph_context": graph_context,
        "hybrid_context": hybrid_text,
        "graph_hit_count": graph_hit_count,
        "hybrid_retrieval_hit_rate": hit_rate,
        "graph_query_focus": query_focus,
        "graph_focus_coverage": focus_coverage,
        "graph_focus_summary": _format_focus_summary(focus_hits),
        "section_graph_hit_count": sum(1 for hits in section_hits.values() if hits),
        "section_graph_focus_coverage": round(sum(1 for hits in section_hits.values() if hits) / len(_SECTION_GRAPH_QUERIES), 4),
        "section_graph_summary": _format_section_summary(section_hits),
        "section_graph_context": _format_section_context(section_hits),
        "section_graph_context_map": _format_section_context_map(section_hits),
        "section_graph_query_summary": _format_section_query_summary(section_queries, section_refinement_map=section_refinement_map),
        "section_graph_query_map": section_queries,
        "section_graph_query_refinement_summary": _format_section_refinement_summary(section_refinement_map),
        "section_graph_query_refinement_map": section_refinement_map,
        "section_graph_query_refined_count": sum(1 for item in section_refinement_map.values() if item),
        "section_graph_refinement_comparison_summary": _format_section_refinement_comparison_summary(section_refinement_comparison),
        "section_graph_refinement_improved_count": sum(1 for item in section_refinement_comparison.values() if item.get("improved")),
        "section_graph_refinement_comparison_map": section_refinement_comparison,
    }


def _infer_query_focus(query_text: str) -> str:
    lowered = query_text.lower()
    if any(token in lowered for token in ("风险", "传导", "risk")):
        return "风险传导"
    if any(token in lowered for token in ("催化", "修复", "catalyst")):
        return "催化因素"
    if any(token in lowered for token in ("同行", "可比", "peer", "竞争")):
        return "同行对比"
    if any(token in lowered for token in ("行业", "industry", "赛道")):
        return "行业归属"
    if any(token in lowered for token in ("估值", "利润", "收入", "指标", "metric")):
        return "指标影响"
    return "通用关系"


def _build_focus_hits(graph_store: GraphStore, graph_key: str, *, base_query_text: str) -> dict[str, list[dict[str, int | str | object]]]:
    focus_hits: dict[str, list[dict[str, int | str | object]]] = {}
    for focus, hint_query in _GRAPH_FOCUS_QUERIES.items():
        merged_query = f"{base_query_text} {hint_query}".strip()
        focus_hits[focus] = graph_store.query_scored(graph_key, merged_query, limit=2)
    return focus_hits


def _append_multi_focus_summary(graph_context: str, focus_hits: dict[str, list[dict[str, int | str | object]]]) -> str:
    lines = [graph_context, "", "多焦点关系摘要："]
    for focus, hits in focus_hits.items():
        if not hits:
            lines.append(f"- {focus}：未命中")
            continue
        top_edge = hits[0]["edge"]
        lines.append(f"- {focus}：{top_edge.source} --{top_edge.relation}--> {top_edge.target}")
    return "\n".join(lines).strip()


def _build_section_queries(
    base_query_text: str,
    *,
    section_query_overrides: dict[str, str] | None = None,
    section_query_refinements: dict[str, str] | None = None,
) -> dict[str, str]:
    section_queries: dict[str, str] = {}
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        override = (section_query_overrides or {}).get(section_id, "").strip()
        refinement = _normalize_refinement(section_id, (section_query_refinements or {}).get(section_id, ""))
        merged_query = f"{base_query_text} {override or meta['query']} {refinement}".strip()
        section_queries[section_id] = merged_query
    return section_queries


def _build_section_hits(graph_store: GraphStore, graph_key: str, *, section_queries: dict[str, str]) -> dict[str, list[dict[str, int | str | object]]]:
    section_hits: dict[str, list[dict[str, int | str | object]]] = {}
    for section_id, query in section_queries.items():
        section_hits[section_id] = graph_store.query_scored(graph_key, query, limit=2)
    return section_hits


def _format_focus_summary(focus_hits: dict[str, list[dict[str, int | str | object]]]) -> str:
    parts: list[str] = []
    for focus, hits in focus_hits.items():
        if hits:
            edge = hits[0]["edge"]
            parts.append(f"{focus}=命中({edge.relation})")
        else:
            parts.append(f"{focus}=未命中")
    return "；".join(parts)


def _format_section_summary(section_hits: dict[str, list[dict[str, int | str | object]]]) -> str:
    parts: list[str] = []
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        hits = section_hits.get(section_id, [])
        if hits:
            edge = hits[0]["edge"]
            parts.append(f"{meta['label']}=命中({edge.relation})")
        else:
            parts.append(f"{meta['label']}=未命中")
    return "；".join(parts)


def _format_section_context(section_hits: dict[str, list[dict[str, int | str | object]]]) -> str:
    lines = ["章节定向关系摘要："]
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        hits = section_hits.get(section_id, [])
        if not hits:
            lines.append(f"- {meta['label']}：未命中")
            continue
        top_edge = hits[0]["edge"]
        lines.append(f"- {meta['label']}：{top_edge.source} --{top_edge.relation}--> {top_edge.target}")
    return "\n".join(lines)


def _format_section_context_map(section_hits: dict[str, list[dict[str, int | str | object]]]) -> dict[str, str]:
    payload: dict[str, str] = {}
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        hits = section_hits.get(section_id, [])
        lines = [f"{meta['label']} Graph Context："]
        if not hits:
            lines.append("- 未命中")
            payload[section_id] = "\n".join(lines)
            continue
        for item in hits:
            edge = item["edge"]
            evidence = f" | 证据 {edge.evidence}" if getattr(edge, "evidence", "") else ""
            lines.append(f"- {edge.source} --{edge.relation}--> {edge.target}{evidence}")
        payload[section_id] = "\n".join(lines)
    return payload


def _normalize_refinement(section_id: str, refinement: str) -> str:
    base = refinement.strip()
    fallback = _SECTION_GRAPH_REFINEMENT_HINTS.get(section_id, "")
    if not base:
        return ""
    if fallback and fallback not in base:
        return f"{base} {fallback}".strip()
    return base


def _build_section_refinement_map(section_query_refinements: dict[str, str] | None) -> dict[str, str]:
    payload: dict[str, str] = {}
    for section_id in _SECTION_GRAPH_QUERIES:
        payload[section_id] = _normalize_refinement(section_id, (section_query_refinements or {}).get(section_id, ""))
    return payload


def _format_section_query_summary(section_queries: dict[str, str], *, section_refinement_map: dict[str, str] | None = None) -> str:
    parts: list[str] = []
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        refinement = (section_refinement_map or {}).get(section_id, "")
        if refinement:
            parts.append(f"{meta['label']}={section_queries.get(section_id, '')} [Refined: {refinement}]")
        else:
            parts.append(f"{meta['label']}={section_queries.get(section_id, '')}")
    return "；".join(parts)


def _build_section_refinement_comparison(
    graph_store: GraphStore,
    graph_key: str,
    *,
    base_query_text: str,
    section_query_overrides: dict[str, str] | None,
    section_refinement_map: dict[str, str],
    refined_hits: dict[str, list[dict[str, int | str | object]]],
) -> dict[str, dict[str, str | int | bool]]:
    baseline_queries = _build_section_queries(base_query_text, section_query_overrides=section_query_overrides)
    baseline_hits = _build_section_hits(graph_store, graph_key, section_queries=baseline_queries)
    comparison: dict[str, dict[str, str | int | bool]] = {}
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        baseline_count = len(baseline_hits.get(section_id, []))
        refined_count = len(refined_hits.get(section_id, []))
        refinement = section_refinement_map.get(section_id, "")
        improved = bool(refinement) and refined_count > baseline_count
        comparison[section_id] = {
            "label": meta["label"],
            "baseline_hit_count": baseline_count,
            "refined_hit_count": refined_count,
            "delta": refined_count - baseline_count,
            "improved": improved,
        }
    return comparison


def _format_section_refinement_summary(section_refinement_map: dict[str, str]) -> str:
    parts: list[str] = []
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        refinement = section_refinement_map.get(section_id, "")
        parts.append(f"{meta['label']}={refinement or '未触发'}")
    return "；".join(parts)


def _format_section_refinement_comparison_summary(section_refinement_comparison: dict[str, dict[str, str | int | bool]]) -> str:
    parts: list[str] = []
    for section_id, meta in _SECTION_GRAPH_QUERIES.items():
        item = section_refinement_comparison.get(section_id, {})
        baseline = item.get("baseline_hit_count", 0)
        refined = item.get("refined_hit_count", 0)
        delta = item.get("delta", 0)
        parts.append(f"{meta['label']}={baseline}->{refined} (Δ{delta})")
    return "；".join(parts)
