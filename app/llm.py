"""统一 LLM 调用层"""
from __future__ import annotations
import logging
import threading
import time
from dataclasses import dataclass

from app.config import (
    ZHIPUAI_API_KEY, LLM_MODEL, LLM_PROVIDER,
    OPENAI_API_KEY, OPENAI_BASE_URL,
)
from app.llm_providers.base import LLMProvider

logger = logging.getLogger("fin.llm")


@dataclass
class TokenStats:
    total_calls: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0

    def __post_init__(self) -> None:
        self._lock = threading.Lock()

    def record(self, prompt_tokens: int, completion_tokens: int) -> None:
        with self._lock:
            self.total_calls += 1
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += prompt_tokens + completion_tokens

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return {
                "total_calls": self.total_calls,
                "total_prompt_tokens": self.total_prompt_tokens,
                "total_completion_tokens": self.total_completion_tokens,
                "total_tokens": self.total_tokens,
            }

    def summary(self) -> str:
        with self._lock:
            return f"{self.total_calls}次调用 | {self.total_tokens} tokens"


token_stats = TokenStats()
_provider: LLMProvider | None = None
_provider_lock = threading.Lock()


def _get_provider() -> LLMProvider:
    """根据配置创建对应的 LLM Provider（线程安全单例）"""
    global _provider
    if _provider is not None:
        return _provider
    with _provider_lock:
        if _provider is not None:
            return _provider
        if LLM_PROVIDER == "openai":
            from app.llm_providers.openai_provider import OpenAIProvider
            _provider = OpenAIProvider(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        else:
            from app.llm_providers.zhipu_provider import ZhipuProvider
            _provider = ZhipuProvider(api_key=ZHIPUAI_API_KEY)
        return _provider


def chat(prompt: str, *, system: str = "你是一个专业的金融分析师。", temperature: float = 0.5, max_tokens: int = 2048, model: str = "") -> str:
    provider = _get_provider()
    use_model = model or LLM_MODEL
    messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    for attempt in range(3):
        try:
            content, usage = provider.chat(
                messages, model=use_model, temperature=temperature, max_tokens=max_tokens,
            )
            if usage:
                token_stats.record(usage["prompt_tokens"], usage["completion_tokens"])
            return content
        except Exception as e:
            logger.warning(f"LLM 失败 (attempt={attempt + 1}): {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError("LLM 调用 3 次均失败")


def chat_json(prompt: str, *, system: str = "你是一个专业的金融分析师。请以JSON格式输出。",
              temperature: float = 0.1, max_tokens: int = 2048) -> dict:
    """调用 LLM 并解析 JSON 输出"""
    import json as _json
    raw = chat(prompt, system=system, temperature=temperature, max_tokens=max_tokens)
    text = raw.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in text:
        text = text.split("```", 1)[1].split("```", 1)[0].strip()
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        for i, ch in enumerate(text):
            if ch in ('{', '['):
                try:
                    return _json.loads(text[i:])
                except _json.JSONDecodeError:
                    continue
        logger.warning(f"JSON 解析失败，原始输出: {raw[:200]}")
        return {"raw": raw}


def chat_with_tools(messages: list[dict], tools: list[dict], *,
                    temperature: float = 0.1) -> dict:
    """使用 function calling 能力调用工具

    Returns: {"type": "tool_call", "tool": name, "arguments": {...}}
             或 {"type": "message", "content": "..."}
    """
    provider = _get_provider()
    for attempt in range(3):
        try:
            result, usage = provider.chat_with_tools(
                messages, tools, model=LLM_MODEL, temperature=temperature,
            )
            if usage:
                token_stats.record(usage["prompt_tokens"], usage["completion_tokens"])
            return result
        except Exception as e:
            logger.warning(f"Function calling 失败 (attempt={attempt + 1}): {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError("Function calling 3 次均失败")


def get_shared_client():
    """获取共享的底层客户端实例（供 embeddings 等模块复用）

    注意：返回类型取决于当前 provider，优先使用 provider.embed() 代替。
    """
    provider = _get_provider()
    if hasattr(provider, "client"):
        return provider.client
    return provider
