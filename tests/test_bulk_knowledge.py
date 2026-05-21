from __future__ import annotations

import json

from app.rag.bulk_knowledge import import_bulk_knowledge, render_financebench_sample, render_stock_universe_entry


def test_render_stock_universe_entry_is_searchable() -> None:
    text = render_stock_universe_entry({"code": "600519", "name": "贵州茅台", "aliases": "maotai"})

    assert "股票代码 600519" in text
    assert "贵州茅台" in text
    assert "股票名称/代码消歧" in text
    assert "使用边界" in text


def test_render_financebench_sample_contains_evidence() -> None:
    sample = {
        "financebench_id": "financebench_id_test",
        "company": "3M",
        "doc_name": "3M_2018_10K",
        "question": "What is capex?",
        "answer": "$100",
        "justification": "Extracted from cash flow statement.",
        "evidence": [{"evidence_text": "Purchases of property, plant and equipment 100"}],
    }

    text = render_financebench_sample(sample)

    assert "FinanceBench 样本" in text
    assert "What is capex?" in text
    assert "Purchases of property" in text
    assert "## 使用边界" in text


def test_import_bulk_knowledge_writes_selected_corpora(tmp_path) -> None:
    cache_dir = tmp_path / "cache"
    benchmark_dir = tmp_path / "benchmarks"
    cache_dir.mkdir()
    (benchmark_dir / "public").mkdir(parents=True)
    (cache_dir / "stock_a_code_name_directory.json").write_text(
        json.dumps({"items": [{"code": "600519", "name": "贵州茅台", "aliases": "maotai"}]}, ensure_ascii=False),
        encoding="utf-8",
    )
    (benchmark_dir / "public" / "financebench_open_source_full.jsonl").write_text(
        json.dumps({"financebench_id": "fb1", "company": "3M", "question": "Q", "answer": "A", "evidence": []}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (benchmark_dir / "tracking_events_real.jsonl").write_text("", encoding="utf-8")
    (benchmark_dir / "agent_tasks.jsonl").write_text("", encoding="utf-8")

    result = import_bulk_knowledge(
        cache_dir=cache_dir,
        benchmark_dir=benchmark_dir,
        output_dir=tmp_path / "kb",
        manifest_path=tmp_path / "manifest.json",
        include_cache_items=False,
        include_daily_bars=False,
    )

    assert result.imported_count == 2
    assert result.corpus_counts["stock_universe"] == 1
    assert result.corpus_counts["financebench"] == 1
    assert (tmp_path / "manifest.json").exists()
