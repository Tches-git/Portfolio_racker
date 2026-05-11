"""轻量表格提取器。"""
from __future__ import annotations

import re


def extract_markdown_like_tables(text: str) -> list[dict]:
    tables: list[dict] = []
    current: list[str] = []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if "|" in stripped and len(stripped) >= 3:
            current.append(stripped)
            continue
        if current:
            table = _build_table(current)
            if table:
                tables.append(table)
            current = []
    if current:
        table = _build_table(current)
        if table:
            tables.append(table)
    return tables


def extract_delimited_tables(text: str) -> list[dict]:
    tables: list[dict] = []
    for block in re.split(r"\n\s*\n", text or ""):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 2:
            continue
        if not all("\t" in line or "," in line for line in lines[: min(5, len(lines))]):
            continue
        delimiter = "\t" if any("\t" in line for line in lines) else ","
        rows = [[cell.strip() for cell in line.split(delimiter)] for line in lines]
        if len({len(row) for row in rows}) != 1 or len(rows[0]) < 2:
            continue
        tables.append({"headers": rows[0], "rows": rows[1:], "format": "delimited"})
    return tables


def extract_tables(text: str) -> list[dict]:
    tables = extract_markdown_like_tables(text)
    if tables:
        return tables
    return extract_delimited_tables(text)


def summarize_tables(tables: list[dict]) -> str:
    if not tables:
        return "未识别到结构化表格"
    parts = []
    for idx, table in enumerate(tables, 1):
        headers = " / ".join(table.get("headers", [])[:5])
        parts.append(f"表{idx}: {len(table.get('rows', []))}行, 字段 {headers}")
    return "；".join(parts)


def _build_table(lines: list[str]) -> dict | None:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 2:
            return None
        rows.append(cells)
    if len(rows) < 2:
        return None
    if all(re.fullmatch(r"[:\-\s]+", cell or "") for cell in rows[1]):
        data_rows = rows[2:]
    else:
        data_rows = rows[1:]
    return {"headers": rows[0], "rows": data_rows, "format": "markdown"}
