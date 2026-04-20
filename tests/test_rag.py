"""RAG 模块单元测试"""
from __future__ import annotations

import pytest
import numpy as np

from app.rag.document import (
    split_sentences,
    semantic_chunk_text,
    build_documents,
    _is_heading,
)


class TestSplitSentences:
    """句子切分测试"""

    def test_chinese_period(self):
        result = split_sentences("第一句。第二句。第三句。")
        assert len(result) == 3

    def test_mixed_punctuation(self):
        result = split_sentences("这是问题？这是感叹！这是结尾。")
        assert len(result) == 3

    def test_double_newline(self):
        result = split_sentences("段落一\n\n段落二")
        assert len(result) == 2

    def test_empty_string(self):
        result = split_sentences("")
        assert result == []


class TestIsHeading:
    """标题识别测试"""

    def test_markdown_heading(self):
        assert _is_heading("## 财务分析")
        assert _is_heading("# 投资要点")

    def test_chinese_heading(self):
        assert _is_heading("第一章 公司概况")
        assert _is_heading("一、投资要点")

    def test_normal_text(self):
        assert not _is_heading("这是一段普通文本。")


class TestSemanticChunk:
    """语义分块测试"""

    def test_short_text_single_chunk(self):
        text = "这是一段很短的文本。"
        chunks = semantic_chunk_text(text, target_size=800)
        assert len(chunks) == 1

    def test_long_text_splits(self):
        text = "。".join([f"这是第{i}个句子，包含一些内容" for i in range(50)])
        chunks = semantic_chunk_text(text, target_size=100)
        assert len(chunks) > 1

    def test_heading_boundary(self):
        text = "前面的内容。更多内容。\n\n## 新章节\n新章节内容。"
        chunks = semantic_chunk_text(text, target_size=800)
        assert len(chunks) >= 1

    def test_empty_text(self):
        assert semantic_chunk_text("") == []

    def test_min_chunk_size_merge(self):
        text = "长句子" * 100 + "。短。"
        chunks = semantic_chunk_text(text, target_size=200, min_chunk_size=50)
        for chunk in chunks:
            assert len(chunk) >= 50 or chunk == chunks[-1]


class TestBuildDocuments:
    """文档构建测试"""

    def test_generates_doc_id(self):
        docs = build_documents("测试文本内容，足够长的文本。" * 3)
        assert len(docs) >= 1
        assert docs[0].doc_id != ""

    def test_metadata_preserved(self):
        docs = build_documents(
            "测试文本。" * 20,
            metadata={"source": "test", "topic": "测试"},
        )
        assert docs[0].metadata["source"] == "test"

    def test_source_page_in_metadata(self):
        docs = build_documents("测试文本。" * 20, source_page=5)
        assert docs[0].metadata.get("source_page") == 5

    def test_chunk_index_tracking(self):
        text = "。".join([f"这是第{i}个句子" for i in range(100)])
        docs = build_documents(text, chunk_size=100)
        if len(docs) > 1:
            assert docs[0].metadata["chunk_index"] == 0
            assert docs[1].metadata["chunk_index"] == 1


class TestVectorStore:
    """向量存储测试（使用 numpy 回退模式）"""

    def test_add_and_search(self):
        from app.rag.vector_store import VectorStore

        store = VectorStore(dimension=4)
        store._use_faiss = False
        store._vectors = []

        embeddings = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
        docs = [
            {"content": "文档A", "metadata": {}, "doc_id": "a"},
            {"content": "文档B", "metadata": {}, "doc_id": "b"},
            {"content": "文档C", "metadata": {}, "doc_id": "c"},
        ]
        store.add(embeddings, docs)
        assert store.size == 3

        results = store.search([1.0, 0.0, 0.0, 0.0], top_k=2)
        assert len(results) == 2
        assert results[0]["content"] == "文档A"

    def test_empty_search(self):
        from app.rag.vector_store import VectorStore

        store = VectorStore(dimension=4)
        results = store.search([1.0, 0.0, 0.0, 0.0])
        assert results == []

    def test_save_and_load(self, tmp_path):
        from app.rag.vector_store import VectorStore

        store = VectorStore(dimension=4)
        store._use_faiss = False
        store._vectors = []

        store.add(
            [[1.0, 0.0, 0.0, 0.0]],
            [{"content": "测试", "metadata": {}, "doc_id": "t1"}],
        )
        store.save(tmp_path)

        store2 = VectorStore(dimension=4)
        store2._use_faiss = False
        store2._vectors = []
        assert store2.load(tmp_path)
        assert store2.size == 1
