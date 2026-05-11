from __future__ import annotations

from app.tracking.history import get_event, query_events, save_events, update_event_status
from app.tracking.models import MarketEvent
from app.tracking.normalizer import infer_event_type


def test_save_events_dedupes_by_event_id(tmp_path):
    first = MarketEvent(event_id="e1", stock_code="600519", title="旧事件", provider="cninfo")
    second = MarketEvent(event_id="e1", stock_code="600519", title="新事件", provider="cninfo")

    save_events([first], output_dir=tmp_path)
    save_events([second], output_dir=tmp_path)

    events = query_events(stock_code="600519", output_dir=tmp_path)
    assert len(events) == 1
    assert events[0].title == "新事件"
    assert get_event("e1", output_dir=tmp_path).provider == "cninfo"


def test_query_events_filters_history(tmp_path):
    save_events([
        MarketEvent(event_id="e1", stock_code="600519", event_type="earnings", impact_level="high", provider="cninfo"),
        MarketEvent(event_id="e2", stock_code="000858", event_type="market_move", impact_level="medium", provider="quote"),
    ], output_dir=tmp_path)

    events = query_events(event_type="earnings", impact_level="high", output_dir=tmp_path)

    assert [event.event_id for event in events] == ["e1"]


def test_event_status_update_persists_and_filters(tmp_path):
    save_events([MarketEvent(event_id="e1", stock_code="600519", title="待处理事件")], output_dir=tmp_path)

    updated = update_event_status("e1", "reviewed", note="已人工复核", actor="alice", output_dir=tmp_path)

    assert updated is not None
    assert updated.status == "reviewed"
    assert updated.status_note == "已人工复核"
    assert updated.status_actor == "alice"
    assert query_events(status="reviewed", output_dir=tmp_path)[0].event_id == "e1"


def test_save_events_preserves_existing_event_status(tmp_path):
    save_events([MarketEvent(event_id="e1", stock_code="600519", title="原事件")], output_dir=tmp_path)
    update_event_status("e1", "ignored", output_dir=tmp_path)

    save_events([MarketEvent(event_id="e1", stock_code="600519", title="实时刷新事件")], output_dir=tmp_path)

    event = get_event("e1", output_dir=tmp_path)
    assert event is not None
    assert event.title == "实时刷新事件"
    assert event.status == "ignored"


def test_save_events_semantically_dedupes_history_and_preserves_status(tmp_path):
    save_events([
        MarketEvent(
            event_id="e1",
            stock_code="600519",
            event_type="announcement",
            title="贵州茅台发布分红公告",
            published_at="2026-05-11T09:00:00",
            url="https://example.com/a",
        )
    ], output_dir=tmp_path)
    update_event_status("e1", "reviewed", note="已核验", output_dir=tmp_path)

    save_events([
        MarketEvent(
            event_id="e2",
            stock_code="600519",
            event_type="announcement",
            title="贵州茅台发布分红公告",
            published_at="2026-05-11T10:00:00",
            url="https://example.com/a?utm=1",
        )
    ], output_dir=tmp_path)

    events = query_events(stock_code="600519", output_dir=tmp_path)
    assert len(events) == 1
    assert events[0].event_id == "e1"
    assert events[0].status == "reviewed"
    assert events[0].status_note == "已核验"


def test_infer_event_type_covers_platform_categories():
    assert infer_event_type("公司业绩快报增长", channel="news") == "earnings"
    assert infer_event_type("收到监管问询函", channel="news") == "regulation"
    assert infer_event_type("股价盘中异动大涨", channel="news") == "market_move"
    assert infer_event_type("券商研报上调评级", channel="news") == "broker_view"
