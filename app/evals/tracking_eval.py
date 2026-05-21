"""金融事件处理离线评测。"""
from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from app.config import OUTPUT_DIR, PROJECT_ROOT
from app.tracking.alerts import build_tracking_alerts
from app.tracking.deduper import dedupe_events
from app.tracking.models import EventCollection, MarketEvent
from app.tracking.normalizer import normalize_source_item
from app.tracking.service import summarize_events

DEFAULT_BENCHMARK_PATH = PROJECT_ROOT / "data" / "benchmarks" / "tracking_events.jsonl"
DEFAULT_TARGET_COUNT = 500


@dataclass
class TrackingEvalSample:
    raw: dict
    expected_event_type: str
    expected_impact_level: str
    duplicate_group: str
    should_alert: bool
    label_source: str = ""
    needs_human_review: bool = False


def load_tracking_benchmark(path: Path = DEFAULT_BENCHMARK_PATH) -> list[TrackingEvalSample]:
    if not path.exists():
        return []
    samples: list[TrackingEvalSample] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        samples.append(
            TrackingEvalSample(
                raw=dict(payload.get("raw") or payload),
                expected_event_type=str(payload.get("expected_event_type") or ""),
                expected_impact_level=str(payload.get("expected_impact_level") or ""),
                duplicate_group=str(payload.get("duplicate_group") or payload.get("event_id") or ""),
                should_alert=bool(payload.get("should_alert", False)),
                label_source=str(payload.get("label_source") or "manual_seed"),
                needs_human_review=bool(payload.get("needs_human_review", False)),
            )
        )
    return samples


def evaluate_tracking_pipeline(samples: list[TrackingEvalSample]) -> dict[str, object]:
    if not samples:
        return {
            "sample_count": 0,
            "dedupe": _metric_payload(0, 0, 0),
            "event_type_accuracy": 0.0,
            "event_type_macro_f1": 0.0,
            "impact": _metric_payload(0, 0, 0),
            "alert": {"false_positive_rate": 0.0, "false_negative_rate": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0},
            "type_labels": {},
            "alert_positive_count": 0,
            "alert_negative_count": 0,
        }

    events = [_event_from_sample(sample) for sample in samples]
    deduped = dedupe_events(events)
    collection = summarize_events(deduped)
    alerts = build_tracking_alerts(collection, limit=max(20, len(samples) * 3))
    alert_event_ids = {alert.event_id for alert in alerts}
    parent_by_event_id = {event.event_id: event.parent_event_id or event.event_id for event in events}

    dedupe_metric = _pairwise_dedupe_metrics(samples, events)
    type_accuracy = _accuracy([event.event_type for event in events], [sample.expected_event_type for sample in samples])
    type_macro_f1, type_labels = _macro_f1([event.event_type for event in events], [sample.expected_event_type for sample in samples])
    impact_metric = _binary_metric(
        [event.impact_level == "high" for event in events],
        [sample.expected_impact_level == "high" for sample in samples],
    )
    alert_metric = _alert_metric(
        [parent_by_event_id.get(event.event_id, event.event_id) in alert_event_ids for event in events],
        [sample.should_alert for sample in samples],
    )

    return {
        "sample_count": len(samples),
        "deduped_event_count": len(deduped),
        "duplicate_source_count": sum(max(0, int(event.duplicate_count or 1) - 1) for event in deduped),
        "dedupe": dedupe_metric,
        "event_type_accuracy": round(type_accuracy, 4),
        "event_type_macro_f1": round(type_macro_f1, 4),
        "impact": impact_metric,
        "alert": alert_metric,
        "alert_positive_count": sum(1 for sample in samples if sample.should_alert),
        "alert_negative_count": sum(1 for sample in samples if not sample.should_alert),
        "needs_human_review_count": sum(1 for sample in samples if sample.needs_human_review),
        "label_source_counts": _count_values(sample.label_source for sample in samples),
        "type_labels": type_labels,
    }


def run_tracking_eval(
    *,
    benchmark_path: Path = DEFAULT_BENCHMARK_PATH,
    output_dir: Path | None = None,
    target_count: int = DEFAULT_TARGET_COUNT,
) -> dict[str, object]:
    samples = load_tracking_benchmark(benchmark_path)
    eval_samples = expand_samples(samples, target_count=target_count)
    result = evaluate_tracking_pipeline(eval_samples)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_dir = output_dir or OUTPUT_DIR / "evals"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"tracking_eval_{timestamp}.json"
    md_path = out_dir / f"tracking_eval_{timestamp}.md"
    result = {
        **result,
        "seed_sample_count": len(samples),
        "target_count": target_count,
        "benchmark_path": str(benchmark_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "json_path": str(json_path),
        "markdown_path": str(md_path),
    }
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(format_tracking_eval_markdown(result), encoding="utf-8")
    return result


def expand_samples(samples: list[TrackingEvalSample], *, target_count: int = DEFAULT_TARGET_COUNT) -> list[TrackingEvalSample]:
    """把种子标注样本扩展为稳定评测集，便于保持仓库体积可控。"""
    if not samples or len(samples) >= target_count:
        return samples
    expanded: list[TrackingEvalSample] = []
    cycle = 0
    while len(expanded) < target_count:
        cycle += 1
        for sample in samples:
            raw = deepcopy(sample.raw)
            raw["id"] = f"{raw.get('id', 'event')}_v{cycle}"
            raw["title"] = f"样本{cycle} {raw.get('title', '')}"
            if raw.get("link"):
                raw["link"] = f"{raw['link']}/v{cycle}"
            if raw.get("url"):
                raw["url"] = f"{raw['url']}/v{cycle}"
            if isinstance(raw.get("time"), str) and len(raw["time"]) >= 10:
                raw["time"] = _shift_date(raw["time"], cycle)
            group = f"{sample.duplicate_group}_v{cycle}"
            expanded.append(TrackingEvalSample(
                raw=raw,
                expected_event_type=sample.expected_event_type,
                expected_impact_level=sample.expected_impact_level,
                duplicate_group=group,
                should_alert=sample.should_alert,
                label_source=sample.label_source,
                needs_human_review=sample.needs_human_review,
            ))
            if len(expanded) >= target_count:
                break
    return expanded


def format_tracking_eval_markdown(result: dict[str, object]) -> str:
    dedupe = dict(result.get("dedupe") or {})
    impact = dict(result.get("impact") or {})
    alert = dict(result.get("alert") or {})
    lines = [
        "# 金融事件处理 Benchmark",
        "",
        f"- 样本数：**{result.get('sample_count', 0)}**",
        f"- 种子样本数：**{result.get('seed_sample_count', result.get('sample_count', 0))}**",
        f"- 待人工复核标签：**{result.get('needs_human_review_count', 0)}**",
        f"- 预警正 / 负样本：**{result.get('alert_positive_count', 0)} / {result.get('alert_negative_count', 0)}**",
        f"- 去重后事件数：**{result.get('deduped_event_count', 0)}**",
        f"- 生成时间：{result.get('generated_at', '')}",
        "",
        "## 核心指标",
        f"- 去重 Precision / Recall / F1：**{dedupe.get('precision', 0):.1%} / {dedupe.get('recall', 0):.1%} / {dedupe.get('f1', 0):.1%}**",
        f"- 事件类型 Accuracy / Macro-F1：**{float(result.get('event_type_accuracy', 0)):.1%} / {float(result.get('event_type_macro_f1', 0)):.1%}**",
        f"- 高影响识别 Precision / Recall / F1：**{impact.get('precision', 0):.1%} / {impact.get('recall', 0):.1%} / {impact.get('f1', 0):.1%}**",
        f"- 预警 Precision / Recall / F1：**{alert.get('precision', 0):.1%} / {alert.get('recall', 0):.1%} / {alert.get('f1', 0):.1%}**",
        f"- 预警误报率 / 漏报率：**{alert.get('false_positive_rate', 0):.1%} / {alert.get('false_negative_rate', 0):.1%}**",
        "",
        "## 简历口径",
        _tracking_resume_scope(result),
    ]
    return "\n".join(lines) + "\n"


def _tracking_resume_scope(result: dict[str, object]) -> str:
    review_count = int(result.get("needs_human_review_count", 0) or 0)
    if review_count:
        return "基于公开公告/新闻等来源元数据生成真实事件初始样本，并标记需人工复核标签；用于暴露事件去重、分类、高影响识别和预警规则的真实问题，不把启发式标签包装成人工标注指标。"
    return "基于项目内金融事件种子标注集扩展出可复现评测样本，对事件去重、分类、高影响识别和预警规则进行离线评测，指标由 `python main.py tracking-eval` 生成。"


def _shift_date(value: str, cycle: int) -> str:
    try:
        base = datetime.fromisoformat(value[:10])
    except Exception:
        return value
    return (base + timedelta(days=max(0, cycle - 1) * 7)).date().isoformat()


def _event_from_sample(sample: TrackingEvalSample) -> MarketEvent:
    raw = dict(sample.raw)
    stock_code = str(raw.pop("stock_code", "600519"))
    stock_name = str(raw.pop("stock_name", ""))
    return normalize_source_item(raw, stock_code=stock_code, stock_name=stock_name)


def _pairwise_dedupe_metrics(samples: list[TrackingEvalSample], events: list[MarketEvent]) -> dict[str, float]:
    expected: list[bool] = []
    predicted: list[bool] = []
    parent_by_event_id = {event.event_id: event.parent_event_id or event.event_id for event in events}
    for left in range(len(samples)):
        for right in range(left + 1, len(samples)):
            expected.append(samples[left].duplicate_group == samples[right].duplicate_group)
            predicted.append(parent_by_event_id.get(events[left].event_id) == parent_by_event_id.get(events[right].event_id))
    return _binary_metric(predicted, expected)


def _alert_metric(predicted: list[bool], expected: list[bool]) -> dict[str, float]:
    metric = _binary_metric(predicted, expected)
    fp = sum(1 for pred, exp in zip(predicted, expected) if pred and not exp)
    fn = sum(1 for pred, exp in zip(predicted, expected) if not pred and exp)
    negative = sum(1 for exp in expected if not exp)
    positive = sum(1 for exp in expected if exp)
    return {
        **metric,
        "false_positive_rate": round(fp / negative, 4) if negative else 0.0,
        "false_negative_rate": round(fn / positive, 4) if positive else 0.0,
    }


def _binary_metric(predicted: list[bool], expected: list[bool]) -> dict[str, float]:
    tp = sum(1 for pred, exp in zip(predicted, expected) if pred and exp)
    fp = sum(1 for pred, exp in zip(predicted, expected) if pred and not exp)
    fn = sum(1 for pred, exp in zip(predicted, expected) if not pred and exp)
    return _metric_payload(tp, fp, fn)


def _metric_payload(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


def _accuracy(predicted: list[str], expected: list[str]) -> float:
    if not expected:
        return 0.0
    return sum(1 for pred, exp in zip(predicted, expected) if pred == exp) / len(expected)


def _macro_f1(predicted: list[str], expected: list[str]) -> tuple[float, dict[str, float]]:
    labels = sorted(set(predicted) | set(expected))
    scores: dict[str, float] = {}
    for label in labels:
        metric = _binary_metric([item == label for item in predicted], [item == label for item in expected])
        scores[label] = metric["f1"]
    return (sum(scores.values()) / len(scores) if scores else 0.0), scores


def _count_values(values) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts
