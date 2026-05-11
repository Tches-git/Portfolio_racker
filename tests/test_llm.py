from __future__ import annotations

from types import SimpleNamespace

import pytest

import app.llm as llm


class DummyProvider:
    def __init__(self, responses=None, failures: int = 0):
        self.responses = responses or []
        self.failures = failures
        self.chat_calls = 0

    def chat(self, messages, *, model, temperature, max_tokens):
        self.chat_calls += 1
        if self.failures > 0:
            self.failures -= 1
            raise RuntimeError("temporary failure")
        return self.responses.pop(0)

    def chat_with_tools(self, messages, tools, *, model, temperature):
        return {"type": "message", "content": "ok"}, {"prompt_tokens": 1, "completion_tokens": 1}


def test_chat_retries_and_records_tokens(monkeypatch):
    provider = DummyProvider(responses=[("done", {"prompt_tokens": 10, "completion_tokens": 5})], failures=2)
    monkeypatch.setattr(llm, "_provider", provider)
    monkeypatch.setattr(llm, "LLM_MODEL", "test-model")
    llm.token_stats = llm.TokenStats()

    result = llm.chat("hello")

    assert result == "done"
    assert provider.chat_calls == 3
    assert llm.token_stats.total_calls == 1
    assert llm.token_stats.total_tokens == 15


def test_chat_json_extracts_json_block(monkeypatch):
    provider = DummyProvider(responses=[("```json\n{\"score\": 95}\n```", {"prompt_tokens": 1, "completion_tokens": 1})])
    monkeypatch.setattr(llm, "_provider", provider)
    assert llm.chat_json("hello") == {"score": 95}


def test_chat_json_fallback_returns_raw(monkeypatch):
    provider = DummyProvider(responses=[("not json at all", {"prompt_tokens": 1, "completion_tokens": 1})])
    monkeypatch.setattr(llm, "_provider", provider)
    assert llm.chat_json("hello") == {"raw": "not json at all"}


def test_zhipu_provider_rejects_empty_choices():
    from app.llm_providers.zhipu_provider import ZhipuProvider

    provider = object.__new__(ZhipuProvider)
    provider._client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(usage=None, choices=[]))
        )
    )

    with pytest.raises(ValueError, match="empty|空"):
        provider.chat([], model="m", temperature=0, max_tokens=10)


def test_openai_provider_rejects_empty_choices():
    from app.llm_providers.openai_provider import OpenAIProvider

    provider = object.__new__(OpenAIProvider)
    provider._client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=lambda **kwargs: SimpleNamespace(usage=None, choices=[]))
        )
    )

    with pytest.raises(ValueError, match="empty|空"):
        provider.chat([], model="m", temperature=0, max_tokens=10)
