"""一键质量门禁脚本 — 本地/CI 统一执行测试与黄金集回归"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from app.config import PROJECT_ROOT, QUALITY_GATE_OUTPUT_DIR

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = PROJECT_ROOT
DEFAULT_REGRESSION_OUTPUT_DIR = QUALITY_GATE_OUTPUT_DIR / "regression"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行一键质量门禁（pytest + 黄金集回归）")
    parser.add_argument("--skip-tests", action="store_true", help="跳过 pytest")
    parser.add_argument("--skip-regression", action="store_true", help="跳过黄金集回归")
    parser.add_argument("--pytest-args", nargs="*", default=["-q"], help="透传给 pytest 的参数")
    parser.add_argument("--stocks", nargs="+", help="透传给 run_regression.py 的股票列表")
    parser.add_argument("--llm-judge", action="store_true", help="回归时启用 LLM-as-Judge")
    parser.add_argument("--min-success-rate", type=float, default=100.0)
    parser.add_argument("--min-avg-score", type=float, default=70.0)
    parser.add_argument("--min-avg-section-coverage", type=float, default=0.875)
    parser.add_argument("--min-anchor-coverage", type=float, default=100.0)
    parser.add_argument("--regression-output-dir", default=str(DEFAULT_REGRESSION_OUTPUT_DIR), help="黄金集回归输出目录")
    return parser.parse_args(argv)


def build_gate_commands(args: argparse.Namespace) -> list[tuple[str, list[str]]]:
    commands: list[tuple[str, list[str]]] = []
    if not args.skip_tests:
        commands.append(("pytest", [sys.executable, "-m", "pytest", *args.pytest_args]))
    if not args.skip_regression:
        regression_cmd = [
            sys.executable,
            str(ROOT / "main.py"),
            "regression",
            "--output-dir",
            args.regression_output_dir,
            "--min-success-rate",
            str(args.min_success_rate),
            "--min-avg-score",
            str(args.min_avg_score),
            "--min-avg-section-coverage",
            str(args.min_avg_section_coverage),
            "--min-anchor-coverage",
            str(args.min_anchor_coverage),
        ]
        if args.stocks:
            regression_cmd.extend(["--stocks", *args.stocks])
        if args.llm_judge:
            regression_cmd.append("--llm-judge")
        commands.append(("golden_regression", regression_cmd))
    return commands


def run_gate(commands: list[tuple[str, list[str]]]) -> list[dict]:
    results: list[dict] = []
    for name, cmd in commands:
        print("=" * 72)
        print(f"[quality-gate] 运行步骤: {name}")
        print(" ".join(cmd))
        print("=" * 72)
        completed = subprocess.run(cmd, cwd=ROOT)
        results.append({"name": name, "command": cmd, "returncode": completed.returncode, "passed": completed.returncode == 0})
    return results


def format_results(results: list[dict]) -> str:
    lines = ["# Quality Gate Summary", ""]
    overall_pass = all(item["passed"] for item in results) if results else False
    lines.append(f"- Overall: {'PASS' if overall_pass else 'FAIL'}")
    for item in results:
        status = "PASS" if item["passed"] else "FAIL"
        lines.append(f"- {item['name']}: {status} (exit={item['returncode']})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    commands = build_gate_commands(args)
    if not commands:
        print("未选择任何质量门禁步骤")
        return 1
    results = run_gate(commands)
    summary = format_results(results)
    print("\n" + summary)
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
