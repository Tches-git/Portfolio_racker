"""生成人工评审包 — 基于种子 benchmark 与自动指标输出 Markdown 模板"""
from __future__ import annotations

import argparse
from pathlib import Path

from app.config import HUMAN_EVAL_OUTPUT_DIR
from app.evals.human_rubric import (
    build_manual_review_payload,
    format_manual_review_markdown,
    load_human_benchmark,
)

ROOT = Path(__file__).parent
DEFAULT_OUTPUT_DIR = HUMAN_EVAL_OUTPUT_DIR


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成研报人工评审包")
    parser.add_argument("report_path", help="待评审的 Markdown 研报路径")
    parser.add_argument("--stock-code", required=True, help="股票代码")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="输出目录")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report_path = Path(args.report_path)
    if not report_path.exists():
        raise FileNotFoundError(f"报告不存在: {report_path}")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = report_path.read_text(encoding="utf-8")
    benchmark = next((item for item in load_human_benchmark() if item.get("stock_code") == args.stock_code), None)
    payload = build_manual_review_payload(report, args.stock_code, benchmark_entry=benchmark)
    md = format_manual_review_markdown(payload)

    output_path = output_dir / f"human_eval_{args.stock_code}.md"
    output_path.write_text(md, encoding="utf-8")
    print(f"人工评审包已生成: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
