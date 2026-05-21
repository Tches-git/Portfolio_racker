from __future__ import annotations

from app.config import EMBED_DIMENSION
from app.rag import embeddings


class _BrokenProvider:
    def embed(self, texts: list[str], *, model: str) -> list[list[float]]:
        raise RuntimeError("embedding endpoint missing")


class _NotFoundProvider:
    calls = 0

    def embed(self, texts: list[str], *, model: str) -> list[list[float]]:
        self.calls += 1
        raise RuntimeError("404 page not found")


def test_embedding_falls_back_to_local_hash(monkeypatch) -> None:
    monkeypatch.setattr(embeddings, "_remote_embedding_disabled", False)
    monkeypatch.setattr(embeddings, "_get_embed_provider", lambda: _BrokenProvider())
    monkeypatch.setattr(embeddings.time, "sleep", lambda _: None)

    vectors = embeddings.embed_texts(["比亚迪 新能源汽车", "贵州茅台 高端白酒"], fail_fast=True)

    assert len(vectors) == 2
    assert len(vectors[0]) == EMBED_DIMENSION
    assert any(value != 0 for value in vectors[0])


def test_query_embedding_uses_same_fallback(monkeypatch) -> None:
    monkeypatch.setattr(embeddings, "_remote_embedding_disabled", False)
    monkeypatch.setattr(embeddings, "_get_embed_provider", lambda: _BrokenProvider())
    monkeypatch.setattr(embeddings.time, "sleep", lambda _: None)

    query_vector = embeddings.embed_query("网络安全 行业 风险")

    assert len(query_vector) == EMBED_DIMENSION
    assert any(value != 0 for value in query_vector)


def test_permanent_embedding_error_disables_remote(monkeypatch) -> None:
    monkeypatch.setattr(embeddings, "_remote_embedding_disabled", False)
    provider = _NotFoundProvider()
    monkeypatch.setattr(embeddings, "_get_embed_provider", lambda: provider)
    monkeypatch.setattr(embeddings.time, "sleep", lambda _: None)

    first = embeddings.embed_texts(["FinanceBench 引用覆盖率"])
    second = embeddings.embed_texts(["AutoGen 多角色工作流"])

    assert len(first) == 1
    assert len(second) == 1
    assert provider.calls == 1
