from __future__ import annotations

from app.rag import reranker


def test_reranker_cache_roundtrip(monkeypatch):
    reranker._rerank_cache.clear()

    calls = {"count": 0}

    def fake_chat_json(prompt, temperature, max_tokens):
        calls["count"] += 1
        return [{"doc_id": 2, "score": 88, "reason": "best"}]

    import app.llm
    monkeypatch.setattr(app.llm, "chat_json", fake_chat_json)

    candidates = [
        {"doc_id": "a", "content": "doc a", "metadata": {}, "score": 0.1},
        {"doc_id": "b", "content": "doc b", "metadata": {}, "score": 0.2},
        {"doc_id": "c", "content": "doc c", "metadata": {}, "score": 0.3},
    ]

    result1 = reranker.rerank("query", candidates, top_k=1)
    result2 = reranker.rerank("query", candidates, top_k=1)

    assert calls["count"] == 1
    assert result1[0]["doc_id"] == "b"
    assert result2[0]["doc_id"] == "b"
