"""从事件流生成追踪预警。"""
from __future__ import annotations

from datetime import datetime
from hashlib import md5
from typing import Callable

from app.tracking.models import AlertRule, EventCollection, MarketEvent, TrackingAlert


AlertPredicate = Callable[[MarketEvent], bool]


ALERT_RULES: tuple[tuple[AlertRule, AlertPredicate, str, str], ...] = (
    (
        AlertRule(
            rule_id="high_impact",
            name="高影响事件",
            description="事件被识别为高影响，建议优先复核并判断是否需要更新研报。",
            alert_type="high_impact",
            severity="high",
            priority="P0",
        ),
        lambda event: event.impact_level == "high",
        "{stock_code} 高影响事件",
        "优先复核事件，并判断是否需要更新研报或估值假设。",
    ),
    (
        AlertRule(
            rule_id="risk_watch",
            name="风险暴露",
            description="负面情绪或风险范围事件，需要检查风险脉络与后续动作。",
            alert_type="risk_watch",
            severity="high",
            priority="P0",
        ),
        lambda event: event.sentiment == "negative" or event.impact_scope == "risk",
        "{stock_code} 风险事件",
        "检查历史风险脉络，必要时触发风险点评。",
    ),
    (
        AlertRule(
            rule_id="source_degraded",
            name="来源降级",
            description="事件来自占位或降级来源，进入正式结论前需要补充可信来源。",
            alert_type="source_degraded",
            severity="low",
            priority="P3",
        ),
        lambda event: event.is_placeholder or event.retrieval_mode == "placeholder",
        "{stock_code} 来源降级",
        "补充来源后再纳入正式研究结论。",
    ),
    (
        AlertRule(
            rule_id="multi_source_event",
            name="多来源共振",
            description="同一事件被多个来源命中，说明需要统一事实口径。",
            alert_type="multi_source_event",
            severity="medium",
            priority="P1",
        ),
        lambda event: len(event.related_sources) >= 2,
        "{stock_code} 多来源共振事件",
        "打开事件时间线，对照多个来源确认事实口径。",
    ),
    (
        AlertRule(
            rule_id="manual_review",
            name="低置信高影响复核",
            description="高影响但置信度偏低的新事件，需要人工复核后再触发研报更新。",
            alert_type="manual_review",
            severity="high",
            priority="P0",
        ),
        lambda event: event.status == "new" and event.impact_level == "high" and event.confidence < 0.65,
        "{stock_code} 人工复核事件",
        "先核验来源与事实，再决定是否生成事件点评。",
    ),
    (
        AlertRule(
            rule_id="regulation_risk",
            name="监管风险",
            description="监管、问询、处罚或调查相关事件，需要优先核查影响范围。",
            alert_type="regulation_risk",
            severity="high",
            priority="P0",
        ),
        lambda event: event.event_type == "regulation" or any(word in f"{event.title} {event.summary}" for word in ("监管", "问询", "处罚", "立案", "调查")),
        "{stock_code} 监管风险事件",
        "复核公告或交易所披露，并检查是否影响风险评级。",
    ),
)


def build_tracking_alerts(collection: EventCollection, *, limit: int = 20) -> list[TrackingAlert]:
    alerts: list[TrackingAlert] = []
    for event in collection.items:
        for rule, predicate, title_template, suggested_action in ALERT_RULES:
            if not rule.enabled or not predicate(event):
                continue
            alerts.append(_alert(
                event,
                rule=rule,
                title=title_template.format(stock_code=event.stock_code),
                message=_alert_message(event, rule),
                suggested_action=suggested_action,
            ))
    return alerts[:limit]


def list_alert_rules() -> list[AlertRule]:
    return [rule for rule, _, _, _ in ALERT_RULES]


def _alert(event: MarketEvent, *, rule: AlertRule, title: str, message: str, suggested_action: str) -> TrackingAlert:
    raw = f"{event.event_id}:{rule.rule_id}:{rule.severity}"
    alert_id = md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]
    alert = TrackingAlert(
        alert_id=alert_id,
        stock_code=event.stock_code,
        event_id=event.event_id,
        rule_id=rule.rule_id,
        rule_name=rule.name,
        alert_type=rule.alert_type,
        title=title,
        message=message,
        severity=_severity_for_event(rule, event),
        priority=rule.priority,
        status="open",
        created_at=datetime.now().isoformat(timespec="seconds"),
        suggested_action=suggested_action,
        explanation=_explain_rule_hit(event, rule),
    )
    if event.status != "new":
        alert.status = event.status
        alert.handled_at = event.status_updated_at
        alert.handled_by = event.status_actor
        alert.handling_note = event.status_note
    return alert


def _severity_for_event(rule: AlertRule, event: MarketEvent) -> str:
    if rule.rule_id == "risk_watch" and event.impact_level != "high":
        return "medium"
    return rule.severity


def _alert_message(event: MarketEvent, rule: AlertRule) -> str:
    if rule.rule_id == "source_degraded":
        return "该事件来自占位或降级来源，建议补充正式公告、研报或新闻来源。"
    if rule.rule_id == "multi_source_event":
        return f"该事件已合并 {len(event.related_sources)} 个来源，可能值得进入研究任务。"
    return event.summary or event.reason or event.title


def _explain_rule_hit(event: MarketEvent, rule: AlertRule) -> str:
    if rule.rule_id == "high_impact":
        return f"影响等级为 {event.impact_level}，当前置信度 {event.confidence:.2f}。"
    if rule.rule_id == "risk_watch":
        return f"情绪为 {event.sentiment}，影响范围为 {event.impact_scope}。"
    if rule.rule_id == "source_degraded":
        return f"retrieval_mode={event.retrieval_mode or 'unknown'}，placeholder={event.is_placeholder}。"
    if rule.rule_id == "multi_source_event":
        return f"已合并 {len(event.related_sources)} 个相关来源。"
    if rule.rule_id == "manual_review":
        return f"高影响但置信度仅 {event.confidence:.2f}，需要人工确认。"
    if rule.rule_id == "regulation_risk":
        return "命中监管、问询、处罚、立案或调查线索。"
    return rule.description
