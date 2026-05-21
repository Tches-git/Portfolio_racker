from __future__ import annotations

from pathlib import Path


KB_DOCS_DIR = Path("data/knowledge_base")


def test_curated_knowledge_docs_exist() -> None:
    docs = sorted(KB_DOCS_DIR.glob("**/*.md"))

    assert len(docs) >= 8
    assert any(path.name == "byd_002594_profile.md" for path in docs)
    assert any(path.name == "financial_benchmark_design.md" for path in docs)


def test_curated_knowledge_docs_have_rag_structure() -> None:
    required_sections = [
        "## 来源",
        "## 关键事实",
        "## 投研关注点",
        "## RAG 检索关键词",
        "## 使用边界",
    ]

    for path in KB_DOCS_DIR.glob("**/*.md"):
        text = path.read_text(encoding="utf-8")
        for section in required_sections:
            assert section in text, f"{path} 缺少 {section}"
        assert "http" in text, f"{path} 缺少来源链接"
