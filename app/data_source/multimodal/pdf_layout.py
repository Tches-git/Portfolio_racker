"""PDF 版面解析适配层。"""
from __future__ import annotations

from io import BytesIO

from app.data_source.multimodal.normalizer import mark_parse_failure, normalize_text_document
from app.data_source.multimodal.table_extractor import extract_tables
from app.models import SourceDocument


def parse_pdf_layout(*, name: str, content: bytes) -> SourceDocument:
    text = _extract_pdf_text(content)
    tables = extract_tables(text)
    document = normalize_text_document(
        name=name,
        text=text,
        source_type="pdf",
        metadata={"parser": "pypdf", "layout_mode": "basic"},
        tables=tables,
    )
    if not document.text_blocks:
        return mark_parse_failure(document, reason="PDF 未解析出可用文本，已降级为空文档", stage="pdf")
    return document


def _extract_pdf_text(content: bytes) -> str:
    if not content:
        return ""
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(BytesIO(content))
        parts: list[str] = []
        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            if text:
                parts.append(text)
        return "\n\n".join(parts)
    except Exception:
        return ""
