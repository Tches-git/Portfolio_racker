"""外部金融知识源目录与 RAG 摘要导入。"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import DATA_DIR, KNOWLEDGE_DOCS_DIR

CATALOG_PATH = DATA_DIR / "external_knowledge_sources" / "catalog.json"
DEFAULT_OUTPUT_DIR = KNOWLEDGE_DOCS_DIR / "external_sources"
IMPORT_MANIFEST_PATH = DATA_DIR / "external_knowledge_sources" / "import_manifest.json"


@dataclass(frozen=True)
class ExternalKnowledgeSource:
    id: str
    name: str
    category: str
    market: str
    language: list[str]
    license: str
    source_type: str
    repository_url: str
    source_url: str
    doc_types: list[str]
    ingestion_mode: str
    enterprise_value: str
    use_cases: list[str]
    limitations: list[str]
    citation: str
    tags: list[str]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ExternalKnowledgeSource":
        return cls(
            id=str(payload["id"]),
            name=str(payload["name"]),
            category=str(payload["category"]),
            market=str(payload["market"]),
            language=[str(item) for item in payload.get("language", [])],
            license=str(payload.get("license", "unknown")),
            source_type=str(payload.get("source_type", "unknown")),
            repository_url=str(payload.get("repository_url", "")),
            source_url=str(payload.get("source_url", "")),
            doc_types=[str(item) for item in payload.get("doc_types", [])],
            ingestion_mode=str(payload.get("ingestion_mode", "catalog_summary")),
            enterprise_value=str(payload.get("enterprise_value", "")),
            use_cases=[str(item) for item in payload.get("use_cases", [])],
            limitations=[str(item) for item in payload.get("limitations", [])],
            citation=str(payload.get("citation", "")),
            tags=[str(item) for item in payload.get("tags", [])],
        )


@dataclass(frozen=True)
class ExternalKnowledgeImportResult:
    imported_count: int
    output_paths: list[Path]
    source_ids: list[str]
    manifest_path: Path


def load_external_sources(catalog_path: Path = CATALOG_PATH) -> list[ExternalKnowledgeSource]:
    if not catalog_path.exists():
        raise FileNotFoundError(f"外部知识源目录不存在: {catalog_path}")
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("外部知识源目录必须是 JSON 数组")
    sources = [ExternalKnowledgeSource.from_dict(item) for item in payload]
    _validate_unique_ids(sources)
    return sources


def filter_external_sources(
    sources: list[ExternalKnowledgeSource],
    *,
    source_ids: list[str] | None = None,
    categories: list[str] | None = None,
    markets: list[str] | None = None,
) -> list[ExternalKnowledgeSource]:
    wanted_ids = {item.strip() for item in source_ids or [] if item.strip()}
    wanted_categories = {item.strip() for item in categories or [] if item.strip()}
    wanted_markets = {item.strip() for item in markets or [] if item.strip()}

    filtered = []
    for source in sources:
        if wanted_ids and source.id not in wanted_ids:
            continue
        if wanted_categories and source.category not in wanted_categories:
            continue
        if wanted_markets and source.market not in wanted_markets:
            continue
        filtered.append(source)

    missing_ids = wanted_ids - {source.id for source in sources}
    if missing_ids:
        raise ValueError(f"未知外部知识源: {', '.join(sorted(missing_ids))}")
    return filtered


def import_external_source_summaries(
    *,
    source_ids: list[str] | None = None,
    categories: list[str] | None = None,
    markets: list[str] | None = None,
    catalog_path: Path = CATALOG_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    manifest_path: Path = IMPORT_MANIFEST_PATH,
) -> ExternalKnowledgeImportResult:
    sources = filter_external_sources(
        load_external_sources(catalog_path),
        source_ids=source_ids,
        categories=categories,
        markets=markets,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for source in sources:
        output_path = output_dir / f"{_slugify(source.id)}.md"
        output_path.write_text(render_source_markdown(source), encoding="utf-8")
        output_paths.append(output_path)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "catalog_path": str(catalog_path),
        "output_dir": str(output_dir),
        "source_ids": [source.id for source in sources],
        "source_count": len(sources),
        "outputs": [str(path) for path in output_paths],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return ExternalKnowledgeImportResult(
        imported_count=len(output_paths),
        output_paths=output_paths,
        source_ids=[source.id for source in sources],
        manifest_path=manifest_path,
    )


def render_source_markdown(source: ExternalKnowledgeSource) -> str:
    use_cases = "\n".join(f"- {item}" for item in source.use_cases)
    limitations = "\n".join(f"- {item}" for item in source.limitations)
    keywords = ", ".join(source.tags)
    languages = ", ".join(source.language)
    doc_types = ", ".join(source.doc_types)
    return f"""# 外部金融知识源：{source.name}

## 来源
- 项目/数据源：{source.source_url}
- 仓库：{source.repository_url or source.source_url}
- 引用：{source.citation}

## 关键事实
- 来源 ID：`{source.id}`。
- 来源类型：`{source.source_type}`；接入模式：`{source.ingestion_mode}`。
- 市场范围：`{source.market}`；语言：{languages or "未标注"}；许可证/使用口径：{source.license}。
- 文档类型：{doc_types or "未标注"}。
- 企业级价值：{source.enterprise_value}

## 投研关注点
{use_cases}

## RAG 检索关键词
{keywords}

## 使用边界
{limitations}
- 本条目是外部知识源目录摘要，用于帮助 RAG 选择数据源、评测集和接入策略；不等同于实时公司事实。
- 如果后续导入原始数据，必须保留 `source_id`、`source_url`、许可证、文档类型、市场范围和引用 ID。

## 外部知识源元数据
- `source_id`: `{source.id}`
- `category`: `{source.category}`
- `market`: `{source.market}`
- `ingestion_mode`: `{source.ingestion_mode}`
- `license`: `{source.license}`
"""


def _validate_unique_ids(sources: list[ExternalKnowledgeSource]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for source in sources:
        if source.id in seen:
            duplicates.add(source.id)
        seen.add(source.id)
    if duplicates:
        raise ValueError(f"外部知识源 ID 重复: {', '.join(sorted(duplicates))}")


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    return value.strip("-") or "external-source"
