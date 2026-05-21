from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_quality_page_and_stock_backtest_tab_are_wired():
    api = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")
    stock = (ROOT / "frontend/src/components/workbench/stock-workbench.tsx").read_text(encoding="utf-8")
    quality = (ROOT / "frontend/src/app/quality/page.tsx").read_text(encoding="utf-8")

    assert "fetchQualityWorkbench" in api
    assert "fetchEventBacktest" in api
    assert "QualityWorkbenchResponse" in types
    assert "agent_eval" in types
    assert "financial_qa_eval" in types
    assert "EventBacktestResponse" in types
    assert "影响回测" in stock
    assert "Agent 可信度报告" in quality
    assert "多角色 Agent 协作" in quality
    assert "公共金融 QA / 检索增强" in quality
    assert "关键答案命中" in quality


def test_big_screen_command_center_components_are_wired():
    dashboard = (ROOT / "frontend/src/components/workbench/dashboard-overview.tsx").read_text(encoding="utf-8")
    runs = (ROOT / "frontend/src/components/workbench/task-delivery-center.tsx").read_text(encoding="utf-8")
    run_detail = (ROOT / "frontend/src/app/runs/[runId]/page.tsx").read_text(encoding="utf-8")
    quality = (ROOT / "frontend/src/app/quality/page.tsx").read_text(encoding="utf-8")
    chart_panel = (ROOT / "frontend/src/components/big-screen/chart-panel.tsx").read_text(encoding="utf-8")
    command_center = (ROOT / "frontend/src/components/big-screen/command-center.tsx").read_text(encoding="utf-8")
    types = (ROOT / "frontend/src/lib/types.ts").read_text(encoding="utf-8")

    assert "CommandCenterShell" in command_center
    assert "HeroRiskBand" in command_center
    assert "AgentFlowPanel" in command_center
    assert "ChartPanel" in chart_panel
    assert "RiskRadarChart" in chart_panel
    assert "DonutChart" in chart_panel
    assert "BarPulseChart" in chart_panel
    assert "CommandCenterShell" in dashboard
    assert "DataCenterHeader" in dashboard
    assert "DataCategoryGrid" in dashboard
    assert "RankPanel" in dashboard
    assert "AgentFlowPanel" in runs
    assert "AgentFlowPanel" in run_detail
    assert "credibilityCommandGrid" in quality
    assert "ChartDatum" in types
    assert "AgentFlowNode" in types


def test_big_screen_motion_layer_is_subtle_and_accessible():
    css = (ROOT / "frontend/src/app/globals.css").read_text(encoding="utf-8")

    assert "commandAmbientSweep" in css
    assert "riskNumberGlow" in css
    assert "panelReveal" in css
    assert "agentNodePulse" in css
    assert "@media (prefers-reduced-motion: no-preference)" in css
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert "animation-iteration-count: 1 !important" in css


def test_global_auto_refresh_control_is_wired():
    app_shell = (ROOT / "frontend/src/components/app-shell.tsx").read_text(encoding="utf-8")
    auto_refresh = (ROOT / "frontend/src/components/auto-refresh-control.tsx").read_text(encoding="utf-8")
    css = (ROOT / "frontend/src/app/globals.css").read_text(encoding="utf-8")

    assert "AutoRefreshControl" in app_shell
    assert "router.refresh()" in auto_refresh
    assert "setInterval" in auto_refresh
    assert "document.visibilityState === 'hidden'" in auto_refresh
    assert "立即刷新" in auto_refresh
    assert "自动刷新" in auto_refresh
    assert "autoRefreshControl" in css
