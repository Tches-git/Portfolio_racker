"""图片/OCR 解析适配层。"""
from __future__ import annotations

from app.data_source.multimodal.normalizer import mark_parse_failure, normalize_text_document
from app.data_source.multimodal.table_extractor import extract_tables
from app.models import SourceDocument


def parse_image_document(*, name: str, content: bytes, content_type: str = "") -> SourceDocument:
    text = _decode_image_bytes(content)
    tables = extract_tables(text)
    document = normalize_text_document(
        name=name,
        text=text,
        source_type="image",
        metadata={"content_type": content_type or "image/unknown", "ocr_engine": "fallback"},
        tables=tables,
    )
    if not document.text_blocks and not document.tables:
        return mark_parse_failure(document, reason="未安装 OCR 引擎，且无法从文件字节中恢复文本", stage="ocr")
    return document


def _decode_image_bytes(content: bytes) -> str:
    if not content:
        return ""
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content.decode("utf-8", errors="ignore")
        except Exception:
            return ""
