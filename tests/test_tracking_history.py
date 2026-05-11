from __future__ import annotations

from app.tracking.history import get_event, query_events, save_events
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


def test_infer_event_type_covers_platform_categories():
    assert infer_event_type("公司业绩快报增长", channel="news") == "earnings"
    assert infer_event_type("收到监管问询函", channel="news") == "regulation"
    assert infer_event_type("股价盘中异动大涨", channel="news") == "market_move"
    assert infer_event_type("券商研报上调评级", channel="news") == "broker_view"
