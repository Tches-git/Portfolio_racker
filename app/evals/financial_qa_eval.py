"""公共金融 QA/RAG benchmark 适配与评测。

支持读取 FinanceBench、FinQA、TAT-QA 等公开数据集的本地子集。仓库不内置
第三方数据本体，避免许可证和体积问题；用户把下载后的 JSON/JSONL 子集放到
本地后即可通过 CLI 评测答案准确率、token-F1、上下文命中和引用覆盖。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from app.config import OUTPUT_DIR


@dataclass
class FinancialQASample:
    sample_id: str
    dataset: str
    question: str
    answer: str
    contexts: list[str]
    source_ids: list[str]


@dataclass
class FinancialQAPrediction:
    sample_id: str
    prediction: str
    cited_source_ids: list[str]


def load_financial_qa_benchmark(path: Path, *, dataset: str = "auto", limit: int = 0) -> list[FinancialQASample]:
    records = _read_records(path)
    samples: list[FinancialQASample] = []
    for index, record in enumerate(records, start=1):
        samples.extend(_samples_from_record(record, index=index, dataset=dataset))
        if limit and len(samples) >= limit:
            return samples[:limit]
    return samples


def load_financial_qa_predictions(path: Path | None) -> list[FinancialQAPrediction]:
    if not path:
        return []
    predictions: list[FinancialQAPrediction] = []
    for index, record in enumerate(_read_records(path), start=1):
        sample_id = str(record.get("sample_id") or record.get("id") or record.get("uid") or index)
        predictions.append(FinancialQAPrediction(
            sample_id=sample_id,
            prediction=str(record.get("prediction") or record.get("answer") or ""),
            cited_source_ids=[str(item) for item in record.get("cited_source_ids") or record.get("sources") or []],
        ))
    return predictions


def evaluate_financial_qa(
    samples: list[FinancialQASample],
    predictions: list[FinancialQAPrediction] | None = None,
) -> dict[str, object]:
    if not samples:
        return {
            "sample_count": 0,
            "prediction_count": 0,
            "answer_exact_match": 0.0,
            "answer_key_hit_rate": 0.0,
            "answer_token_f1": 0.0,
            "context_answer_hit_rate": 0.0,
            "citation_coverage_rate": 0.0,
            "dataset_counts": {},
        }

    pred_by_id = {item.sample_id: item for item in (predictions or [])}
    exact_scores: list[float] = []
    key_hit_scores: list[float] = []
    f1_scores: list[float] = []
    context_hits: list[float] = []
    citation_hits: list[float] = []
    dataset_counts: dict[str, int] = {}
    preview: list[dict[str, object]] = []

    for sample in samples:
        prediction = pred_by_id.get(sample.sample_id)
        pred_text = prediction.prediction if prediction else ""
        exact_scores.append(1.0 if _normalize_answer(pred_text) == _normalize_answer(sample.answer) and pred_text else 0.0)
        key_hit_scores.append(1.0 if pred_text and _answer_key_hit(pred_text, sample.answer) else 0.0)
        f1_scores.append(_token_f1(pred_text, sample.answer) if pred_text else 0.0)
        context_hits.append(1.0 if _answer_in_context(sample.answer, sample.contexts) else 0.0)
        citation_hits.append(_citation_hit(sample, prediction))
        dataset_counts[sample.dataset] = dataset_counts.get(sample.dataset, 0) + 1
        if len(preview) < 8:
            preview.append({
                "sample_id": sample.sample_id,
                "dataset": sample.dataset,
                "question": sample.question[:120],
                "has_prediction": bool(pred_text),
                "context_hit": bool(context_hits[-1]),
            })

    return {
        "sample_count": len(samples),
        "prediction_count": len(pred_by_id),
        "answer_exact_match": round(sum(exact_scores) / len(exact_scores), 4),
        "answer_key_hit_rate": round(sum(key_hit_scores) / len(key_hit_scores), 4),
        "answer_token_f1": round(sum(f1_scores) / len(f1_scores), 4),
        "context_answer_hit_rate": round(sum(context_hits) / len(context_hits), 4),
        "citation_coverage_rate": round(sum(citation_hits) / len(citation_hits), 4),
        "dataset_counts": dataset_counts,
        "samples_preview": preview,
    }


def run_financial_qa_eval(
    *,
    benchmark_path: Path,
    predictions_path: Path | None = None,
    output_dir: Path | None = None,
    dataset: str = "auto",
    limit: int = 0,
) -> dict[str, object]:
    samples = load_financial_qa_benchmark(benchmark_path, dataset=dataset, limit=limit)
    predictions = load_financial_qa_predictions(predictions_path)
    result = evaluate_financial_qa(samples, predictions)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_dir = output_dir or OUTPUT_DIR / "evals"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"financial_qa_eval_{timestamp}.json"
    md_path = out_dir / f"financial_qa_eval_{timestamp}.md"
    result = {
        **result,
        "benchmark_path": str(benchmark_path),
        "predictions_path": str(predictions_path or ""),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "benchmark_scope": "FinanceBench / FinQA / TAT-QA 等公共金融 QA/RAG 数据集的本地子集适配评测",
    }
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(format_financial_qa_eval_markdown(result), encoding="utf-8")
    return result


def format_financial_qa_eval_markdown(result: dict[str, object]) -> str:
    lines = [
        "# 公共金融 QA/RAG Benchmark 评测",
        "",
        f"- 样本数：**{result.get('sample_count', 0)}**",
        f"- 预测数：**{result.get('prediction_count', 0)}**",
        f"- 数据路径：{result.get('benchmark_path', '')}",
        f"- 生成时间：{result.get('generated_at', '')}",
        "",
        "## 核心指标",
        f"- Exact Match：**{float(result.get('answer_exact_match', 0) or 0):.1%}**",
        f"- 关键答案命中率：**{float(result.get('answer_key_hit_rate', 0) or 0):.1%}**",
        f"- Token-F1：**{float(result.get('answer_token_f1', 0) or 0):.1%}**",
        f"- 上下文答案命中率：**{float(result.get('context_answer_hit_rate', 0) or 0):.1%}**",
        f"- 引用覆盖率：**{float(result.get('citation_coverage_rate', 0) or 0):.1%}**",
        "",
        "## 数据集分布",
    ]
    counts = dict(result.get("dataset_counts") or {})
    if counts:
        for name, count in sorted(counts.items()):
            lines.append(f"- {name}: {count}")
    else:
        lines.append("- 暂无")
    lines.extend([
        "",
        "## 简历口径",
        "接入公共金融 QA/RAG benchmark 的本地子集适配器，对检索上下文、答案准确率和引用覆盖进行离线评测；未提供预测文件时仅统计上下文答案命中，不夸大生成准确率。",
    ])
    return "\n".join(lines) + "\n"


def _read_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("data", "items", "examples", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    return []


def _samples_from_record(record: dict[str, Any], *, index: int, dataset: str) -> list[FinancialQASample]:
    guessed = _guess_dataset(record, dataset)
    if guessed == "tatqa" and isinstance(record.get("questions"), list):
        contexts = _tatqa_contexts(record)
        samples: list[FinancialQASample] = []
        for q_index, question in enumerate(record.get("questions") or [], start=1):
            if not isinstance(question, dict):
                continue
            samples.append(FinancialQASample(
                sample_id=str(question.get("uid") or question.get("id") or f"tatqa_{index}_{q_index}"),
                dataset="tatqa",
                question=str(question.get("question") or ""),
                answer=_answer_to_text(question.get("answer")),
                contexts=contexts,
                source_ids=_source_ids(record, default=f"tatqa_doc_{index}"),
            ))
        return [sample for sample in samples if sample.question and sample.answer]

    if guessed == "finqa":
        qa = record.get("qa") if isinstance(record.get("qa"), dict) else record
        contexts = _flatten_texts([record.get("pre_text"), record.get("table"), record.get("post_text"), record.get("context")])
        return [_single_sample(
            sample_id=str(record.get("id") or record.get("uid") or f"finqa_{index}"),
            dataset="finqa",
            question=str(qa.get("question") or record.get("question") or ""),
            answer=_answer_to_text(qa.get("answer") or record.get("answer")),
            contexts=contexts,
            source_ids=_source_ids(record, default=f"finqa_doc_{index}"),
        )]

    contexts = _flatten_texts([record.get("context"), record.get("contexts"), record.get("evidence"), record.get("source"), record.get("sources")])
    return [_single_sample(
        sample_id=str(record.get("id") or record.get("uid") or record.get("sample_id") or record.get("financebench_id") or f"{guessed}_{index}"),
        dataset=guessed,
        question=str(record.get("question") or record.get("query") or ""),
        answer=_answer_to_text(record.get("answer") or record.get("gold_answer") or record.get("expected_answer")),
        contexts=contexts,
        source_ids=_source_ids(record, default=f"{guessed}_doc_{index}"),
    )]


def _single_sample(*, sample_id: str, dataset: str, question: str, answer: str, contexts: list[str], source_ids: list[str]) -> FinancialQASample:
    return FinancialQASample(
        sample_id=sample_id,
        dataset=dataset,
        question=question,
        answer=answer,
        contexts=contexts,
        source_ids=source_ids,
    )


def _guess_dataset(record: dict[str, Any], dataset: str) -> str:
    if dataset != "auto":
        return dataset.lower()
    if "qa" in record or "pre_text" in record or "post_text" in record:
        return "finqa"
    if "questions" in record and ("paragraphs" in record or "table" in record):
        return "tatqa"
    if "doc_name" in record or "evidence" in record:
        return "financebench"
    return "generic_financial_qa"


def _tatqa_contexts(record: dict[str, Any]) -> list[str]:
    return _flatten_texts([record.get("paragraphs"), record.get("table")])


def _flatten_texts(values: Iterable[Any]) -> list[str]:
    texts: list[str] = []
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            if value.strip():
                texts.append(value.strip())
        elif isinstance(value, dict):
            joined = " ".join(str(item) for item in value.values() if item not in (None, ""))
            if joined.strip():
                texts.append(joined.strip())
        elif isinstance(value, list):
            texts.extend(_flatten_texts(value))
        else:
            text = str(value).strip()
            if text:
                texts.append(text)
    return texts


def _source_ids(record: dict[str, Any], *, default: str) -> list[str]:
    raw = record.get("source_ids") or record.get("doc_name") or record.get("filename") or record.get("source")
    if isinstance(raw, list):
        return [str(item) for item in raw]
    if raw:
        return [str(raw)]
    return [default]


def _answer_to_text(answer: Any) -> str:
    if answer is None:
        return ""
    if isinstance(answer, list):
        return " ".join(str(item) for item in answer)
    if isinstance(answer, dict):
        return " ".join(str(item) for item in answer.values() if item not in (None, ""))
    return str(answer)


def _normalize_answer(text: str) -> str:
    return re.sub(r"\s+", " ", str(text).strip().lower())


def _tokens(text: str) -> list[str]:
    normalized = _normalize_answer(text)
    if re.search(r"[\u4e00-\u9fff]", normalized):
        return [ch for ch in normalized if re.match(r"[\u4e00-\u9fffA-Za-z0-9.%+-]", ch)]
    return re.findall(r"[A-Za-z0-9.%+-]+", normalized)


def _token_f1(prediction: str, answer: str) -> float:
    pred_tokens = _tokens(prediction)
    answer_tokens = _tokens(answer)
    if not pred_tokens or not answer_tokens:
        return 0.0
    answer_counts: dict[str, int] = {}
    for token in answer_tokens:
        answer_counts[token] = answer_counts.get(token, 0) + 1
    overlap = 0
    for token in pred_tokens:
        if answer_counts.get(token, 0) > 0:
            overlap += 1
            answer_counts[token] -= 1
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred_tokens)
    recall = overlap / len(answer_tokens)
    return round(2 * precision * recall / (precision + recall), 4)


def _answer_in_context(answer: str, contexts: list[str]) -> bool:
    answer_norm = _normalize_answer(answer)
    if not answer_norm:
        return False
    context_norm = _normalize_answer("\n".join(contexts))
    if answer_norm in context_norm:
        return True
    if _answer_key_hit(context_norm, answer):
        return True
    answer_tokens = [token for token in _tokens(answer) if len(token) >= 2]
    if not answer_tokens:
        return False
    matched = sum(1 for token in answer_tokens[:8] if token in context_norm)
    return matched >= max(1, min(3, len(answer_tokens)))


def _answer_key_hit(prediction: str, answer: str) -> bool:
    pred_norm = _normalize_answer(prediction)
    answer_norm = _normalize_answer(answer)
    if not pred_norm or not answer_norm:
        return False
    if pred_norm == answer_norm or pred_norm in answer_norm or answer_norm in pred_norm:
        return True
    pred_yes_no = _yes_no_prefix(pred_norm)
    answer_yes_no = _yes_no_prefix(answer_norm)
    if pred_yes_no and pred_yes_no == answer_yes_no:
        return True
    pred_numbers = _numeric_values(pred_norm)
    answer_numbers = _numeric_values(answer_norm)
    for left in pred_numbers:
        for right in answer_numbers:
            tolerance = max(0.05, abs(right) * 0.01)
            if abs(left - right) <= tolerance:
                return True
    return False


def _yes_no_prefix(text: str) -> str:
    value = text.strip().lower()
    if value.startswith(("yes", "是")):
        return "yes"
    if value.startswith(("no", "否")):
        return "no"
    return ""


def _numeric_values(text: str) -> list[float]:
    values: list[float] = []
    for match in re.findall(r"[-+]?\$?\d[\d,]*(?:\.\d+)?%?", text):
        raw = match.replace("$", "").replace(",", "")
        is_percent = raw.endswith("%")
        raw = raw.rstrip("%")
        try:
            value = float(raw)
        except ValueError:
            continue
        values.append(value / 100 if is_percent else value)
    return values


def _citation_hit(sample: FinancialQASample, prediction: FinancialQAPrediction | None) -> float:
    if not prediction or not prediction.cited_source_ids:
        return 0.0
    expected = set(sample.source_ids)
    cited = set(prediction.cited_source_ids)
    if not expected:
        return 0.0
    return 1.0 if expected & cited else 0.0
