"""一键质量门禁脚本 — 本地/CI 统一执行测试与黄金集回归"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from app.config import PROJECT_ROOT, QUALITY_GATE_OUTPUT_DIR

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = PROJECT_ROOT
DEFAULT_REGRESSION_OUTPUT_DIR = QUALITY_GATE_OUTPUT_DIR / "regression"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    argv_list = list(argv or [])
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
    args, unknown = parser.parse_known_args(argv_list)
    if "--pytest-args" in argv_list:
        args.pytest_args = [*args.pytest_args, *unknown]
        return args
    if unknown:
        parser.error(f"unrecognized arguments: {' '.join(unknown)}")
    return args


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


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _extract_gate_artifacts(results: list[dict]) -> dict[str, Any]:
    regression_summary_path = DEFAULT_REGRESSION_OUTPUT_DIR / "regression_summary.json"
    regression_payload = _load_json_if_exists(regression_summary_path)
    failed_steps = [item["name"] for item in results if not item.get("passed")]
    return {
        "step_count": len(results),
        "passed_steps": [item["name"] for item in results if item.get("passed")],
        "failed_steps": failed_steps,
        "step_categories": {item["name"]: ("verification" if item["name"] == "pytest" else "regression") for item in results},
        "regression_summary_path": str(regression_summary_path) if regression_payload else "",
        "regression_overall_pass": regression_payload.get("regression", {}).get("overall_pass") if regression_payload else None,
        "regression_samples": regression_payload.get("regression", {}).get("samples") if regression_payload else None,
        "regression_checks": regression_payload.get("regression", {}).get("checks") if regression_payload else None,
        "regression_aggregate": regression_payload.get("aggregate") if regression_payload else None,
        "regression_history_summary": regression_payload.get("history_summary") if regression_payload else None,
        "regression_artifact_index": regression_payload.get("artifact_index") if regression_payload else None,
    }


def _build_summary_payload(summary: str, results: list[dict]) -> dict:
    return {
        "summary_markdown": summary,
        "overall_pass": all(item["passed"] for item in results) if results else False,
        "results": results,
        "artifacts": _extract_gate_artifacts(results),
    }


def write_summary(summary: str, results: list[dict] | None = None) -> Path:
    QUALITY_GATE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = QUALITY_GATE_OUTPUT_DIR / "quality_gate_summary.md"
    summary_path.write_text(summary, encoding="utf-8")
    summary_json_path = QUALITY_GATE_OUTPUT_DIR / "quality_gate_summary.json"
    summary_json_path.write_text(
        json.dumps(_build_summary_payload(summary, results or []), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary_path


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    commands = build_gate_commands(args)
    if not commands:
        print("未选择任何质量门禁步骤")
        return 1
    results = run_gate(commands)
    summary = format_results(results)
    summary_path = write_summary(summary, results)
    print("\n" + summary)
    print(f"\n质量门禁汇总已保存到 {summary_path}")
    return 0 if all(item["passed"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
