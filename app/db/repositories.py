"""Repository helpers bridging ORM records and existing dataclasses."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.db.models import AnalysisRunRecord, ExportArtifactRecord, MarketEventRecord, WatchlistRecord, WatchlistStockRecord
from app.tracking.deduper import dedupe_events
from app.tracking.models import EventCollection, MarketEvent, Watchlist
from app.tracking.service import summarize_events
from app.tracking.watchlist import normalize_stock_codes

VALID_EVENT_STATUSES = {"new", "reviewed", "ignored", "converted_to_report"}


def list_user_watchlists(db: Session, *, user_id: str) -> list[Watchlist]:
    records = list(db.scalars(
        select(WatchlistRecord)
        .where(WatchlistRecord.user_id == user_id)
        .options(selectinload(WatchlistRecord.stocks))
        .order_by(WatchlistRecord.updated_at.desc())
    ))
    return [_watchlist_from_record(record) for record in records]


def get_user_watchlist(db: Session, *, user_id: str, watchlist_id: str) -> Watchlist | None:
    record = db.scalar(
        select(WatchlistRecord)
        .where(WatchlistRecord.user_id == user_id, WatchlistRecord.id == watchlist_id)
        .options(selectinload(WatchlistRecord.stocks))
    )
    return _watchlist_from_record(record) if record else None


def create_user_watchlist(db: Session, *, user_id: str, name: str, stock_codes: list[str], description: str = "") -> Watchlist:
    codes = normalize_stock_codes(stock_codes)
    now = datetime.utcnow()
    record = WatchlistRecord(user_id=user_id, name=name.strip() or "未命名组合", description=description.strip(), updated_at=now)
    record.stocks = [
        WatchlistStockRecord(stock_code=code, position=index)
        for index, code in enumerate(codes)
    ]
    db.add(record)
    db.commit()
    db.refresh(record)
    record = db.scalar(select(WatchlistRecord).where(WatchlistRecord.id == record.id).options(selectinload(WatchlistRecord.stocks))) or record
    return _watchlist_from_record(record)


def update_user_watchlist(
    db: Session,
    *,
    user_id: str,
    watchlist_id: str,
    name: str | None = None,
    stock_codes: list[str] | None = None,
    description: str | None = None,
) -> Watchlist | None:
    record = db.scalar(
        select(WatchlistRecord)
        .where(WatchlistRecord.user_id == user_id, WatchlistRecord.id == watchlist_id)
        .options(selectinload(WatchlistRecord.stocks))
    )
    if record is None:
        return None
    now = datetime.utcnow()
    if name is not None:
        record.name = name.strip() or "未命名组合"
    if description is not None:
        record.description = description.strip()
    if stock_codes is not None:
        codes = normalize_stock_codes(stock_codes)
        record.stocks = [
            WatchlistStockRecord(stock_code=code, position=index)
            for index, code in enumerate(codes)
        ]
    record.updated_at = now
    db.commit()
    db.refresh(record)
    record = db.scalar(select(WatchlistRecord).where(WatchlistRecord.id == record.id).options(selectinload(WatchlistRecord.stocks))) or record
    return _watchlist_from_record(record)


def delete_user_watchlist(db: Session, *, user_id: str, watchlist_id: str) -> bool:
    record = db.scalar(select(WatchlistRecord).where(WatchlistRecord.user_id == user_id, WatchlistRecord.id == watchlist_id))
    if record is None:
        return False
    db.delete(record)
    db.commit()
    return True


def mark_user_watchlist_refreshed(db: Session, *, user_id: str, watchlist_id: str) -> Watchlist | None:
    record = db.scalar(
        select(WatchlistRecord)
        .where(WatchlistRecord.user_id == user_id, WatchlistRecord.id == watchlist_id)
        .options(selectinload(WatchlistRecord.stocks))
    )
    if record is None:
        return None
    now = datetime.utcnow()
    record.updated_at = now
    record.last_refreshed_at = now
    db.commit()
    db.refresh(record)
    return _watchlist_from_record(record)


def save_user_events(db: Session, *, user_id: str, events: list[MarketEvent]) -> None:
    existing = list_user_events(db, user_id=user_id, limit=10000).items
    existing_event_ids = {event.event_id for event in existing}
    merged = dedupe_events([*existing, *events])
    stale_event_ids = existing_event_ids - {event.event_id for event in merged}
    try:
        _persist_user_events(db, user_id=user_id, events=merged, stale_event_ids=stale_event_ids)
        db.commit()
    except IntegrityError:
        db.rollback()
        _persist_user_events(db, user_id=user_id, events=merged, stale_event_ids=stale_event_ids)
        db.commit()


def _persist_user_events(db: Session, *, user_id: str, events: list[MarketEvent], stale_event_ids: set[str]) -> None:
    merged = dedupe_events(events)
    merged_by_id = {event.event_id: event for event in merged}
    existing_records = {
        record.event_id: record
        for record in db.scalars(select(MarketEventRecord).where(MarketEventRecord.user_id == user_id))
    }
    for event_id, event in merged_by_id.items():
        record = existing_records.get(event_id)
        if record is None:
            db.add(_event_record_from_dataclass(event, user_id=user_id))
            continue
        _apply_event_to_record(record, event, preserve_status=True)
    for event_id, record in existing_records.items():
        if event_id in stale_event_ids:
            db.delete(record)


def list_user_events(
    db: Session,
    *,
    user_id: str,
    stock_codes: list[str] | None = None,
    provider: str = "",
    event_type: str = "",
    impact_level: str = "",
    status: str = "",
    start: str = "",
    end: str = "",
    limit: int = 120,
) -> EventCollection:
    stmt = select(MarketEventRecord).where(MarketEventRecord.user_id == user_id)
    if stock_codes:
        stmt = stmt.where(MarketEventRecord.stock_code.in_(stock_codes))
    if provider:
        stmt = stmt.where(MarketEventRecord.provider == provider)
    if event_type:
        stmt = stmt.where(MarketEventRecord.event_type == event_type)
    if impact_level:
        stmt = stmt.where(MarketEventRecord.impact_level == impact_level)
    if status and status != "all":
        stmt = stmt.where(MarketEventRecord.status == status)
    if start:
        stmt = stmt.where(MarketEventRecord.published_at >= start)
    if end:
        stmt = stmt.where(MarketEventRecord.published_at <= end)
    records = db.scalars(stmt.order_by(MarketEventRecord.published_at.desc(), MarketEventRecord.created_at.desc()).limit(max(1, min(limit, 1000))))
    return summarize_events([_event_from_record(record) for record in records])


def get_user_event(db: Session, *, user_id: str, event_id: str) -> MarketEvent | None:
    record = db.scalar(select(MarketEventRecord).where(MarketEventRecord.user_id == user_id, MarketEventRecord.event_id == event_id))
    return _event_from_record(record) if record else None


def update_user_event_status(db: Session, *, user_id: str, event_id: str, status: str, note: str = "", actor: str = "system") -> MarketEvent | None:
    if status not in VALID_EVENT_STATUSES:
        raise ValueError(f"不支持的事件状态: {status}")
    record = db.scalar(select(MarketEventRecord).where(MarketEventRecord.user_id == user_id, MarketEventRecord.event_id == event_id))
    if record is None:
        return None
    record.status = status
    record.status_note = note
    record.status_actor = actor
    record.status_updated_at = datetime.utcnow().isoformat(timespec="seconds")
    db.commit()
    db.refresh(record)
    return _event_from_record(record)


def save_user_run(db: Session, *, user_id: str, run) -> None:
    record = db.scalar(
        select(AnalysisRunRecord).where(
            AnalysisRunRecord.user_id == user_id,
            AnalysisRunRecord.run_id == run.run_id,
        )
    )
    if record is None:
        record = AnalysisRunRecord(user_id=user_id, run_id=run.run_id, stock_code=run.stock_code)
        db.add(record)
    _apply_run_to_record(record, run)
    _save_user_run_exports(db, user_id=user_id, run=run)
    db.commit()


def user_has_export(db: Session, *, user_id: str, filename: str) -> bool:
    return db.scalar(
        select(ExportArtifactRecord.id).where(
            ExportArtifactRecord.user_id == user_id,
            ExportArtifactRecord.filename == filename,
        )
    ) is not None


def get_user_export_artifact(db: Session, *, user_id: str, filename: str) -> ExportArtifactRecord | None:
    return db.scalar(
        select(ExportArtifactRecord).where(
            ExportArtifactRecord.user_id == user_id,
            ExportArtifactRecord.filename == filename,
        )
    )


def _apply_run_to_record(record: AnalysisRunRecord, run) -> None:
    defaults = {"multi_agent_trace": {}}
    for field in [
        "stock_code", "status", "created_at", "updated_at", "detail", "last_event", "error",
        "owner", "owner_role", "archived", "retry_of_run_id", "canceled", "latest_report_url",
        "history_url", "recovery_status", "stale_after_restart", "attempts", "max_attempts",
        "priority", "worker_id", "locked_at", "next_retry_at", "run_metrics", "multi_agent_trace", "event_context",
        "event_report_summary", "exports", "events", "audit_events",
    ]:
        value = getattr(run, field, defaults[field]) if field in defaults else getattr(run, field)
        setattr(record, field, value)


def _save_user_run_exports(db: Session, *, user_id: str, run) -> None:
    for export in list(getattr(run, "exports", []) or []):
        if not isinstance(export, dict):
            continue
        filename = str(export.get("filename") or "").strip()
        if not filename:
            continue
        artifact = db.scalar(
            select(ExportArtifactRecord).where(
                ExportArtifactRecord.user_id == user_id,
                ExportArtifactRecord.filename == filename,
            )
        )
        if artifact is None:
            artifact = ExportArtifactRecord(user_id=user_id, filename=filename)
            db.add(artifact)
        artifact.run_id = run.run_id
        artifact.stock_code = run.stock_code
        artifact.kind = str(export.get("kind") or "")
        artifact.path = str(export.get("path") or "")
        artifact.download_url = str(export.get("download_url") or f"/api/v1/exports/{filename}")


def _watchlist_from_record(record: WatchlistRecord) -> Watchlist:
    stock_codes = [stock.stock_code for stock in sorted(record.stocks, key=lambda item: item.position)]
    return Watchlist(
        watchlist_id=record.id,
        name=record.name,
        stock_codes=stock_codes,
        description=record.description,
        created_at=_iso(record.created_at),
        updated_at=_iso(record.updated_at),
        last_refreshed_at=_iso(record.last_refreshed_at),
    )


def _event_record_from_dataclass(event: MarketEvent, *, user_id: str) -> MarketEventRecord:
    record = MarketEventRecord(user_id=user_id, event_id=event.event_id, stock_code=event.stock_code)
    _apply_event_to_record(record, event, preserve_status=False)
    return record


def _apply_event_to_record(record: MarketEventRecord, event: MarketEvent, *, preserve_status: bool) -> None:
    original_status = record.status
    original_note = record.status_note
    original_actor = record.status_actor
    original_updated_at = record.status_updated_at
    for field in [
        "stock_code", "stock_name", "title", "summary", "source", "provider", "url", "published_at",
        "collected_at", "event_type", "sentiment", "impact_level", "impact_scope", "confidence",
        "reason", "channel", "retrieval_mode", "evidence_type", "is_placeholder", "related_sources",
        "is_duplicate", "parent_event_id", "status", "status_updated_at", "status_note", "status_actor",
    ]:
        setattr(record, field, getattr(event, field))
    if preserve_status and original_status != "new":
        record.status = original_status
        record.status_note = original_note
        record.status_actor = original_actor
        record.status_updated_at = original_updated_at
    record.duplicate_count = int(getattr(event, "duplicate_count", 0) or 0)


def _event_from_record(record: MarketEventRecord) -> MarketEvent:
    return MarketEvent(
        event_id=record.event_id,
        stock_code=record.stock_code,
        stock_name=record.stock_name,
        title=record.title,
        summary=record.summary,
        source=record.source,
        provider=record.provider,
        url=record.url,
        published_at=record.published_at,
        collected_at=record.collected_at,
        event_type=record.event_type,
        sentiment=record.sentiment,
        impact_level=record.impact_level,
        impact_scope=record.impact_scope,
        confidence=record.confidence,
        reason=record.reason,
        channel=record.channel,
        retrieval_mode=record.retrieval_mode,
        evidence_type=record.evidence_type,
        is_placeholder=record.is_placeholder,
        related_sources=list(record.related_sources or []),
        is_duplicate=record.is_duplicate,
        parent_event_id=record.parent_event_id,
        duplicate_count=record.duplicate_count,
        status=record.status,
        status_updated_at=record.status_updated_at,
        status_note=record.status_note,
        status_actor=record.status_actor,
    )


def _iso(value: object) -> str:
    return value.isoformat(timespec="seconds") if hasattr(value, "isoformat") else ""
