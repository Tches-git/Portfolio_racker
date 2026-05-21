from __future__ import annotations

import json

from app.rag.cache_knowledge import build_stock_cache_payload, import_stock_cache_knowledge, render_stock_cache_markdown


def test_build_stock_cache_payload_reads_profile_and_items(tmp_path) -> None:
    (tmp_path / "profile_600519.json").write_text(
        json.dumps({"code": "600519", "name": "贵州茅台", "industry": "白酒", "market_cap": 100.0}, ensure_ascii=False),
        encoding="utf-8",
    )
    (tmp_path / "announcement_cninfo_600519_12.json").write_text(
        json.dumps({"items": [{"title": "年度报告", "time": "2026-04-01", "source": "cninfo", "link": "http://example.com/a"}]}, ensure_ascii=False),
        encoding="utf-8",
    )

    payload = build_stock_cache_payload("600519", cache_dir=tmp_path)

    assert payload is not None
    assert payload["name"] == "贵州茅台"
    assert payload["announcements"][0]["title"] == "年度报告"


def test_render_stock_cache_markdown_has_rag_structure(tmp_path) -> None:
    (tmp_path / "profile_002594.json").write_text(
        json.dumps({"code": "002594", "name": "比亚迪", "industry": "汽车", "market_cap": 100.0, "pe_ratio": 20.0}, ensure_ascii=False),
        encoding="utf-8",
    )
    payload = build_stock_cache_payload("002594", cache_dir=tmp_path)

    markdown = render_stock_cache_markdown(payload)

    assert "# A股公司知识快照：比亚迪（002594）" in markdown
    assert "## 来源" in markdown
    assert "## 关键事实" in markdown
    assert "## 投研关注点" in markdown
    assert "## RAG 检索关键词" in markdown
    assert "## 使用边界" in markdown
    assert "http" in markdown


def test_import_stock_cache_knowledge_writes_docs_and_manifest(tmp_path) -> None:
    (tmp_path / "profile_600036.json").write_text(
        json.dumps({"code": "600036", "name": "招商银行", "industry": "银行Ⅱ", "pb_ratio": 0.8}, ensure_ascii=False),
        encoding="utf-8",
    )
    output_dir = tmp_path / "kb"
    manifest_path = tmp_path / "manifest.json"

    result = import_stock_cache_knowledge(cache_dir=tmp_path, output_dir=output_dir, manifest_path=manifest_path)

    assert result.imported_count == 1
    assert result.output_paths[0].exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["imported_count"] == 1
    assert manifest["stock_codes"] == ["600036"]
