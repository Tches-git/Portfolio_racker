"""事件追踪简报生成。"""
from __future__ import annotations

from datetime import datetime

from app.tracking.alerts import build_tracking_alerts
from app.tracking.models import DailyBriefing, EventCollection, MarketEvent


def build_daily_briefing(collection: EventCollection, *, title: str = "今日金融事件简报") -> DailyBriefing:
    key_events = select_key_events(collection.items)
    alerts = build_tracking_alerts(collection, limit=8)
    negative_count = sum(1 for event in collection.items if event.sentiment == "negative")
    summary = (
        f"共追踪 {collection.total} 条事件，其中高影响 {collection.high_impact_count} 条、"
        f"偏利空/风险 {negative_count} 条，覆盖 {collection.source_count} 个来源。"
    )
    actions = build_suggested_actions(collection, alerts)
    themes = build_themes(collection.items)
    review_required = [
        event for event in key_events
        if event.impact_level == "high" or event.is_placeholder or event.confidence < 0.55
    ][:5]
    return DailyBriefing(
        title=title,
        summary=summary,
        generated_at=datetime.now().isoformat(timespec="seconds"),
        total_events=collection.total,
        high_impact_count=collection.high_impact_count,
        negative_event_count=negative_count,
        source_count=collection.source_count,
        key_events=key_events,
        alerts=alerts,
        suggested_actions=actions,
        themes=themes,
        review_required_events=review_required,
    )


def select_key_events(events: list[MarketEvent], *, limit: int = 6) -> list[MarketEvent]:
    level_rank = {"high": 3, "medium": 2, "low": 1}
    sentiment_rank = {"negative": 3, "positive": 2, "uncertain": 1, "neutral": 0}
    return sorted(
        events,
        key=lambda event: (level_rank.get(event.impact_level, 0), sentiment_rank.get(event.sentiment, 0), event.confidence),
        reverse=True,
    )[:limit]


def build_suggested_actions(collection: EventCollection, alerts) -> list[str]:
    actions: list[str] = []
    if collection.high_impact_count:
        actions.append("优先复核高影响事件，并判断是否触发研报更新。")
    if any(alert.alert_type == "risk_watch" for alert in alerts):
        actions.append("对风险事件做历史对照，检查是否出现重复风险模式。")
    if collection.placeholder_count:
        actions.append("补齐降级或占位来源，避免低质量来源直接进入结论。")
    if not actions:
        actions.append("当前事件影响较低，可继续观察并等待更多来源确认。")
    return actions


def build_themes(events: list[MarketEvent], *, limit: int = 5) -> list[str]:
    labels = {
        "earnings": "业绩与盈利变化",
        "announcement": "公告披露",
        "regulation": "监管与合规风险",
        "industry_policy": "行业政策",
        "market_move": "市场异动",
        "broker_view": "研报观点",
        "risk_sentiment": "风险舆情",
    }
    counts: dict[str, int] = {}
    for event in events:
        counts[event.event_type] = counts.get(event.event_type, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [f"{labels.get(event_type, event_type)} {count} 条" for event_type, count in ranked[:limit]]
