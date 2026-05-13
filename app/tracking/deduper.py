"""事件去重与聚合。"""
from __future__ import annotations

from difflib import SequenceMatcher
import re
from urllib.parse import urlsplit, urlunsplit

from app.tracking.models import MarketEvent


def dedupe_events(events: list[MarketEvent]) -> list[MarketEvent]:
    """按 URL、标题和同日标题相似度合并重复事件。"""
    ordered: list[MarketEvent] = []
    for event in events:
        parent = _find_parent(event, ordered)
        if parent is None:
            event.duplicate_count = max(1, int(getattr(event, "duplicate_count", 0) or 1))
            ordered.append(event)
            continue
        merge_duplicate_event(parent, event)
    return ordered


def normalize_title(title: str) -> str:
    text = re.sub(r"\s+", "", title or "")
    text = re.sub(r"[：:丨|【】\\[\\]（）()《》,，.。]", "", text)
    return text[:28]


def merge_duplicate_event(parent: MarketEvent, event: MarketEvent) -> MarketEvent:
    """把重复事件的信息合并到主事件上。"""
    event.is_duplicate = True
    event.parent_event_id = parent.event_id
    parent.duplicate_count = max(1, int(getattr(parent, "duplicate_count", 0) or 1)) + max(1, int(getattr(event, "duplicate_count", 0) or 1))
    fallback_sources = [] if event.related_sources else [_source_from_event(event)]
    parent.related_sources = _unique_sources(parent.related_sources + event.related_sources + fallback_sources)
    if not parent.summary and event.summary:
        parent.summary = event.summary
    if not parent.source and event.source:
        parent.source = event.source
    if not parent.provider and event.provider:
        parent.provider = event.provider
    if not parent.url and event.url:
        parent.url = event.url
    if not parent.published_at and event.published_at:
        parent.published_at = event.published_at
    if not parent.reason and event.reason:
        parent.reason = event.reason
    if parent.sentiment in {"", "neutral", "uncertain"} and event.sentiment not in {"", "neutral", "uncertain"}:
        parent.sentiment = event.sentiment
    if parent.impact_scope in {"", "sentiment"} and event.impact_scope:
        parent.impact_scope = event.impact_scope
    parent.impact_level = stronger_level(parent.impact_level, event.impact_level)
    parent.confidence = max(parent.confidence, event.confidence)
    parent.is_placeholder = parent.is_placeholder and event.is_placeholder
    if parent.retrieval_mode == "placeholder" and event.retrieval_mode:
        parent.retrieval_mode = event.retrieval_mode
    return parent


def stronger_level(left: str, right: str) -> str:
    order = {"low": 1, "medium": 2, "high": 3}
    return left if order.get(left, 0) >= order.get(right, 0) else right


def _find_parent(event: MarketEvent, ordered: list[MarketEvent]) -> MarketEvent | None:
    event_url = normalize_url(event.url)
    event_title = normalize_title(event.title)
    event_date = _event_date(event)
    for parent in ordered:
        if parent.stock_code != event.stock_code or parent.event_type != event.event_type:
            continue
        parent_url = normalize_url(parent.url)
        if event_url and parent_url and event_url == parent_url:
            return parent
        parent_title = normalize_title(parent.title)
        if event_title and parent_title and event_title == parent_title:
            return parent
        if event_date and event_date == _event_date(parent) and _title_similarity(event_title, parent_title) >= 0.82:
            return parent
    return None


def normalize_url(url: str) -> str:
    value = str(url or "").strip()
    if not value:
        return ""
    try:
        parsed = urlsplit(value)
    except ValueError:
        return value.rstrip("/")
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), "", ""))


def _event_date(event: MarketEvent) -> str:
    value = event.published_at or event.collected_at
    return str(value or "")[:10]


def _title_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def _unique_sources(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str, str, str, str]] = set()
    for item in sources:
        if not isinstance(item, dict):
            continue
        payload = {
            "title": str(item.get("title") or ""),
            "source": str(item.get("source") or ""),
            "provider": str(item.get("provider") or ""),
            "url": str(item.get("url") or ""),
            "time": str(item.get("time") or ""),
        }
        key = (payload["title"], payload["source"], payload["provider"], normalize_url(payload["url"]), payload["time"])
        if not any(key) or key in seen:
            continue
        seen.add(key)
        unique.append(payload)
    return unique


def _source_from_event(event: MarketEvent) -> dict[str, str]:
    return {
        "title": event.title,
        "source": event.source,
        "provider": event.provider,
        "url": event.url,
        "time": event.published_at or event.collected_at,
    }
