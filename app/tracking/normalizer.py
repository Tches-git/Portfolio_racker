"""把公告、新闻、行情、研报等来源归一化为 MarketEvent。"""
from __future__ import annotations

from datetime import datetime
from hashlib import md5

from app.tracking.models import MarketEvent


_EVENT_TYPE_BY_CHANNEL = {
    "announcement": "announcement",
    "filing": "filing",
    "broker_report": "broker_view",
    "fund_holding": "shareholder",
    "live_quote": "market_move",
    "news": "news",
}


def normalize_source_item(item: dict, *, stock_code: str, stock_name: str = "") -> MarketEvent:
    """把 live_tools/news 返回的 dict 转成统一事件。"""
    channel = str(item.get("channel") or item.get("source_type") or "news")
    title = str(item.get("title") or "").strip()
    published_at = str(item.get("time") or item.get("published_at") or "").strip()
    source = str(item.get("source") or "").strip()
    provider = str(item.get("provider") or item.get("channel") or source or "unknown").strip()
    summary = str(item.get("summary") or item.get("content") or "").strip()
    evidence_type = str(item.get("evidence_type") or "").strip()
    retrieval_mode = str(item.get("retrieval_mode") or "").strip()
    event_type = infer_event_type(title, channel=channel, evidence_type=evidence_type)
    sentiment, impact_level, impact_scope, confidence, reason = infer_impact(
        title=title,
        summary=summary,
        channel=channel,
        event_type=event_type,
        evidence_type=evidence_type,
        is_placeholder=bool(item.get("is_placeholder", False)),
    )
    event_id = str(item.get("event_id") or item.get("id") or stable_event_id(stock_code, title, published_at, source, channel))
    return MarketEvent(
        event_id=event_id,
        stock_code=stock_code,
        stock_name=stock_name,
        title=title or f"{stock_code} 未命名事件",
        summary=summary,
        source=source,
        provider=provider,
        url=str(item.get("url") or item.get("link") or ""),
        published_at=published_at,
        collected_at=datetime.now().isoformat(timespec="seconds"),
        event_type=event_type,
        sentiment=sentiment,
        impact_level=impact_level,
        impact_scope=impact_scope,
        confidence=confidence,
        reason=reason,
        channel=channel,
        retrieval_mode=retrieval_mode,
        evidence_type=evidence_type,
        is_placeholder=bool(item.get("is_placeholder", False)),
        related_sources=[source_payload(item)],
    )


def infer_event_type(title: str, *, channel: str, evidence_type: str = "") -> str:
    text = f"{title} {evidence_type}"
    if channel in _EVENT_TYPE_BY_CHANNEL and channel != "news":
        return _EVENT_TYPE_BY_CHANNEL[channel]
    if any(keyword in text for keyword in ("业绩", "预告", "快报", "利润", "营收", "年报", "季报", "半年报")):
        return "earnings"
    if any(keyword in text for keyword in ("公告", "披露", "停牌", "复牌", "分红")):
        return "announcement"
    if any(keyword in text for keyword in ("问询", "处罚", "监管", "立案", "调查")):
        return "regulation"
    if any(keyword in text for keyword in ("回购", "减持", "增持", "股东", "质押", "持股")):
        return "shareholder"
    if any(keyword in text for keyword in ("提价", "降价", "价格", "涨价")):
        return "product_price"
    if any(keyword in text for keyword in ("订单", "产能", "交付", "中标")):
        return "capacity_order"
    if any(keyword in text for keyword in ("政策", "行业", "补贴", "监管规则")):
        return "industry_policy"
    if any(keyword in text for keyword in ("异动", "涨停", "跌停", "大涨", "大跌", "波动")):
        return "market_move"
    if any(keyword in text for keyword in ("研报", "券商", "评级", "目标价", "买入")):
        return "broker_view"
    if any(keyword in text for keyword in ("舆情", "风险", "诉讼", "违约", "亏损", "下滑")):
        return "risk_sentiment"
    if channel in _EVENT_TYPE_BY_CHANNEL:
        return _EVENT_TYPE_BY_CHANNEL[channel]
    return "other"


def infer_impact(*, title: str, summary: str, channel: str, event_type: str, evidence_type: str, is_placeholder: bool) -> tuple[str, str, str, float, str]:
    text = f"{title} {summary} {evidence_type}"
    if is_placeholder:
        return "uncertain", "low", "sentiment", 0.25, "占位或降级来源，仅作为追踪线索，需人工复核。"
    negative_words = ("处罚", "问询", "立案", "调查", "亏损", "下滑", "减持", "违约", "诉讼", "风险", "终止")
    positive_words = ("增长", "上调", "买入", "增持", "回购", "中标", "提价", "突破", "盈利", "创新高")
    if any(word in text for word in negative_words):
        sentiment = "negative"
    elif any(word in text for word in positive_words):
        sentiment = "positive"
    else:
        sentiment = "neutral"

    if event_type in {"earnings", "regulation", "product_price", "risk_sentiment"} or any(word in text for word in ("重大", "年报", "提价", "处罚", "立案")):
        impact_level = "high"
    elif event_type in {"announcement", "filing", "broker_view", "shareholder", "capacity_order", "industry_policy", "market_move"}:
        impact_level = "medium"
    else:
        impact_level = "low"

    if event_type in {"earnings", "product_price", "capacity_order"}:
        impact_scope = "fundamentals"
    elif event_type == "broker_view":
        impact_scope = "valuation"
    elif event_type in {"regulation", "risk_sentiment"}:
        impact_scope = "risk"
    elif event_type == "industry_policy":
        impact_scope = "industry"
    else:
        impact_scope = "sentiment"

    confidence = 0.82 if channel in {"announcement", "filing", "live_quote"} else 0.68
    if sentiment == "neutral":
        confidence -= 0.08
    reason = build_reason(sentiment=sentiment, impact_level=impact_level, impact_scope=impact_scope, event_type=event_type)
    return sentiment, impact_level, impact_scope, max(0.1, min(confidence, 0.95)), reason


def build_reason(*, sentiment: str, impact_level: str, impact_scope: str, event_type: str) -> str:
    sentiment_label = {"positive": "偏利好", "negative": "偏利空", "neutral": "中性", "uncertain": "不确定"}.get(sentiment, "中性")
    scope_label = {
        "fundamentals": "基本面",
        "valuation": "估值预期",
        "sentiment": "短期情绪",
        "industry": "行业景气",
        "risk": "风险暴露",
    }.get(impact_scope, "短期情绪")
    level_label = {"high": "高影响", "medium": "中等影响", "low": "低影响"}.get(impact_level, "低影响")
    return f"{event_type} 事件被识别为{sentiment_label}，主要影响{scope_label}，当前标记为{level_label}。"


def source_payload(item: dict) -> dict[str, str]:
    return {
        "title": str(item.get("title") or ""),
        "source": str(item.get("source") or ""),
        "provider": str(item.get("provider") or ""),
        "url": str(item.get("url") or item.get("link") or ""),
        "time": str(item.get("time") or ""),
    }


def stable_event_id(*parts: str) -> str:
    raw = "::".join(str(part or "") for part in parts)
    return md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]
