"""结构化追踪系统 — 记录分析流程的每个步骤"""
import time
import uuid
import json
import threading
from dataclasses import dataclass, field
from pathlib import Path
from contextlib import contextmanager
from typing import Any


@dataclass
class Span:
    """一个追踪跨度（某个操作的记录）"""
    name: str                      # 操作名称
    span_type: str                 # 类型: phase / tool / llm / rag
    start_time: float = 0.0
    end_time: float = 0.0
    duration_ms: float = 0.0       # 耗时(毫秒)
    status: str = "ok"             # ok / error
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list["Span"] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "name": self.name,
            "type": self.span_type,
            "duration_ms": round(self.duration_ms, 1),
            "status": self.status,
        }
        if self.metadata:
            d["metadata"] = self.metadata
        if self.children:
            d["children"] = [c.to_dict() for c in self.children]
        return d


class Tracer:
    """分析流程追踪器"""

    def __init__(self):
        self.trace_id: str = uuid.uuid4().hex[:12]
        self.spans: list[Span] = []
        self._span_stack: list[Span] = []  # 用于嵌套 span
        self._lock = threading.Lock()
        self._start_time = time.time()

    @contextmanager
    def span(self, name: str, span_type: str = "phase", **metadata):
        """上下文管理器：记录一个操作的耗时

        用法：
            with tracer.span("research_agent", "phase"):
                ...
            with tracer.span("fetch_profile", "tool", tool="fetch_stock_profile"):
                ...
        """
        s = Span(name=name, span_type=span_type, start_time=time.time(), metadata=metadata)
        with self._lock:
            if self._span_stack:
                self._span_stack[-1].children.append(s)
            else:
                self.spans.append(s)
            self._span_stack.append(s)
        try:
            yield s
        except Exception as e:
            s.status = "error"
            s.metadata["error"] = str(e)
            raise
        finally:
            s.end_time = time.time()
            s.duration_ms = (s.end_time - s.start_time) * 1000
            with self._lock:
                self._span_stack.pop()

    def record(self, name: str, span_type: str, duration_ms: float, **metadata):
        """直接记录一个已完成的 span（不使用上下文管理器）"""
        s = Span(name=name, span_type=span_type, duration_ms=duration_ms,
                 start_time=time.time() - duration_ms / 1000, end_time=time.time(),
                 metadata=metadata)
        with self._lock:
            if self._span_stack:
                self._span_stack[-1].children.append(s)
            else:
                self.spans.append(s)

    def summary(self) -> dict:
        """生成追踪摘要统计"""
        total_time = (time.time() - self._start_time) * 1000

        # 按类型统计
        stats: dict[str, list[Span]] = {"phase": [], "tool": [], "llm": [], "rag": []}

        def _collect(spans: list[Span]):
            for s in spans:
                if s.span_type in stats:
                    stats[s.span_type].append(s)
                _collect(s.children)
        with self._lock:
            spans_snapshot = list(self.spans)
        _collect(spans_snapshot)

        phase_spans = stats["phase"]
        tool_calls = stats["tool"]
        llm_calls = stats["llm"]
        failed_phases = [s for s in phase_spans if s.status == "error"]

        return {
            "trace_id": self.trace_id,
            "total_duration_ms": round(total_time, 1),
            "total_duration_s": round(total_time / 1000, 1),
            "phases": len(phase_spans),
            "phase_total_ms": round(sum(s.duration_ms for s in phase_spans), 1),
            "phase_breakdown": [
                {"name": s.name, "status": s.status, "ms": round(s.duration_ms, 1)}
                for s in phase_spans
            ],
            "failed_phases": [
                {"name": s.name, "status": s.status, "ms": round(s.duration_ms, 1)}
                for s in failed_phases
            ],
            "tool_calls": len(tool_calls),
            "tool_total_ms": round(sum(s.duration_ms for s in tool_calls), 1),
            "llm_calls": len(llm_calls),
            "llm_total_ms": round(sum(s.duration_ms for s in llm_calls), 1),
            "errors": sum(1 for s in phase_spans + tool_calls + llm_calls if s.status == "error"),
            # 最慢的 3 个操作
            "slowest": [
                {"name": s.name, "type": s.span_type, "ms": round(s.duration_ms, 1)}
                for s in sorted(tool_calls + llm_calls,
                                key=lambda x: x.duration_ms, reverse=True)[:3]
            ],
        }

    def _snapshot_spans(self) -> list[Span]:
        with self._lock:
            return list(self.spans)

    def export_json(self, path: Path) -> None:
        """导出完整 trace 到 JSON 文件"""
        data = {
            "trace_id": self.trace_id,
            "summary": self.summary(),
            "spans": [s.to_dict() for s in self._snapshot_spans()],
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ── 全局活跃追踪器 ──
_active_tracer: Tracer | None = None
_tracer_lock = threading.Lock()


def set_active_tracer(tracer: Tracer | None) -> None:
    global _active_tracer
    with _tracer_lock:
        _active_tracer = tracer


def get_active_tracer() -> Tracer | None:
    with _tracer_lock:
        return _active_tracer
