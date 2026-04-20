"""基于 JSON 文件持久化的分析记忆存储"""
from __future__ import annotations

import json
import re
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from app.config import DATA_DIR
from app.models import AnalysisState


@dataclass
class AnalysisRecord:
    stock_code: str
    stock_name: str
    timestamp: str  # ISO格式时间戳
    industry: str = ""
    # 核心指标快照
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    revenue: float = 0.0       # 最新一期营收
    net_profit: float = 0.0    # 最新一期净利润
    roe: float = 0.0
    gross_margin: float = 0.0
    debt_ratio: float = 0.0
    cash_flow: float = 0.0
    # 估值
    dcf_per_share: float = 0.0
    dcf_upside: float = 0.0
    current_price: float = 0.0
    # 评级
    rating: str = ""
    rating_score: float = 0.0
    # 摘要
    conclusion: str = ""       # 结论摘要（截取前500字）
    risk_count: int = 0
    risk_summary: str = ""     # 主要风险简述


class MemoryStore:
    """分析记忆存储，基于 JSON 文件持久化"""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or (DATA_DIR / "memory")
        self._dir.mkdir(parents=True, exist_ok=True)
        self._file = self._dir / "history.json"
        self._lock = threading.Lock()
        self._records: list[AnalysisRecord] = []
        self._load()

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def save_analysis(self, state: AnalysisState) -> AnalysisRecord:
        """从 AnalysisState 提取关键信息保存为 AnalysisRecord，追加到历史并持久化"""
        profile = state.profile
        latest_metric = state.metrics[0] if state.metrics else None

        record = AnalysisRecord(
            stock_code=state.stock_code,
            stock_name=state.stock_name,
            timestamp=datetime.now().isoformat(),
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
            conclusion=state.sections.get("research_conclusion", "")[:500],
            risk_count=len(state.risks),
            risk_summary=self._build_risk_summary(state),
        )

        with self._lock:
            self._records.append(record)
            self._save()
        return record

    def get_history(
        self, stock_code: str | None = None, limit: int = 50
    ) -> list[AnalysisRecord]:
        """获取分析历史。如指定 stock_code 则只返回该股票。按时间降序"""
        with self._lock:
            records = self._records
        if stock_code:
            records = [r for r in records if r.stock_code == stock_code]
        return sorted(records, key=lambda r: r.timestamp, reverse=True)[:limit]

    def get_latest(self, stock_code: str) -> AnalysisRecord | None:
        """获取某股票最近一次的分析记录"""
        history = self.get_history(stock_code=stock_code, limit=1)
        return history[0] if history else None

    def get_all_stocks(self) -> list[dict]:
        """返回所有分析过的股票列表

        Returns:
            [{"code": "600519", "name": "贵州茅台", "count": 3, "latest": "2024-..."}]
        """
        with self._lock:
            records = self._records

        stock_map: dict[str, dict] = {}
        for r in records:
            if r.stock_code not in stock_map:
                stock_map[r.stock_code] = {
                    "code": r.stock_code,
                    "name": r.stock_name,
                    "count": 0,
                    "latest": r.timestamp,
                }
            entry = stock_map[r.stock_code]
            entry["count"] += 1
            if r.timestamp > entry["latest"]:
                entry["latest"] = r.timestamp

        return sorted(stock_map.values(), key=lambda x: x["latest"], reverse=True)

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """从 JSON 加载"""
        if not self._file.exists():
            self._records = []
            return
        try:
            data = json.loads(self._file.read_text(encoding="utf-8"))
            self._records = [AnalysisRecord(**item) for item in data]
        except (json.JSONDecodeError, TypeError, KeyError):
            self._records = []

    def _save(self) -> None:
        """持久化到 JSON"""
        data = [asdict(r) for r in self._records]
        self._file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _parse_rating_score(state: AnalysisState) -> float:
        """从 state.sections 中解析评分，格式为 '综合评分 XX/100'"""
        text = state.sections.get("rating_detail", "")
        match = re.search(r"综合评分\s*(\d+(?:\.\d+)?)\s*/\s*100", text)
        return float(match.group(1)) if match else 0.0

    @staticmethod
    def _build_risk_summary(state: AnalysisState) -> str:
        """取前3条风险的 description 拼接"""
        if not state.risks:
            return ""
        return "；".join(r.description for r in state.risks[:3])


# ------------------------------------------------------------------
# 单例工厂
# ------------------------------------------------------------------

_instance: MemoryStore | None = None
_instance_lock = threading.Lock()


def get_memory_store() -> MemoryStore:
    """获取 MemoryStore 单例"""
    global _instance
    if _instance is None:
        with _instance_lock:
            if _instance is None:
                _instance = MemoryStore()
    return _instance
