"""add multi agent trace to analysis runs

Revision ID: 20260514_0003
Revises: 20260512_0002
Create Date: 2026-05-14
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260514_0003"
down_revision = "20260512_0002"
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
    op.add_column(
        "analysis_runs",
        sa.Column("multi_agent_trace", _json_type(), nullable=False, server_default=_json_default("{}")),
    )


def downgrade() -> None:
    op.drop_column("analysis_runs", "multi_agent_trace")

