from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from app.api.services import NotFoundError, get_latest_report, get_stock_history
from app.memory.store import AnalysisRecord, StockMemorySnapshot


class DummyStore:
    def __init__(self, latest=None, records=None, memory=None):
        self._latest = latest
        self._records = records or []
        self._memory = memory or []

    def get_latest(self, stock_code: str):
        return self._latest if self._latest and self._latest.stock_code == stock_code else None

    def get_history(self, stock_code: str | None = None, limit: int = 50):
        items = self._records
        if stock_code:
            items = [item for item in items if item.stock_code == stock_code]
        return items[:limit]

    def get_stock_memory(self, stock_code: str, limit: int = 10):
        items = [item for item in self._memory if True]
        return items[:limit]

    def build_memory_context(self, stock_code: str):
        return {
            "memory_conflict_count": 0,
            "rating_drift_summary": "",
            "thesis_stability_score": 1.0,
            "repeated_risk_patterns": "暂无",
            "repeated_catalyst_patterns": "暂无",
            "memory_pattern_summary": "历史记忆摘要",
        }


def test_get_latest_report_maps_latest_record(tmp_path):
    timestamp = "2026-05-07T01:00:00"
    (tmp_path / "report_600519_20260507_010000.md").write_text("# report", encoding="utf-8")
    (tmp_path / "report_600519_20260507_010000.html").write_text("<html></html>", encoding="utf-8")
    latest = AnalysisRecord(
        stock_code="600519",
        stock_name="贵州茅台",
        timestamp=timestamp,
        industry="白酒",
        rating="推荐",
        rating_score=82.0,
        conclusion="结论摘要",
        dcf_per_share=364.05,
        current_price=1375.0,
        dcf_upside=-73.5,
        source_reference_count=3,
        placeholder_source_count=1,
    )

    payload = get_latest_report("600519", store=DummyStore(latest=latest), output_dir=tmp_path)

    assert payload.stock.code == "600519"
    assert payload.summary.rating == "推荐"
    assert payload.valuation.per_share_value == 364.05
    assert payload.quality.source_reference_count == 3
    assert payload.generated_at == timestamp
    assert [item.kind for item in payload.exports] == ["markdown", "html"]
    assert payload.exports[0].download_url == "/api/v1/exports/report_600519_20260507_010000.md"


def test_get_latest_report_raises_not_found_for_missing_stock(tmp_path):
    with pytest.raises(NotFoundError):
        get_latest_report("000001", store=DummyStore(), output_dir=tmp_path)


def test_get_stock_history_maps_records_and_memory():
    record = AnalysisRecord(stock_code="600519", stock_name="贵州茅台", timestamp="2026-05-07T01:00:00", industry="白酒", rating="推荐", conclusion="结论")
    snapshot = StockMemorySnapshot(stock_code="600519", timestamp="2026-05-07T01:00:00", thesis="盈利稳健", rating="推荐", key_risks=["需求波动"])

    payload = get_stock_history("600519", store=DummyStore(records=[record], memory=[snapshot]))

    assert payload.stock.name == "贵州茅台"
    assert payload.records[0].rating == "推荐"
    assert payload.memory[0].thesis == "盈利稳健"


def test_get_stock_history_raises_not_found_for_missing_stock():
    with pytest.raises(NotFoundError):
        get_stock_history("000001", store=DummyStore())
