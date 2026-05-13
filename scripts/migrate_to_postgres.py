"""Import legacy JSON/SQLite data into the multi-user database.

Usage:
    DATABASE_URL=postgresql+psycopg://... python scripts/migrate_to_postgres.py --user-email admin@example.com
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth.security import hash_password, normalize_email, normalize_username
from app.config import OUTPUT_DIR
from app.db.base import Base
from app.db.models import User, WatchlistRecord, WatchlistStockRecord
from app.db.repositories import save_user_events, save_user_run
from app.db.session import SessionLocal, engine
from app.tracking.history import load_events
from app.tracking.watchlist import normalize_stock_codes


def main() -> None:
    args = _parse_args()
    output_dir = Path(args.output_dir).resolve()
    if args.create_tables:
        Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = _get_or_create_user(
            db,
            email=args.user_email,
            username=args.username,
            password=args.password,
        )
        watchlist_count = _import_watchlists(db, user_id=user.id, output_dir=output_dir)
        event_count = _import_events(db, user_id=user.id, output_dir=output_dir)
        run_count = _import_runs(db, user_id=user.id, owner=user.username, output_dir=output_dir)
        print(
            json.dumps(
                {
                    "user": user.email,
                    "watchlists": watchlist_count,
                    "events": event_count,
                    "runs": run_count,
                },
                ensure_ascii=False,
            )
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Migrate legacy local data to PostgreSQL-compatible storage.")
    parser.add_argument("--user-email", required=True, help="Target owner email for imported data.")
    parser.add_argument("--username", default="", help="Username to create when the user does not exist.")
    parser.add_argument("--password", default="ChangeMe123!", help="Temporary password for newly created user.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Legacy OUTPUT_DIR path.")
    parser.add_argument("--create-tables", action="store_true", help="Create tables directly when Alembic was not run.")
    return parser.parse_args()


def _get_or_create_user(db, *, email: str, username: str, password: str) -> User:
    normalized_email = normalize_email(email)
    user = db.scalar(select(User).where(User.email == normalized_email))
    if user is not None:
        return user
    normalized_username = normalize_username(username, normalized_email)
    existing_username = db.scalar(select(User).where(User.username == normalized_username))
    if existing_username is not None:
        normalized_username = f"{normalized_username}_{len(normalized_email)}"
    user = User(
        email=normalized_email,
        username=normalized_username,
        password_hash=hash_password(password),
        role="admin",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _import_watchlists(db, *, user_id: str, output_dir: Path) -> int:
    path = output_dir / "tracking_watchlists.json"
    if not path.exists():
        return 0
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        return 0
    imported = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        watchlist_id = str(item.get("watchlist_id") or "").strip()
        if not watchlist_id:
            continue
        record = db.scalar(
            select(WatchlistRecord)
            .where(WatchlistRecord.user_id == user_id, WatchlistRecord.id == watchlist_id)
            .options(selectinload(WatchlistRecord.stocks))
        )
        if record is None:
            record = WatchlistRecord(id=watchlist_id, user_id=user_id)
            db.add(record)
        record.name = str(item.get("name") or "未命名组合")
        record.description = str(item.get("description") or "")
        record.stocks = [
            WatchlistStockRecord(stock_code=code, position=index)
            for index, code in enumerate(normalize_stock_codes(list(item.get("stock_codes") or [])))
        ]
        imported += 1
    db.commit()
    return imported


def _import_events(db, *, user_id: str, output_dir: Path) -> int:
    events = load_events(output_dir=output_dir)
    if events:
        save_user_events(db, user_id=user_id, events=events)
    return len(events)


def _import_runs(db, *, user_id: str, owner: str, output_dir: Path) -> int:
    path = output_dir / "api_runs.db"
    if not path.exists():
        return 0
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        try:
            rows = conn.execute("SELECT * FROM api_runs ORDER BY updated_at DESC").fetchall()
        except sqlite3.DatabaseError:
            return 0
    for row in rows:
        payload = dict(row)
        run = SimpleNamespace(
            run_id=str(payload.get("run_id") or ""),
            stock_code=str(payload.get("stock_code") or ""),
            status=str(payload.get("status") or "failed"),
            created_at=str(payload.get("created_at") or ""),
            updated_at=str(payload.get("updated_at") or ""),
            detail=str(payload.get("detail") or ""),
            last_event=str(payload.get("last_event") or ""),
            error=str(payload.get("error") or ""),
            owner=str(payload.get("owner") or owner),
            owner_role=str(payload.get("owner_role") or "admin"),
            archived=bool(payload.get("archived") or False),
            retry_of_run_id=str(payload.get("retry_of_run_id") or ""),
            canceled=bool(payload.get("canceled") or False),
            latest_report_url=str(payload.get("latest_report_url") or ""),
            history_url=str(payload.get("history_url") or ""),
            recovery_status=str(payload.get("recovery_status") or "normal"),
            stale_after_restart=bool(payload.get("stale_after_restart") or False),
            attempts=int(payload.get("attempts") or 0),
            max_attempts=int(payload.get("max_attempts") or 2),
            priority=int(payload.get("priority") or 0),
            worker_id=str(payload.get("worker_id") or ""),
            locked_at=str(payload.get("locked_at") or ""),
            next_retry_at=str(payload.get("next_retry_at") or ""),
            run_metrics=_json_load(payload.get("run_metrics_json"), {}),
            event_context=_json_load(payload.get("event_context_json"), {}),
            event_report_summary=_json_load(payload.get("event_report_summary_json"), {}),
            exports=_json_load(payload.get("exports_json"), []),
            events=_json_load(payload.get("events_json"), []),
            audit_events=_json_load(payload.get("audit_events_json"), []),
        )
        if run.run_id:
            save_user_run(db, user_id=user_id, run=run)
    return len(rows)


def _json_load(value: object, fallback):
    if not value:
        return fallback
    try:
        return json.loads(str(value))
    except Exception:
        return fallback


if __name__ == "__main__":
    main()
