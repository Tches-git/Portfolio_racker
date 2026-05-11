"""多模态文档解析入口。"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from app.models import SourceDocument

_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}
_TEXT_SUFFIXES = {".txt", ".md"}


def parse_uploaded_items(items: list[dict[str, Any]]) -> list[SourceDocument]:
    documents: list[SourceDocument] = []
    for item in items or []:
        name = str(item.get("name", "") or "").strip()
        content = item.get("content", b"") or b""
        content_type = str(item.get("content_type", "") or "")
        if not name:
            continue
        documents.append(parse_uploaded_content(name=name, content=content, content_type=content_type))
    return documents


def parse_uploaded_content(*, name: str, content: bytes, content_type: str = "") -> SourceDocument:
    suffix = Path(name).suffix.lower()
    if suffix == ".pdf":
        from app.data_source.multimodal.pdf_layout import parse_pdf_layout

        return parse_pdf_layout(name=name, content=content)
    if suffix in _IMAGE_SUFFIXES or content_type.startswith("image/"):
        from app.data_source.multimodal.ocr import parse_image_document

        return parse_image_document(name=name, content=content, content_type=content_type)
    if suffix in _TEXT_SUFFIXES or content_type.startswith("text/"):
        from app.data_source.multimodal.normalizer import normalize_text_document
        from app.data_source.multimodal.table_extractor import extract_tables

        text = content.decode("utf-8", errors="ignore")
        return normalize_text_document(name=name, text=text, source_type="text", tables=extract_tables(text))

    from app.data_source.multimodal.normalizer import normalize_text_document
    from app.data_source.multimodal.table_extractor import extract_tables

    fallback = content.decode("utf-8", errors="ignore") if content else ""
    return normalize_text_document(name=name, text=fallback, source_type="unknown", tables=extract_tables(fallback))
