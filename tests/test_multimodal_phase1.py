from __future__ import annotations

from app.data_source.live_tools import extract_document_summary
from app.data_source.multimodal import parse_uploaded_content
from app.data_source.multimodal.table_extractor import extract_tables


def test_parse_uploaded_text_document_extracts_blocks():
    document = parse_uploaded_content(name="memo.txt", content="第一段\n第二段".encode("utf-8"), content_type="text/plain")

    assert document.source_type == "text"
    assert document.text_blocks[:2] == ["第一段", "第二段"]


def test_extract_tables_detects_markdown_table():
    tables = extract_tables("|列A|列B|\n|---|---|\n|1|2|")

    assert len(tables) == 1
    assert tables[0]["headers"] == ["列A", "列B"]


def test_extract_document_summary_returns_partial_status_for_empty_doc():
    document = parse_uploaded_content(name="image.png", content=b"", content_type="image/png")
    summary = extract_document_summary(document)

    assert summary["parse_status"] == "partial"


def test_parse_uploaded_pdf_degrades_gracefully_without_text():
    document = parse_uploaded_content(name="sample.pdf", content=b"%PDF-1.4\n", content_type="application/pdf")

    assert document.source_type == "pdf"
    assert document.metadata.get("parse_status") == "partial"
