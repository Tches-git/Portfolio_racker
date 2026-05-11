from __future__ import annotations

from app.tracking.deduper import dedupe_events
from app.tracking.models import MarketEvent


def test_dedupe_events_merges_same_url_with_different_event_ids():
    events = dedupe_events([
        MarketEvent(event_id="e1", stock_code="600519", event_type="announcement", title="茅台发布分红公告", url="https://example.com/a?from=x", related_sources=[{"title": "来源A", "url": "https://example.com/a"}]),
        MarketEvent(event_id="e2", stock_code="600519", event_type="announcement", title="贵州茅台分红公告", url="https://example.com/a?from=y", impact_level="high", confidence=0.9, related_sources=[{"title": "来源B", "url": "https://example.com/a?from=y"}]),
    ])

    assert len(events) == 1
    assert events[0].impact_level == "high"
    assert events[0].confidence == 0.9
    assert len(events[0].related_sources) == 2


def test_dedupe_events_merges_similar_same_day_titles():
    events = dedupe_events([
        MarketEvent(event_id="e1", stock_code="600519", event_type="regulation", title="贵州茅台收到监管问询函", published_at="2026-05-11T09:00:00", related_sources=[{"title": "交易所", "url": "https://example.com/a"}]),
        MarketEvent(event_id="e2", stock_code="600519", event_type="regulation", title="贵州茅台收到监管问询", published_at="2026-05-11T10:00:00", summary="问询函细节", related_sources=[{"title": "新闻", "url": "https://example.com/b"}]),
    ])

    assert len(events) == 1
    assert events[0].summary == "问询函细节"
    assert len(events[0].related_sources) == 2


def test_dedupe_events_keeps_different_stocks_separate():
    events = dedupe_events([
        MarketEvent(event_id="e1", stock_code="600519", event_type="announcement", title="发布业绩快报"),
        MarketEvent(event_id="e2", stock_code="000858", event_type="announcement", title="发布业绩快报"),
    ])

    assert len(events) == 2
