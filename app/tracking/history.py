"""轻量事件历史存储。"""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR
from app.tracking.deduper import dedupe_events
from app.tracking.models import MarketEvent

VALID_EVENT_STATUSES = {"new", "reviewed", "ignored", "converted_to_report"}


def save_events(events: list[MarketEvent], *, output_dir: Path = OUTPUT_DIR) -> None:
    """按 event_id 和语义重复关系保存事件历史。"""
    if not events:
        return
    current = {event.event_id: event for event in load_events(output_dir=output_dir)}
    for event in events:
        if event.event_id:
            _preserve_existing_status(event, current.get(event.event_id))
            current[event.event_id] = event
    merged = dedupe_events(list(current.values()))
    ordered = sorted(merged, key=lambda item: item.published_at or item.collected_at, reverse=True)
    _save(ordered, output_dir=output_dir)


def load_events(*, output_dir: Path = OUTPUT_DIR) -> list[MarketEvent]:
    path = _history_path(output_dir)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        return []
    return [_event_from_dict(item) for item in items if isinstance(item, dict)]


def query_events(
    *,
    stock_code: str = "",
    provider: str = "",
    event_type: str = "",
    impact_level: str = "",
    start: str = "",
    end: str = "",
    status: str = "",
    limit: int = 100,
    output_dir: Path = OUTPUT_DIR,
) -> list[MarketEvent]:
    events = load_events(output_dir=output_dir)
    filtered = []
    for event in events:
        event_time = event.published_at or event.collected_at
        if stock_code and event.stock_code != stock_code:
            continue
        if provider and provider not in {event.provider, event.source}:
            continue
        if event_type and event.event_type != event_type:
            continue
        if impact_level and event.impact_level != impact_level:
            continue
        if status and status != "all" and event.status != status:
            continue
        if start and event_time and event_time < start:
            continue
        if end and event_time and event_time > end:
            continue
        filtered.append(event)
    return filtered[: max(1, limit)]


def get_event(event_id: str, *, output_dir: Path = OUTPUT_DIR) -> MarketEvent | None:
    for event in load_events(output_dir=output_dir):
        if event.event_id == event_id:
            return event
    return None


def update_event_status(event_id: str, status: str, *, note: str = "", actor: str = "system", output_dir: Path = OUTPUT_DIR) -> MarketEvent | None:
    """更新事件处理状态并持久化。"""
    normalized_status = normalize_event_status(status)
    events = load_events(output_dir=output_dir)
    updated: MarketEvent | None = None
    now = datetime.now().isoformat(timespec="seconds")
    for event in events:
        if event.event_id != event_id:
            continue
        event.status = normalized_status
        event.status_updated_at = now
        event.status_note = note.strip()
        event.status_actor = actor.strip() or "system"
        updated = event
        break
    if updated is None:
        return None
    _save(events, output_dir=output_dir)
    return updated


def normalize_event_status(status: str) -> str:
    normalized = str(status or "").strip()
    if normalized not in VALID_EVENT_STATUSES:
        raise ValueError(f"unsupported event status: {status}")
    return normalized


def _history_path(output_dir: Path) -> Path:
    return output_dir / "tracking_events.json"


def _save(events: list[MarketEvent], *, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"items": [asdict(event) for event in events]}
    _history_path(output_dir).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _event_from_dict(item: dict) -> MarketEvent:
    return MarketEvent(
        event_id=str(item.get("event_id", "")),
        stock_code=str(item.get("stock_code", "")),
        stock_name=str(item.get("stock_name", "")),
        title=str(item.get("title", "")),
        summary=str(item.get("summary", "")),
        source=str(item.get("source", "")),
        provider=str(item.get("provider", "")),
        url=str(item.get("url", "")),
        published_at=str(item.get("published_at", "")),
        collected_at=str(item.get("collected_at", "")),
        event_type=str(item.get("event_type", "other")),
        sentiment=str(item.get("sentiment", "neutral")),
        impact_level=str(item.get("impact_level", "low")),
        impact_scope=str(item.get("impact_scope", "sentiment")),
        confidence=float(item.get("confidence", 0.5) or 0.5),
        reason=str(item.get("reason", "")),
        channel=str(item.get("channel", "")),
        retrieval_mode=str(item.get("retrieval_mode", "")),
        evidence_type=str(item.get("evidence_type", "")),
        is_placeholder=bool(item.get("is_placeholder", False)),
        related_sources=list(item.get("related_sources", []) or []),
        is_duplicate=bool(item.get("is_duplicate", False)),
        parent_event_id=str(item.get("parent_event_id", "")),
        duplicate_count=int(item.get("duplicate_count", 0) or 0),
        status=str(item.get("status", "new") or "new"),
        status_updated_at=str(item.get("status_updated_at", "")),
        status_note=str(item.get("status_note", "")),
        status_actor=str(item.get("status_actor", "")),
    )


def _preserve_existing_status(event: MarketEvent, existing: MarketEvent | None) -> None:
    if existing is None or existing.status == "new":
        return
    if event.status != "new":
        return
    event.status = existing.status
    event.status_updated_at = existing.status_updated_at
    event.status_note = existing.status_note
    event.status_actor = existing.status_actor
