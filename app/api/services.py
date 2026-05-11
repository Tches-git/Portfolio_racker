"""API 读服务。"""
from __future__ import annotations

from pathlib import Path

from app.api.mappers import map_latest_record, map_stock_history
from app.api.schemas import LatestReportResponse, StockHistoryResponse
from app.config import OUTPUT_DIR
from app.memory.store import MemoryStore, get_memory_store


class NotFoundError(RuntimeError):
    """未找到资源。"""


def _latest_export_timestamp(stock_code: str, *, output_dir: Path) -> str:
    report_files = sorted(output_dir.glob(f"report_{stock_code}_*.md"), reverse=True)
    for path in report_files:
        suffix = path.stem.removeprefix(f"report_{stock_code}_")
        if suffix:
            return suffix
    return ""


def get_latest_report(stock_code: str, *, store: MemoryStore | None = None, output_dir: Path = OUTPUT_DIR) -> LatestReportResponse:
    memory_store = store or get_memory_store()
    record = memory_store.get_latest(stock_code)
    if record is None:
        raise NotFoundError(f"未找到股票 {stock_code} 的历史分析记录")
    payload = map_latest_record(record, output_dir=output_dir)
    export_timestamp = _latest_export_timestamp(stock_code, output_dir=output_dir)
    if export_timestamp:
        payload.exports = [item for item in payload.exports if f"_{export_timestamp}." in item.filename]
    return payload


def get_stock_history(stock_code: str, *, store: MemoryStore | None = None) -> StockHistoryResponse:
    memory_store = store or get_memory_store()
    records = memory_store.get_history(stock_code=stock_code, limit=10)
    if not records:
        raise NotFoundError(f"未找到股票 {stock_code} 的历史分析记录")
    latest = records[0]
    memory = memory_store.get_stock_memory(stock_code, limit=10)
    insights = memory_store.build_memory_context(stock_code)
    return map_stock_history(
        code=stock_code,
        name=latest.stock_name,
        industry=latest.industry,
        records=records,
        memory=memory,
        insights=insights,
    )
