"""基于 JSON 文件持久化的分析记忆存储"""
from __future__ import annotations

import json
import re
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime
from math import exp
from pathlib import Path

from app.config import DATA_DIR
from app.models import AnalysisState


def _analysis_value(state: AnalysisState, key: str, default: str = "") -> str:
    return str((getattr(state, "analysis_payload", {}) or {}).get(key, state.sections.get(key, default)) or default)


@dataclass
class StockMemorySnapshot:
    stock_code: str
    timestamp: str
    thesis: str = ""
    rating: str = ""
    target_range: str = ""
    key_risks: list[str] = field(default_factory=list)
    catalysts: list[str] = field(default_factory=list)
    valuation_summary: str = ""
    confidence_signals: dict[str, float] = field(default_factory=dict)
    historical_delta: str = ""
    conflict_flag: bool = False
    conflict_reason: str = ""


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
    source_reference_count: int = 0
    placeholder_source_count: int = 0


class MemoryStore:
    """分析记忆存储，基于 JSON 文件持久化"""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._dir = data_dir or (DATA_DIR / "memory")
        self._dir.mkdir(parents=True, exist_ok=True)
        self._file = self._dir / "history.json"
        self._stock_memory_file = self._dir / "stock_memory.json"
        self._lock = threading.Lock()
        self._records: list[AnalysisRecord] = []
        self._stock_memory: dict[str, list[StockMemorySnapshot]] = {}
        self._load()

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def save_analysis(self, state: AnalysisState) -> AnalysisRecord:
        """从 AnalysisState 提取关键信息保存为 AnalysisRecord，追加到历史并持久化"""
        profile = state.profile
        latest_metric = state.metrics[0] if state.metrics else None
        previous_snapshot = self.get_latest_stock_memory(state.stock_code)

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
            conclusion=_analysis_value(state, "research_conclusion", "")[:500],
            risk_count=len(state.risks),
            risk_summary=self._build_risk_summary(state),
            source_reference_count=len(state.source_refs),
            placeholder_source_count=sum(1 for ref in state.source_refs if ref.get("is_placeholder")),
        )

        snapshot = self._build_stock_memory_snapshot(state, record, previous_snapshot)

        with self._lock:
            self._records.append(record)
            self._stock_memory.setdefault(state.stock_code, []).append(snapshot)
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

    def get_stock_memory(self, stock_code: str, limit: int = 10) -> list[StockMemorySnapshot]:
        with self._lock:
            snapshots = list(self._stock_memory.get(stock_code, []))
        return sorted(snapshots, key=lambda item: item.timestamp, reverse=True)[:limit]

    def get_ranked_stock_memory(self, stock_code: str, limit: int = 6) -> list[StockMemorySnapshot]:
        snapshots = self.get_stock_memory(stock_code, limit=max(limit * 3, 12))
        return self._select_memory_snapshots(snapshots, limit=limit)

    def get_latest_stock_memory(self, stock_code: str) -> StockMemorySnapshot | None:
        history = self.get_stock_memory(stock_code, limit=1)
        return history[0] if history else None

    def build_memory_context(self, stock_code: str) -> dict[str, str | int | float]:
        raw_snapshots = self.get_stock_memory(stock_code, limit=12)
        selected_snapshots = self._select_memory_snapshots(raw_snapshots, limit=6)
        if not selected_snapshots:
            return {
                "summary": "暂无长期记忆",
                "timeline": "",
                "memory_hit_count": 0,
                "historical_delta_coverage": 0.0,
                "duplicate_memory_injection_rate": 0.0,
                "memory_conflict_count": 0,
                "governance_notes": "无长期记忆可治理",
                "repeated_risk_patterns": "暂无",
                "repeated_catalyst_patterns": "暂无",
                "repeated_risk_pattern_count": 0,
                "repeated_catalyst_pattern_count": 0,
                "thesis_stability_score": 0.0,
                "rating_drift_summary": "暂无评级漂移",
                "rating_drift_count": 0,
                "memory_pattern_summary": "暂无长期模式",
            }
        latest = selected_snapshots[0]
        previous = selected_snapshots[1] if len(selected_snapshots) > 1 else None
        repeated_thesis = len({self._memory_signature(item) for item in raw_snapshots if self._memory_signature(item)})
        duplicate_rate = 0.0
        if raw_snapshots:
            duplicate_rate = round(max(0, len(raw_snapshots) - repeated_thesis) / len(raw_snapshots), 4)
        delta_coverage = 1.0 if latest.historical_delta else 0.0
        if previous and latest.historical_delta:
            delta_coverage = 1.0
        timeline = "\n".join(
            f"- {item.timestamp[:10]} | 评级 {item.rating or '未知'} | thesis: {(item.thesis or '暂无').strip()[:80]}"
            for item in selected_snapshots
        )
        summary_parts = [latest.thesis or "暂无 thesis 摘要"]
        if previous and previous.rating != latest.rating:
            summary_parts.append(f"评级由 {previous.rating or '未知'} 变为 {latest.rating or '未知'}")
        if latest.conflict_reason:
            summary_parts.append(f"冲突原因：{latest.conflict_reason}")
        governance_notes = self._build_governance_notes(raw_snapshots, selected_snapshots)
        pattern_summary = self._build_pattern_summary(selected_snapshots)
        return {
            "summary": "；".join(part for part in summary_parts if part),
            "timeline": timeline,
            "memory_hit_count": len(selected_snapshots),
            "historical_delta_coverage": delta_coverage,
            "duplicate_memory_injection_rate": duplicate_rate,
            "memory_conflict_count": sum(1 for item in selected_snapshots if item.conflict_flag),
            "governance_notes": governance_notes,
            "repeated_risk_patterns": pattern_summary["repeated_risk_patterns"],
            "repeated_catalyst_patterns": pattern_summary["repeated_catalyst_patterns"],
            "repeated_risk_pattern_count": pattern_summary["repeated_risk_pattern_count"],
            "repeated_catalyst_pattern_count": pattern_summary["repeated_catalyst_pattern_count"],
            "thesis_stability_score": pattern_summary["thesis_stability_score"],
            "rating_drift_summary": pattern_summary["rating_drift_summary"],
            "rating_drift_count": pattern_summary["rating_drift_count"],
            "memory_pattern_summary": pattern_summary["memory_pattern_summary"],
        }

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """从 JSON 加载"""
        if self._file.exists():
            try:
                data = json.loads(self._file.read_text(encoding="utf-8"))
                self._records = [AnalysisRecord(**item) for item in data]
            except (json.JSONDecodeError, TypeError, KeyError):
                self._records = []
        else:
            self._records = []
        if self._stock_memory_file.exists():
            try:
                data = json.loads(self._stock_memory_file.read_text(encoding="utf-8"))
                self._stock_memory = {
                    code: [StockMemorySnapshot(**item) for item in items]
                    for code, items in data.items()
                }
            except (json.JSONDecodeError, TypeError, KeyError):
                self._stock_memory = {}
        else:
            self._stock_memory = {}

    def _save(self) -> None:
        """持久化到 JSON"""
        data = [asdict(r) for r in self._records]
        self._file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._stock_memory_file.write_text(
            json.dumps({code: [asdict(item) for item in items] for code, items in self._stock_memory.items()}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _parse_rating_score(state: AnalysisState) -> float:
        """从 state.sections 中解析评分，格式为 '综合评分 XX/100'"""
        text = state.sections.get("rating_detail", "")
        match = re.search(r"综合评分\s*(\d+(?:\.\d+)?)\s*/\s*100", text)
        return float(match.group(1)) if match else 0.0

    def _build_stock_memory_snapshot(
        self,
        state: AnalysisState,
        record: AnalysisRecord,
        previous: StockMemorySnapshot | None,
    ) -> StockMemorySnapshot:
        target_range = self._extract_target_range(state)
        thesis = self._extract_thesis(state)
        valuation_summary = self._build_valuation_summary(record, target_range)
        key_risks = [r.description for r in state.risks[:3] if getattr(r, "description", "")]
        catalysts = self._extract_catalysts(state)
        historical_delta = self._build_historical_delta(record, previous)
        confidence_signals = {
            "rating_score": record.rating_score,
            "source_reference_count": float(record.source_reference_count),
            "placeholder_source_ratio": (record.placeholder_source_count / record.source_reference_count) if record.source_reference_count else 0.0,
        }
        conflict_flag = bool(previous and previous.rating and previous.rating != record.rating)
        return StockMemorySnapshot(
            stock_code=record.stock_code,
            timestamp=record.timestamp,
            thesis=thesis,
            rating=record.rating,
            target_range=target_range,
            key_risks=key_risks,
            catalysts=catalysts,
            valuation_summary=valuation_summary,
            confidence_signals=confidence_signals,
            historical_delta=historical_delta,
            conflict_flag=conflict_flag,
            conflict_reason=self._build_conflict_reason(record, previous, key_risks) if conflict_flag else "",
        )

    @staticmethod
    def _extract_thesis(state: AnalysisState) -> str:
        text = _analysis_value(state, "research_conclusion", "").strip()
        if not text:
            return ""
        return text[:220]

    @staticmethod
    def _extract_target_range(state: AnalysisState) -> str:
        report = state.final_report or ""
        match = re.search(r"(?:目标价|估值区间|合理估值区间|估值锚)[：:]?\s*([^\n]{0,40})", report)
        if match:
            return match.group(1).strip()
        if state.dcf and state.dcf.per_share_value > 0:
            return f"DCF每股价值 {state.dcf.per_share_value:.2f}元"
        return ""

    @staticmethod
    def _build_valuation_summary(record: AnalysisRecord, target_range: str) -> str:
        summary = f"DCF每股价值 {record.dcf_per_share:.2f}元，上涨空间 {record.dcf_upside:+.1f}%"
        if target_range:
            summary += f"；目标/估值锚 {target_range}"
        return summary

    @staticmethod
    def _extract_catalysts(state: AnalysisState) -> list[str]:
        text = _analysis_value(state, "research_conclusion", "")
        candidates = []
        for chunk in re.split(r"[。；\n]", text):
            snippet = chunk.strip()
            if any(keyword in snippet for keyword in ("催化", "改善", "增长", "修复", "扩张")):
                candidates.append(snippet[:60])
        return candidates[:3]

    @staticmethod
    def _build_historical_delta(record: AnalysisRecord, previous: StockMemorySnapshot | None) -> str:
        if previous is None:
            return ""
        delta_parts: list[str] = []
        if previous.rating != record.rating:
            delta_parts.append(f"评级 {previous.rating or '未知'}→{record.rating or '未知'}")
        if previous.target_range:
            delta_parts.append(f"估值锚由 {previous.target_range} 更新")
        previous_risks = set(previous.key_risks)
        return "；".join(delta_parts + [f"新增风险 {risk}" for risk in record.risk_summary.split('；') if risk and risk not in previous_risks][:2])

    @staticmethod
    def _memory_signature(snapshot: StockMemorySnapshot) -> str:
        return "|".join([
            (snapshot.rating or "").strip(),
            (snapshot.target_range or "").strip(),
            (snapshot.thesis or "").strip()[:80],
        ])

    @staticmethod
    def _memory_decay_weight(snapshot: StockMemorySnapshot) -> float:
        try:
            ts = datetime.fromisoformat(snapshot.timestamp)
        except ValueError:
            return 1.0
        age_days = max((datetime.now() - ts).days, 0)
        return round(exp(-age_days / 45), 4)

    def _select_memory_snapshots(self, snapshots: list[StockMemorySnapshot], limit: int) -> list[StockMemorySnapshot]:
        if not snapshots:
            return []
        ordered = sorted(snapshots, key=lambda item: item.timestamp, reverse=True)
        selected: list[StockMemorySnapshot] = []
        seen_signatures: set[str] = set()
        for item in ordered:
            signature = self._memory_signature(item)
            if signature and signature in seen_signatures:
                continue
            seen_signatures.add(signature)
            selected.append(item)
            if len(selected) >= limit:
                break
        selected.sort(
            key=lambda item: (
                item.conflict_flag,
                bool(item.historical_delta),
                self._memory_decay_weight(item),
                item.timestamp,
            ),
            reverse=True,
        )
        return selected[:limit]

    def _build_governance_notes(self, raw_snapshots: list[StockMemorySnapshot], selected_snapshots: list[StockMemorySnapshot]) -> str:
        if not raw_snapshots:
            return "无长期记忆可治理"
        deduped_count = max(0, len(raw_snapshots) - len(selected_snapshots))
        stale_count = sum(1 for item in raw_snapshots if self._memory_decay_weight(item) < 0.35)
        conflict_count = sum(1 for item in selected_snapshots if item.conflict_flag)
        parts = [f"去重 {deduped_count} 条", f"衰减低权重 {stale_count} 条", f"保留冲突 {conflict_count} 条"]
        return "；".join(parts)

    def _build_pattern_summary(self, snapshots: list[StockMemorySnapshot]) -> dict[str, str | int | float]:
        if not snapshots:
            return {
                "repeated_risk_patterns": "暂无",
                "repeated_catalyst_patterns": "暂无",
                "repeated_risk_pattern_count": 0,
                "repeated_catalyst_pattern_count": 0,
                "thesis_stability_score": 0.0,
                "rating_drift_summary": "暂无评级漂移",
                "rating_drift_count": 0,
                "memory_pattern_summary": "暂无长期模式",
            }
        risk_counts: dict[str, int] = {}
        catalyst_counts: dict[str, int] = {}
        thesis_signatures: dict[str, int] = {}
        for item in snapshots:
            thesis_signature = (item.thesis or "").strip()[:80]
            if thesis_signature:
                thesis_signatures[thesis_signature] = thesis_signatures.get(thesis_signature, 0) + 1
            for risk in item.key_risks:
                if risk:
                    risk_counts[risk] = risk_counts.get(risk, 0) + 1
            for catalyst in item.catalysts:
                if catalyst:
                    catalyst_counts[catalyst] = catalyst_counts.get(catalyst, 0) + 1
        repeated_risks = [item for item, count in sorted(risk_counts.items(), key=lambda pair: (-pair[1], pair[0])) if count >= 2][:3]
        repeated_catalysts = [item for item, count in sorted(catalyst_counts.items(), key=lambda pair: (-pair[1], pair[0])) if count >= 2][:3]
        thesis_stability = 0.0
        if snapshots:
            thesis_stability = round(max(thesis_signatures.values(), default=0) / len(snapshots), 4)
        rating_drift_count = 0
        rating_drift_parts: list[str] = []
        for previous, current in zip(snapshots[1:], snapshots[:-1]):
            if previous.rating and current.rating and previous.rating != current.rating:
                rating_drift_count += 1
                rating_drift_parts.append(f"{previous.rating}→{current.rating}")
        repeated_risk_text = "；".join(repeated_risks) if repeated_risks else "暂无"
        repeated_catalyst_text = "；".join(repeated_catalysts) if repeated_catalysts else "暂无"
        rating_drift_summary = "；".join(rating_drift_parts) if rating_drift_parts else "评级基本稳定"
        pattern_bits = [
            f"重复风险：{repeated_risk_text}",
            f"重复催化：{repeated_catalyst_text}",
            f"thesis稳定度：{thesis_stability:.0%}",
            f"评级漂移：{rating_drift_summary}",
        ]
        return {
            "repeated_risk_patterns": repeated_risk_text,
            "repeated_catalyst_patterns": repeated_catalyst_text,
            "repeated_risk_pattern_count": len(repeated_risks),
            "repeated_catalyst_pattern_count": len(repeated_catalysts),
            "thesis_stability_score": thesis_stability,
            "rating_drift_summary": rating_drift_summary,
            "rating_drift_count": rating_drift_count,
            "memory_pattern_summary": "；".join(pattern_bits),
        }

    @staticmethod
    def _build_conflict_reason(record: AnalysisRecord, previous: StockMemorySnapshot | None, key_risks: list[str]) -> str:
        if previous is None or previous.rating == record.rating:
            return ""
        reasons: list[str] = []
        previous_rating_score = float(previous.confidence_signals.get("rating_score", 0.0) or 0.0)
        if record.rating_score and previous_rating_score and abs(record.rating_score - previous_rating_score) >= 5:
            reasons.append(f"评分变化 {previous_rating_score:.1f}→{record.rating_score:.1f}")
        new_risks = [risk for risk in key_risks if risk and risk not in set(previous.key_risks)]
        if new_risks:
            reasons.append(f"新增风险 {'；'.join(new_risks[:2])}")
        if previous.target_range:
            reasons.append(f"估值锚由 {previous.target_range} 调整")
        return "；".join(reasons[:3])

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
