"""PostgreSQL-first ORM models for the multi-user platform."""
from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.db.base import Base

JSONType = JSON().with_variant(postgresql.JSONB, "postgresql")


def new_id() -> str:
    return str(uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    watchlists: Mapped[list["WatchlistRecord"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class WatchlistRecord(Base):
    __tablename__ = "watchlists"
    __table_args__ = (
        Index("idx_watchlists_user_updated", "user_id", "updated_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    last_refreshed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="watchlists")
    stocks: Mapped[list["WatchlistStockRecord"]] = relationship(back_populates="watchlist", cascade="all, delete-orphan", order_by="WatchlistStockRecord.position")


class WatchlistStockRecord(Base):
    __tablename__ = "watchlist_stocks"
    __table_args__ = (
        UniqueConstraint("watchlist_id", "stock_code", name="uq_watchlist_stock"),
        Index("idx_watchlist_stocks_code", "stock_code"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    watchlist_id: Mapped[str] = mapped_column(String(36), ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False, index=True)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    stock_name: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    watchlist: Mapped[WatchlistRecord] = relationship(back_populates="stocks")


class MarketEventRecord(Base):
    __tablename__ = "market_events"
    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_market_events_user_event"),
        Index("idx_market_events_user_stock_time", "user_id", "stock_code", "published_at"),
        Index("idx_market_events_user_status", "user_id", "status"),
        Index("idx_market_events_user_type", "user_id", "event_type"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    event_id: Mapped[str] = mapped_column(String(160), nullable=False)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    stock_name: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    title: Mapped[str] = mapped_column(Text, nullable=False, default="")
    summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    source: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    provider: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    published_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    collected_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, default="other")
    sentiment: Mapped[str] = mapped_column(String(32), nullable=False, default="neutral")
    impact_level: Mapped[str] = mapped_column(String(32), nullable=False, default="low")
    impact_scope: Mapped[str] = mapped_column(String(64), nullable=False, default="sentiment")
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    channel: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    retrieval_mode: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    evidence_type: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    is_placeholder: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    related_sources: Mapped[list[dict[str, str]]] = mapped_column(JSONType, nullable=False, default=list)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_event_id: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    duplicate_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(48), nullable=False, default="new")
    status_updated_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    status_note: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status_actor: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class TrackingAlertRecord(Base):
    __tablename__ = "tracking_alerts"
    __table_args__ = (
        UniqueConstraint("user_id", "alert_id", name="uq_tracking_alerts_user_alert"),
        Index("idx_tracking_alerts_user_status", "user_id", "status"),
        Index("idx_tracking_alerts_user_rule", "user_id", "rule_id"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    alert_id: Mapped[str] = mapped_column(String(160), nullable=False)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    event_id: Mapped[str] = mapped_column(String(160), nullable=False)
    rule_id: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    rule_name: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    alert_type: Mapped[str] = mapped_column(String(80), nullable=False, default="high_impact")
    title: Mapped[str] = mapped_column(Text, nullable=False, default="")
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    severity: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    priority: Mapped[str] = mapped_column(String(16), nullable=False, default="P2")
    status: Mapped[str] = mapped_column(String(48), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    suggested_action: Mapped[str] = mapped_column(Text, nullable=False, default="")
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    handled_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    handled_by: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    handling_note: Mapped[str] = mapped_column(Text, nullable=False, default="")


class AnalysisRunRecord(Base):
    __tablename__ = "analysis_runs"
    __table_args__ = (
        UniqueConstraint("user_id", "run_id", name="uq_analysis_runs_user_run"),
        Index("idx_analysis_runs_user_status_updated", "user_id", "status", "updated_at"),
        Index("idx_analysis_runs_user_stock_updated", "user_id", "stock_code", "updated_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    run_id: Mapped[str] = mapped_column(String(160), nullable=False)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(48), nullable=False, default="queued")
    created_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    detail: Mapped[str] = mapped_column(Text, nullable=False, default="")
    last_event: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    error: Mapped[str] = mapped_column(Text, nullable=False, default="")
    owner: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    owner_role: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    retry_of_run_id: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    canceled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    latest_report_url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    history_url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    recovery_status: Mapped[str] = mapped_column(String(80), nullable=False, default="normal")
    stale_after_restart: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    worker_id: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    locked_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    next_retry_at: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    run_metrics: Mapped[dict] = mapped_column(JSONType, nullable=False, default=dict)
    event_context: Mapped[dict] = mapped_column(JSONType, nullable=False, default=dict)
    event_report_summary: Mapped[dict] = mapped_column(JSONType, nullable=False, default=dict)
    exports: Mapped[list[dict]] = mapped_column(JSONType, nullable=False, default=list)
    events: Mapped[list[dict]] = mapped_column(JSONType, nullable=False, default=list)
    audit_events: Mapped[list[dict]] = mapped_column(JSONType, nullable=False, default=list)


class ExportArtifactRecord(Base):
    __tablename__ = "export_artifacts"
    __table_args__ = (
        UniqueConstraint("user_id", "filename", name="uq_export_artifacts_user_filename"),
        Index("idx_export_artifacts_user_stock", "user_id", "stock_code"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    run_id: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    kind: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(Text, nullable=False, default="")
    download_url: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class ResearchRecord(Base):
    __tablename__ = "research_records"
    __table_args__ = (
        UniqueConstraint("user_id", "stock_code", "timestamp", name="uq_research_records_user_stock_time"),
        Index("idx_research_records_user_stock_time", "user_id", "stock_code", "timestamp"),
        Index("idx_research_records_user_time", "user_id", "timestamp"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    stock_name: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    industry: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    market_cap: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pe_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pb_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    revenue: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    net_profit: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    roe: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    gross_margin: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    debt_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cash_flow: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    dcf_per_share: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    dcf_upside: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    current_price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    rating: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    rating_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    conclusion: Mapped[str] = mapped_column(Text, nullable=False, default="")
    risk_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    risk_summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    source_reference_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    placeholder_source_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class StockMemorySnapshotRecord(Base):
    __tablename__ = "stock_memory_snapshots"
    __table_args__ = (
        UniqueConstraint("user_id", "stock_code", "timestamp", name="uq_stock_memory_user_stock_time"),
        Index("idx_stock_memory_user_stock_time", "user_id", "stock_code", "timestamp"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    stock_code: Mapped[str] = mapped_column(String(32), nullable=False)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    thesis: Mapped[str] = mapped_column(Text, nullable=False, default="")
    rating: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    target_range: Mapped[str] = mapped_column(Text, nullable=False, default="")
    key_risks: Mapped[list[str]] = mapped_column(JSONType, nullable=False, default=list)
    catalysts: Mapped[list[str]] = mapped_column(JSONType, nullable=False, default=list)
    valuation_summary: Mapped[str] = mapped_column(Text, nullable=False, default="")
    confidence_signals: Mapped[dict[str, float]] = mapped_column(JSONType, nullable=False, default=dict)
    historical_delta: Mapped[str] = mapped_column(Text, nullable=False, default="")
    conflict_flag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    conflict_reason: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class AuditLogRecord(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_logs_user_created", "user_id", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(160), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    resource_id: Mapped[str] = mapped_column(String(160), nullable=False, default="")
    detail: Mapped[dict] = mapped_column(JSONType, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class RateLimitEventRecord(Base):
    __tablename__ = "rate_limit_events"
    __table_args__ = (
        Index("idx_rate_limit_events_key_created", "key", "created_at"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
