"""消融/基线评测脚本 — 输出质量、耗时、Token、成功率等指标"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from app.config import ABLATION_OUTPUT_DIR
from app.models import AblationConfig

DEFAULT_STOCKS = ["600519", "000858", "300750"]
DEFAULT_EXPERIMENTS = ["baseline", "no_reflection", "no_rag"]
OUTPUT_DIR = ABLATION_OUTPUT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class AblationExperiment:
    label: str
    banner: str
    config: AblationConfig


def _build_experiment(label: str) -> AblationExperiment:
    if label == "no_reflection":
        return AblationExperiment(
            label=label,
            banner="-Reflection（移除反思阶段）",
            config=AblationConfig(label=label, enable_reflection=False),
        )
    if label == "no_rag":
        return AblationExperiment(
            label=label,
            banner="-RAG（移除知识库检索）",
            config=AblationConfig(label=label, enable_rag=False),
        )
    return AblationExperiment(
        label=label,
        banner="Baseline（完整系统）",
        config=AblationConfig(label=label),
    )


def _build_ablation_config(label: str) -> AblationConfig:
    return _build_experiment(label).config


def _run_experiment(stock_code: str, *, label: str, banner: str | None = None):
    experiment = _build_experiment(label)
    print("=" * 60)
    print(f"{banner or experiment.banner} | 股票: {stock_code}")
    print("=" * 60)
    from app.engine import ReportEngine

    engine = ReportEngine(ablation_config=experiment.config)
    state = engine.run(stock_code)
    return state


def run_baseline(stock_code: str):
    return _run_experiment(stock_code, label="baseline")


def run_no_reflection(stock_code: str):
    return _run_experiment(stock_code, label="no_reflection")


def run_no_rag(stock_code: str):
    return _run_experiment(stock_code, label="no_rag")


RUNNERS = {
    "baseline": run_baseline,
    "no_reflection": run_no_reflection,
    "no_rag": run_no_rag,
}


def _build_artifact_index(output_dir: Path, rows: list[dict]) -> dict[str, Any]:
    stocks: dict[str, dict[str, dict[str, str]]] = {}
    for row in rows:
        stock_code = row.get("stock_code", "")
        label = row.get("label", "")
        if not stock_code or not label:
            continue
        stocks.setdefault(stock_code, {})[label] = {
            "report_path": str(output_dir / stock_code / f"report_{label}.md"),
            "eval_markdown_path": str(output_dir / stock_code / f"eval_{label}.md"),
            "eval_json_path": str(output_dir / stock_code / f"eval_{label}.json"),
        }
    return {"stocks": stocks, "summary_markdown_path": str(output_dir / "ablation_summary.md"), "summary_json_path": str(output_dir / "ablation_summary.json")}


def _build_history_summary(current: dict[str, dict], previous: dict[str, dict] | None) -> dict[str, dict[str, float | None]]:
    if not previous:
        return {}
    history: dict[str, dict[str, float | None]] = {}
    for label, item in current.items():
        previous_item = previous.get(label, {}) if isinstance(previous.get(label, {}), dict) else {}
        history[label] = {
            "previous_avg_score": previous_item.get("avg_score"),
            "score_delta": round(item.get("avg_score", 0.0) - previous_item.get("avg_score", 0.0), 2) if "avg_score" in previous_item else None,
            "previous_avg_duration_s": previous_item.get("avg_duration_s"),
            "duration_delta_s": round(item.get("avg_duration_s", 0.0) - previous_item.get("avg_duration_s", 0.0), 2) if "avg_duration_s" in previous_item else None,
            "previous_avg_tokens": previous_item.get("avg_tokens"),
            "tokens_delta": round(item.get("avg_tokens", 0.0) - previous_item.get("avg_tokens", 0.0), 1) if "avg_tokens" in previous_item else None,
        }
    return history


def _load_previous_summary(output_dir: Path, summary_name: str) -> dict[str, Any] | None:
    summary_path = output_dir / summary_name
    if not summary_path.exists() or not summary_path.is_file():
        return None
    try:
        return json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def evaluate_state(state, label: str, stock_code: str, *, use_llm_judge: bool, output_dir: Path) -> dict | None:
    from app.evals.report_eval import evaluate_report, evaluate_report_with_metrics, format_eval_report

    experiment = _build_experiment(label)
    ablation_config = asdict(experiment.config)
    if not state.final_report:
        print(f"  ❌ {label}/{stock_code}: 研报生成失败")
        return {
            "label": label,
            "experiment_banner": experiment.banner,
            "ablation_config": ablation_config,
            "stock_code": stock_code,
            "success": False,
            "overall_score": 0.0,
            "duration_s": state.run_metrics.get("duration_s", 0),
            "total_tokens": state.run_metrics.get("total_tokens", 0),
            "agent_steps": int(state.sections.get("agent_steps", "0") or 0),
            "rag_hits": int(state.sections.get("rag_hits", "0") or 0),
            "news_count": len(getattr(state, "news", []) or []),
            "risk_count": len(getattr(state, "risks", []) or []),
            "postprocess_fix_count": int(state.sections.get("postprocess_fix_count", "0") or 0),
        }

    eval_result = evaluate_report(state.final_report, state, stock_code, use_llm_judge=use_llm_judge)
    metrics_payload = evaluate_report_with_metrics(state.final_report, state, stock_code, use_llm_judge=use_llm_judge)
    stock_dir = output_dir / stock_code
    stock_dir.mkdir(parents=True, exist_ok=True)

    report_path = stock_dir / f"report_{label}.md"
    eval_md_path = stock_dir / f"eval_{label}.md"
    eval_json_path = stock_dir / f"eval_{label}.json"
    report_path.write_text(state.final_report, encoding="utf-8")
    eval_md_path.write_text(format_eval_report(eval_result), encoding="utf-8")
    eval_json_path.write_text(json.dumps(metrics_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    run_metrics = metrics_payload.get("run_metrics", {})
    row = {
        "label": label,
        "experiment_banner": experiment.banner,
        "ablation_config": ablation_config,
        "stock_code": stock_code,
        "success": True,
        "overall_score": eval_result.overall_score,
        "section_coverage": eval_result.section_coverage,
        "has_tables": eval_result.has_tables,
        "has_numbers": eval_result.has_numbers,
        "completeness": eval_result.completeness,
        "data_support": eval_result.data_support,
        "reasoning_quality": eval_result.reasoning_quality,
        "readability": eval_result.readability,
        "report_length": eval_result.report_length,
        "numeric_references": eval_result.numeric_references,
        "risk_evidence_count": eval_result.risk_evidence_count,
        "risk_transmission_count": eval_result.risk_transmission_count,
        "investment_anchor_present": eval_result.investment_anchor_present,
        "postprocess_fix_count": eval_result.postprocess_fix_count,
        "agent_steps": int(state.sections.get("agent_steps", "0") or 0),
        "rag_hits": int(state.sections.get("rag_hits", "0") or 0),
        "news_count": len(getattr(state, "news", []) or []),
        "risk_count": len(getattr(state, "risks", []) or []),
        "duration_s": run_metrics.get("duration_s", 0),
        "llm_calls": run_metrics.get("llm_calls", 0),
        "tool_calls": run_metrics.get("tool_calls", 0),
        "total_tokens": run_metrics.get("total_tokens", 0),
        "errors": run_metrics.get("errors", 0),
        "trace_id": run_metrics.get("trace_id", ""),
    }

    print(
        f"  ✅ {label}/{stock_code}: 评分 {row['overall_score']:.1f} | "
        f"耗时 {row['duration_s']:.2f}s | tokens {row['total_tokens']} | "
        f"步数 {row['agent_steps']} | RAG {row['rag_hits']}"
    )
    return row


def summarize_results(rows: list[dict], *, use_llm_judge: bool, previous_aggregate: dict[str, dict] | None = None) -> tuple[str, dict]:
    experiment_contracts = {
        label: {
            "banner": _build_experiment(label).banner,
            "ablation_config": asdict(_build_experiment(label).config),
        }
        for label in sorted({row["label"] for row in rows})
    }
    summary_lines = [
        "# 消融实验结果",
        "",
        f"> 评测日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 样本股票: {', '.join(sorted({row['stock_code'] for row in rows}))}",
        f"> LLM 评委: {'开启' if use_llm_judge else '关闭（仅规则指标）'}",
        "",
        "## 单次结果",
        "",
        "| 股票 | 实验组 | 成功 | 综合评分 | 耗时(s) | Tokens | LLM调用 | 工具调用 | Agent步数 | RAG命中 | 新闻数 | 风险数 | 风险证据 | 风险传导 | 估值锚 | 自动修补 | 字数 | 数值引用 | 错误数 |",
        "|------|--------|------|----------|---------|--------|---------|----------|-----------|----------|--------|--------|----------|----------|--------|----------|------|----------|--------|",
    ]

    for row in rows:
        summary_lines.append(
            f"| {row['stock_code']} | {row['label']} | {'✅' if row['success'] else '❌'} | "
            f"{row['overall_score']:.1f} | {row['duration_s']:.2f} | {row['total_tokens']} | "
            f"{row.get('llm_calls', 0)} | {row.get('tool_calls', 0)} | {row['agent_steps']} | {row['rag_hits']} | "
            f"{row.get('news_count', 0)} | {row.get('risk_count', 0)} | {row.get('risk_evidence_count', 0)} | {row.get('risk_transmission_count', 0)} | "
            f"{'✅' if row.get('investment_anchor_present') else '❌'} | {row.get('postprocess_fix_count', 0)} | {row.get('report_length', 0)} | {row.get('numeric_references', 0)} | {row.get('errors', 0)} |"
        )

    experiments = sorted({row["label"] for row in rows})
    aggregate: dict[str, dict] = {}
    summary_lines.extend(["", "## 聚合指标", ""])
    summary_lines.append(
        "| 实验组 | 样本数 | 成功率 | 平均评分 | 平均耗时(s) | 平均Tokens | 平均LLM调用 | 平均工具调用 | 平均字数 | 平均RAG命中 | 平均新闻数 | 平均风险数 | 平均风险证据 | 平均风险传导 | 估值锚覆盖率 | 平均自动修补次数 |"
    )
    summary_lines.append(
        "|--------|--------|--------|----------|-------------|------------|-------------|--------------|----------|-------------|------------|------------|--------------|--------------|--------------|------------------|"
    )

    for label in experiments:
        subset = [row for row in rows if row["label"] == label]
        success_rows = [row for row in subset if row["success"]]
        aggregate[label] = {
            "samples": len(subset),
            "success_rate": round(len(success_rows) / len(subset) * 100, 1) if subset else 0.0,
            "avg_score": round(mean(row["overall_score"] for row in subset), 2) if subset else 0.0,
            "avg_duration_s": round(mean(row["duration_s"] for row in subset), 2) if subset else 0.0,
            "avg_tokens": round(mean(row["total_tokens"] for row in subset), 1) if subset else 0.0,
            "avg_llm_calls": round(mean(row.get("llm_calls", 0) for row in subset), 1) if subset else 0.0,
            "avg_tool_calls": round(mean(row.get("tool_calls", 0) for row in subset), 1) if subset else 0.0,
            "avg_report_length": round(mean(row.get("report_length", 0) for row in success_rows), 1) if success_rows else 0.0,
            "avg_rag_hits": round(mean(row["rag_hits"] for row in subset), 1) if subset else 0.0,
            "avg_news_count": round(mean(row.get("news_count", 0) for row in subset), 1) if subset else 0.0,
            "avg_risk_count": round(mean(row.get("risk_count", 0) for row in subset), 1) if subset else 0.0,
            "avg_risk_evidence_count": round(mean(row.get("risk_evidence_count", 0) for row in success_rows), 1) if success_rows else 0.0,
            "avg_risk_transmission_count": round(mean(row.get("risk_transmission_count", 0) for row in success_rows), 1) if success_rows else 0.0,
            "investment_anchor_coverage": round(mean(1 if row.get("investment_anchor_present") else 0 for row in success_rows) * 100, 1) if success_rows else 0.0,
            "avg_postprocess_fix_count": round(mean(row.get("postprocess_fix_count", 0) for row in success_rows), 1) if success_rows else 0.0,
        }
        item = aggregate[label]
        summary_lines.append(
            f"| {label} | {item['samples']} | {item['success_rate']:.1f}% | {item['avg_score']:.2f} | "
            f"{item['avg_duration_s']:.2f} | {item['avg_tokens']:.1f} | {item['avg_llm_calls']:.1f} | "
            f"{item['avg_tool_calls']:.1f} | {item['avg_report_length']:.1f} | {item['avg_rag_hits']:.1f} | "
            f"{item['avg_news_count']:.1f} | {item['avg_risk_count']:.1f} | {item['avg_risk_evidence_count']:.1f} | "
            f"{item['avg_risk_transmission_count']:.1f} | {item['investment_anchor_coverage']:.1f}% | {item['avg_postprocess_fix_count']:.1f} |"
        )

    if "baseline" in aggregate:
        baseline = aggregate["baseline"]
        summary_lines.extend(["", "## 相对 Baseline 的变化", ""])
        for label, item in aggregate.items():
            if label == "baseline":
                continue
            summary_lines.append(
                f"- **{label}**：评分 {item['avg_score'] - baseline['avg_score']:+.2f}，"
                f"耗时 {item['avg_duration_s'] - baseline['avg_duration_s']:+.2f}s，"
                f"Tokens {item['avg_tokens'] - baseline['avg_tokens']:+.1f}，"
                f"RAG命中 {item['avg_rag_hits'] - baseline['avg_rag_hits']:+.1f}"
            )

    history_summary = _build_history_summary(aggregate, previous_aggregate)
    if history_summary:
        summary_lines.extend(["", "## 相对上次汇总的变化", ""])
        for label, item in history_summary.items():
            if item["score_delta"] is None:
                continue
            summary_lines.append(
                f"- **{label}**：评分 {item['score_delta']:+.2f}，耗时 {item['duration_delta_s']:+.2f}s，Tokens {item['tokens_delta']:+.1f}"
            )

    return "\n".join(summary_lines), {
        "experiments": aggregate,
        "experiment_contracts": experiment_contracts,
        "history_summary": history_summary,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行金融研报系统消融/基线评测")
    parser.add_argument("--stocks", nargs="+", default=DEFAULT_STOCKS, help="评测股票代码列表")
    parser.add_argument("--experiments", nargs="+", default=DEFAULT_EXPERIMENTS, choices=sorted(RUNNERS.keys()))
    parser.add_argument("--llm-judge", action="store_true", help="启用 LLM-as-Judge 评分（成本更高）")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="输出目录")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    previous_summary = _load_previous_summary(output_dir, "ablation_summary.json") or {}
    previous_aggregate = previous_summary.get("aggregate") if isinstance(previous_summary.get("aggregate"), dict) else None

    rows: list[dict] = []
    for stock_code in args.stocks:
        for label in args.experiments:
            state = RUNNERS[label](stock_code)
            row = evaluate_state(
                state,
                label,
                stock_code,
                use_llm_judge=args.llm_judge,
                output_dir=output_dir,
            )
            if row:
                rows.append(row)

    summary_md, aggregate = summarize_results(rows, use_llm_judge=args.llm_judge, previous_aggregate=previous_aggregate)
    artifact_index = _build_artifact_index(output_dir, rows)
    summary_path = output_dir / "ablation_summary.md"
    summary_json_path = output_dir / "ablation_summary.json"
    summary_path.write_text(summary_md, encoding="utf-8")
    summary_json_path.write_text(
        json.dumps({"rows": rows, "aggregate": aggregate["experiments"], "experiment_contracts": aggregate["experiment_contracts"], "history_summary": aggregate["history_summary"], "artifact_index": artifact_index}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n" + summary_md)
    print(f"\n结果已保存到 {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
