"""事件流服务。"""
from __future__ import annotations

from app.data_source.live_tools import fetch_announcements, fetch_broker_reports, fetch_exchange_filings, fetch_live_quotes
from app.memory.store import get_memory_store
from app.tracking.deduper import dedupe_events
from app.tracking.history import get_event, query_events, save_events
from app.tracking.models import EventCollection, MarketEvent
from app.tracking.normalizer import normalize_source_item


DEFAULT_TRACKING_STOCKS = ["600519", "000858", "300750", "600036"]


def collect_stock_events(stock_code: str, *, stock_name: str = "", limit: int = 6, include_history: bool = False) -> EventCollection:
    """实时采集单只股票的追踪事件。"""
    raw_items: list[dict] = []
    quote = _safe_call(lambda: fetch_live_quotes(stock_code), default={})
    if quote:
        raw_items.append(quote)
        stock_name = stock_name or str(quote.get("title", "")).replace(" 实时行情快照", "")
    raw_items.extend(_safe_call(lambda: fetch_announcements(stock_code, stock_name, limit=limit), default=[]))
    raw_items.extend(_safe_call(lambda: fetch_exchange_filings(stock_code, stock_name, limit=max(2, limit // 2)), default=[]))
    raw_items.extend(_safe_call(lambda: fetch_broker_reports(stock_code, stock_name, limit=max(2, limit // 2)), default=[]))
    live_events = [
        normalize_source_item(item, stock_code=stock_code, stock_name=stock_name)
        for item in raw_items
        if item
    ]
    events = dedupe_events(live_events)
    save_events(events)
    if not include_history:
        return summarize_events(events)
    historical = query_events(stock_code=stock_code, limit=max(limit * 2, 12))
    combined = sorted(dedupe_events(events + historical), key=lambda item: item.published_at or item.collected_at, reverse=True)
    return summarize_events(combined[: max(1, limit)])


def collect_market_events(*, stock_codes: list[str] | None = None, limit_per_stock: int = 4) -> EventCollection:
    """采集全局事件流。"""
    codes = stock_codes or _tracked_stock_codes()
    events: list[MarketEvent] = []
    for code in codes:
        collection = collect_stock_events(code, limit=limit_per_stock)
        events.extend(collection.items)
    events = sorted(events, key=lambda item: item.published_at or item.collected_at, reverse=True)
    return summarize_events(dedupe_events(events))


def collect_historical_events(
    *,
    stock_codes: list[str] | None = None,
    provider: str = "",
    event_type: str = "",
    impact_level: str = "",
    status: str = "",
    start: str = "",
    end: str = "",
    limit: int = 100,
) -> EventCollection:
    """查询已沉淀事件历史。"""
    if stock_codes:
        events: list[MarketEvent] = []
        per_stock_limit = max(1, limit)
        for code in stock_codes:
            events.extend(query_events(
                stock_code=code,
                provider=provider,
                event_type=event_type,
                impact_level=impact_level,
                status=status,
                start=start,
                end=end,
                limit=per_stock_limit,
            ))
    else:
        events = query_events(
            provider=provider,
            event_type=event_type,
            impact_level=impact_level,
            status=status,
            start=start,
            end=end,
            limit=limit,
        )
    events = sorted(dedupe_events(events), key=lambda item: item.published_at or item.collected_at, reverse=True)
    return summarize_events(events[: max(1, limit)])


def find_market_event(event_id: str, *, stock_codes: list[str] | None = None, limit_per_stock: int = 8) -> MarketEvent | None:
    """先查历史，未命中再用实时事件集合兜底。"""
    event = get_event(event_id)
    if event:
        return event
    collection = collect_market_events(stock_codes=stock_codes, limit_per_stock=limit_per_stock)
    for item in collection.items:
        if item.event_id == event_id:
            return item
    return None


def collect_tracking_universe(*, stock_codes: list[str] | None = None, limit_per_stock: int = 4) -> EventCollection:
    """供预警和简报复用的追踪范围。"""
    return collect_market_events(stock_codes=stock_codes, limit_per_stock=limit_per_stock)


def summarize_events(events: list[MarketEvent]) -> EventCollection:
    sources = {event.provider or event.source for event in events if event.provider or event.source}
    return EventCollection(
        items=events,
        total=len(events),
        high_impact_count=sum(1 for event in events if event.impact_level == "high"),
        placeholder_count=sum(1 for event in events if event.is_placeholder),
        duplicate_count=sum(max(0, len(event.related_sources) - 1) for event in events),
        source_count=len(sources),
    )


def _tracked_stock_codes() -> list[str]:
    try:
        stocks = get_memory_store().get_all_stocks()
    except Exception:
        return list(DEFAULT_TRACKING_STOCKS)
    codes = [str(item.get("code") or "").strip() for item in stocks if str(item.get("code") or "").strip()]
    return codes[:8] or list(DEFAULT_TRACKING_STOCKS)


def _safe_call(fn, *, default):
    try:
        return fn()
    except Exception:
        return default
