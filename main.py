"""统一 CLI 入口 — 支持研报生成、知识库重建、消融评测、回归、质量门禁与人工评审包"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.config import EVAL_DIR, OUTPUT_DIR, PROJECT_ROOT

ROOT = PROJECT_ROOT
SUBCOMMAND_MODULES = {
    "ablation": "scripts.ablation",
    "regression": "scripts.regression",
    "quality-gate": "scripts.quality_gate",
    "human-eval": "scripts.human_eval",
}
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def print_root_help() -> None:
    print(
        """金融研报智能分析系统 — 统一 CLI 入口

用法:
  python main.py [股票代码] [--eval] [--mc-sims N] [--rebuild-kb] [--doc PATH]
  python main.py analyze [股票代码] [--eval] [--mc-sims N] [--rebuild-kb] [--doc PATH]
  python main.py api [uvicorn 参数...]
  python main.py ablation [run_ablation 参数...]
  python main.py regression [run_regression 参数...]
  python main.py quality-gate [run_quality_gate 参数...]
  python main.py human-eval <report_path> --stock-code <code>

说明:
  - 省略子命令时，默认按 analyze 处理，兼容原有 `python main.py 600519` 用法
  - `--doc` 可重复传入 PDF / 图片 / 文本材料，作为 Phase 1 的可选补充上下文
  - run_*.py 仍可直接调用，但推荐优先使用 main.py 统一入口
"""
    )


def build_analyze_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成单只股票深度研报")
    parser.add_argument("code", nargs="?", help="A股股票代码，默认 600519")
    parser.add_argument("--rebuild-kb", action="store_true", help="重建知识库索引")
    parser.add_argument("--eval", action="store_true", help="运行研报质量评测")
    parser.add_argument("--mc-sims", type=int, default=None, help="蒙特卡洛模拟次数")
    parser.add_argument("--doc", dest="doc_paths", action="append", default=[], help="可选补充文档/图片路径，可重复传入")
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


def _load_uploaded_items(doc_paths: list[str]) -> list[dict]:
    uploaded_items: list[dict] = []
    for raw_path in doc_paths:
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = (ROOT / path).resolve()
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"补充文档不存在: {path}")
        uploaded_items.append({
            "name": path.name,
            "content": path.read_bytes(),
            "content_type": _guess_content_type(path),
            "path": str(path),
        })
    return uploaded_items


def _guess_content_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return "application/pdf"
    if suffix in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}:
        return f"image/{suffix.lstrip('.')}"
    if suffix in {".txt", ".md"}:
        return "text/plain"
    return "application/octet-stream"


def _run_analysis(argv: list[str] | None = None) -> int:
    args = build_analyze_parser().parse_args(argv)

    if args.mc_sims is not None:
        import app.config as app_config

        os.environ["MC_SIMULATIONS"] = str(args.mc_sims)
        app_config.MC_SIMULATIONS = args.mc_sims

    if args.rebuild_kb:
        _rebuild_knowledge_base()
        if args.code is None:
            return 0

    try:
        uploaded_items = _load_uploaded_items(args.doc_paths)
    except FileNotFoundError as exc:
        print(str(exc))
        return 1
    code = args.code or "600519"
    print(f"正在分析 {code}...\n")
    if uploaded_items:
        print(f"附加文档: {len(uploaded_items)} 份")

    def on_step(event, detail, state):
        if event.endswith("_start") or event in ("planning", "reflecting", "plan_ready"):
            print(f">> {detail}")
        elif event == "reflection_done":
            print(f">> 反思完成: {detail}")

    from app.engine import ReportEngine

    engine = ReportEngine(on_step=on_step)
    state = engine.run(code, uploaded_items=uploaded_items)

    if not state.final_report:
        print("分析失败")
        return 1

    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    from app.exports.storage import save_output_files

    report_file, trace_file = save_output_files(state, root=ROOT, timestamp=timestamp)
    html_export = state.sections.get("report_html_export", "")
    pdf_export = state.sections.get("report_pdf_export", "")
    sources_export = state.sections.get("source_refs_export", "")
    print(f"\n{'=' * 60}")
    print(state.final_report[:500] + "...")
    print(f"\n完整研报已保存到 {report_file.relative_to(ROOT)}")
    print(f"Trace: {len(state.trace)} 条 → {trace_file.relative_to(ROOT)}")
    if html_export:
        print(f"HTML 展示版: output\\{html_export}")
    if pdf_export:
        print(f"PDF 展示版: output\\{pdf_export}")
    if sources_export:
        print(f"来源索引: output\\{sources_export}")

    if args.eval:
        print(f"\n{'=' * 60}")
        print("正在评测研报质量...")
        from app.evals.report_eval import evaluate_report_with_metrics, format_eval_report, EvalResult

        eval_payload = evaluate_report_with_metrics(state.final_report, state, code)
        eval_result = EvalResult(**{key: value for key, value in eval_payload.items() if key != "summary" and key != "run_metrics"})
        eval_text = format_eval_report(eval_result)
        print(eval_text)
        EVAL_DIR.mkdir(parents=True, exist_ok=True)
        eval_md_file = EVAL_DIR / f"eval_{code}_{timestamp}.md"
        eval_json_file = EVAL_DIR / f"eval_{code}_{timestamp}.json"
        eval_md_file.write_text(eval_text, encoding="utf-8")
        eval_json_file.write_text(json.dumps(eval_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n评测报告已保存到 {eval_md_file}")
        print(f"评测指标 JSON 已保存到 {eval_json_file}")
    return 0


def _dispatch_script(module_name: str, argv: list[str]) -> int:
    module = importlib.import_module(module_name)
    result = module.main(argv)
    return int(result or 0)


def _run_api(argv: list[str]) -> int:
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.api.server:app",
        "--host",
        API_HOST,
        "--port",
        str(API_PORT),
        *argv,
    ]
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
        if command == "api":
            return _run_api(args[1:])
        module_name = SUBCOMMAND_MODULES.get(command)
        if module_name:
            return _dispatch_script(module_name, args[1:])
    return _run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
