"""事件去重与聚合。"""
from __future__ import annotations

import re

from app.tracking.models import MarketEvent


def dedupe_events(events: list[MarketEvent]) -> list[MarketEvent]:
    """按股票、事件类型和标题关键词做轻量去重。"""
    grouped: dict[tuple[str, str, str], MarketEvent] = {}
    ordered: list[MarketEvent] = []
    for event in events:
        key = (event.stock_code, event.event_type, normalize_title(event.title))
        parent = grouped.get(key)
        if parent is None:
            grouped[key] = event
            ordered.append(event)
            continue
        parent.related_sources.extend(event.related_sources)
        parent.summary = parent.summary or event.summary
        parent.impact_level = stronger_level(parent.impact_level, event.impact_level)
        parent.confidence = max(parent.confidence, event.confidence)
        event.is_duplicate = True
        event.parent_event_id = parent.event_id
    return ordered


def normalize_title(title: str) -> str:
    text = re.sub(r"\s+", "", title or "")
    text = re.sub(r"[：:丨|【】\\[\\]（）()《》,，.。]", "", text)
    return text[:28]


def stronger_level(left: str, right: str) -> str:
    order = {"low": 1, "medium": 2, "high": 3}
    return left if order.get(left, 0) >= order.get(right, 0) else right

