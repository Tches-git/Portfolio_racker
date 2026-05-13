"""User-scoped research memory backed by PostgreSQL/SQLAlchemy."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ResearchRecord, StockMemorySnapshotRecord
from app.memory.store import AnalysisRecord, MemoryStore, StockMemorySnapshot, _analysis_value
from app.models import AnalysisState


class UserMemoryStore(MemoryStore):
    """MemoryStore-compatible facade scoped to one authenticated user."""

    def __init__(self, db: Session, user_id: str) -> None:
        self._db = db
        self.user_id = user_id

    def save_analysis(self, state: AnalysisState) -> AnalysisRecord:
        profile = state.profile
        latest_metric = state.metrics[0] if state.metrics else None
        previous_snapshot = self.get_latest_stock_memory(state.stock_code)
        timestamp = datetime.now().isoformat()
        record = AnalysisRecord(
            stock_code=state.stock_code,
            stock_name=state.stock_name,
            timestamp=timestamp,
            industry=profile.industry if profile else "",
            market_cap=profile.market_cap if profile else 0.0,
            pe_ratio=profile.pe_ratio if profile else 0.0,
            pb_ratio=profile.pb_ratio if profile else 0.0,
            revenue=latest_metric.revenue if latest_metric else 0.0,
            net_profit=latest_metric.net_profit if latest_metric else 0.0,
            roe=latest_metric.roe if latest_metric else 0.0,
            gross_margin=latest_metric.gross_margin if latest_metric else 0.0,
            debt_ratio=latest_metric.debt_ratio if latest_metric else 0.0,
            cash_flow=latest_metric.cash_flow if latest_metric else 0.0,
            dcf_per_share=state.dcf.per_share_value if state.dcf else 0.0,
            dcf_upside=state.dcf.upside if state.dcf else 0.0,
            current_price=state.dcf.current_price if state.dcf else 0.0,
            rating=state.sections.get("rating", ""),
            rating_score=self._parse_rating_score(state),
            conclusion=_analysis_value(state, "research_conclusion", "")[:500],
            risk_count=len(state.risks),
            risk_summary=self._build_risk_summary(state),
            source_reference_count=len(state.source_refs),
            placeholder_source_count=sum(1 for ref in state.source_refs if ref.get("is_placeholder")),
        )
        snapshot = self._build_stock_memory_snapshot(state, record, previous_snapshot)
        existing = self._db.scalar(
            select(ResearchRecord).where(
                ResearchRecord.user_id == self.user_id,
                ResearchRecord.stock_code == record.stock_code,
                ResearchRecord.timestamp == record.timestamp,
            )
        )
        if existing is None:
            existing = ResearchRecord(user_id=self.user_id)
            self._db.add(existing)
        _apply_analysis_record(existing, record)

        snapshot_record = self._db.scalar(
            select(StockMemorySnapshotRecord).where(
                StockMemorySnapshotRecord.user_id == self.user_id,
                StockMemorySnapshotRecord.stock_code == snapshot.stock_code,
                StockMemorySnapshotRecord.timestamp == snapshot.timestamp,
            )
        )
        if snapshot_record is None:
            snapshot_record = StockMemorySnapshotRecord(user_id=self.user_id)
            self._db.add(snapshot_record)
        _apply_snapshot_record(snapshot_record, snapshot)
        self._db.commit()
        return record

    def get_history(self, stock_code: str | None = None, limit: int = 50) -> list[AnalysisRecord]:
        stmt = select(ResearchRecord).where(ResearchRecord.user_id == self.user_id)
        if stock_code:
            stmt = stmt.where(ResearchRecord.stock_code == stock_code)
        records = self._db.scalars(stmt.order_by(ResearchRecord.timestamp.desc()).limit(max(1, limit)))
        return [_analysis_from_record(record) for record in records]

    def get_latest(self, stock_code: str) -> AnalysisRecord | None:
        history = self.get_history(stock_code=stock_code, limit=1)
        return history[0] if history else None

    def get_all_stocks(self) -> list[dict]:
        records = self.get_history(limit=10_000)
        stock_map: dict[str, dict] = {}
        for record in records:
            entry = stock_map.setdefault(
                record.stock_code,
                {
                    "code": record.stock_code,
                    "name": record.stock_name,
                    "count": 0,
                    "latest": record.timestamp,
                },
            )
            entry["count"] += 1
            if record.timestamp > str(entry["latest"]):
                entry["latest"] = record.timestamp
                entry["name"] = record.stock_name
        return sorted(stock_map.values(), key=lambda item: str(item["latest"]), reverse=True)

    def get_stock_memory(self, stock_code: str, limit: int = 10) -> list[StockMemorySnapshot]:
        records = self._db.scalars(
            select(StockMemorySnapshotRecord)
            .where(StockMemorySnapshotRecord.user_id == self.user_id, StockMemorySnapshotRecord.stock_code == stock_code)
            .order_by(StockMemorySnapshotRecord.timestamp.desc())
            .limit(max(1, limit))
        )
        return [_snapshot_from_record(record) for record in records]


def _apply_analysis_record(record: ResearchRecord, item: AnalysisRecord) -> None:
    for field in (
        "stock_code",
        "stock_name",
        "timestamp",
        "industry",
        "market_cap",
        "pe_ratio",
        "pb_ratio",
        "revenue",
        "net_profit",
        "roe",
        "gross_margin",
        "debt_ratio",
        "cash_flow",
        "dcf_per_share",
        "dcf_upside",
        "current_price",
        "rating",
        "rating_score",
        "conclusion",
        "risk_count",
        "risk_summary",
        "source_reference_count",
        "placeholder_source_count",
    ):
        setattr(record, field, getattr(item, field))


def _apply_snapshot_record(record: StockMemorySnapshotRecord, item: StockMemorySnapshot) -> None:
    for field in (
        "stock_code",
        "timestamp",
        "thesis",
        "rating",
        "target_range",
        "key_risks",
        "catalysts",
        "valuation_summary",
        "confidence_signals",
        "historical_delta",
        "conflict_flag",
        "conflict_reason",
    ):
        setattr(record, field, getattr(item, field))


def _analysis_from_record(record: ResearchRecord) -> AnalysisRecord:
    return AnalysisRecord(
        stock_code=record.stock_code,
        stock_name=record.stock_name,
        timestamp=record.timestamp,
        industry=record.industry,
        market_cap=record.market_cap,
        pe_ratio=record.pe_ratio,
        pb_ratio=record.pb_ratio,
        revenue=record.revenue,
        net_profit=record.net_profit,
        roe=record.roe,
        gross_margin=record.gross_margin,
        debt_ratio=record.debt_ratio,
        cash_flow=record.cash_flow,
        dcf_per_share=record.dcf_per_share,
        dcf_upside=record.dcf_upside,
        current_price=record.current_price,
        rating=record.rating,
        rating_score=record.rating_score,
        conclusion=record.conclusion,
        risk_count=record.risk_count,
        risk_summary=record.risk_summary,
        source_reference_count=record.source_reference_count,
        placeholder_source_count=record.placeholder_source_count,
    )


def _snapshot_from_record(record: StockMemorySnapshotRecord) -> StockMemorySnapshot:
    return StockMemorySnapshot(
        stock_code=record.stock_code,
        timestamp=record.timestamp,
        thesis=record.thesis,
        rating=record.rating,
        target_range=record.target_range,
        key_risks=list(record.key_risks or []),
        catalysts=list(record.catalysts or []),
        valuation_summary=record.valuation_summary,
        confidence_signals=dict(record.confidence_signals or {}),
        historical_delta=record.historical_delta,
        conflict_flag=record.conflict_flag,
        conflict_reason=record.conflict_reason,
    )
