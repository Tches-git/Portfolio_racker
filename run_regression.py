"""固定黄金集回归脚本 — 用于持续验证当前版本研报质量"""
from __future__ import annotations

import argparse
import json
import sys
from statistics import mean

import run_ablation
from app.config import REGRESSION_OUTPUT_DIR

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_GOLDEN_STOCKS = ["600519", "000858", "300750", "600036", "002594"]
OUTPUT_DIR = REGRESSION_OUTPUT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_regression_checks(
    rows: list[dict],
    *,
    min_success_rate: float,
    min_avg_score: float,
    min_avg_section_coverage: float,
    min_anchor_coverage: float,
) -> dict:
    success_rows = [row for row in rows if row.get("success")]
    success_rate = round(len(success_rows) / len(rows) * 100, 1) if rows else 0.0
    avg_score = round(mean(row.get("overall_score", 0.0) for row in rows), 2) if rows else 0.0
    avg_section_coverage = round(mean(row.get("section_coverage", 0.0) for row in success_rows), 3) if success_rows else 0.0
    anchor_coverage = round(mean(1 if row.get("investment_anchor_present") else 0 for row in success_rows) * 100, 1) if success_rows else 0.0
    checks = {
        "success_rate": {
            "actual": success_rate,
            "threshold": min_success_rate,
            "passed": success_rate >= min_success_rate,
        },
        "avg_score": {
            "actual": avg_score,
            "threshold": min_avg_score,
            "passed": avg_score >= min_avg_score,
        },
        "avg_section_coverage": {
            "actual": avg_section_coverage,
            "threshold": min_avg_section_coverage,
            "passed": avg_section_coverage >= min_avg_section_coverage,
        },
        "investment_anchor_coverage": {
            "actual": anchor_coverage,
            "threshold": min_anchor_coverage,
            "passed": anchor_coverage >= min_anchor_coverage,
        },
    }
    return {
        "overall_pass": all(item["passed"] for item in checks.values()),
        "checks": checks,
        "samples": len(rows),
    }


def append_regression_section(summary_md: str, regression: dict) -> str:
    status = "✅ 通过" if regression.get("overall_pass") else "❌ 未通过"
    lines = [summary_md, "", "## 黄金集回归判定", "", f"- 总体结果：**{status}**"]
    label_map = {
        "success_rate": "成功率",
        "avg_score": "平均评分",
        "avg_section_coverage": "平均章节覆盖率",
        "investment_anchor_coverage": "估值锚覆盖率",
    }
    for key, item in regression.get("checks", {}).items():
        actual = item.get("actual", 0)
        threshold = item.get("threshold", 0)
        passed = "✅" if item.get("passed") else "❌"
        if key == "avg_section_coverage":
            actual_text = f"{actual:.1%}"
            threshold_text = f"{threshold:.1%}"
        else:
            actual_text = f"{actual:.1f}"
            threshold_text = f"{threshold:.1f}"
        lines.append(f"- {passed} {label_map.get(key, key)}：实际 {actual_text} / 阈值 {threshold_text}")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行固定黄金集回归评测")
    parser.add_argument("--stocks", nargs="+", default=DEFAULT_GOLDEN_STOCKS, help="固定回归股票代码列表")
    parser.add_argument("--llm-judge", action="store_true", help="启用 LLM-as-Judge 评分（成本更高）")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="输出目录")
    parser.add_argument("--min-success-rate", type=float, default=100.0, help="最低成功率阈值（百分比）")
    parser.add_argument("--min-avg-score", type=float, default=70.0, help="最低平均评分阈值")
    parser.add_argument("--min-avg-section-coverage", type=float, default=0.875, help="最低平均章节覆盖率阈值")
    parser.add_argument("--min-anchor-coverage", type=float, default=100.0, help="最低估值锚覆盖率阈值（百分比）")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for stock_code in args.stocks:
        state = run_ablation.RUNNERS["baseline"](stock_code)
        row = run_ablation.evaluate_state(
            state,
            "baseline",
            stock_code,
            use_llm_judge=args.llm_judge,
            output_dir=output_dir,
        )
        if row:
            rows.append(row)

    summary_md, aggregate = run_ablation.summarize_results(rows, use_llm_judge=args.llm_judge)
    regression = build_regression_checks(
        rows,
        min_success_rate=args.min_success_rate,
        min_avg_score=args.min_avg_score,
        min_avg_section_coverage=args.min_avg_section_coverage,
        min_anchor_coverage=args.min_anchor_coverage,
    )
    summary_md = append_regression_section(summary_md, regression)

    summary_path = output_dir / "regression_summary.md"
    summary_json_path = output_dir / "regression_summary.json"
    summary_path.write_text(summary_md, encoding="utf-8")
    summary_json_path.write_text(
        json.dumps({"rows": rows, "aggregate": aggregate, "regression": regression}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n" + summary_md)
    print(f"\n结果已保存到 {output_dir}")
    return 0 if regression.get("overall_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
