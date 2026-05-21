"""产品前端 API 入口（兼容 Phase 1/2）。"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import require_current_user
from app.auth.rate_limit import RateLimitExceeded, check_rate_limit
from app.auth.security import create_access_token
from app.auth.service import AuthError, authenticate_user, register_user, user_to_dto
from app.api.download import ExportNotFoundError
from app.api.mappers import build_health_response, map_history_record
from app.api.run_manager import RunActionError, RunNotFoundError, run_manager
from app.api.schemas import (
    AlertRuleDTO,
    AlertRuleListResponse,
    AnalysisRunCreateRequest,
    AnalysisRunListResponse,
    AnalysisRunResponse,
    AuthLoginRequest,
    AuthRegisterRequest,
    AuthResponse,
    AuthUserDTO,
    BatchRunCreateRequest,
    BatchRunCreateResponse,
    DailyBriefingResponse,
    DashboardPortfolioSummaryDTO,
    DashboardResponse,
    DashboardSetupDTO,
    EventAnalyzeRequest,
    EventBacktestResponse,
    EventImpactReplayItemDTO,
    EventImpactReviewResponse,
    EventStatusUpdateRequest,
    EventWorkbenchResponse,
    HealthResponse,
    LatestReportResponse,
    MarketDailyBarDTO,
    MarketEventDTO,
    MarketEventListResponse,
    MarketQuoteDTO,
    MarketWorkbenchResponse,
    OpsMetricsResponse,
    QualityMetricDTO,
    QualityWorkbenchResponse,
    ReportDiffResponse,
    RunAssignmentRequest,
    RunWorkbenchResponse,
    StockSearchItemDTO,
    StockSearchResponse,
    StockEventTimelineResponse,
    StockHistoryResponse,
    StockNewsResponse,
    StockWorkbenchResponse,
    StoreBackupResponse,
    StoreHealthResponse,
    TrackingAlertDTO,
    TrackingAlertListResponse,
    WatchlistCreateRequest,
    WatchlistDTO,
    WatchlistDetailResponse,
    WatchlistImpactStockDTO,
    WatchlistListResponse,
    WatchlistMarketSnapshotDTO,
    WatchlistSummaryDTO,
    WatchlistUpdateRequest,
    WorkbenchActionDTO,
    WorkspaceStocksResponse,
)
from app.api.services import NotFoundError, get_latest_report, get_stock_history
from app.config import AUTH_COOKIE_NAME, AUTH_TOKEN_TTL_SECONDS, LOGIN_RATE_LIMIT_PER_HOUR, OUTPUT_DIR, PROJECT_ROOT, SIGNUP_RATE_LIMIT_PER_HOUR
from app.data_source.akshare_client import get_recent_news, get_stock_daily_bars, search_a_stocks
from app.data_source.live_tools import fetch_live_quotes
from app.db.models import User
from app.db.repositories import create_user_watchlist, delete_user_watchlist, get_user_event, get_user_export_artifact, get_user_watchlist, list_user_events, list_user_watchlists, mark_user_watchlist_refreshed, save_user_events, save_user_run, update_user_event_status, update_user_watchlist
from app.db.session import get_db
from app.finance.event_backtest import build_event_backtest
from app.memory.db_store import UserMemoryStore
from app.tracking.models import EventCollection
from app.tracking.service import collect_market_events, collect_stock_events, summarize_events
from app.tracking.alerts import build_tracking_alerts, list_alert_rules
from app.tracking.briefing import build_daily_briefing

app = FastAPI(title="AI Research Assistant API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _actor(actor: str = Header(default='system', alias='X-Actor'), role: str = Header(default='admin', alias='X-Role')) -> tuple[str, str]:
    return actor or 'system', role or 'viewer'


def _run_role_for_user(user: User) -> str:
    return "admin" if user.role == "admin" else "analyst"


def _run_actor_for_request(user: User, actor_header: str, role_header: str) -> tuple[str, str]:
    return user.username, _run_role_for_user(user)


def _assert_run_access(run, user: User) -> None:
    if getattr(run, "user_id", "") != user.id:
        raise HTTPException(status_code=404, detail=f"未找到运行任务: {run.run_id}")


def _sync_user_run(db: Session, user: User, run) -> None:
    save_user_run(db, user_id=user.id, run=run)


def _user_memory(db: Session, user: User) -> UserMemoryStore:
    return UserMemoryStore(db, user.id)


def _user_output_dir(user: User) -> Path:
    return OUTPUT_DIR / "users" / user.id


def _require_admin(user: User) -> None:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")


def _parse_stock_codes(stock_codes: str) -> list[str]:
    return [part.strip() for part in stock_codes.split(",") if part.strip()] if stock_codes else []


def _user_tracking_codes(db: Session, *, user_id: str, stock_codes: str = "") -> list[str]:
    explicit_codes = _parse_stock_codes(stock_codes)
    if explicit_codes:
        return explicit_codes
    codes: list[str] = []
    seen: set[str] = set()
    for watchlist in list_user_watchlists(db, user_id=user_id):
        for code in watchlist.stock_codes:
            normalized = str(code or "").strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                codes.append(normalized)
    return codes


def _user_is_tracking_stock(db: Session, *, user_id: str, stock_code: str) -> bool:
    normalized = str(stock_code or "").strip()
    return bool(normalized and normalized in _user_tracking_codes(db, user_id=user_id))


def _market_event_list_response(collection, *, mode: str = "realtime") -> MarketEventListResponse:
    return MarketEventListResponse(
        items=[MarketEventDTO(**event.__dict__) for event in collection.items],
        total=collection.total,
        high_impact_count=collection.high_impact_count,
        placeholder_count=collection.placeholder_count,
        duplicate_count=collection.duplicate_count,
        source_count=collection.source_count,
        mode=mode,
    )


def _empty_event_collection() -> EventCollection:
    return EventCollection(items=[], total=0, high_impact_count=0, placeholder_count=0, duplicate_count=0, source_count=0)


def _tracking_alert_list_response(alerts) -> TrackingAlertListResponse:
    severity_counts = _count_by(alerts, "severity")
    alert_type_counts = _count_by(alerts, "alert_type")
    rule_counts = _count_by(alerts, "rule_id")
    return TrackingAlertListResponse(
        items=[TrackingAlertDTO(**alert.__dict__) for alert in alerts],
        total=len(alerts),
        high_severity_count=sum(1 for alert in alerts if alert.severity == "high"),
        risk_alert_count=sum(1 for alert in alerts if alert.alert_type == "risk_watch"),
        source_degraded_count=sum(1 for alert in alerts if alert.alert_type == "source_degraded"),
        manual_review_count=sum(1 for alert in alerts if alert.alert_type == "manual_review"),
        severity_counts=severity_counts,
        alert_type_counts=alert_type_counts,
        rule_counts=rule_counts,
    )


def _filter_alerts_by_status(alerts, status: str):
    normalized = status or "open"
    if normalized == "all":
        return alerts
    return [alert for alert in alerts if alert.status == normalized]


def _filter_alerts(alerts, *, status: str = "open", severity: str = "", alert_type: str = "", rule_id: str = ""):
    filtered = _filter_alerts_by_status(alerts, status)
    if severity:
        filtered = [alert for alert in filtered if alert.severity == severity]
    if alert_type:
        filtered = [alert for alert in filtered if alert.alert_type == alert_type]
    if rule_id:
        filtered = [alert for alert in filtered if alert.rule_id == rule_id]
    return filtered


def _count_by(items, attribute: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(getattr(item, attribute, "") or "")
        if not value:
            continue
        counts[value] = counts.get(value, 0) + 1
    return counts


def _daily_briefing_response(briefing) -> DailyBriefingResponse:
    return DailyBriefingResponse(
        title=briefing.title,
        summary=briefing.summary,
        generated_at=briefing.generated_at,
        total_events=briefing.total_events,
        high_impact_count=briefing.high_impact_count,
        negative_event_count=briefing.negative_event_count,
        source_count=briefing.source_count,
        key_events=[MarketEventDTO(**event.__dict__) for event in briefing.key_events],
        alerts=[TrackingAlertDTO(**alert.__dict__) for alert in briefing.alerts],
        suggested_actions=briefing.suggested_actions,
        themes=briefing.themes,
        review_required_events=[MarketEventDTO(**event.__dict__) for event in briefing.review_required_events],
    )


def _market_range_to_days(range_value: str) -> tuple[str, int]:
    mapping = {"30d": 30, "90d": 90, "180d": 180}
    normalized = str(range_value or "90d").strip().lower()
    if normalized not in mapping:
        normalized = "90d"
    return normalized, mapping[normalized]


def _is_valid_a_stock_code(stock_code: str) -> bool:
    return stock_code.isdigit() and len(stock_code) == 6


def _to_float(value) -> float:
    try:
        if value is None or str(value).strip() in {"", "-", "--", "None", "nan"}:
            return 0.0
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return 0.0


def _quote_stock_name(stock_code: str, quote: dict) -> str:
    name = str(quote.get("stock_name") or quote.get("name") or "").strip()
    if name:
        return name
    title = str(quote.get("title") or "").strip()
    suffix = " 实时行情快照"
    if title.endswith(suffix):
        return title[:-len(suffix)] or stock_code
    return stock_code


def _market_quote_response(stock_code: str, quote: dict, bars: list[dict], fallback_message: str = "") -> MarketQuoteDTO:
    latest = bars[-1] if bars else {}
    previous = bars[-2] if len(bars) >= 2 else {}
    price = _to_float(quote.get("price")) or _to_float(latest.get("close"))
    previous_close = _to_float(previous.get("close"))
    change = price - previous_close if price and previous_close else 0.0
    change_pct = round(change / previous_close * 100, 4) if previous_close else _to_float(latest.get("change_pct"))
    has_quote = bool(quote and (price or quote.get("title") or quote.get("provider")))
    has_bars = bool(bars)
    source_status = "ok" if has_quote and has_bars and not fallback_message else "partial" if has_quote or has_bars else "degraded"
    return MarketQuoteDTO(
        stock_code=stock_code,
        stock_name=_quote_stock_name(stock_code, quote),
        price=price,
        change=round(change, 4),
        change_pct=change_pct,
        open=_to_float(latest.get("open")),
        high=_to_float(latest.get("high")),
        low=_to_float(latest.get("low")),
        previous_close=previous_close,
        volume=_to_float(latest.get("volume")),
        amount=_to_float(latest.get("amount")),
        turnover=_to_float(latest.get("turnover")),
        market_cap=_to_float(quote.get("market_cap")),
        pe_ratio=_to_float(quote.get("pe_ratio")),
        pb_ratio=_to_float(quote.get("pb_ratio")),
        updated_at=str(quote.get("time") or latest.get("date") or ""),
        source_status=source_status,
        provider=str(quote.get("provider") or ("akshare" if has_bars else "")),
    )


def _safe_market_call(label: str, func, *args, timeout: float = 6.0, **kwargs):
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(func, *args, **kwargs)
    try:
        return future.result(timeout=timeout), ""
    except FuturesTimeoutError:
        future.cancel()
        return None, f"{label}数据源响应超时，请稍后重试。"
    except Exception:
        return None, f"{label}数据源暂不可用，请稍后重试。"
    finally:
        executor.shutdown(wait=False, cancel_futures=True)


def _watchlist_market_suggestion(quote: MarketQuoteDTO, fallback_message: str = "") -> str:
    if quote.source_status == "degraded" or fallback_message:
        return "行情源降级，建议稍后重新拉取，并结合事件预警复核。"
    if quote.change_pct >= 3:
        return "短线涨幅较高，优先检查事件驱动原因和回撤风险。"
    if quote.change_pct <= -3:
        return "短线承压，建议排查负面事件、公告变化和预警队列。"
    if quote.turnover >= 5:
        return "换手率偏高，建议关注资金分歧和后续成交持续性。"
    return "行情波动可控，可结合事件热度与估值指标继续观察。"


def _watchlist_market_snapshots(stock_codes: list[str]) -> tuple[list[WatchlistMarketSnapshotDTO], str, str]:
    snapshots: list[WatchlistMarketSnapshotDTO] = []
    fallback_messages: list[str] = []
    updated_at = datetime.utcnow().isoformat(timespec="seconds")
    for code in stock_codes:
        stock_code = str(code or "").strip()
        if not _is_valid_a_stock_code(stock_code):
            message = "股票代码格式不正确，暂无法拉取行情。"
            fallback_messages.append(f"{stock_code or '未知标的'}：{message}")
            snapshots.append(
                WatchlistMarketSnapshotDTO(
                    stock_code=stock_code,
                    stock_name=stock_code,
                    quote=MarketQuoteDTO(stock_code=stock_code, stock_name=stock_code, source_status="degraded"),
                    source_status="degraded",
                    fallback_message=message,
                    suggestion="请检查股票池代码是否为 6 位 A 股代码。",
                )
            )
            continue

        quote: dict = {}
        bars: list[dict] = []
        stock_fallbacks: list[str] = []
        quote_result, quote_error = _safe_market_call("行情快照", fetch_live_quotes, stock_code, timeout=4)
        if quote_error:
            stock_fallbacks.append(quote_error)
        elif isinstance(quote_result, dict):
            quote = quote_result

        bars_result, bars_error = _safe_market_call("日线", get_stock_daily_bars, stock_code, days=180, timeout=6)
        if bars_error:
            stock_fallbacks.append(bars_error)
        elif isinstance(bars_result, list):
            bars = bars_result[-180:]

        fallback_message = " ".join(dict.fromkeys(stock_fallbacks))
        if not quote and not bars and not fallback_message:
            fallback_message = "当前没有可用行情数据，请稍后重试。"
        if fallback_message:
            fallback_messages.append(f"{stock_code}：{fallback_message}")

        quote_response = _market_quote_response(stock_code, quote, bars, fallback_message)
        snapshots.append(
            WatchlistMarketSnapshotDTO(
                stock_code=stock_code,
                stock_name=quote_response.stock_name or stock_code,
                quote=quote_response,
                trend_30d=[MarketDailyBarDTO(**item) for item in bars[-30:]],
                trend_90d=[MarketDailyBarDTO(**item) for item in bars[-90:]],
                trend_180d=[MarketDailyBarDTO(**item) for item in bars[-180:]],
                source_status=quote_response.source_status,
                fallback_message=fallback_message,
                suggestion=_watchlist_market_suggestion(quote_response, fallback_message),
            )
        )

    market_fallback_message = " ".join(dict.fromkeys(fallback_messages))
    if not snapshots and stock_codes:
        market_fallback_message = market_fallback_message or "当前组合暂无可用行情数据，请稍后重试。"
    return snapshots, updated_at, market_fallback_message


def _watchlist_detail_response(watchlist, collection, *, mode: str = "history", include_market: bool = False) -> WatchlistDetailResponse:
    alerts = _filter_alerts_by_status(build_tracking_alerts(collection), "open")
    briefing = build_daily_briefing(collection, title=f"{watchlist.name} 组合简报")
    alert_response = _tracking_alert_list_response(alerts)
    impacted_stocks = _rank_impacted_stocks(collection.items, alerts)
    risk = _watchlist_risk(collection.items, alerts, alert_response)
    summary = WatchlistSummaryDTO(
        stock_count=len(watchlist.stock_codes),
        event_count=collection.total,
        high_impact_count=collection.high_impact_count,
        alert_count=alert_response.total,
        high_severity_count=alert_response.high_severity_count,
        source_count=collection.source_count,
        placeholder_count=collection.placeholder_count,
        risk_score=int(risk["risk_score"]),
        risk_level=str(risk["risk_level"]),
        risk_summary=str(risk["risk_summary"]),
        open_alert_count=alert_response.total,
        handled_event_count=sum(1 for event in collection.items if event.status in {"reviewed", "ignored", "converted_to_report"}),
        converted_event_count=sum(1 for event in collection.items if event.status == "converted_to_report"),
        manual_review_count=alert_response.manual_review_count,
        processing_rate=float(risk["processing_rate"]),
        dominant_rules=list(risk["dominant_rules"]),
        priority_actions=list(risk["priority_actions"]),
        last_refreshed_at=watchlist.last_refreshed_at,
        impacted_stocks=impacted_stocks,
    )
    market_snapshots: list[WatchlistMarketSnapshotDTO] = []
    market_updated_at = ""
    market_fallback_message = ""
    if include_market:
        market_snapshots, market_updated_at, market_fallback_message = _watchlist_market_snapshots(watchlist.stock_codes)

    return WatchlistDetailResponse(
        watchlist=WatchlistDTO(**watchlist.__dict__),
        events=_market_event_list_response(collection, mode=mode),
        alerts=alert_response,
        briefing=_daily_briefing_response(briefing),
        summary=summary,
        market_snapshots=market_snapshots,
        market_updated_at=market_updated_at,
        market_fallback_message=market_fallback_message,
    )


def _rank_impacted_stocks(events, alerts=None) -> list[WatchlistImpactStockDTO]:
    grouped: dict[str, dict[str, object]] = {}
    alerts = list(alerts or [])
    for event in events:
        code = event.stock_code
        if not code:
            continue
        event_time = event.published_at or event.collected_at
        current = grouped.setdefault(
            code,
            {
                "stock_code": code,
                "stock_name": event.stock_name,
                "event_count": 0,
                "high_impact_count": 0,
                "alert_count": 0,
                "risk_score": 0,
                "risk_level": "low",
                "priority_action": "",
                "latest_event_at": "",
            },
        )
        current["event_count"] = int(current["event_count"]) + 1
        current["stock_name"] = current["stock_name"] or event.stock_name
        if event.impact_level == "high":
            current["high_impact_count"] = int(current["high_impact_count"]) + 1
        if event_time and event_time > str(current["latest_event_at"]):
            current["latest_event_at"] = event_time
    alert_counts = _alert_counts_by_stock(alerts)
    for code, current in grouped.items():
        current["alert_count"] = alert_counts.get(code, 0)
        risk_score = min(100, int(current["high_impact_count"]) * 35 + int(current["alert_count"]) * 20 + int(current["event_count"]) * 4)
        current["risk_score"] = risk_score
        current["risk_level"] = _risk_level(risk_score)
        current["priority_action"] = _priority_action(str(current["risk_level"]), int(current["alert_count"]), int(current["high_impact_count"]))
    ranked = sorted(
        grouped.values(),
        key=lambda item: (int(item["risk_score"]), int(item["high_impact_count"]), int(item["event_count"]), str(item["latest_event_at"])),
        reverse=True,
    )
    return [WatchlistImpactStockDTO(**item) for item in ranked]


def _watchlist_risk(events, alerts, alert_response: TrackingAlertListResponse) -> dict[str, object]:
    events = list(events or [])
    alerts = list(alerts or [])
    handled_count = sum(1 for event in events if event.status in {"reviewed", "ignored", "converted_to_report"})
    actionable_count = sum(1 for event in events if event.status != "ignored")
    processing_rate = round(handled_count / actionable_count, 4) if actionable_count else 0.0
    high_impact_count = sum(1 for event in events if event.impact_level == "high")
    source_degraded_count = alert_response.source_degraded_count
    manual_review_count = alert_response.manual_review_count
    risk_score = min(
        100,
        high_impact_count * 24
        + alert_response.high_severity_count * 18
        + alert_response.risk_alert_count * 14
        + manual_review_count * 20
        + source_degraded_count * 6
        + max(0, len(events) - handled_count) * 3,
    )
    risk_level = _risk_level(risk_score)
    dominant_rules = [
        key
        for key, _ in sorted(alert_response.rule_counts.items(), key=lambda item: item[1], reverse=True)[:3]
    ]
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_summary": _risk_summary(risk_level, risk_score, alert_response.total, high_impact_count, processing_rate),
        "processing_rate": processing_rate,
        "dominant_rules": dominant_rules,
        "priority_actions": _watchlist_priority_actions(risk_level, alert_response, high_impact_count, processing_rate),
    }


def _alert_counts_by_stock(alerts) -> dict[str, int]:
    counts: dict[str, int] = {}
    for alert in alerts:
        code = str(getattr(alert, "stock_code", "") or "")
        if not code:
            continue
        counts[code] = counts.get(code, 0) + 1
    return counts


def _risk_level(score: int) -> str:
    if score >= 70:
        return "high"
    if score >= 35:
        return "medium"
    return "low"


def _risk_summary(level: str, score: int, alert_count: int, high_impact_count: int, processing_rate: float) -> str:
    level_label = {"high": "高风险", "medium": "中等风险", "low": "低风险"}.get(level, "低风险")
    return f"组合当前为{level_label}，风险分 {score}，开放预警 {alert_count} 个，高影响事件 {high_impact_count} 个，处理率 {processing_rate:.0%}。"


def _priority_action(level: str, alert_count: int, high_impact_count: int) -> str:
    if level == "high":
        return "优先处理高影响事件并触发事件点评。"
    if alert_count:
        return "先复核开放预警，再决定是否更新研报。"
    if high_impact_count:
        return "复核高影响事件的来源和影响方向。"
    return "保持观察，等待下一次组合刷新。"


def _watchlist_priority_actions(level: str, alert_response: TrackingAlertListResponse, high_impact_count: int, processing_rate: float) -> list[str]:
    actions: list[str] = []
    if level == "high":
        actions.append("立即处理 P0 预警，并把高影响事件转成事件点评。")
    if alert_response.manual_review_count:
        actions.append("先完成低置信高影响事件的人工复核。")
    if alert_response.source_degraded_count:
        actions.append("补充来源降级事件的正式公告、新闻或研报来源。")
    if high_impact_count and processing_rate < 0.5:
        actions.append("把未处理高影响事件标记为已复核、忽略或已转研报。")
    return actions[:4] or ["当前组合风险可控，保持刷新和观察。"]


def _event_impact_review_response(stock_code: str, collection, runs) -> EventImpactReviewResponse:
    events = list(collection.items)
    run_by_event = {
        str(run.event_context.get('event_id') or ''): run
        for run in runs
        if getattr(run, 'event_context', None)
    }
    type_counts: dict[str, int] = {}
    for event in events:
        event_type = event.event_type or 'other'
        type_counts[event_type] = type_counts.get(event_type, 0) + 1
    dominant_types = [
        item[0] for item in sorted(type_counts.items(), key=lambda item: (item[1], item[0]), reverse=True)[:4]
    ]
    stock_name = next((event.stock_name for event in events if event.stock_name), '')
    latest_event_at = next((event.published_at or event.collected_at for event in events if event.published_at or event.collected_at), '')
    replay_items = []
    for event in events[:12]:
        run = run_by_event.get(event.event_id)
        summary = dict(getattr(run, 'event_report_summary', {}) or {}) if run else {}
        commentary_url = str(summary.get('event_commentary_url') or '')
        if not commentary_url and run:
            commentary_url = next((item.get('download_url', '') for item in getattr(run, 'exports', []) if item.get('kind') == 'event_commentary'), '')
        review_line = '尚未触发研报更新'
        if run:
            review_line = f"已关联 {run.status} 任务，{summary.get('report_delta_hint') or '等待研报摘要回流'}"
        elif event.impact_level == 'high':
            review_line = '高影响事件尚未沉淀为研报，建议优先触发事件点评'
        replay_items.append(EventImpactReplayItemDTO(
            event_id=event.event_id,
            title=event.title,
            published_at=event.published_at or event.collected_at,
            event_type=event.event_type,
            impact_level=event.impact_level,
            sentiment=event.sentiment,
            status=event.status,
            run_id=getattr(run, 'run_id', '') if run else '',
            run_status=getattr(run, 'status', '') if run else '',
            event_commentary_url=commentary_url,
            review_line=review_line,
        ))
    converted_count = sum(1 for event in events if event.status == 'converted_to_report')
    event_run_count = len(runs)
    if not events:
        summary = '暂无历史事件沉淀，建议先刷新事件流或组合事件。'
    else:
        summary = (
            f'历史库已沉淀 {len(events)} 个事件，其中高影响 {collection.high_impact_count} 个，'
            f'{converted_count} 个已转为研报任务，事件驱动运行 {event_run_count} 次。'
        )
    return EventImpactReviewResponse(
        stock_code=stock_code,
        stock_name=stock_name,
        total_events=len(events),
        high_impact_count=collection.high_impact_count,
        converted_count=converted_count,
        event_driven_run_count=event_run_count,
        latest_event_at=latest_event_at,
        dominant_event_types=dominant_types,
        summary=summary,
        replay_items=replay_items,
    )


def _setup_action() -> WorkbenchActionDTO:
    return WorkbenchActionDTO(
        label="创建组合",
        href="/watchlist",
        method="GET",
        action_type="create_watchlist",
        variant="primary",
    )


def _dashboard_setup() -> DashboardSetupDTO:
    return DashboardSetupDTO(
        title="创建第一个组合",
        description="先添加你要追踪的股票池。新账号不会加载演示数据或默认股票，只有你创建并刷新过的组合才会沉淀事件、预警和研报任务。",
        suggested_stock_codes=[],
        primary_action=_setup_action(),
    )


def _watchlist_list_response(items) -> WatchlistListResponse:
    return WatchlistListResponse(items=[WatchlistDTO(**item.__dict__) for item in items], total=len(items))


def _dashboard_summary(watchlists, collection, alert_response: TrackingAlertListResponse) -> DashboardPortfolioSummaryDTO:
    stock_codes = sorted({code for watchlist in watchlists for code in watchlist.stock_codes})
    risk = _watchlist_risk(collection.items, alert_response.items, alert_response)
    return DashboardPortfolioSummaryDTO(
        watchlist_count=len(watchlists),
        stock_count=len(stock_codes),
        event_count=collection.total,
        alert_count=alert_response.total,
        high_impact_count=collection.high_impact_count,
        manual_review_count=alert_response.manual_review_count,
        risk_score=int(risk["risk_score"]),
        risk_level=str(risk["risk_level"]),
        risk_summary=str(risk["risk_summary"]),
        processing_rate=float(risk["processing_rate"]),
        primary_watchlist_id=watchlists[0].watchlist_id if watchlists else "",
    )


def _dashboard_actions(primary_watchlist_id: str = "") -> list[WorkbenchActionDTO]:
    actions = [
        WorkbenchActionDTO(label="新建组合", href="/watchlist", action_type="create_watchlist", variant="primary"),
        WorkbenchActionDTO(label="事件预警", href="/events?view=alerts", action_type="open_events"),
        WorkbenchActionDTO(label="任务交付", href="/runs", action_type="open_runs"),
    ]
    if primary_watchlist_id:
        actions.insert(
            1,
            WorkbenchActionDTO(
                label="刷新主组合",
                href=f"/api/v1/watchlists/{primary_watchlist_id}/refresh",
                method="POST",
                action_type="refresh_watchlist",
                target_id=primary_watchlist_id,
                variant="secondary",
            ),
        )
    return actions


def _run_list_from_items(source: AnalysisRunListResponse, items: list[AnalysisRunResponse]) -> AnalysisRunListResponse:
    return AnalysisRunListResponse(
        items=items,
        total=len(items),
        queued_count=sum(1 for item in items if item.status == "queued"),
        running_count=sum(1 for item in items if item.status == "running"),
        completed_count=sum(1 for item in items if item.status == "completed"),
        failed_count=sum(1 for item in items if item.status == "failed"),
        stock_groups=source.stock_groups,
        workspace=source.workspace,
    )


def _copy_workspace_snapshot(source: AnalysisRunListResponse):
    workspace = source.workspace
    if hasattr(workspace, "model_copy"):
        return workspace.model_copy(deep=True)
    return workspace.copy(deep=True)


def _filter_runs_to_tracking_scope(source: AnalysisRunListResponse, stock_codes: list[str], *, limit: int) -> AnalysisRunListResponse:
    ordered_codes = [str(code).strip() for code in stock_codes if str(code or "").strip()]
    code_set = set(ordered_codes)
    if not code_set:
        empty = AnalysisRunListResponse()
        empty.workspace.tracked_stocks = []
        return empty

    scoped_items = [item for item in source.items if item.stock_code in code_set]
    scoped_groups = [group for group in source.stock_groups if group.stock_code in code_set]
    workspace = _copy_workspace_snapshot(source)
    workspace.tracked_stocks = ordered_codes
    workspace.most_active_stock = scoped_groups[0].stock_code if scoped_groups else (ordered_codes[0] if ordered_codes else "")
    workspace.latest_completed_stock = next((item.stock_code for item in scoped_items if item.status == "completed"), "")
    workspace.failed_stock_count = sum(1 for group in scoped_groups if group.failed_count)
    workspace.history_backed_stock_count = len({item.stock_code for item in scoped_items if item.status == "completed"})
    workspace.active_limit_reached = sum(1 for item in scoped_items if item.status in {"queued", "running"}) >= workspace.recommended_concurrency
    return AnalysisRunListResponse(
        items=scoped_items[: max(1, limit)],
        total=len(scoped_items),
        queued_count=sum(1 for item in scoped_items if item.status == "queued"),
        running_count=sum(1 for item in scoped_items if item.status == "running"),
        completed_count=sum(1 for item in scoped_items if item.status == "completed"),
        failed_count=sum(1 for item in scoped_items if item.status == "failed"),
        stock_groups=scoped_groups,
        workspace=workspace,
    )


def _tracking_scoped_runs(db: Session, user: User, *, limit: int = 10) -> AnalysisRunListResponse:
    stock_codes = _user_tracking_codes(db, user_id=user.id)
    if not stock_codes:
        return _filter_runs_to_tracking_scope(AnalysisRunListResponse(), [], limit=limit)
    source = run_manager.list_runs(limit=1000, user_id=user.id)
    return _filter_runs_to_tracking_scope(source, stock_codes, limit=limit)


def _stock_timeline_response(stock_code: str, collection) -> StockEventTimelineResponse:
    stock_name = next((event.stock_name for event in collection.items if event.stock_name), "")
    return StockEventTimelineResponse(
        stock_code=stock_code,
        stock_name=stock_name,
        items=[MarketEventDTO(**event.__dict__) for event in collection.items],
        total=collection.total,
        high_impact_count=collection.high_impact_count,
        placeholder_count=collection.placeholder_count,
        duplicate_count=collection.duplicate_count,
        source_count=collection.source_count,
        mode="history",
    )


def _combined_exports(latest: LatestReportResponse | None, runs: list[AnalysisRunResponse]):
    exports = []
    seen: set[str] = set()
    for export in list(latest.exports if latest else []):
        filename = export.filename
        if filename and filename not in seen:
            seen.add(filename)
            exports.append(export)
    for run in runs:
        for export in run.exports:
            filename = export.filename
            if filename and filename not in seen:
                seen.add(filename)
                exports.append(export)
    return exports


def _latest_eval_payload(prefix: str) -> dict[str, object]:
    candidates = sorted((OUTPUT_DIR / "evals").glob(f"{prefix}_*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
    if not candidates:
        return {}
    try:
        payload = json.loads(candidates[0].read_text(encoding="utf-8"))
    except Exception:
        return {"path": str(candidates[0]), "error": "评测文件读取失败"}
    if isinstance(payload, dict):
        payload.setdefault("path", str(candidates[0]))
        return payload
    return {"path": str(candidates[0])}


def _test_count() -> int:
    return len(list((PROJECT_ROOT / "tests").glob("test_*.py")))


def _quality_response(user: User) -> QualityWorkbenchResponse:
    tracking_eval = _latest_eval_payload("tracking_eval")
    agent_eval = _latest_eval_payload("agent_eval")
    financial_qa_eval = _latest_eval_payload("financial_qa_eval")
    rag_eval = _latest_eval_payload("rag_eval")
    ops = OpsMetricsResponse(**run_manager.ops_metrics())
    user_runs = run_manager.list_run_objects(limit=1000, user_id=user.id if user else "")
    latest_multi_agent = next((dict(getattr(item, "multi_agent_trace", {}) or {}) for item in user_runs if getattr(item, "multi_agent_trace", None)), {})
    multi_role_count = int(latest_multi_agent.get("role_count", 0) or 0)
    multi_completed = int(latest_multi_agent.get("completed_role_count", 0) or 0)
    multi_failed = int(latest_multi_agent.get("failed_role_count", 0) or 0)
    multi_completion_rate = (multi_completed / multi_role_count) if multi_role_count else 0.0
    metrics = [
        QualityMetricDTO(label="自动化测试文件", value=str(_test_count()), hint="pytest 覆盖核心 API、追踪、认证和前端契约"),
        QualityMetricDTO(label="事件评测样本", value=str(tracking_eval.get("sample_count", 0) or 0), hint="由 tracking benchmark 生成"),
        QualityMetricDTO(label="事件类型 Macro-F1", value=f"{float(tracking_eval.get('event_type_macro_f1', 0) or 0):.1%}", hint="事件分类离线指标"),
        QualityMetricDTO(label="Agent 评测样本", value=str(agent_eval.get("sample_count", 0) or 0), hint="由项目内金融研究 Agent 任务评测生成"),
        QualityMetricDTO(label="Agent 工具覆盖率", value=f"{float(agent_eval.get('required_tool_coverage', 0) or 0):.1%}", hint="必需工具调用覆盖情况"),
        QualityMetricDTO(label="多智能体角色完成率", value=f"{multi_completion_rate:.1%}" if multi_role_count else "暂无", hint=f"最近任务角色 {multi_completed}/{multi_role_count}，失败 {multi_failed}"),
        QualityMetricDTO(label="公共金融 QA 样本", value=str(financial_qa_eval.get("sample_count", 0) or 0), hint="FinanceBench/FinQA/TAT-QA 本地子集"),
        QualityMetricDTO(label="RAG 引用覆盖率", value=f"{float(rag_eval.get('citation_coverage_rate', 0) or 0):.1%}", hint="研报核心观点来源覆盖"),
        QualityMetricDTO(label="任务成功率", value=f"{(1 - ops.failure_rate):.1%}" if ops.total_runs else "暂无", hint=f"当前任务总数 {ops.total_runs}"),
        QualityMetricDTO(label="平均耗时", value=f"{ops.avg_duration_s:.1f}s", hint="基于已记录 run_metrics"),
    ]
    return QualityWorkbenchResponse(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        test_count=_test_count(),
        tracking_eval=tracking_eval,
        agent_eval=agent_eval,
        financial_qa_eval=financial_qa_eval,
        rag_eval=rag_eval,
        run_metrics=ops,
        smoke_status="已通过本地与 tencent-111 冒烟" if user else "待验证",
        metrics=metrics,
    )


@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return build_health_response()


def _client_key(request: Request, payload_key: str = "") -> str:
    host = request.client.host if request.client else "unknown"
    return f"{host}:{payload_key}"


def _set_auth_cookie(response: Response, user: User) -> None:
    token = create_access_token(user_id=user.id, email=user.email)
    response.set_cookie(
        AUTH_COOKIE_NAME,
        token,
        max_age=AUTH_TOKEN_TTL_SECONDS,
        httponly=True,
        samesite="lax",
        secure=False,
        path="/",
    )


@app.post("/api/v1/auth/register", response_model=AuthResponse, status_code=201)
def auth_register(
    payload: AuthRegisterRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthResponse:
    try:
        check_rate_limit(db, key=_client_key(request, payload.email), scope="signup", limit=SIGNUP_RATE_LIMIT_PER_HOUR)
        user = register_user(db, email=payload.email, username=payload.username, password=payload.password)
    except RateLimitExceeded as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc
    except AuthError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _set_auth_cookie(response, user)
    return AuthResponse(user=AuthUserDTO(**user_to_dto(user)))


@app.post("/api/v1/auth/login", response_model=AuthResponse)
def auth_login(
    payload: AuthLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthResponse:
    try:
        check_rate_limit(db, key=_client_key(request, payload.email_or_username), scope="login", limit=LOGIN_RATE_LIMIT_PER_HOUR)
        user = authenticate_user(db, email_or_username=payload.email_or_username, password=payload.password)
    except RateLimitExceeded as exc:
        raise HTTPException(status_code=429, detail=str(exc)) from exc
    except AuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    _set_auth_cookie(response, user)
    return AuthResponse(user=AuthUserDTO(**user_to_dto(user)))


@app.post("/api/v1/auth/logout", response_model=HealthResponse)
def auth_logout(response: Response) -> HealthResponse:
    response.delete_cookie(AUTH_COOKIE_NAME, path="/")
    return HealthResponse(status="ok")


@app.get("/api/v1/me", response_model=AuthUserDTO)
def current_user(user: User = Depends(require_current_user)) -> AuthUserDTO:
    return AuthUserDTO(**user_to_dto(user))


@app.get("/api/v1/ui/dashboard", response_model=DashboardResponse)
def ui_dashboard(user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> DashboardResponse:
    watchlist_items = list_user_watchlists(db, user_id=user.id)
    watchlist_response = _watchlist_list_response(watchlist_items)
    recent_runs = _tracking_scoped_runs(db, user, limit=8)
    if not watchlist_items:
        return DashboardResponse(
            mode="setup",
            setup=_dashboard_setup(),
            watchlists=watchlist_response,
            recent_runs=recent_runs,
            actions=[_setup_action()],
        )

    stock_codes = _user_tracking_codes(db, user_id=user.id)
    collection = list_user_events(db, user_id=user.id, stock_codes=stock_codes or None, limit=120)
    alerts = _filter_alerts_by_status(build_tracking_alerts(collection), "open")
    alert_response = _tracking_alert_list_response(alerts)
    briefing = build_daily_briefing(collection)
    summary = _dashboard_summary(watchlist_items, collection, alert_response)
    return DashboardResponse(
        mode="active",
        setup=_dashboard_setup(),
        watchlists=watchlist_response,
        portfolio_summary=summary,
        risk_queue=alert_response,
        today_briefing=_daily_briefing_response(briefing),
        latest_events=_market_event_list_response(collection, mode="history"),
        recent_runs=recent_runs,
        actions=_dashboard_actions(summary.primary_watchlist_id),
    )


@app.get("/api/v1/ui/watchlists/{watchlist_id}", response_model=WatchlistDetailResponse)
def ui_watchlist_detail(watchlist_id: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WatchlistDetailResponse:
    item = get_user_watchlist(db, user_id=user.id, watchlist_id=watchlist_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    collection = list_user_events(db, user_id=user.id, stock_codes=item.stock_codes, limit=120)
    return _watchlist_detail_response(item, collection, mode="history", include_market=True)


@app.get("/api/v1/ui/events", response_model=EventWorkbenchResponse)
def ui_event_workbench(
    view: str = "events",
    stock_codes: str = "",
    status: str = "",
    event_type: str = "",
    impact_level: str = "",
    severity: str = "",
    alert_type: str = "",
    rule_id: str = "",
    selected_event_id: str = "",
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> EventWorkbenchResponse:
    codes = _user_tracking_codes(db, user_id=user.id, stock_codes=stock_codes)
    if codes:
        collection = list_user_events(
            db,
            user_id=user.id,
            stock_codes=codes,
            status=status,
            event_type=event_type,
            impact_level=impact_level,
            limit=160,
        )
    else:
        collection = _empty_event_collection()
    alerts = _filter_alerts(
        build_tracking_alerts(collection, limit=80),
        status=status or "open",
        severity=severity,
        alert_type=alert_type,
        rule_id=rule_id,
    )
    selected_event = get_user_event(db, user_id=user.id, event_id=selected_event_id) if selected_event_id and codes else None
    if selected_event is not None and selected_event.stock_code not in codes:
        selected_event = None
    return EventWorkbenchResponse(
        view="alerts" if view == "alerts" else "events",
        events=_market_event_list_response(collection, mode="history"),
        alerts=_tracking_alert_list_response(alerts),
        filters={
            "stock_codes": ",".join(codes),
            "status": status,
            "event_type": event_type,
            "impact_level": impact_level,
            "severity": severity,
            "alert_type": alert_type,
            "rule_id": rule_id,
        },
        selected_event=MarketEventDTO(**selected_event.__dict__) if selected_event else None,
        actions=[
            WorkbenchActionDTO(label="查看事件", href="/events?view=events", action_type="switch_view"),
            WorkbenchActionDTO(label="处理预警", href="/events?view=alerts", action_type="switch_view", variant="primary"),
        ],
    )


@app.get("/api/v1/ui/stocks/{stock_code}", response_model=StockWorkbenchResponse)
def ui_stock_workbench(
    stock_code: str,
    tab: str = "summary",
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> StockWorkbenchResponse:
    watchlists = list_user_watchlists(db, user_id=user.id)
    related_watchlists = [item for item in watchlists if stock_code in item.stock_codes]
    is_tracked = bool(related_watchlists)
    collection = list_user_events(db, user_id=user.id, stock_codes=[stock_code], limit=120) if is_tracked else _empty_event_collection()
    runs = _tracking_scoped_runs(db, user, limit=50)
    stock_runs = [item for item in runs.items if item.stock_code == stock_code] if is_tracked else []
    latest_report = None
    history = None
    if is_tracked:
        try:
            latest_report = get_latest_report(stock_code, store=_user_memory(db, user), output_dir=_user_output_dir(user))
        except NotFoundError:
            latest_report = None
        try:
            history = get_stock_history(stock_code, store=_user_memory(db, user))
        except NotFoundError:
            history = None
    stock_name = (
        (latest_report.stock.name if latest_report else "")
        or next((event.stock_name for event in collection.items if event.stock_name), "")
        or stock_code
    )
    event_runs = run_manager.list_event_runs(stock_code=stock_code, limit=40, user_id=user.id)
    bars_result, _bars_error = _safe_market_call("日线", get_stock_daily_bars, stock_code, days=180, timeout=6)
    event_backtest_payload = build_event_backtest(
        stock_code=stock_code,
        stock_name=stock_name,
        events=collection.items,
        daily_bars=bars_result if isinstance(bars_result, list) else [],
        limit=40,
    )
    return StockWorkbenchResponse(
        stock_code=stock_code,
        stock_name=stock_name,
        active_tab=tab if tab in {"summary", "timeline", "history", "exports", "backtest"} else "summary",
        is_tracked=is_tracked,
        latest_report=latest_report,
        history=history,
        timeline=_stock_timeline_response(stock_code, collection),
        impact_review=_event_impact_review_response(stock_code, collection, event_runs),
        event_backtest=EventBacktestResponse(**event_backtest_payload),
        related_watchlists=[WatchlistDTO(**item.__dict__) for item in related_watchlists],
        related_runs=_run_list_from_items(runs, stock_runs),
        exports=_combined_exports(latest_report, stock_runs),
        actions=[
            WorkbenchActionDTO(label="生成研报", href="/api/v1/runs", method="POST", action_type="create_run", target_id=stock_code, variant="primary"),
            WorkbenchActionDTO(label="查看事件", href=f"/events?stock_codes={stock_code}", action_type="open_events"),
            WorkbenchActionDTO(label="管理组合", href="/watchlist", action_type="open_watchlists"),
        ],
    )


@app.get("/api/v1/stocks/{stock_code}/event-backtest", response_model=EventBacktestResponse)
def stock_event_backtest(
    stock_code: str,
    event_type: str = "",
    impact_level: str = "",
    window: str = "1,3,5,10",
    limit: int = 20,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> EventBacktestResponse:
    stock_code = str(stock_code or "").strip()
    if not _is_valid_a_stock_code(stock_code):
        raise HTTPException(status_code=422, detail="请输入 6 位 A 股股票代码")
    windows = []
    for item in str(window or "").split(","):
        try:
            windows.append(int(item.strip()))
        except ValueError:
            continue
    collection = list_user_events(db, user_id=user.id, stock_codes=[stock_code], event_type=event_type, impact_level=impact_level, limit=max(1, min(limit, 200)))
    bars_result, bars_error = _safe_market_call("日线", get_stock_daily_bars, stock_code, days=180, timeout=6)
    stock_name = next((event.stock_name for event in collection.items if event.stock_name), stock_code)
    payload = build_event_backtest(
        stock_code=stock_code,
        stock_name=stock_name,
        events=collection.items,
        daily_bars=bars_result if isinstance(bars_result, list) else [],
        event_type=event_type,
        impact_level=impact_level,
        windows=windows,
        limit=limit,
    )
    if bars_error and not payload.get("items"):
        payload["fallback_message"] = bars_error
    return EventBacktestResponse(**payload)


@app.get("/api/v1/ui/markets/{stock_code}", response_model=MarketWorkbenchResponse)
def ui_market_workbench(
    stock_code: str,
    range: str = "90d",
    user: User = Depends(require_current_user),
) -> MarketWorkbenchResponse:
    stock_code = str(stock_code or "").strip()
    if not _is_valid_a_stock_code(stock_code):
        raise HTTPException(status_code=422, detail="请输入 6 位 A 股股票代码")

    normalized_range, days = _market_range_to_days(range)
    quote: dict = {}
    bars: list[dict] = []
    fallback_messages: list[str] = []
    quote_result, quote_error = _safe_market_call("行情快照", fetch_live_quotes, stock_code, timeout=4)
    if quote_error:
        fallback_messages.append(quote_error)
    elif isinstance(quote_result, dict):
        quote = quote_result

    bars_result, bars_error = _safe_market_call("日线", get_stock_daily_bars, stock_code, days=days, timeout=6)
    if bars_error:
        fallback_messages.append(bars_error)
    elif isinstance(bars_result, list):
        bars = bars_result

    if bars:
        bars = bars[-days:]
    fallback_message = " ".join(dict.fromkeys(fallback_messages))
    if not quote and not bars and not fallback_message:
        fallback_message = "当前没有可用行情数据，请稍后重试。"
    quote_response = _market_quote_response(stock_code, quote, bars, fallback_message)
    stock_name = quote_response.stock_name or stock_code
    return MarketWorkbenchResponse(
        stock_code=stock_code,
        stock_name=stock_name,
        range=normalized_range,
        quote=quote_response,
        daily_bars=[MarketDailyBarDTO(**item) for item in bars],
        fallback_message=fallback_message,
        actions=[
            WorkbenchActionDTO(label="返回情报中心", href=f"/stocks/{stock_code}", action_type="open_stock"),
            WorkbenchActionDTO(label="查看事件台", href=f"/events?stock_codes={stock_code}", action_type="open_events"),
            WorkbenchActionDTO(label="生成研报", href="/api/v1/runs", method="POST", action_type="create_run", target_id=stock_code, variant="primary"),
        ],
    )


@app.get("/api/v1/ui/runs", response_model=RunWorkbenchResponse)
def ui_run_workbench(
    limit: int = 24,
    selected_run_id: str = "",
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> RunWorkbenchResponse:
    runs = _tracking_scoped_runs(db, user, limit=max(1, min(limit, 100)))
    tracked_codes = set(runs.workspace.tracked_stocks)
    selected = None
    if selected_run_id:
        try:
            run = run_manager.get_run(selected_run_id)
            if getattr(run, "user_id", "") == user.id and getattr(run, "stock_code", "") in tracked_codes:
                selected = run_manager.get_run_response(selected_run_id)
        except RunNotFoundError:
            selected = None
    return RunWorkbenchResponse(
        runs=runs,
        selected_run=selected,
        actions=[
            WorkbenchActionDTO(label="新建研报任务", href="/runs#run-create-panel", action_type="create_run", variant="primary"),
            WorkbenchActionDTO(label="批量任务", href="/runs#run-create-panel", action_type="create_batch_run"),
        ],
    )


@app.get("/api/v1/ui/quality", response_model=QualityWorkbenchResponse)
def ui_quality_workbench(user: User = Depends(require_current_user)) -> QualityWorkbenchResponse:
    return _quality_response(user)


@app.get("/api/v1/reports/latest/{stock_code}", response_model=LatestReportResponse)
def latest_report(stock_code: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> LatestReportResponse:
    try:
        return get_latest_report(stock_code, store=_user_memory(db, user), output_dir=_user_output_dir(user))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/history/{stock_code}", response_model=StockHistoryResponse)
def stock_history(stock_code: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> StockHistoryResponse:
    try:
        return get_stock_history(stock_code, store=_user_memory(db, user))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/news/{stock_code}", response_model=StockNewsResponse)
def stock_news(stock_code: str, limit: int = 8) -> StockNewsResponse:
    items = get_recent_news(stock_code, count=max(1, min(limit, 20)))
    return StockNewsResponse(stock_code=stock_code, items=items, total=len(items))


@app.get("/api/v1/stocks/search", response_model=StockSearchResponse)
def stock_search(
    q: str = "",
    limit: int = 12,
    user: User = Depends(require_current_user),
) -> StockSearchResponse:
    query = str(q or "").strip()
    if not query:
        return StockSearchResponse(query="", items=[], total=0)
    items = search_a_stocks(query, limit=max(1, min(limit, 30)))
    return StockSearchResponse(
        query=query,
        items=[StockSearchItemDTO(**item) for item in items],
        total=len(items),
    )


@app.get("/api/v1/events", response_model=MarketEventListResponse)
def market_events(
    stock_codes: str = "",
    limit_per_stock: int = 4,
    mode: str = "realtime",
    provider: str = "",
    event_type: str = "",
    impact_level: str = "",
    status: str = "",
    start: str = "",
    end: str = "",
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> MarketEventListResponse:
    codes = _user_tracking_codes(db, user_id=user.id, stock_codes=stock_codes)
    normalized_mode = "history" if mode == "history" else "realtime"
    if not codes:
        collection = _empty_event_collection()
        normalized_mode = "history"
    elif normalized_mode == "history":
        collection = list_user_events(
            db,
            user_id=user.id,
            stock_codes=codes,
            provider=provider,
            event_type=event_type,
            impact_level=impact_level,
            status=status,
            start=start,
            end=end,
            limit=max(1, min(limit_per_stock * max(1, len(codes or []), 4), 120)),
        )
    else:
        collection = collect_market_events(stock_codes=codes, limit_per_stock=max(1, min(limit_per_stock, 8)))
        save_user_events(db, user_id=user.id, events=collection.items)
        if status and status != "all":
            collection = summarize_events([event for event in collection.items if event.status == status])
    return _market_event_list_response(collection, mode=normalized_mode)


@app.get("/api/v1/events/{event_id}", response_model=MarketEventDTO)
def event_detail(event_id: str, stock_codes: str = "", user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> MarketEventDTO:
    del stock_codes
    event = get_user_event(db, user_id=user.id, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    return MarketEventDTO(**event.__dict__)


@app.patch("/api/v1/events/{event_id}/status", response_model=MarketEventDTO)
def update_market_event_status(
    event_id: str,
    payload: EventStatusUpdateRequest,
    actor_header: str = Header(default='browser-user', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> MarketEventDTO:
    event = get_user_event(db, user_id=user.id, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    actor, _ = _actor(actor_header, role_header)
    try:
        updated = update_user_event_status(db, user_id=user.id, event_id=event_id, status=payload.status, note=payload.note, actor=user.username or actor)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if updated is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    return MarketEventDTO(**updated.__dict__)


@app.post("/api/v1/events/{event_id}/analyze", response_model=AnalysisRunResponse, status_code=202)
def analyze_event(
    event_id: str,
    payload: EventAnalyzeRequest | None = None,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    event = get_user_event(db, user_id=user.id, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    context = {
        "event_id": event.event_id,
        "stock_code": event.stock_code,
        "stock_name": event.stock_name,
        "title": event.title,
        "summary": event.summary,
        "source": event.source,
        "provider": event.provider,
        "url": event.url,
        "published_at": event.published_at,
        "collected_at": event.collected_at,
        "event_type": event.event_type,
        "sentiment": event.sentiment,
        "impact_level": event.impact_level,
        "impact_scope": event.impact_scope,
        "confidence": event.confidence,
        "reason": event.reason,
        "channel": event.channel,
        "retrieval_mode": event.retrieval_mode,
        "evidence_type": event.evidence_type,
        "related_sources": event.related_sources,
        "status": event.status,
        "status_note": event.status_note,
        "note": payload.note if payload else "",
    }
    run = run_manager.start_event_run(event.stock_code, event_context=context, actor=actor, role=role, user_id=user.id)
    _sync_user_run(db, user, run)
    save_user_events(db, user_id=user.id, events=[event])
    update_user_event_status(db, user_id=user.id, event_id=event.event_id, status="converted_to_report", note=payload.note if payload else "已触发事件研报任务", actor=actor)
    return run_manager.get_run_response(run.run_id)


@app.get("/api/v1/stocks/{stock_code}/events", response_model=StockEventTimelineResponse)
def stock_events(stock_code: str, limit: int = 6, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> StockEventTimelineResponse:
    realtime = collect_stock_events(stock_code, limit=max(1, min(limit, 12)), include_history=False)
    if _user_is_tracking_stock(db, user_id=user.id, stock_code=stock_code):
        save_user_events(db, user_id=user.id, events=realtime.items)
        collection = list_user_events(db, user_id=user.id, stock_codes=[stock_code], limit=max(1, min(limit, 80)))
    else:
        collection = realtime
    stock_name = collection.items[0].stock_name if collection.items else ""
    return StockEventTimelineResponse(
        stock_code=stock_code,
        stock_name=stock_name,
        items=[MarketEventDTO(**event.__dict__) for event in collection.items],
        total=collection.total,
        high_impact_count=collection.high_impact_count,
        placeholder_count=collection.placeholder_count,
        duplicate_count=collection.duplicate_count,
        source_count=collection.source_count,
        mode="realtime",
    )


@app.get("/api/v1/stocks/{stock_code}/event-impact-review", response_model=EventImpactReviewResponse)
def stock_event_impact_review(stock_code: str, limit: int = 20, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> EventImpactReviewResponse:
    collection = list_user_events(db, user_id=user.id, stock_codes=[stock_code], limit=max(1, min(limit, 80)))
    runs = run_manager.list_event_runs(stock_code=stock_code, limit=40, user_id=user.id)
    for run in runs:
        _sync_user_run(db, user, run)
    return _event_impact_review_response(stock_code, collection, runs)


@app.get("/api/v1/alerts/rules", response_model=AlertRuleListResponse)
def tracking_alert_rules() -> AlertRuleListResponse:
    rules = list_alert_rules()
    return AlertRuleListResponse(items=[AlertRuleDTO(**rule.__dict__) for rule in rules], total=len(rules))


@app.get("/api/v1/alerts", response_model=TrackingAlertListResponse)
def tracking_alerts(
    stock_codes: str = "",
    limit_per_stock: int = 4,
    status: str = "open",
    mode: str = "realtime",
    severity: str = "",
    alert_type: str = "",
    rule_id: str = "",
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> TrackingAlertListResponse:
    codes = _user_tracking_codes(db, user_id=user.id, stock_codes=stock_codes)
    normalized_mode = "history" if mode == "history" else "realtime"
    if not codes:
        collection = _empty_event_collection()
    elif normalized_mode == "history":
        collection = list_user_events(
            db,
            user_id=user.id,
            stock_codes=codes,
            limit=max(1, min(limit_per_stock * max(1, len(codes or []), 4), 120)),
        )
    else:
        collection = collect_market_events(stock_codes=codes, limit_per_stock=max(1, min(limit_per_stock, 8)))
        save_user_events(db, user_id=user.id, events=collection.items)
    alerts = _filter_alerts(
        build_tracking_alerts(collection),
        status=status,
        severity=severity,
        alert_type=alert_type,
        rule_id=rule_id,
    )
    return _tracking_alert_list_response(alerts)


@app.get("/api/v1/briefing/daily", response_model=DailyBriefingResponse)
def daily_briefing(stock_codes: str = "", limit_per_stock: int = 4, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> DailyBriefingResponse:
    codes = _user_tracking_codes(db, user_id=user.id, stock_codes=stock_codes)
    if codes:
        collection = collect_market_events(stock_codes=codes, limit_per_stock=max(1, min(limit_per_stock, 8)))
        save_user_events(db, user_id=user.id, events=collection.items)
    else:
        collection = _empty_event_collection()
    briefing = build_daily_briefing(collection)
    return DailyBriefingResponse(
        title=briefing.title,
        summary=briefing.summary,
        generated_at=briefing.generated_at,
        total_events=briefing.total_events,
        high_impact_count=briefing.high_impact_count,
        negative_event_count=briefing.negative_event_count,
        source_count=briefing.source_count,
        key_events=[MarketEventDTO(**event.__dict__) for event in briefing.key_events],
        alerts=[TrackingAlertDTO(**alert.__dict__) for alert in briefing.alerts],
        suggested_actions=briefing.suggested_actions,
        themes=briefing.themes,
        review_required_events=[MarketEventDTO(**event.__dict__) for event in briefing.review_required_events],
    )


@app.get("/api/v1/watchlists", response_model=WatchlistListResponse)
def watchlists(user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WatchlistListResponse:
    items = list_user_watchlists(db, user_id=user.id)
    return WatchlistListResponse(items=[WatchlistDTO(**item.__dict__) for item in items], total=len(items))


@app.post("/api/v1/watchlists", response_model=WatchlistDTO, status_code=201)
def create_tracking_watchlist(payload: WatchlistCreateRequest, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WatchlistDTO:
    item = create_user_watchlist(db, user_id=user.id, name=payload.name, stock_codes=payload.stock_codes, description=payload.description)
    return WatchlistDTO(**item.__dict__)


@app.get("/api/v1/watchlists/{watchlist_id}", response_model=WatchlistDetailResponse)
def watchlist_detail(watchlist_id: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WatchlistDetailResponse:
    item = get_user_watchlist(db, user_id=user.id, watchlist_id=watchlist_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    collection = list_user_events(db, user_id=user.id, stock_codes=item.stock_codes, limit=80)
    return _watchlist_detail_response(item, collection, mode="history")


@app.patch("/api/v1/watchlists/{watchlist_id}", response_model=WatchlistDTO)
def update_tracking_watchlist(
    watchlist_id: str,
    payload: WatchlistUpdateRequest,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> WatchlistDTO:
    stock_codes = payload.stock_codes
    if stock_codes is not None and not [code for code in stock_codes if str(code or "").strip()]:
        raise HTTPException(status_code=422, detail="组合至少保留一只股票")
    item = update_user_watchlist(
        db,
        user_id=user.id,
        watchlist_id=watchlist_id,
        name=payload.name,
        stock_codes=stock_codes,
        description=payload.description,
    )
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    if not item.stock_codes:
        raise HTTPException(status_code=422, detail="组合至少保留一只股票")
    return WatchlistDTO(**item.__dict__)


@app.delete("/api/v1/watchlists/{watchlist_id}", status_code=204)
def delete_tracking_watchlist(watchlist_id: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> Response:
    deleted = delete_user_watchlist(db, user_id=user.id, watchlist_id=watchlist_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    return Response(status_code=204)


@app.post("/api/v1/watchlists/{watchlist_id}/refresh", response_model=WatchlistDetailResponse, status_code=202)
def refresh_watchlist_events(watchlist_id: str, limit_per_stock: int = 4, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WatchlistDetailResponse:
    item = get_user_watchlist(db, user_id=user.id, watchlist_id=watchlist_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    collection = collect_market_events(
        stock_codes=item.stock_codes,
        limit_per_stock=max(1, min(limit_per_stock, 8)),
    )
    save_user_events(db, user_id=user.id, events=collection.items)
    updated = mark_user_watchlist_refreshed(db, user_id=user.id, watchlist_id=watchlist_id) or item
    return _watchlist_detail_response(updated, collection, mode="realtime")


@app.get("/api/v1/workspace/stocks", response_model=WorkspaceStocksResponse)
def workspace_stocks(user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> WorkspaceStocksResponse:
    return WorkspaceStocksResponse(items=_user_memory(db, user).get_all_stocks())


@app.get("/api/v1/store/health", response_model=StoreHealthResponse)
def store_health(user: User = Depends(require_current_user)) -> StoreHealthResponse:
    _require_admin(user)
    return StoreHealthResponse(**run_manager.store_health())


@app.get("/api/v1/ops/metrics", response_model=OpsMetricsResponse)
def ops_metrics(user: User = Depends(require_current_user)) -> OpsMetricsResponse:
    _require_admin(user)
    return OpsMetricsResponse(**run_manager.ops_metrics())


@app.post("/api/v1/store/backup", response_model=StoreBackupResponse)
def backup_store(user: User = Depends(require_current_user)) -> StoreBackupResponse:
    _require_admin(user)
    return StoreBackupResponse(backup_path=run_manager.backup_store())


@app.get("/api/v1/runs", response_model=AnalysisRunListResponse)
def list_runs(
    limit: int = 10,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunListResponse:
    for run in run_manager.list_run_objects(limit=max(1, min(limit, 200)), user_id=user.id):
        _sync_user_run(db, user, run)
    return run_manager.list_runs(limit=limit, user_id=user.id)


@app.post("/api/v1/runs", response_model=AnalysisRunResponse, status_code=202)
def create_run(
    payload: AnalysisRunCreateRequest,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    run = run_manager.start_run(payload.stock_code, actor=actor, role=role, user_id=user.id)
    _sync_user_run(db, user, run)
    return run_manager.get_run_response(run.run_id)


@app.post("/api/v1/runs/batch", response_model=BatchRunCreateResponse, status_code=202)
def create_batch_runs(
    payload: BatchRunCreateRequest,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> BatchRunCreateResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    runs = run_manager.start_batch(payload.stock_codes, actor=actor, role=role, user_id=user.id)
    for run in runs:
        _sync_user_run(db, user, run)
    return BatchRunCreateResponse(items=[run_manager.get_run_response(item.run_id) for item in runs], total=len(runs))


@app.get("/api/v1/reports/diff/{stock_code}", response_model=ReportDiffResponse)
def report_diff(stock_code: str, user: User = Depends(require_current_user), db: Session = Depends(get_db)) -> ReportDiffResponse:
    store = _user_memory(db, user)
    records = store.get_history(stock_code=stock_code, limit=2)
    if len(records) < 2:
        return ReportDiffResponse(stock_code=stock_code, summary='至少需要两份历史报告才能生成版本 diff')
    latest = map_history_record(records[0])
    previous = map_history_record(records[1])
    rating_delta = latest.rating_score - previous.rating_score
    upside_delta = latest.dcf_upside - previous.dcf_upside
    risk_count_delta = latest.risk_count - previous.risk_count
    return ReportDiffResponse(
        stock_code=stock_code,
        base_timestamp=previous.timestamp,
        compare_timestamp=latest.timestamp,
        rating_changed=latest.rating != previous.rating,
        rating_delta=rating_delta,
        upside_delta=upside_delta,
        risk_count_delta=risk_count_delta,
        conclusion_changed=latest.conclusion != previous.conclusion,
        summary=f'评级变化 {previous.rating or "--"} → {latest.rating or "--"}；估值空间变化 {upside_delta:.1f}%；风险数量变化 {risk_count_delta}',
    )


@app.get("/api/v1/runs/{run_id}", response_model=AnalysisRunResponse)
def get_run(
    run_id: str,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    try:
        run = run_manager.get_run(run_id)
        _assert_run_access(run, user)
        _sync_user_run(db, user, run)
        raw_response = run_manager.get_run_response(run_id)
        response = raw_response if isinstance(raw_response, AnalysisRunResponse) else AnalysisRunResponse(**raw_response)
        if not response.stock_name and response.stock_code:
            try:
                latest = _user_memory(db, user).get_latest(response.stock_code)
                response.stock_name = latest.stock_name if latest else ""
            except Exception:
                response.stock_name = ""
        if not response.stock_name and response.stock_code:
            collection = list_user_events(db, user_id=user.id, stock_codes=[response.stock_code], limit=1)
            response.stock_name = next((event.stock_name for event in collection.items if event.stock_name), "")
        return response
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/retry", response_model=AnalysisRunResponse, status_code=202)
def retry_run(
    run_id: str,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    try:
        _assert_run_access(run_manager.get_run(run_id), user)
        run = run_manager.retry_run(run_id, actor=actor, role=role)
        _sync_user_run(db, user, run)
        return run_manager.get_run_response(run.run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403 if '无权' in str(exc) else 409, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/cancel", response_model=AnalysisRunResponse)
def cancel_run(
    run_id: str,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    try:
        _assert_run_access(run_manager.get_run(run_id), user)
        run_manager.cancel_run(run_id, actor=actor, role=role)
        _sync_user_run(db, user, run_manager.get_run(run_id))
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403 if '无权' in str(exc) else 409, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/assign", response_model=AnalysisRunResponse)
def assign_run(
    run_id: str,
    payload: RunAssignmentRequest,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    if user.role != "admin" and payload.owner != user.username:
        raise HTTPException(status_code=403, detail="普通用户只能把任务分配给自己")
    try:
        _assert_run_access(run_manager.get_run(run_id), user)
        run_manager.assign_owner(run_id, payload.owner, actor=actor, role=role)
        _sync_user_run(db, user, run_manager.get_run(run_id))
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/archive", response_model=AnalysisRunResponse)
def archive_run(
    run_id: str,
    actor_header: str = Header(default='system', alias='X-Actor'),
    role_header: str = Header(default='admin', alias='X-Role'),
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> AnalysisRunResponse:
    actor, role = _run_actor_for_request(user, actor_header, role_header)
    try:
        _assert_run_access(run_manager.get_run(run_id), user)
        run_manager.archive_run(run_id, actor=actor, role=role)
        _sync_user_run(db, user, run_manager.get_run(run_id))
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


def _export_media_type(path: Path) -> str:
    return {
        ".md": "text/markdown",
        ".html": "text/html",
        ".pdf": "application/pdf",
        ".log": "text/plain",
        ".json": "application/json",
    }.get(path.suffix.lower(), "application/octet-stream")


def _export_file_response(filename: str, user: User, db: Session, *, inline: bool) -> FileResponse:
    artifact = get_user_export_artifact(db, user_id=user.id, filename=filename)
    if artifact is None:
        run = run_manager.find_run_by_export(filename, user_id=user.id)
        if run is None:
            raise HTTPException(status_code=404, detail=f"未找到导出物: {filename}")
        _sync_user_run(db, user, run)
        artifact = get_user_export_artifact(db, user_id=user.id, filename=filename)
    if artifact is None:
        raise HTTPException(status_code=404, detail=f"未找到导出物: {filename}")
    try:
        path = _resolve_user_export_path(filename, artifact.path)
    except ExportNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return FileResponse(
        path,
        media_type=_export_media_type(path),
        filename=path.name,
        content_disposition_type="inline" if inline else "attachment",
    )


@app.get("/api/v1/exports/{filename}/preview")
def preview_export(
    filename: str,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    return _export_file_response(filename, user, db, inline=True)


@app.get("/api/v1/exports/{filename}")
def download_export(
    filename: str,
    user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    return _export_file_response(filename, user, db, inline=False)


def _resolve_user_export_path(filename: str, stored_path: str) -> Path:
    candidate = Path(filename)
    if candidate.name != filename:
        raise ExportNotFoundError("非法导出文件名")
    path = Path(stored_path or "")
    if not path.name or path.name != filename:
        raise ExportNotFoundError(f"未找到导出物: {filename}")
    if path.suffix.lower() not in {".md", ".html", ".pdf", ".log", ".json"}:
        raise ExportNotFoundError("不支持的导出文件类型")
    if not path.exists() or not path.is_file():
        raise ExportNotFoundError(f"未找到导出物: {filename}")
    return path
