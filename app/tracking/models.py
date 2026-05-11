"""金融消息追踪数据模型。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MarketEvent:
    """标准化后的金融事件。"""

    event_id: str
    stock_code: str
    stock_name: str = ""
    title: str = ""
    summary: str = ""
    source: str = ""
    provider: str = ""
    url: str = ""
    published_at: str = ""
    collected_at: str = ""
    event_type: str = "other"
    sentiment: str = "neutral"
    impact_level: str = "low"
    impact_scope: str = "sentiment"
    confidence: float = 0.5
    reason: str = ""
    channel: str = ""
    retrieval_mode: str = ""
    evidence_type: str = ""
    is_placeholder: bool = False
    related_sources: list[dict[str, str]] = field(default_factory=list)
    is_duplicate: bool = False
    parent_event_id: str = ""
    status: str = "new"
    status_updated_at: str = ""
    status_note: str = ""


@dataclass
class EventCollection:
    """事件流聚合结果。"""

    items: list[MarketEvent] = field(default_factory=list)
    total: int = 0
    high_impact_count: int = 0
    placeholder_count: int = 0
    duplicate_count: int = 0
    source_count: int = 0


@dataclass
class TrackingAlert:
    """由事件流派生的预警。"""

    alert_id: str
    stock_code: str
    event_id: str
    alert_type: str = "high_impact"
    title: str = ""
    message: str = ""
    severity: str = "medium"
    status: str = "open"
    created_at: str = ""
    suggested_action: str = ""


@dataclass
class DailyBriefing:
    """事件追踪简报。"""

    title: str
    summary: str
    generated_at: str
    total_events: int = 0
    high_impact_count: int = 0
    negative_event_count: int = 0
    source_count: int = 0
    key_events: list[MarketEvent] = field(default_factory=list)
    alerts: list[TrackingAlert] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    review_required_events: list[MarketEvent] = field(default_factory=list)


@dataclass
class Watchlist:
    """追踪股票组合。"""

    watchlist_id: str
    name: str
    stock_codes: list[str] = field(default_factory=list)
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
    last_refreshed_at: str = ""
