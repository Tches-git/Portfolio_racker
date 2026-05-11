"""产品前端 API 入口（兼容 Phase 1/2）。"""
from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.download import ExportNotFoundError, resolve_export_file
from app.api.mappers import build_health_response, map_history_record
from app.api.run_manager import RunActionError, RunNotFoundError, run_manager
from app.api.schemas import AnalysisRunCreateRequest, AnalysisRunListResponse, AnalysisRunResponse, BatchRunCreateRequest, BatchRunCreateResponse, DailyBriefingResponse, EventAnalyzeRequest, EventImpactReplayItemDTO, EventImpactReviewResponse, EventStatusUpdateRequest, HealthResponse, LatestReportResponse, MarketEventDTO, MarketEventListResponse, OpsMetricsResponse, ReportDiffResponse, RunAssignmentRequest, StockEventTimelineResponse, StockHistoryResponse, StockNewsResponse, StoreBackupResponse, StoreHealthResponse, TrackingAlertDTO, TrackingAlertListResponse, WatchlistCreateRequest, WatchlistDTO, WatchlistDetailResponse, WatchlistImpactStockDTO, WatchlistListResponse, WatchlistSummaryDTO, WorkspaceStocksResponse
from app.api.services import NotFoundError, get_latest_report, get_stock_history
from app.data_source.akshare_client import get_recent_news
from app.memory.store import get_memory_store
from app.tracking.service import collect_historical_events, collect_market_events, collect_stock_events, find_market_event, summarize_events
from app.tracking.history import save_events, update_event_status
from app.tracking.alerts import build_tracking_alerts
from app.tracking.briefing import build_daily_briefing
from app.tracking.watchlist import create_watchlist, get_watchlist, list_watchlists, mark_watchlist_refreshed

app = FastAPI(title="AI Research Assistant API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _actor(actor: str = Header(default='system', alias='X-Actor'), role: str = Header(default='admin', alias='X-Role')) -> tuple[str, str]:
    return actor or 'system', role or 'viewer'


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


def _tracking_alert_list_response(alerts) -> TrackingAlertListResponse:
    return TrackingAlertListResponse(
        items=[TrackingAlertDTO(**alert.__dict__) for alert in alerts],
        total=len(alerts),
        high_severity_count=sum(1 for alert in alerts if alert.severity == "high"),
        risk_alert_count=sum(1 for alert in alerts if alert.alert_type == "risk_watch"),
        source_degraded_count=sum(1 for alert in alerts if alert.alert_type == "source_degraded"),
    )


def _filter_alerts_by_status(alerts, status: str):
    normalized = status or "open"
    if normalized == "all":
        return alerts
    return [alert for alert in alerts if alert.status == normalized]


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


def _watchlist_detail_response(watchlist, collection, *, mode: str = "history") -> WatchlistDetailResponse:
    alerts = _filter_alerts_by_status(build_tracking_alerts(collection), "open")
    briefing = build_daily_briefing(collection, title=f"{watchlist.name} 组合简报")
    alert_response = _tracking_alert_list_response(alerts)
    impacted_stocks = _rank_impacted_stocks(collection.items)
    summary = WatchlistSummaryDTO(
        stock_count=len(watchlist.stock_codes),
        event_count=collection.total,
        high_impact_count=collection.high_impact_count,
        alert_count=alert_response.total,
        high_severity_count=alert_response.high_severity_count,
        source_count=collection.source_count,
        placeholder_count=collection.placeholder_count,
        last_refreshed_at=watchlist.last_refreshed_at,
        impacted_stocks=impacted_stocks,
    )
    return WatchlistDetailResponse(
        watchlist=WatchlistDTO(**watchlist.__dict__),
        events=_market_event_list_response(collection, mode=mode),
        alerts=alert_response,
        briefing=_daily_briefing_response(briefing),
        summary=summary,
    )


def _rank_impacted_stocks(events) -> list[WatchlistImpactStockDTO]:
    grouped: dict[str, dict[str, object]] = {}
    for event in events:
        code = event.stock_code
        if not code:
            continue
        event_time = event.published_at or event.collected_at
        current = grouped.setdefault(
            code,
            {"stock_code": code, "stock_name": event.stock_name, "event_count": 0, "high_impact_count": 0, "latest_event_at": ""},
        )
        current["event_count"] = int(current["event_count"]) + 1
        current["stock_name"] = current["stock_name"] or event.stock_name
        if event.impact_level == "high":
            current["high_impact_count"] = int(current["high_impact_count"]) + 1
        if event_time and event_time > str(current["latest_event_at"]):
            current["latest_event_at"] = event_time
    ranked = sorted(
        grouped.values(),
        key=lambda item: (int(item["high_impact_count"]), int(item["event_count"]), str(item["latest_event_at"])),
        reverse=True,
    )
    return [WatchlistImpactStockDTO(**item) for item in ranked]


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


@app.get("/api/v1/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return build_health_response()


@app.get("/api/v1/reports/latest/{stock_code}", response_model=LatestReportResponse)
def latest_report(stock_code: str) -> LatestReportResponse:
    try:
        return get_latest_report(stock_code)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/history/{stock_code}", response_model=StockHistoryResponse)
def stock_history(stock_code: str) -> StockHistoryResponse:
    try:
        return get_stock_history(stock_code)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/v1/news/{stock_code}", response_model=StockNewsResponse)
def stock_news(stock_code: str, limit: int = 8) -> StockNewsResponse:
    items = get_recent_news(stock_code, count=max(1, min(limit, 20)))
    return StockNewsResponse(stock_code=stock_code, items=items, total=len(items))


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
) -> MarketEventListResponse:
    codes = [part.strip() for part in stock_codes.split(",") if part.strip()] if stock_codes else None
    normalized_mode = "history" if mode == "history" else "realtime"
    if normalized_mode == "history":
        collection = collect_historical_events(
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
        if status and status != "all":
            collection = summarize_events([event for event in collection.items if event.status == status])
    return _market_event_list_response(collection, mode=normalized_mode)


@app.get("/api/v1/events/{event_id}", response_model=MarketEventDTO)
def event_detail(event_id: str, stock_codes: str = "") -> MarketEventDTO:
    codes = [part.strip() for part in stock_codes.split(",") if part.strip()] if stock_codes else None
    event = find_market_event(event_id, stock_codes=codes)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    return MarketEventDTO(**event.__dict__)


@app.patch("/api/v1/events/{event_id}/status", response_model=MarketEventDTO)
def update_market_event_status(event_id: str, payload: EventStatusUpdateRequest) -> MarketEventDTO:
    event = find_market_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    save_events([event])
    try:
        updated = update_event_status(event_id, payload.status, note=payload.note)
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
) -> AnalysisRunResponse:
    event = find_market_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"未找到事件: {event_id}")
    actor, role = _actor(actor_header, role_header)
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
    run = run_manager.start_event_run(event.stock_code, event_context=context, actor=actor, role=role)
    save_events([event])
    update_event_status(event.event_id, "converted_to_report", note=payload.note if payload else "已触发事件研报任务")
    return run_manager.get_run_response(run.run_id)


@app.get("/api/v1/stocks/{stock_code}/events", response_model=StockEventTimelineResponse)
def stock_events(stock_code: str, limit: int = 6) -> StockEventTimelineResponse:
    collection = collect_stock_events(stock_code, limit=max(1, min(limit, 12)), include_history=True)
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
def stock_event_impact_review(stock_code: str, limit: int = 20) -> EventImpactReviewResponse:
    collection = collect_historical_events(stock_codes=[stock_code], limit=max(1, min(limit, 80)))
    runs = run_manager.list_event_runs(stock_code=stock_code, limit=40)
    return _event_impact_review_response(stock_code, collection, runs)


@app.get("/api/v1/alerts", response_model=TrackingAlertListResponse)
def tracking_alerts(stock_codes: str = "", limit_per_stock: int = 4, status: str = "open") -> TrackingAlertListResponse:
    codes = [part.strip() for part in stock_codes.split(",") if part.strip()] if stock_codes else None
    collection = collect_market_events(stock_codes=codes, limit_per_stock=max(1, min(limit_per_stock, 8)))
    alerts = _filter_alerts_by_status(build_tracking_alerts(collection), status)
    return _tracking_alert_list_response(alerts)


@app.get("/api/v1/briefing/daily", response_model=DailyBriefingResponse)
def daily_briefing(stock_codes: str = "", limit_per_stock: int = 4) -> DailyBriefingResponse:
    codes = [part.strip() for part in stock_codes.split(",") if part.strip()] if stock_codes else None
    collection = collect_market_events(stock_codes=codes, limit_per_stock=max(1, min(limit_per_stock, 8)))
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
def watchlists() -> WatchlistListResponse:
    items = list_watchlists()
    return WatchlistListResponse(items=[WatchlistDTO(**item.__dict__) for item in items], total=len(items))


@app.post("/api/v1/watchlists", response_model=WatchlistDTO, status_code=201)
def create_tracking_watchlist(payload: WatchlistCreateRequest) -> WatchlistDTO:
    item = create_watchlist(payload.name, payload.stock_codes, description=payload.description)
    return WatchlistDTO(**item.__dict__)


@app.get("/api/v1/watchlists/{watchlist_id}", response_model=WatchlistDetailResponse)
def watchlist_detail(watchlist_id: str) -> WatchlistDetailResponse:
    item = get_watchlist(watchlist_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    collection = collect_historical_events(stock_codes=item.stock_codes, limit=80)
    return _watchlist_detail_response(item, collection, mode="history")


@app.post("/api/v1/watchlists/{watchlist_id}/refresh", response_model=WatchlistDetailResponse, status_code=202)
def refresh_watchlist_events(watchlist_id: str, limit_per_stock: int = 4) -> WatchlistDetailResponse:
    item = get_watchlist(watchlist_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"未找到组合: {watchlist_id}")
    collection = collect_market_events(
        stock_codes=item.stock_codes,
        limit_per_stock=max(1, min(limit_per_stock, 8)),
    )
    updated = mark_watchlist_refreshed(watchlist_id) or item
    return _watchlist_detail_response(updated, collection, mode="realtime")


@app.get("/api/v1/workspace/stocks", response_model=WorkspaceStocksResponse)
def workspace_stocks() -> WorkspaceStocksResponse:
    store = get_memory_store()
    return WorkspaceStocksResponse(items=store.get_all_stocks())


@app.get("/api/v1/store/health", response_model=StoreHealthResponse)
def store_health() -> StoreHealthResponse:
    return StoreHealthResponse(**run_manager.store_health())


@app.get("/api/v1/ops/metrics", response_model=OpsMetricsResponse)
def ops_metrics() -> OpsMetricsResponse:
    return OpsMetricsResponse(**run_manager.ops_metrics())


@app.post("/api/v1/store/backup", response_model=StoreBackupResponse)
def backup_store(actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> StoreBackupResponse:
    _actor(actor_header, role_header)
    return StoreBackupResponse(backup_path=run_manager.backup_store())


@app.get("/api/v1/runs", response_model=AnalysisRunListResponse)
def list_runs(limit: int = 10) -> AnalysisRunListResponse:
    return run_manager.list_runs(limit=limit)


@app.post("/api/v1/runs", response_model=AnalysisRunResponse, status_code=202)
def create_run(payload: AnalysisRunCreateRequest, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> AnalysisRunResponse:
    actor, role = _actor(actor_header, role_header)
    run = run_manager.start_run(payload.stock_code, actor=actor, role=role)
    return run_manager.get_run_response(run.run_id)


@app.post("/api/v1/runs/batch", response_model=BatchRunCreateResponse, status_code=202)
def create_batch_runs(payload: BatchRunCreateRequest, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> BatchRunCreateResponse:
    actor, role = _actor(actor_header, role_header)
    runs = run_manager.start_batch(payload.stock_codes, actor=actor, role=role)
    return BatchRunCreateResponse(items=[run_manager.get_run_response(item.run_id) for item in runs], total=len(runs))


@app.get("/api/v1/reports/diff/{stock_code}", response_model=ReportDiffResponse)
def report_diff(stock_code: str) -> ReportDiffResponse:
    store = get_memory_store()
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
def get_run(run_id: str) -> AnalysisRunResponse:
    try:
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/retry", response_model=AnalysisRunResponse, status_code=202)
def retry_run(run_id: str, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> AnalysisRunResponse:
    actor, role = _actor(actor_header, role_header)
    try:
        run = run_manager.retry_run(run_id, actor=actor, role=role)
        return run_manager.get_run_response(run.run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403 if '无权' in str(exc) else 409, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/cancel", response_model=AnalysisRunResponse)
def cancel_run(run_id: str, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> AnalysisRunResponse:
    actor, role = _actor(actor_header, role_header)
    try:
        run_manager.cancel_run(run_id, actor=actor, role=role)
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403 if '无权' in str(exc) else 409, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/assign", response_model=AnalysisRunResponse)
def assign_run(run_id: str, payload: RunAssignmentRequest, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> AnalysisRunResponse:
    actor, role = _actor(actor_header, role_header)
    try:
        run_manager.assign_owner(run_id, payload.owner, actor=actor, role=role)
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/api/v1/runs/{run_id}/archive", response_model=AnalysisRunResponse)
def archive_run(run_id: str, actor_header: str = Header(default='system', alias='X-Actor'), role_header: str = Header(default='admin', alias='X-Role')) -> AnalysisRunResponse:
    actor, role = _actor(actor_header, role_header)
    try:
        run_manager.archive_run(run_id, actor=actor, role=role)
        return run_manager.get_run_response(run_id)
    except RunNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RunActionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.get("/api/v1/exports/{filename}")
def download_export(filename: str) -> FileResponse:
    try:
        path = resolve_export_file(filename)
    except ExportNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    media_type = {
        ".md": "text/markdown",
        ".html": "text/html",
        ".pdf": "application/pdf",
        ".log": "text/plain",
        ".json": "application/json",
    }.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path, media_type=media_type, filename=path.name)
