from __future__ import annotations

from types import SimpleNamespace

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.auth.security import hash_password, verify_password
from app.db.base import Base
from app.db.models import User
from app.db.repositories import create_user_watchlist, get_user_export_artifact, list_user_events, list_user_watchlists, save_user_events, save_user_run, user_has_export
from app.memory.db_store import UserMemoryStore
from app.models import AnalysisState, DCFResult, FinancialMetrics, StockProfile
from app.tracking.models import MarketEvent


def _session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, future=True)
    return Session()


def test_password_hash_is_not_plaintext_and_verifies():
    password_hash = hash_password("Secret123!")

    assert password_hash != "Secret123!"
    assert verify_password("Secret123!", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_user_watchlists_are_isolated_by_user_id():
    db = _session()
    user_a = User(email="a@example.com", username="alice", password_hash="x")
    user_b = User(email="b@example.com", username="bob", password_hash="x")
    db.add_all([user_a, user_b])
    db.commit()

    create_user_watchlist(db, user_id=user_a.id, name="A 组合", stock_codes=["600519"])
    create_user_watchlist(db, user_id=user_b.id, name="B 组合", stock_codes=["000858"])

    assert list_user_watchlists(db, user_id=user_a.id)[0].stock_codes == ["600519"]
    assert list_user_watchlists(db, user_id=user_b.id)[0].stock_codes == ["000858"]


def test_new_user_watchlist_list_starts_empty():
    db = _session()
    user = User(email="empty@example.com", username="empty", password_hash="x")
    db.add(user)
    db.commit()

    assert list_user_watchlists(db, user_id=user.id) == []


def test_user_events_are_isolated_and_deduped():
    db = _session()
    user_a = User(email="a@example.com", username="alice", password_hash="x")
    user_b = User(email="b@example.com", username="bob", password_hash="x")
    db.add_all([user_a, user_b])
    db.commit()

    event = MarketEvent(event_id="event_1", stock_code="600519", title="重大公告", url="https://example.com/a")
    save_user_events(db, user_id=user_a.id, events=[event, MarketEvent(event_id="event_2", stock_code="600519", title="重大公告", url="https://example.com/a")])
    save_user_events(db, user_id=user_b.id, events=[MarketEvent(event_id="event_1", stock_code="000858", title="另一条公告")])

    user_a_events = list_user_events(db, user_id=user_a.id).items
    user_b_events = list_user_events(db, user_id=user_b.id).items

    assert len(user_a_events) == 1
    assert user_a_events[0].duplicate_count >= 2
    assert user_b_events[0].stock_code == "000858"


def test_user_run_exports_are_indexed_for_download_authorization():
    db = _session()
    user = User(email="a@example.com", username="alice", password_hash="x")
    db.add(user)
    db.commit()
    run = SimpleNamespace(
        run_id="run_1",
        stock_code="600519",
        status="completed",
        created_at="2026-05-12T10:00:00",
        updated_at="2026-05-12T10:01:00",
        detail="done",
        last_event="run_completed",
        error="",
        owner="alice",
        owner_role="analyst",
        archived=False,
        retry_of_run_id="",
        canceled=False,
        latest_report_url="/api/v1/reports/latest/600519",
        history_url="/api/v1/history/600519",
        recovery_status="normal",
        stale_after_restart=False,
        attempts=1,
        max_attempts=2,
        priority=0,
        worker_id="",
        locked_at="",
        next_retry_at="",
        run_metrics={"success": True},
        event_context={},
        event_report_summary={},
        exports=[{"kind": "markdown", "filename": "report_600519.md", "path": "output/report_600519.md", "download_url": "/api/v1/exports/report_600519.md"}],
        events=[],
        audit_events=[],
    )

    save_user_run(db, user_id=user.id, run=run)

    assert user_has_export(db, user_id=user.id, filename="report_600519.md")
    assert not user_has_export(db, user_id=user.id, filename="other.md")
    assert get_user_export_artifact(db, user_id=user.id, filename="report_600519.md").path == "output/report_600519.md"


def test_user_memory_store_isolates_research_history_by_user_id():
    db = _session()
    user_a = User(email="a@example.com", username="alice", password_hash="x")
    user_b = User(email="b@example.com", username="bob", password_hash="x")
    db.add_all([user_a, user_b])
    db.commit()
    state = AnalysisState(
        stock_code="600519",
        stock_name="贵州茅台",
        profile=StockProfile(code="600519", name="贵州茅台", industry="白酒", market_cap=1000, pe_ratio=25, pb_ratio=8),
        metrics=[FinancialMetrics(code="600519", period="2026Q1", revenue=100, net_profit=40, roe=20, gross_margin=90)],
        dcf=DCFResult(per_share_value=1888, current_price=1600, upside=18),
        analysis_payload={"research_conclusion": "高端白酒龙头，现金流稳健"},
        sections={"rating": "推荐", "rating_detail": "综合评分 88/100"},
    )

    UserMemoryStore(db, user_a.id).save_analysis(state)

    assert UserMemoryStore(db, user_a.id).get_latest("600519").rating == "推荐"
    assert UserMemoryStore(db, user_b.id).get_latest("600519") is None
    assert UserMemoryStore(db, user_a.id).get_all_stocks()[0]["code"] == "600519"
    assert UserMemoryStore(db, user_b.id).get_all_stocks() == []
