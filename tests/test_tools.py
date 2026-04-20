"""Agent 工具模块单元测试"""
from __future__ import annotations

import pytest

from app.models import AnalysisState, ToolCallRecord
from app.agent.tools import Tool, execute_tool


def _make_tool(name: str = "test_tool", retryable: bool = True,
               cacheable: bool = True, fn=None) -> Tool:
    """创建测试用工具"""
    if fn is None:
        fn = lambda **kwargs: f"result_{kwargs.get('x', 'default')}"
    return Tool(
        name=name,
        description="测试工具",
        parameters_schema={"type": "object", "properties": {}, "required": []},
        function=fn,
        retryable=retryable,
        cacheable=cacheable,
    )


class TestExecuteTool:
    """execute_tool 函数测试"""

    def test_basic_execution(self):
        tool = _make_tool(fn=lambda **kw: "hello")
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state)
        assert result == "hello"
        assert len(state.tool_memory) == 1
        assert state.tool_memory[0].success is True

    def test_unknown_tool(self):
        result = execute_tool([], "nonexistent", {})
        assert "未知工具" in result

    def test_cache_hit(self):
        call_count = 0

        def counting_fn(**kw):
            nonlocal call_count
            call_count += 1
            return "cached_result"

        tool = _make_tool(fn=counting_fn, cacheable=True)
        state = AnalysisState()

        # 第一次调用
        result1 = execute_tool([tool], "test_tool", {}, state=state)
        assert result1 == "cached_result"
        assert call_count == 1

        # 第二次调用应命中缓存
        result2 = execute_tool([tool], "test_tool", {}, state=state)
        assert "[缓存]" in result2
        assert call_count == 1  # 没有再次调用

    def test_no_cache_when_disabled(self):
        call_count = 0

        def counting_fn(**kw):
            nonlocal call_count
            call_count += 1
            return "result"

        tool = _make_tool(fn=counting_fn, cacheable=False)
        state = AnalysisState()

        execute_tool([tool], "test_tool", {}, state=state)
        execute_tool([tool], "test_tool", {}, state=state)
        assert call_count == 2

    def test_retry_on_failure(self):
        attempt_count = 0

        def failing_fn(**kw):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise RuntimeError("模拟失败")
            return "success"

        tool = _make_tool(fn=failing_fn, retryable=True)
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state, max_retries=2)
        assert result == "success"

    def test_all_retries_fail(self):
        def always_fail(**kw):
            raise RuntimeError("永远失败")

        tool = _make_tool(fn=always_fail, retryable=True)
        state = AnalysisState()
        result = execute_tool([tool], "test_tool", {}, state=state, max_retries=1)
        assert "失败" in result
        assert state.tool_memory[-1].success is False

    def test_records_tool_memory(self):
        tool = _make_tool(fn=lambda **kw: "ok")
        state = AnalysisState()
        execute_tool([tool], "test_tool", {"x": "1"}, state=state)
        assert len(state.tool_memory) == 1
        rec = state.tool_memory[0]
        assert rec.tool_name == "test_tool"
        assert rec.args == {"x": "1"}
        assert rec.observation == "ok"
