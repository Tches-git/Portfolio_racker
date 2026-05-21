"""OpenAI 兼容 Provider 实现（同时兼容 DeepSeek / 通义千问等）"""
from __future__ import annotations
import json
import os


class OpenAIProvider:
    """基于 OpenAI SDK 的 LLM Provider（可选依赖）"""

    def __init__(self, api_key: str, base_url: str = "") -> None:
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "使用 OpenAI Provider 需要安装 openai 库: pip install openai"
            )
        kwargs: dict = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self._timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "90"))
        kwargs["timeout"] = self._timeout
        self._client = OpenAI(**kwargs)

    def chat(self, messages: list[dict], *, model: str,
             temperature: float, max_tokens: int) -> tuple[str, dict]:
        resp = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=self._timeout,
        )
        usage = resp.usage
        usage_dict = {}
        if usage:
            usage_dict = {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
            }
        if not getattr(resp, "choices", None):
            raise ValueError("LLM 返回空 choices")
        message = resp.choices[0].message
        content = getattr(message, "content", None)
        if not content:
            raise ValueError("LLM 返回空响应")
        return content.strip(), usage_dict

    def chat_with_tools(self, messages: list[dict], tools: list[dict], *,
                        model: str, temperature: float) -> tuple[dict, dict]:
        resp = self._client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=temperature,
            timeout=self._timeout,
        )
        usage = resp.usage
        usage_dict = {}
        if usage:
            usage_dict = {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
            }
        if not getattr(resp, "choices", None):
            raise ValueError("LLM 返回空 choices")
        choice = resp.choices[0]
        msg = choice.message

        if msg.tool_calls:
            tc = msg.tool_calls[0]
            try:
                args = json.loads(tc.function.arguments)
            except Exception:
                args = {}
            result = {
                "type": "tool_call",
                "tool": tc.function.name,
                "arguments": args,
                "raw_message": msg,
            }
        else:
            result = {
                "type": "message",
                "content": msg.content.strip() if msg.content else "",
            }
        return result, usage_dict

    def embed(self, texts: list[str], *, model: str) -> list[list[float]]:
        resp = self._client.embeddings.create(model=model, input=texts, timeout=self._timeout)
        return [item.embedding for item in resp.data]
