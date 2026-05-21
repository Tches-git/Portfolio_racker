"""事件影响日线回测。"""
from __future__ import annotations

from datetime import datetime

from app.tracking.models import MarketEvent

WINDOWS = [1, 3, 5, 10]


def build_event_backtest(
    *,
    stock_code: str,
    events: list[MarketEvent],
    daily_bars: list[dict],
    stock_name: str = "",
    event_type: str = "",
    impact_level: str = "",
    windows: list[int] | None = None,
    limit: int = 20,
) -> dict[str, object]:
    active_windows = [item for item in (windows or WINDOWS) if item in WINDOWS] or WINDOWS
    filtered = [
        event for event in events
        if (not event_type or event.event_type == event_type)
        and (not impact_level or event.impact_level == impact_level)
    ][: max(1, limit)]
    bars = _normalize_bars(daily_bars)
    if not bars:
        return _empty_response(stock_code, stock_name, active_windows, "暂无可用日线行情，无法完成事件影响回测。")
    items = [
        item for item in (
            _backtest_event(event, bars=bars, windows=active_windows)
            for event in filtered
        )
        if item is not None
    ]
    fallback = ""
    if filtered and not items:
        fallback = "事件日期与行情区间未匹配，建议扩大行情缓存或选择更近期事件。"
    elif not filtered:
        fallback = "当前筛选条件下暂无历史事件。"
    return {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "windows": active_windows,
        "total_events": len(filtered),
        "matched_event_count": len(items),
        "fallback_message": fallback,
        "groups": _group_items(items, active_windows),
        "items": items,
    }


def _empty_response(stock_code: str, stock_name: str, windows: list[int], message: str) -> dict[str, object]:
    return {
        "stock_code": stock_code,
        "stock_name": stock_name,
        "windows": windows,
        "total_events": 0,
        "matched_event_count": 0,
        "fallback_message": message,
        "groups": [],
        "items": [],
    }


def _normalize_bars(daily_bars: list[dict]) -> list[dict]:
    items = []
    for item in daily_bars:
        date = str(item.get("date") or "")
        close = _to_float(item.get("close"))
        if not date or close <= 0:
            continue
        items.append({
            "date": date[:10],
            "close": close,
            "low": _to_float(item.get("low")) or close,
            "volume": _to_float(item.get("volume")),
        })
    items.sort(key=lambda item: item["date"])
    return items


def _backtest_event(event: MarketEvent, *, bars: list[dict], windows: list[int]) -> dict[str, object] | None:
    event_date = _event_date(event)
    if not event_date:
        return None
    base_index = _first_bar_at_or_after(bars, event_date)
    if base_index is None:
        return None
    base = bars[base_index]
    base_close = float(base["close"])
    returns: dict[str, float] = {}
    for window in windows:
        target_index = min(base_index + window, len(bars) - 1)
        if target_index <= base_index:
            returns[f"t{window}"] = 0.0
        else:
            returns[f"t{window}"] = round((float(bars[target_index]["close"]) / base_close - 1) * 100, 4)
    max_window = max(windows)
    end_index = min(base_index + max_window, len(bars) - 1)
    lows = [float(item["low"]) for item in bars[base_index:end_index + 1]]
    max_drawdown = round((min(lows) / base_close - 1) * 100, 4) if lows else 0.0
    volume_change_pct = 0.0
    if base_index > 0 and _to_float(bars[base_index - 1].get("volume")) > 0:
        volume_change_pct = round((_to_float(base.get("volume")) / _to_float(bars[base_index - 1].get("volume")) - 1) * 100, 4)
    return {
        "event_id": event.event_id,
        "title": event.title,
        "published_at": event.published_at or event.collected_at,
        "event_type": event.event_type,
        "impact_level": event.impact_level,
        "sentiment": event.sentiment,
        "base_date": base["date"],
        "base_close": base_close,
        "returns": returns,
        "max_drawdown": max_drawdown,
        "volume_change_pct": volume_change_pct,
    }


def _group_items(items: list[dict[str, object]], windows: list[int]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = {}
    for item in items:
        key = str(item.get("event_type") or "other")
        grouped.setdefault(key, []).append(item)
    result = []
    for key, group_items in sorted(grouped.items(), key=lambda pair: len(pair[1]), reverse=True):
        avg_returns: dict[str, float] = {}
        for window in windows:
            values = [float(dict(item.get("returns") or {}).get(f"t{window}", 0.0) or 0.0) for item in group_items]
            avg_returns[f"t{window}"] = round(sum(values) / len(values), 4) if values else 0.0
        t1_values = [float(dict(item.get("returns") or {}).get("t1", 0.0) or 0.0) for item in group_items]
        drawdowns = [float(item.get("max_drawdown", 0.0) or 0.0) for item in group_items]
        result.append({
            "key": key,
            "label": _type_label(key),
            "event_count": len(group_items),
            "positive_rate": round(sum(1 for value in t1_values if value > 0) / len(t1_values), 4) if t1_values else 0.0,
            "average_returns": avg_returns,
            "average_max_drawdown": round(sum(drawdowns) / len(drawdowns), 4) if drawdowns else 0.0,
        })
    return result


def _first_bar_at_or_after(bars: list[dict], event_date: str) -> int | None:
    for index, bar in enumerate(bars):
        if str(bar["date"]) >= event_date:
            return index
    return None


def _event_date(event: MarketEvent) -> str:
    value = str(event.published_at or event.collected_at or "")
    if len(value) >= 10:
        return value[:10]
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except Exception:
        return ""


def _to_float(value) -> float:
    try:
        return float(str(value).replace(",", ""))
    except Exception:
        return 0.0


def _type_label(key: str) -> str:
    return {
        "earnings": "业绩",
        "announcement": "公告",
        "filing": "披露",
        "regulation": "监管",
        "industry_policy": "行业政策",
        "market_move": "市场异动",
        "broker_view": "研报观点",
        "risk_sentiment": "风险舆情",
    }.get(key, key or "其他")
