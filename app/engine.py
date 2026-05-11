"""金融研报生成引擎 — Agent + RAG 架构"""
from __future__ import annotations

import time
from typing import Callable

from app.agent.orchestrator import AgentOrchestrator
from app.config import ensure_runtime_config
from app.llm import token_stats
from app.models import AblationConfig, AnalysisState

StepCallback = Callable[[str, str, AnalysisState], None]


class ReportEngine:
    """研报引擎 — 基于多Agent编排 + RAG增强"""

    def __init__(self, on_step: StepCallback | None = None, *, ablation_config: AblationConfig | None = None) -> None:
        self.on_step = on_step or (lambda *_: None)
        self.ablation_config = ablation_config or AblationConfig()
        self._orchestrator: AgentOrchestrator | None = None
        self._last_run_metrics: dict = {}

    def run(self, stock_code: str, *, uploaded_items: list[dict] | None = None, event_context: dict | None = None) -> AnalysisState:
        ensure_runtime_config(require_api_key=False)
        start = time.perf_counter()
        before_tokens = token_stats.snapshot()
        self._orchestrator = AgentOrchestrator(on_step=self.on_step, ablation_config=self.ablation_config)
        state = self._orchestrator.run(stock_code, uploaded_items=uploaded_items, event_context=event_context)
        elapsed_ms = (time.perf_counter() - start) * 1000
        after_tokens = token_stats.snapshot()
        run_metrics = {
            "duration_ms": round(elapsed_ms, 1),
            "duration_s": round(elapsed_ms / 1000, 2),
            "llm_calls": after_tokens["total_calls"] - before_tokens["total_calls"],
            "prompt_tokens": after_tokens["total_prompt_tokens"] - before_tokens["total_prompt_tokens"],
            "completion_tokens": after_tokens["total_completion_tokens"] - before_tokens["total_completion_tokens"],
            "total_tokens": after_tokens["total_tokens"] - before_tokens["total_tokens"],
            "success": bool(state.final_report),
        }
        if self._orchestrator and self._orchestrator.tracer:
            trace_summary = self._orchestrator.tracer.summary()
            run_metrics["trace_id"] = trace_summary.get("trace_id", "")
            run_metrics["tool_calls"] = trace_summary.get("tool_calls", 0)
            run_metrics["errors"] = trace_summary.get("errors", 0)
        self._last_run_metrics = run_metrics
        state.run_metrics = run_metrics
        state.run_payload["metrics"] = dict(run_metrics)
        state.sections["run_metrics"] = str(run_metrics)
        return state

    @property
    def agent_trace(self) -> list[dict]:
        if self._orchestrator:
            return self._orchestrator.agent_trace
        return []

    @property
    def rag_trace(self) -> list[dict]:
        if self._orchestrator:
            return self._orchestrator.rag_trace
        return []

    @property
    def trace_summary(self) -> dict:
        if self._orchestrator and self._orchestrator.tracer:
            return self._orchestrator.tracer.summary()
        return {}

    @property
    def last_run_metrics(self) -> dict:
        return dict(self._last_run_metrics)
