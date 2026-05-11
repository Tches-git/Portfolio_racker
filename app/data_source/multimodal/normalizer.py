"""多模态解析结果归一化。"""
from __future__ import annotations

from datetime import datetime
from hashlib import md5

from app.models import SourceDocument


def build_source_id(name: str, content: bytes | str = b"") -> str:
    raw = content.encode("utf-8", errors="ignore") if isinstance(content, str) else bytes(content)
    return md5(f"{name}::{raw[:256]!r}".encode("utf-8", errors="ignore")).hexdigest()[:16]


def normalize_text_document(*, name: str, text: str, source_type: str, metadata: dict[str, str] | None = None, tables: list[dict] | None = None) -> SourceDocument:
    clean_blocks = [line.strip() for line in (text or "").splitlines() if line.strip()]
    return SourceDocument(
        source_id=build_source_id(name, text),
        source_type=source_type,
        title=name,
        text_blocks=clean_blocks[:50],
        tables=list(tables or []),
        metadata={"file_name": name, **(metadata or {})},
        extracted_at=datetime.now().isoformat(),
    )


def mark_parse_failure(document: SourceDocument, *, reason: str, stage: str) -> SourceDocument:
    document.metadata.setdefault("parse_status", "partial")
    document.metadata[f"{stage}_error"] = reason
    return document
