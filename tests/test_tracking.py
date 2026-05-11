from __future__ import annotations

from app.tracking.deduper import dedupe_events
from app.tracking.normalizer import normalize_source_item
from app.tracking.service import collect_stock_events


def test_normalize_source_item_infers_high_impact_event():
    event = normalize_source_item(
        {
            "title": "贵州茅台发布年度业绩增长公告",
            "summary": "净利润增长 18%",
            "time": "2026-05-01",
            "source": "cninfo",
            "provider": "cninfo",
            "channel": "announcement",
            "retrieval_mode": "api",
            "evidence_type": "announcement_update",
        },
        stock_code="600519",
        stock_name="贵州茅台",
    )

    assert event.stock_code == "600519"
    assert event.event_type == "announcement"
    assert event.sentiment == "positive"
    assert event.impact_level in {"medium", "high"}
    assert event.related_sources[0]["provider"] == "cninfo"


def test_dedupe_events_merges_related_sources():
    first = normalize_source_item({"title": "公司收到问询函", "time": "2026-05-01", "source": "cninfo", "channel": "announcement"}, stock_code="600519")
    second = normalize_source_item({"title": "公司收到问询函", "time": "2026-05-01", "source": "eastmoney", "channel": "announcement"}, stock_code="600519")

    events = dedupe_events([first, second])

    assert len(events) == 1
    assert len(events[0].related_sources) == 2


def test_collect_stock_events_uses_live_tool_sources(monkeypatch):
    monkeypatch.setattr("app.tracking.service.fetch_live_quotes", lambda code: {"title": "贵州茅台 实时行情快照", "time": "2026-05-01", "source": "akshare", "provider": "akshare", "channel": "live_quote", "price": 1688})
    monkeypatch.setattr("app.tracking.service.fetch_announcements", lambda code, name="", limit=6: [{"title": "年度报告披露", "time": "2026-05-01", "source": "cninfo", "provider": "cninfo", "channel": "announcement"}])
    monkeypatch.setattr("app.tracking.service.fetch_exchange_filings", lambda code, name="", limit=3: [])
    monkeypatch.setattr("app.tracking.service.fetch_broker_reports", lambda code, name="", limit=3: [{"title": "券商上调盈利预测", "time": "2026-05-02", "source": "中信证券", "provider": "eastmoney_research", "channel": "broker_report"}])

    collection = collect_stock_events("600519", stock_name="贵州茅台", limit=6)

    assert collection.total == 3
    assert collection.source_count == 3
    assert {item.event_type for item in collection.items} >= {"market_move", "announcement", "broker_view"}
