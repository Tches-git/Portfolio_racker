"""自选股 / 组合追踪存储。"""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from hashlib import md5
from pathlib import Path

from app.config import OUTPUT_DIR
from app.memory.store import get_memory_store
from app.tracking.models import Watchlist

DEFAULT_TRACKING_STOCKS = ["600519", "000858", "300750", "600036"]


def list_watchlists(*, output_dir: Path = OUTPUT_DIR) -> list[Watchlist]:
    items = _load_watchlists(output_dir=output_dir)
    if items:
        return items
    return [_default_watchlist()]


def create_watchlist(name: str, stock_codes: list[str], *, description: str = "", output_dir: Path = OUTPUT_DIR) -> Watchlist:
    codes = normalize_stock_codes(stock_codes)
    now = datetime.now().isoformat(timespec="seconds")
    watchlist = Watchlist(
        watchlist_id=_stable_watchlist_id(name, codes, now),
        name=name.strip() or "未命名组合",
        stock_codes=codes,
        description=description.strip(),
        created_at=now,
        updated_at=now,
    )
    items = _load_watchlists(output_dir=output_dir)
    items.append(watchlist)
    _save_watchlists(items, output_dir=output_dir)
    return watchlist


def normalize_stock_codes(stock_codes: list[str]) -> list[str]:
    seen = set()
    normalized: list[str] = []
    for raw_code in stock_codes:
        code = str(raw_code or "").strip()
        if not code or code in seen:
            continue
        seen.add(code)
        normalized.append(code)
    return normalized


def _default_watchlist() -> Watchlist:
    codes = _memory_stock_codes() or list(DEFAULT_TRACKING_STOCKS)
    now = datetime.now().isoformat(timespec="seconds")
    return Watchlist(
        watchlist_id="default_tracking",
        name="默认追踪组合",
        stock_codes=codes[:8],
        description="由历史研究记录和内置核心股票生成，适合作为金融事件追踪起点。",
        created_at=now,
        updated_at=now,
    )


def _memory_stock_codes() -> list[str]:
    try:
        stocks = get_memory_store().get_all_stocks()
    except Exception:
        return []
    return normalize_stock_codes([str(item.get("code") or "") for item in stocks])


def _watchlist_path(output_dir: Path) -> Path:
    return output_dir / "tracking_watchlists.json"


def _load_watchlists(*, output_dir: Path) -> list[Watchlist]:
    path = _watchlist_path(output_dir)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        return []
    return [
        Watchlist(
            watchlist_id=str(item.get("watchlist_id", "")),
            name=str(item.get("name", "")),
            stock_codes=normalize_stock_codes(list(item.get("stock_codes", []) or [])),
            description=str(item.get("description", "")),
            created_at=str(item.get("created_at", "")),
            updated_at=str(item.get("updated_at", "")),
        )
        for item in items
        if isinstance(item, dict)
    ]


def _save_watchlists(items: list[Watchlist], *, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"items": [asdict(item) for item in items]}
    _watchlist_path(output_dir).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _stable_watchlist_id(name: str, codes: list[str], timestamp: str) -> str:
    raw = f"{name}:{','.join(codes)}:{timestamp}"
    return "wl_" + md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]
