"""导出物下载与解析。"""
from __future__ import annotations

from pathlib import Path

from app.config import OUTPUT_DIR


class ExportNotFoundError(RuntimeError):
    """导出物不存在。"""


_ALLOWED_EXTENSIONS = {'.md', '.html', '.pdf', '.log', '.json'}


def resolve_export_file(filename: str, *, output_dir: Path = OUTPUT_DIR) -> Path:
    candidate = Path(filename)
    if candidate.name != filename:
        raise ExportNotFoundError('非法导出文件名')
    if candidate.suffix.lower() not in _ALLOWED_EXTENSIONS:
        raise ExportNotFoundError('不支持的导出文件类型')
    path = output_dir / candidate.name
    if not path.exists() or not path.is_file():
        raise ExportNotFoundError(f'未找到导出物: {filename}')
    return path
