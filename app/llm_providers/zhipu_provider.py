"""智谱 AI Provider 实现"""
from __future__ import annotations
import json
from zhipuai import ZhipuAI


class ZhipuProvider:
    """基于智谱 AI SDK 的 LLM Provider"""

    def __init__(self, api_key: str) -> None:
        self._client = ZhipuAI(api_key=api_key)

    @property
    def client(self) -> ZhipuAI:
        """暴露底层客户端，供 embeddings 等模块直接使用"""
        return self._client

    def chat(self, messages: list[dict], *, model: str,
             temperature: float, max_tokens: int) -> tuple[str, dict]:
        resp = self._client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
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
        resp = self._client.embeddings.create(model=model, input=texts)
        return [item.embedding for item in resp.data]
