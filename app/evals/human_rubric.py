"""人工评审 Rubric 与种子基准集工具"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.evals.report_eval import evaluate_report_with_metrics

DEFAULT_BENCHMARK_PATH = Path(__file__).parent.parent.parent / "data" / "evals" / "human_benchmark_seed.json"

RUBRIC_DIMENSIONS = [
    {
        "key": "structure_completeness",
        "title": "结构完整性",
        "scale": "1-5",
        "question": "是否覆盖投资要点、财务、估值、风险、投资建议等核心章节，且结构清晰可读？",
    },
    {
        "key": "evidence_quality",
        "title": "证据充分性",
        "scale": "1-5",
        "question": "核心判断是否绑定具体数字、表格、风险证据或同行对比，而不是泛化表述？",
    },
    {
        "key": "reasoning_quality",
        "title": "推理质量",
        "scale": "1-5",
        "question": "是否体现因果链条、历史比较、同行比较和估值推导，而不仅是数据复述？",
    },
    {
        "key": "reliability",
        "title": "可靠性",
        "scale": "1-5",
        "question": "报告是否显式披露数据缺口、保持结论克制，并与状态数据/估值结果一致？",
    },
    {
        "key": "readability",
        "title": "可读性",
        "scale": "1-5",
        "question": "语言是否专业、克制，适合作为可交付初稿继续打磨？",
    },
]


def load_human_benchmark(path: Path | None = None) -> list[dict[str, Any]]:
    benchmark_path = path or DEFAULT_BENCHMARK_PATH
    if not benchmark_path.exists():
        return []
    return json.loads(benchmark_path.read_text(encoding="utf-8"))


def build_manual_review_payload(report: str, stock_code: str, *, benchmark_entry: dict[str, Any] | None = None, state=None) -> dict[str, Any]:
    automated = evaluate_report_with_metrics(report, state=state, stock_code=stock_code, use_llm_judge=False)
    return {
        "stock_code": stock_code,
        "benchmark": benchmark_entry or {},
        "automated_metrics": automated,
        "manual_rubric": [
            {
                **item,
                "score": None,
                "comment": "",
            }
            for item in RUBRIC_DIMENSIONS
        ],
        "overall_comment": "",
    }


def format_manual_review_markdown(payload: dict[str, Any]) -> str:
    benchmark = payload.get("benchmark", {})
    automated = payload.get("automated_metrics", {})
    lines = [
        f"# 人工评审表 — {payload.get('stock_code', '')}",
        "",
        "## Benchmark 标签",
        f"- 股票: {benchmark.get('stock_name', '未知')} ({payload.get('stock_code', '')})",
        f"- 行业: {benchmark.get('industry', '未知')}",
        f"- 关注点: {', '.join(benchmark.get('review_focus', [])) or '无'}",
        f"- 关键风险: {', '.join(benchmark.get('key_risks', [])) or '无'}",
        "",
        "## 自动指标参考",
        f"- 综合评分: **{automated.get('overall_score', 0)}**",
        f"- 章节覆盖率: **{automated.get('section_coverage', 0):.0%}**",
        f"- 风险证据条目: **{automated.get('risk_evidence_count', 0)}**",
        f"- 风险传导条目: **{automated.get('risk_transmission_count', 0)}**",
        f"- 估值锚覆盖: {'✅' if automated.get('investment_anchor_present') else '❌'}",
        f"- 数据降级披露: **{automated.get('data_gap_disclosure_count', 0)}**",
        "",
        "## 人工 Rubric（1-5）",
    ]
    for item in payload.get("manual_rubric", []):
        lines.extend(
            [
                f"### {item['title']}",
                f"- 评分: `{item.get('score')}` / {item['scale']}",
                f"- 评审问题: {item['question']}",
                f"- 备注: {item.get('comment', '')}",
                "",
            ]
        )
    lines.extend(
        [
            "## 综合评语",
            payload.get("overall_comment", ""),
        ]
    )
    return "\n".join(lines)
