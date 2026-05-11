from __future__ import annotations

import json

from app.tracking.watchlist import create_watchlist, list_watchlists, normalize_stock_codes


def test_watchlist_defaults_when_store_is_empty(tmp_path, monkeypatch):
    monkeypatch.setattr("app.tracking.watchlist._memory_stock_codes", lambda: [])

    items = list_watchlists(output_dir=tmp_path)

    assert items[0].watchlist_id == "default_tracking"
    assert items[0].stock_codes


def test_create_watchlist_dedupes_and_persists_codes(tmp_path):
    created = create_watchlist("白酒组合", ["600519", "600519", " 000858 "], description="核心白酒", output_dir=tmp_path)

    assert created.stock_codes == ["600519", "000858"]
    payload = json.loads((tmp_path / "tracking_watchlists.json").read_text(encoding="utf-8"))
    assert payload["items"][0]["name"] == "白酒组合"
    assert list_watchlists(output_dir=tmp_path)[0].description == "核心白酒"


def test_normalize_stock_codes_removes_empty_and_duplicates():
    assert normalize_stock_codes(["", "600519", "600519", "000858"]) == ["600519", "000858"]
