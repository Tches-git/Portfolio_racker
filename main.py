"""统一 CLI 入口 — 支持研报生成、知识库重建、消融评测、回归、质量门禁与人工评审包"""
from __future__ import annotations

import argparse
import importlib
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR, PROJECT_ROOT

ROOT = PROJECT_ROOT
SUBCOMMAND_MODULES = {
    "ablation": "scripts.ablation",
    "regression": "scripts.regression",
    "quality-gate": "scripts.quality_gate",
    "human-eval": "scripts.human_eval",
}

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def print_root_help() -> None:
    print(
        """金融研报智能分析系统 — 统一 CLI 入口

用法:
  python main.py [股票代码] [--eval] [--mc-sims N] [--rebuild-kb]
  python main.py analyze [股票代码] [--eval] [--mc-sims N] [--rebuild-kb]
  python main.py web [streamlit 参数...]
  python main.py ablation [run_ablation 参数...]
  python main.py regression [run_regression 参数...]
  python main.py quality-gate [run_quality_gate 参数...]
  python main.py human-eval <report_path> --stock-code <code>

说明:
  - 省略子命令时，默认按 analyze 处理，兼容原有 `python main.py 600519` 用法
  - run_*.py 仍可直接调用，但推荐优先使用 main.py 统一入口
"""
    )


def build_analyze_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成单只股票深度研报")
    parser.add_argument("code", nargs="?", help="A股股票代码，默认 600519")
    parser.add_argument("--rebuild-kb", action="store_true", help="重建知识库索引")
    parser.add_argument("--eval", action="store_true", help="运行研报质量评测")
    parser.add_argument("--mc-sims", type=int, default=None, help="蒙特卡洛模拟次数")
    return parser


def _rebuild_knowledge_base() -> None:
    print("正在重建知识库...")
    from app.config import KB_INDEX_DIR
    from app.rag.knowledge_base import get_knowledge_base

    if KB_INDEX_DIR.exists():
        shutil.rmtree(KB_INDEX_DIR)
        KB_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    kb = get_knowledge_base()
    kb.init()
    kb.save()
    print(f"知识库重建完成: {kb.store.size} 条文档")


def _run_analysis(argv: list[str] | None = None) -> int:
    args = build_analyze_parser().parse_args(argv)

    if args.mc_sims:
        os.environ["MC_SIMULATIONS"] = str(args.mc_sims)

    if args.rebuild_kb:
        _rebuild_knowledge_base()
        if args.code is None:
            return 0

    code = args.code or "600519"
    print(f"正在分析 {code}...\n")

    def on_step(event, detail, state):
        if event.endswith("_start") or event in ("planning", "reflecting", "plan_ready"):
            print(f">> {detail}")
        elif event == "reflection_done":
            print(f">> 反思完成: {detail}")

    from app.engine import ReportEngine

    engine = ReportEngine(on_step=on_step)
    state = engine.run(code)

    if not state.final_report:
        print("分析失败")
        return 1

    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = OUTPUT_DIR / f"report_{code}_{timestamp}.md"
    trace_file = OUTPUT_DIR / f"trace_{code}_{timestamp}.log"
    report_file.write_text(state.final_report, encoding="utf-8")
    trace_file.write_text("\n".join(state.trace), encoding="utf-8")
    print(f"\n{'=' * 60}")
    print(state.final_report[:500] + "...")
    print(f"\n完整研报已保存到 {report_file.relative_to(ROOT)}")
    print(f"Trace: {len(state.trace)} 条 → {trace_file.relative_to(ROOT)}")

    if args.eval:
        print(f"\n{'=' * 60}")
        print("正在评测研报质量...")
        from app.config import EVAL_DIR
        from app.evals.report_eval import evaluate_report, format_eval_report

        eval_result = evaluate_report(state.final_report, state, code)
        eval_text = format_eval_report(eval_result)
        print(eval_text)
        eval_file = EVAL_DIR / f"eval_{code}_{timestamp}.md"
        eval_file.write_text(eval_text, encoding="utf-8")
        print(f"\n评测报告已保存到 {eval_file}")
    return 0


def _dispatch_script(module_name: str, argv: list[str]) -> int:
    module = importlib.import_module(module_name)
    result = module.main(argv)
    return int(result or 0)


def _run_web(argv: list[str]) -> int:
    cmd = [sys.executable, "-m", "streamlit", "run", str(ROOT / "web_app.py"), *argv]
    return subprocess.run(cmd, cwd=ROOT).returncode


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"-h", "--help"}:
        print_root_help()
        return 0
    if args:
        command = args[0]
        if command == "analyze":
            return _run_analysis(args[1:])
        if command == "web":
            return _run_web(args[1:])
        module_name = SUBCOMMAND_MODULES.get(command)
        if module_name:
            return _dispatch_script(module_name, args[1:])
    return _run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
