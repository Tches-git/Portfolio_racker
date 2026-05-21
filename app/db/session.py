"""Database engine and session helpers."""
from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from app.config import DATABASE_URL
from app.db.base import Base
from app.db import models  # noqa: F401


def _connect_args(url: str) -> dict[str, object]:
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True, connect_args=_connect_args(DATABASE_URL))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, future=True)


def ensure_sqlite_compat_schema() -> None:
    """Patch local SQLite databases created before the latest Alembic step.

    Deployed PostgreSQL should use Alembic. The local desktop flow often keeps an
    existing output/portfolio_tracker.db without an alembic_version table, so a
    narrow compatibility patch prevents newer ORM columns from causing 500s.
    """
    if not DATABASE_URL.startswith("sqlite"):
        return
    Base.metadata.create_all(bind=engine, checkfirst=True)
    with engine.begin() as connection:
        tables = {row[0] for row in connection.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))}
        if "analysis_runs" not in tables:
            return
        columns = {row[1] for row in connection.execute(text("PRAGMA table_info(analysis_runs)"))}
        if "multi_agent_trace" not in columns:
            connection.execute(text("ALTER TABLE analysis_runs ADD COLUMN multi_agent_trace JSON NOT NULL DEFAULT '{}'"))


ensure_sqlite_compat_schema()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding one database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
