"""LLM Provider 抽象接口定义"""
from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    """LLM 供应商抽象接口"""

    def chat(self, messages: list[dict], *, model: str,
             temperature: float, max_tokens: int) -> tuple[str, dict]:
        """聊天补全，返回 (content, usage_dict)

        usage_dict: {"prompt_tokens": int, "completion_tokens": int}
        """
        ...

    def chat_with_tools(self, messages: list[dict], tools: list[dict], *,
                        model: str, temperature: float) -> tuple[dict, dict]:
        """工具调用，返回 (result_dict, usage_dict)

        result_dict: {"type": "tool_call"/"message", ...}
        usage_dict: {"prompt_tokens": int, "completion_tokens": int}
        """
        ...

    def embed(self, texts: list[str], *, model: str) -> list[list[float]]:
        """生成文本向量"""
        ...
