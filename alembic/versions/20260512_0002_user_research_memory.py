"""add user scoped research memory tables

Revision ID: 20260512_0002
Revises: 20260512_0001
Create Date: 2026-05-12
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260512_0002"
down_revision = "20260512_0001"
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
        "research_records",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("stock_name", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("timestamp", sa.String(length=64), nullable=False),
        sa.Column("industry", sa.String(length=160), nullable=False, server_default=""),
        sa.Column("market_cap", sa.Float(), nullable=False, server_default="0"),
        sa.Column("pe_ratio", sa.Float(), nullable=False, server_default="0"),
        sa.Column("pb_ratio", sa.Float(), nullable=False, server_default="0"),
        sa.Column("revenue", sa.Float(), nullable=False, server_default="0"),
        sa.Column("net_profit", sa.Float(), nullable=False, server_default="0"),
        sa.Column("roe", sa.Float(), nullable=False, server_default="0"),
        sa.Column("gross_margin", sa.Float(), nullable=False, server_default="0"),
        sa.Column("debt_ratio", sa.Float(), nullable=False, server_default="0"),
        sa.Column("cash_flow", sa.Float(), nullable=False, server_default="0"),
        sa.Column("dcf_per_share", sa.Float(), nullable=False, server_default="0"),
        sa.Column("dcf_upside", sa.Float(), nullable=False, server_default="0"),
        sa.Column("current_price", sa.Float(), nullable=False, server_default="0"),
        sa.Column("rating", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("rating_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("conclusion", sa.Text(), nullable=False, server_default=""),
        sa.Column("risk_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("risk_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("source_reference_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("placeholder_source_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "stock_code", "timestamp", name="uq_research_records_user_stock_time"),
    )
    op.create_index("ix_research_records_user_id", "research_records", ["user_id"])
    op.create_index("idx_research_records_user_stock_time", "research_records", ["user_id", "stock_code", "timestamp"])
    op.create_index("idx_research_records_user_time", "research_records", ["user_id", "timestamp"])

    op.create_table(
        "stock_memory_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stock_code", sa.String(length=32), nullable=False),
        sa.Column("timestamp", sa.String(length=64), nullable=False),
        sa.Column("thesis", sa.Text(), nullable=False, server_default=""),
        sa.Column("rating", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("target_range", sa.Text(), nullable=False, server_default=""),
        sa.Column("key_risks", json_type, nullable=False, server_default=_json_default("[]")),
        sa.Column("catalysts", json_type, nullable=False, server_default=_json_default("[]")),
        sa.Column("valuation_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("confidence_signals", json_type, nullable=False, server_default=_json_default("{}")),
        sa.Column("historical_delta", sa.Text(), nullable=False, server_default=""),
        sa.Column("conflict_flag", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("conflict_reason", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("user_id", "stock_code", "timestamp", name="uq_stock_memory_user_stock_time"),
    )
    op.create_index("ix_stock_memory_snapshots_user_id", "stock_memory_snapshots", ["user_id"])
    op.create_index("idx_stock_memory_user_stock_time", "stock_memory_snapshots", ["user_id", "stock_code", "timestamp"])


def downgrade() -> None:
    op.drop_index("idx_stock_memory_user_stock_time", table_name="stock_memory_snapshots")
    op.drop_index("ix_stock_memory_snapshots_user_id", table_name="stock_memory_snapshots")
    op.drop_table("stock_memory_snapshots")
    op.drop_index("idx_research_records_user_time", table_name="research_records")
    op.drop_index("idx_research_records_user_stock_time", table_name="research_records")
    op.drop_index("ix_research_records_user_id", table_name="research_records")
    op.drop_table("research_records")
