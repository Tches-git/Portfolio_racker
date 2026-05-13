"""create multi user core tables

Revision ID: 20260512_0001
Revises:
Create Date: 2026-05-12
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260512_0001"
down_revision = None
branch_labels = None
depends_on = None


def _json_type() -> sa.types.TypeEngine:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        return postgresql.JSONB(astext_type=sa.Text())
    return sa.JSON()


def _json_default(value: str) -> object:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        return sa.text(f"'{value}'::jsonb")
    return value


def upgrade() -> None:
    json_type = _json_type()
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "watchlists",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("last_refreshed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_watchlists_user_id", "watchlists", ["user_id"])
    op.create_index("idx_watchlists_user_updated", "watchlists", ["user_id", "updated_at"])

    op.create_table(
        "watchlist_stocks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("watchlist_id", sa.String(length=36), sa.ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("stock_name", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("watchlist_id", "stock_code", name="uq_watchlist_stock"),
    )
    op.create_index("ix_watchlist_stocks_watchlist_id", "watchlist_stocks", ["watchlist_id"])
    op.create_index("idx_watchlist_stocks_code", "watchlist_stocks", ["stock_code"])

    op.create_table(
        "market_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_id", sa.String(length=160), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("stock_name", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("source", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("provider", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("url", sa.Text(), nullable=False, server_default=""),
        sa.Column("published_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("collected_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("event_type", sa.String(length=64), nullable=False, server_default="other"),
        sa.Column("sentiment", sa.String(length=32), nullable=False, server_default="neutral"),
        sa.Column("impact_level", sa.String(length=32), nullable=False, server_default="low"),
        sa.Column("impact_scope", sa.String(length=64), nullable=False, server_default="sentiment"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("channel", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("retrieval_mode", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("evidence_type", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("is_placeholder", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("related_sources", json_type, nullable=False, server_default=_json_default("[]")),
        sa.Column("is_duplicate", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("parent_event_id", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("duplicate_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=48), nullable=False, server_default="new"),
        sa.Column("status_updated_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("status_note", sa.Text(), nullable=False, server_default=""),
        sa.Column("status_actor", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "event_id", name="uq_market_events_user_event"),
    )
    op.create_index("ix_market_events_user_id", "market_events", ["user_id"])
    op.create_index("idx_market_events_user_stock_time", "market_events", ["user_id", "stock_code", "published_at"])
    op.create_index("idx_market_events_user_status", "market_events", ["user_id", "status"])
    op.create_index("idx_market_events_user_type", "market_events", ["user_id", "event_type"])

    op.create_table(
        "tracking_alerts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("alert_id", sa.String(length=160), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("event_id", sa.String(length=160), nullable=False),
        sa.Column("rule_id", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("rule_name", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("alert_type", sa.String(length=80), nullable=False, server_default="high_impact"),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("message", sa.Text(), nullable=False, server_default=""),
        sa.Column("severity", sa.String(length=32), nullable=False, server_default="medium"),
        sa.Column("priority", sa.String(length=16), nullable=False, server_default="P2"),
        sa.Column("status", sa.String(length=48), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("suggested_action", sa.Text(), nullable=False, server_default=""),
        sa.Column("explanation", sa.Text(), nullable=False, server_default=""),
        sa.Column("handled_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("handled_by", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("handling_note", sa.Text(), nullable=False, server_default=""),
        sa.UniqueConstraint("user_id", "alert_id", name="uq_tracking_alerts_user_alert"),
    )
    op.create_index("ix_tracking_alerts_user_id", "tracking_alerts", ["user_id"])
    op.create_index("idx_tracking_alerts_user_status", "tracking_alerts", ["user_id", "status"])
    op.create_index("idx_tracking_alerts_user_rule", "tracking_alerts", ["user_id", "rule_id"])

    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("run_id", sa.String(length=160), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=48), nullable=False, server_default="queued"),
        sa.Column("created_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("updated_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("detail", sa.Text(), nullable=False, server_default=""),
        sa.Column("last_event", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("error", sa.Text(), nullable=False, server_default=""),
        sa.Column("owner", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("owner_role", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("retry_of_run_id", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("canceled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("latest_report_url", sa.Text(), nullable=False, server_default=""),
        sa.Column("history_url", sa.Text(), nullable=False, server_default=""),
        sa.Column("recovery_status", sa.String(length=80), nullable=False, server_default="normal"),
        sa.Column("stale_after_restart", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("worker_id", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("locked_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("next_retry_at", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("run_metrics", json_type, nullable=False, server_default=_json_default("{}")),
        sa.Column("event_context", json_type, nullable=False, server_default=_json_default("{}")),
        sa.Column("event_report_summary", json_type, nullable=False, server_default=_json_default("{}")),
        sa.Column("exports", json_type, nullable=False, server_default=_json_default("[]")),
        sa.Column("events", json_type, nullable=False, server_default=_json_default("[]")),
        sa.Column("audit_events", json_type, nullable=False, server_default=_json_default("[]")),
        sa.UniqueConstraint("user_id", "run_id", name="uq_analysis_runs_user_run"),
    )
    op.create_index("ix_analysis_runs_user_id", "analysis_runs", ["user_id"])
    op.create_index("idx_analysis_runs_user_status_updated", "analysis_runs", ["user_id", "status", "updated_at"])
    op.create_index("idx_analysis_runs_user_stock_updated", "analysis_runs", ["user_id", "stock_code", "updated_at"])

    op.create_table(
        "export_artifacts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("run_id", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("stock_code", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("kind", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("path", sa.Text(), nullable=False, server_default=""),
        sa.Column("download_url", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "filename", name="uq_export_artifacts_user_filename"),
    )
    op.create_index("ix_export_artifacts_user_id", "export_artifacts", ["user_id"])
    op.create_index("idx_export_artifacts_user_stock", "export_artifacts", ["user_id", "stock_code"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action", sa.String(length=160), nullable=False),
        sa.Column("resource_type", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("resource_id", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("detail", json_type, nullable=False, server_default=_json_default("{}")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("idx_audit_logs_user_created", "audit_logs", ["user_id", "created_at"])

    op.create_table(
        "rate_limit_events",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("key", sa.String(length=255), nullable=False),
        sa.Column("scope", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("idx_rate_limit_events_key_created", "rate_limit_events", ["key", "created_at"])


def downgrade() -> None:
    op.drop_index("idx_rate_limit_events_key_created", table_name="rate_limit_events")
    op.drop_table("rate_limit_events")
    op.drop_index("idx_audit_logs_user_created", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("idx_export_artifacts_user_stock", table_name="export_artifacts")
    op.drop_index("ix_export_artifacts_user_id", table_name="export_artifacts")
    op.drop_table("export_artifacts")
    op.drop_index("idx_analysis_runs_user_stock_updated", table_name="analysis_runs")
    op.drop_index("idx_analysis_runs_user_status_updated", table_name="analysis_runs")
    op.drop_index("ix_analysis_runs_user_id", table_name="analysis_runs")
    op.drop_table("analysis_runs")
    op.drop_index("idx_tracking_alerts_user_rule", table_name="tracking_alerts")
    op.drop_index("idx_tracking_alerts_user_status", table_name="tracking_alerts")
    op.drop_index("ix_tracking_alerts_user_id", table_name="tracking_alerts")
    op.drop_table("tracking_alerts")
    op.drop_index("idx_market_events_user_type", table_name="market_events")
    op.drop_index("idx_market_events_user_status", table_name="market_events")
    op.drop_index("idx_market_events_user_stock_time", table_name="market_events")
    op.drop_index("ix_market_events_user_id", table_name="market_events")
    op.drop_table("market_events")
    op.drop_index("idx_watchlist_stocks_code", table_name="watchlist_stocks")
    op.drop_index("ix_watchlist_stocks_watchlist_id", table_name="watchlist_stocks")
    op.drop_table("watchlist_stocks")
    op.drop_index("idx_watchlists_user_updated", table_name="watchlists")
    op.drop_index("ix_watchlists_user_id", table_name="watchlists")
    op.drop_table("watchlists")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
