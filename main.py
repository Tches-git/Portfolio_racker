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
  python main.py tracking-eval [--benchmark PATH] [--target-count N]
  python main.py build-tracking-benchmark [--output PATH] [--stock-codes codes] [--live]
  python main.py agent-eval [--benchmark PATH] [--target-count N]
  python main.py finance-qa-predict --benchmark PATH [--limit N]
  python main.py finance-qa-eval --benchmark PATH [--predictions PATH]
  python main.py kb-sources list|import [--source SOURCE_ID] [--category CATEGORY] [--market MARKET]
  python main.py kb-cache import [--stock-code CODE] [--limit N] [--rebuild-kb]
  python main.py kb-bulk import [--rebuild-kb]
  python main.py rag-eval --stock-code <股票代码>

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

    report_file, trace_file = save_output_files(state, timestamp=timestamp)
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


def _run_tracking_eval(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="评测金融事件处理 Pipeline")
    parser.add_argument("--benchmark", default="", help="JSONL 标注集路径，默认 data/benchmarks/tracking_events.jsonl")
    parser.add_argument("--target-count", type=int, default=500, help="扩展后的评测样本数量，默认 500")
    parser.add_argument("--no-expand", action="store_true", help="只评测 benchmark 文件中的原始样本，不做可复现扩展")
    args = parser.parse_args(argv)
    from app.evals.tracking_eval import DEFAULT_BENCHMARK_PATH, format_tracking_eval_markdown, run_tracking_eval

    benchmark = Path(args.benchmark).expanduser() if args.benchmark else DEFAULT_BENCHMARK_PATH
    if not benchmark.is_absolute():
        benchmark = (ROOT / benchmark).resolve()
    result = run_tracking_eval(benchmark_path=benchmark, target_count=0 if args.no_expand else max(1, args.target_count))
    print(format_tracking_eval_markdown(result))
    print(f"JSON: {result['json_path']}")
    print(f"Markdown: {result['markdown_path']}")
    return 0


def _run_build_tracking_benchmark(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="从公开公告/新闻缓存或实时采集结果构建真实事件 benchmark")
    parser.add_argument("--output", default="data/benchmarks/tracking_events_real.jsonl", help="输出 JSONL 路径")
    parser.add_argument("--stock-codes", default="", help="逗号分隔股票代码；为空时读取缓存里已有股票")
    parser.add_argument("--target-count", type=int, default=150, help="最多输出样本数，默认 150")
    parser.add_argument("--live", action="store_true", help="允许实时调用公开数据源补充样本")
    args = parser.parse_args(argv)
    from app.evals.tracking_benchmark_builder import build_real_tracking_benchmark

    output = Path(args.output).expanduser()
    if not output.is_absolute():
        output = (ROOT / output).resolve()
    codes = [item.strip() for item in args.stock_codes.split(",") if item.strip()]
    result = build_real_tracking_benchmark(
        output_path=output,
        stock_codes=codes,
        target_count=max(0, args.target_count),
        include_live=args.live,
    )
    print(f"真实事件样本数: {result.sample_count}")
    print(f"股票池: {', '.join(result.stock_codes) or '暂无'}")
    print(f"来源文件数: {len(result.source_files)}")
    print(f"输出: {result.output_path}")
    if result.sample_count < 100:
        print("提示: 当前样本少于 100 条，可增加 --stock-codes 并使用 --live 采集后再人工复核。")
    return 0


def _run_rag_eval(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="评测研报 RAG 引用可信度")
    parser.add_argument("--stock-code", default="600519", help="股票代码")
    args = parser.parse_args(argv)
    from app.evals.rag_eval import format_rag_eval_markdown, run_rag_eval

    result = run_rag_eval(stock_code=args.stock_code)
    print(format_rag_eval_markdown(result))
    print(f"JSON: {result['json_path']}")
    print(f"Markdown: {result['markdown_path']}")
    return 0


def _run_agent_eval(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="评测金融研究 Agent 任务链路")
    parser.add_argument("--benchmark", default="", help="JSONL 任务集路径，默认 data/benchmarks/agent_tasks.jsonl")
    parser.add_argument("--target-count", type=int, default=300, help="扩展后的评测任务数量，默认 300")
    args = parser.parse_args(argv)
    from app.evals.agent_eval import DEFAULT_AGENT_BENCHMARK_PATH, format_agent_eval_markdown, run_agent_eval

    benchmark = Path(args.benchmark).expanduser() if args.benchmark else DEFAULT_AGENT_BENCHMARK_PATH
    if not benchmark.is_absolute():
        benchmark = (ROOT / benchmark).resolve()
    result = run_agent_eval(benchmark_path=benchmark, target_count=max(1, args.target_count))
    print(format_agent_eval_markdown(result))
    print(f"JSON: {result['json_path']}")
    print(f"Markdown: {result['markdown_path']}")
    return 0


def _run_finance_qa_eval(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="评测公共金融 QA/RAG benchmark 本地子集")
    parser.add_argument("--benchmark", required=True, help="FinanceBench / FinQA / TAT-QA 本地 JSON/JSONL 子集路径")
    parser.add_argument("--predictions", default="", help="可选预测 JSON/JSONL 路径，包含 sample_id/prediction/cited_source_ids")
    parser.add_argument("--dataset", default="auto", help="数据集格式：auto / financebench / finqa / tatqa / generic")
    parser.add_argument("--limit", type=int, default=0, help="最多评测样本数，0 表示不限")
    args = parser.parse_args(argv)
    from app.evals.financial_qa_eval import format_financial_qa_eval_markdown, run_financial_qa_eval

    benchmark = Path(args.benchmark).expanduser()
    if not benchmark.is_absolute():
        benchmark = (ROOT / benchmark).resolve()
    predictions = Path(args.predictions).expanduser() if args.predictions else None
    if predictions and not predictions.is_absolute():
        predictions = (ROOT / predictions).resolve()
    result = run_financial_qa_eval(
        benchmark_path=benchmark,
        predictions_path=predictions,
        dataset=args.dataset,
        limit=max(0, args.limit),
    )
    print(format_financial_qa_eval_markdown(result))
    print(f"JSON: {result['json_path']}")
    print(f"Markdown: {result['markdown_path']}")
    return 0


def _run_finance_qa_predict(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="使用当前 LLM 对公共金融 QA/RAG benchmark 本地子集生成预测")
    parser.add_argument("--benchmark", required=True, help="FinanceBench / FinQA / TAT-QA 本地 JSON/JSONL 子集路径")
    parser.add_argument("--output", default="", help="预测 JSONL 输出路径，默认 output/evals")
    parser.add_argument("--dataset", default="auto", help="数据集格式：auto / financebench / finqa / tatqa / generic")
    parser.add_argument("--limit", type=int, default=5, help="最多预测样本数，默认 5")
    parser.add_argument("--max-context-chars", type=int, default=6000, help="单题最多上下文字符数")
    args = parser.parse_args(argv)
    from app.evals.financial_qa_predictor import run_financial_qa_predictions

    benchmark = Path(args.benchmark).expanduser()
    if not benchmark.is_absolute():
        benchmark = (ROOT / benchmark).resolve()
    output = Path(args.output).expanduser() if args.output else None
    if output and not output.is_absolute():
        output = (ROOT / output).resolve()
    result = run_financial_qa_predictions(
        benchmark_path=benchmark,
        output_path=output,
        dataset=args.dataset,
        limit=max(1, args.limit),
        max_context_chars=max(500, args.max_context_chars),
    )
    print(f"预测数: {result['prediction_count']}")
    print(f"输出: {result['output_path']}")
    return 0


def _run_kb_sources(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="管理外部金融知识源目录")
    subparsers = parser.add_subparsers(dest="action", required=True)

    list_parser = subparsers.add_parser("list", help="列出已登记的外部金融知识源")
    list_parser.add_argument("--category", action="append", default=[], help="按来源类别筛选，可重复")
    list_parser.add_argument("--market", action="append", default=[], help="按市场筛选，可重复，如 china/us/global")

    import_parser = subparsers.add_parser("import", help="将外部知识源摘要导入 data/knowledge_base")
    import_parser.add_argument("--source", action="append", default=[], help="指定 source_id，可重复；为空导入筛选后的全部")
    import_parser.add_argument("--category", action="append", default=[], help="按来源类别筛选，可重复")
    import_parser.add_argument("--market", action="append", default=[], help="按市场筛选，可重复")
    import_parser.add_argument("--rebuild-kb", action="store_true", help="导入后重建知识库索引")

    args = parser.parse_args(argv)
    from app.rag.external_sources import filter_external_sources, import_external_source_summaries, load_external_sources

    if args.action == "list":
        sources = filter_external_sources(
            load_external_sources(),
            categories=args.category,
            markets=args.market,
        )
        for source in sources:
            print(f"{source.id}\t{source.market}\t{source.category}\t{source.license}\t{source.name}")
        print(f"共 {len(sources)} 个外部金融知识源")
        return 0

    if args.action == "import":
        result = import_external_source_summaries(
            source_ids=args.source,
            categories=args.category,
            markets=args.market,
        )
        print(f"导入外部知识源摘要: {result.imported_count} 个")
        print(f"Manifest: {result.manifest_path}")
        for path in result.output_paths:
            print(f"- {path}")
        if args.rebuild_kb:
            _rebuild_knowledge_base()
        return 0

    return 1


def _run_kb_cache(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="将本地公开数据缓存导入 RAG 知识库")
    subparsers = parser.add_subparsers(dest="action", required=True)
    import_parser = subparsers.add_parser("import", help="导入公司画像、公告、研报观点和行情缓存")
    import_parser.add_argument("--stock-code", action="append", default=[], help="指定股票代码，可重复；为空导入全部 profile 缓存")
    import_parser.add_argument("--limit", type=int, default=0, help="最多导入多少只股票，0 表示不限")
    import_parser.add_argument("--rebuild-kb", action="store_true", help="导入后重建知识库索引")

    args = parser.parse_args(argv)
    from app.rag.cache_knowledge import import_stock_cache_knowledge

    if args.action == "import":
        result = import_stock_cache_knowledge(stock_codes=args.stock_code, limit=max(0, args.limit))
        print(f"导入股票缓存知识: {result.imported_count} 只")
        print(f"股票池: {', '.join(result.stock_codes) or '暂无'}")
        print(f"Manifest: {result.manifest_path}")
        for path in result.output_paths:
            print(f"- {path}")
        if args.rebuild_kb:
            _rebuild_knowledge_base()
        return 0
    return 1


def _run_kb_bulk(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="批量导入公共 benchmark、A 股证券目录、缓存事件和行情序列")
    subparsers = parser.add_subparsers(dest="action", required=True)
    import_parser = subparsers.add_parser("import", help="导入大规模本地公开语料")
    import_parser.add_argument("--skip-universe", action="store_true", help="跳过 A 股代码名称目录")
    import_parser.add_argument("--skip-benchmarks", action="store_true", help="跳过 FinanceBench / 事件 / Agent benchmark")
    import_parser.add_argument("--skip-cache-items", action="store_true", help="跳过公告/研报/披露缓存条目")
    import_parser.add_argument("--skip-daily-bars", action="store_true", help="跳过日线行情序列")
    import_parser.add_argument("--rebuild-kb", action="store_true", help="导入后重建知识库索引")

    args = parser.parse_args(argv)
    from app.rag.bulk_knowledge import import_bulk_knowledge

    if args.action == "import":
        result = import_bulk_knowledge(
            include_universe=not args.skip_universe,
            include_benchmarks=not args.skip_benchmarks,
            include_cache_items=not args.skip_cache_items,
            include_daily_bars=not args.skip_daily_bars,
        )
        print(f"批量导入知识语料文件: {result.imported_count} 个")
        for name, count in result.corpus_counts.items():
            print(f"- {name}: {count}")
        print(f"Manifest: {result.manifest_path}")
        if args.rebuild_kb:
            _rebuild_knowledge_base()
        return 0
    return 1


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
        if command == "tracking-eval":
            return _run_tracking_eval(args[1:])
        if command == "build-tracking-benchmark":
            return _run_build_tracking_benchmark(args[1:])
        if command == "agent-eval":
            return _run_agent_eval(args[1:])
        if command == "finance-qa-predict":
            return _run_finance_qa_predict(args[1:])
        if command == "finance-qa-eval":
            return _run_finance_qa_eval(args[1:])
        if command == "kb-sources":
            return _run_kb_sources(args[1:])
        if command == "kb-cache":
            return _run_kb_cache(args[1:])
        if command == "kb-bulk":
            return _run_kb_bulk(args[1:])
        if command == "rag-eval":
            return _run_rag_eval(args[1:])
        module_name = SUBCOMMAND_MODULES.get(command)
        if module_name:
            return _dispatch_script(module_name, args[1:])
    return _run_analysis(args)


if __name__ == "__main__":
    raise SystemExit(main())
