"""从事件流生成追踪预警。"""
from __future__ import annotations

from datetime import datetime
from hashlib import md5

from app.tracking.models import EventCollection, MarketEvent, TrackingAlert


def build_tracking_alerts(collection: EventCollection, *, limit: int = 20) -> list[TrackingAlert]:
    alerts: list[TrackingAlert] = []
    for event in collection.items:
        if event.impact_level == "high":
            alerts.append(_alert(
                event,
                alert_type="high_impact",
                severity="high",
                title=f"{event.stock_code} 高影响事件",
                message=event.reason or event.title,
                suggested_action="优先复核事件，并判断是否需要更新研报或估值假设。",
            ))
        if event.sentiment == "negative" or event.impact_scope == "risk":
            alerts.append(_alert(
                event,
                alert_type="risk_watch",
                severity="high" if event.impact_level == "high" else "medium",
                title=f"{event.stock_code} 风险事件",
                message=event.summary or event.reason or event.title,
                suggested_action="检查历史风险脉络，必要时触发风险点评。",
            ))
        if event.is_placeholder or event.retrieval_mode == "placeholder":
            alerts.append(_alert(
                event,
                alert_type="source_degraded",
                severity="low",
                title=f"{event.stock_code} 来源降级",
                message="该事件来自占位或降级来源，建议补充正式公告、研报或新闻来源。",
                suggested_action="补充来源后再纳入正式研究结论。",
            ))
        if len(event.related_sources) >= 2:
            alerts.append(_alert(
                event,
                alert_type="multi_source_event",
                severity="medium",
                title=f"{event.stock_code} 多来源共振事件",
                message=f"该事件已合并 {len(event.related_sources)} 个来源，可能值得进入研究任务。",
                suggested_action="打开事件时间线，对照多个来源确认事实口径。",
            ))
    return alerts[:limit]


def _alert(event: MarketEvent, *, alert_type: str, severity: str, title: str, message: str, suggested_action: str) -> TrackingAlert:
    raw = f"{event.event_id}:{alert_type}:{severity}"
    alert_id = md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]
    alert = TrackingAlert(
        alert_id=alert_id,
        stock_code=event.stock_code,
        event_id=event.event_id,
        alert_type=alert_type,
        title=title,
        message=message,
        severity=severity,
        status="open",
        created_at=datetime.now().isoformat(timespec="seconds"),
        suggested_action=suggested_action,
    )
    if event.status != "new":
        alert.status = event.status
    return alert
