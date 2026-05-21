from __future__ import annotations

import json

from app.rag.external_sources import (
    filter_external_sources,
    import_external_source_summaries,
    load_external_sources,
    render_source_markdown,
)


def test_external_source_catalog_loads() -> None:
    sources = load_external_sources()

    source_ids = {source.id for source in sources}
    assert len(sources) >= 8
    assert "ai4finance-fingpt" in source_ids
    assert "dgunning-edgartools" in source_ids
    assert "finagent-benchmark" in source_ids


def test_filter_external_sources_by_market_and_category() -> None:
    sources = load_external_sources()

    filtered = filter_external_sources(
        sources,
        categories=["sec_filings_connector"],
        markets=["us"],
    )

    assert [source.id for source in filtered] == ["dgunning-edgartools"]


def test_render_source_markdown_has_rag_sections() -> None:
    source = filter_external_sources(load_external_sources(), source_ids=["ai4finance-finrobot"])[0]

    markdown = render_source_markdown(source)

    assert "# 外部金融知识源：FinRobot" in markdown
    assert "## 来源" in markdown
    assert "## 投研关注点" in markdown
    assert "## RAG 检索关键词" in markdown
    assert "## 使用边界" in markdown
    assert "`ai4finance-finrobot`" in markdown


def test_import_external_source_summaries_writes_docs(tmp_path) -> None:
    output_dir = tmp_path / "kb"
    manifest_path = tmp_path / "manifest.json"

    result = import_external_source_summaries(
        source_ids=["ai4finance-fingpt", "dgunning-edgartools"],
        output_dir=output_dir,
        manifest_path=manifest_path,
    )

    assert result.imported_count == 2
    assert (output_dir / "ai4finance-fingpt.md").exists()
    assert (output_dir / "dgunning-edgartools.md").exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["source_count"] == 2
    assert manifest["source_ids"] == ["ai4finance-fingpt", "dgunning-edgartools"]
