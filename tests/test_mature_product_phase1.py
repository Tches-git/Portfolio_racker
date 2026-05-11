from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_layout_includes_global_run_center():
    layout = (ROOT / 'frontend/src/app/layout.tsx').read_text(encoding='utf-8')
    run_center = (ROOT / 'frontend/src/components/global-run-center.tsx').read_text(encoding='utf-8')

    assert 'GlobalRunCenter' in layout
    assert '全局运行中心' in run_center
    assert 'fetchRecentRuns' in run_center
    assert 'globalRunStats' in run_center


def test_homepage_includes_rebuilt_command_center():
    home = (ROOT / 'frontend/src/app/page.tsx').read_text(encoding='utf-8')
    command_center = (ROOT / 'frontend/src/components/command-center.tsx').read_text(encoding='utf-8')
    stock_grid = (ROOT / 'frontend/src/components/stock-card-grid.tsx').read_text(encoding='utf-8')

    assert 'CommandCenter' in home
    assert 'QuickActions' in home
    assert 'StockCardGrid' in home
    assert '今日金融追踪工作台' in command_center
    assert '关键事件雷达' in home
    assert '今日研究简报' in home
    assert '组合跟踪' in stock_grid


def test_exports_page_has_master_detail_snapshot():
    exports_page = (ROOT / 'frontend/src/app/stocks/[stockCode]/exports/page.tsx').read_text(encoding='utf-8')

    assert 'selectedArtifact' in exports_page
    assert 'searchParams' in exports_page
    assert '当前选中导出物' in exports_page
