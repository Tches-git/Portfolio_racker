from __future__ import annotations

from pathlib import Path

import pytest

from app.api.download import ExportNotFoundError, resolve_export_file


def test_resolve_export_file_returns_existing_file(tmp_path):
    path = tmp_path / 'report_600519_demo.html'
    path.write_text('<html></html>', encoding='utf-8')

    resolved = resolve_export_file(path.name, output_dir=tmp_path)

    assert resolved == path


def test_resolve_export_file_rejects_path_traversal(tmp_path):
    with pytest.raises(ExportNotFoundError):
        resolve_export_file('../secret.txt', output_dir=tmp_path)


def test_resolve_export_file_rejects_unsupported_extension(tmp_path):
    path = tmp_path / 'report_600519_demo.exe'
    path.write_text('x', encoding='utf-8')

    with pytest.raises(ExportNotFoundError):
        resolve_export_file(path.name, output_dir=tmp_path)
