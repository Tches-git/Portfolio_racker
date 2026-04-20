"""首页输入区与空状态。"""
from __future__ import annotations

from app.ui.alerts import classify_run_error
from app.ui.session_state import queue_run, set_workspace_view

POPULAR_STOCK_PILLS = ["600519", "300750", "600036", "002594", "000333"]
_WORKSPACE_HINTS = {
    "home": "当前为首页概览：适合快速开始、查看流程说明和历史入口。",
    "run": "当前为分析工作台：聚焦输入、进度与失败恢复。",
    "result": "当前为结果浏览：聚焦告警、核心摘要与多层结果页。",
}


def render_sidebar_controls(st_module, popular_stocks: dict[str, str], *, disabled: bool = False, initial_stock_code: str = "", workspace_view: str = "home") -> tuple[str, bool]:
    with st_module.sidebar:
        st_module.header("分析设置")
        st_module.caption(_WORKSPACE_HINTS.get(workspace_view, _WORKSPACE_HINTS["home"]))
        options = ["自定义", *popular_stocks.keys()]
        reverse_map = {code: name for name, code in popular_stocks.items()}
        selected_name = reverse_map.get(initial_stock_code, "自定义")
        stock_name = st_module.selectbox("常用股票", options, index=options.index(selected_name), disabled=disabled)
        default_code = initial_stock_code or (popular_stocks.get(stock_name, "") if stock_name != "自定义" else "")
        stock_code = st_module.text_input("股票代码", value=default_code, placeholder="例如 600519", disabled=disabled)
        st_module.caption("示例：600519 / 300750 / 600036")
        run_clicked = st_module.button("开始分析", type="primary", use_container_width=True, disabled=disabled)
    return stock_code, run_clicked


def render_quick_start(st_module, *, session_state, rerun_fn, disabled: bool = False) -> None:
    st_module.markdown("### 快速开始")
    cols = st_module.columns(len(POPULAR_STOCK_PILLS))
    for col, code in zip(cols, POPULAR_STOCK_PILLS):
        with col:
            if st_module.button(code, use_container_width=True, key=f"quick_start_{code}", disabled=disabled):
                queue_run(session_state, code)
                set_workspace_view(session_state, "run")
                rerun_fn()


def render_loading_placeholders(st_module) -> None:
    st_module.markdown('<div class="placeholder-card">分析尚未开始，运行后这里会展示阶段进度、实时日志与指标摘要。</div>', unsafe_allow_html=True)
    st_module.markdown('<div class="placeholder-card">结果浏览页将提供结果总览、分组标签页与自动评测明细。</div>', unsafe_allow_html=True)


def render_failure_state(st_module, stock_code: str, *, retry_fn=None, error_message: str = "") -> None:
    classified = classify_run_error(error_message)
    st_module.error(f"最近一次分析失败：{stock_code or '未知股票'}")
    st_module.markdown(
        f"""
<div class="tip-card">
  <strong>{classified['title']}</strong><br/>
  {classified['hint']}<br/><br/>
  <strong>建议排查顺序</strong><br/>
  1. 先确认股票代码是否有效<br/>
  2. 再检查 LLM / API 配置与网络状态<br/>
  3. 如为短暂波动，可直接使用下方入口重试
</div>
        """,
        unsafe_allow_html=True,
    )
    if retry_fn and st_module.button("重试上次分析", type="primary", use_container_width=True):
        retry_fn()


def render_empty_state(st_module) -> None:
    st_module.markdown(
        """
<div class="tip-card">
  <strong>开始前你会看到什么？</strong><br/>
  • 运行进度：查看知识准备、研究、写作各阶段状态<br/>
  • 结果总览：先确认结论、评级、风险和质量完成度<br/>
  • 分层结果页：再按总览 / 分析 / 诊断逐层展开内容
</div>
        """,
        unsafe_allow_html=True,
    )
