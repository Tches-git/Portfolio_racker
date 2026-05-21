"""公共金融 QA benchmark 的轻量预测器。"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR
from app.evals.financial_qa_eval import FinancialQASample, load_financial_qa_benchmark
from app.llm import chat


def run_financial_qa_predictions(
    *,
    benchmark_path: Path,
    output_path: Path | None = None,
    dataset: str = "auto",
    limit: int = 5,
    max_context_chars: int = 6000,
) -> dict[str, object]:
    samples = load_financial_qa_benchmark(benchmark_path, dataset=dataset, limit=max(1, limit))
    out_path = output_path or OUTPUT_DIR / "evals" / f"finance_qa_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    predictions: list[dict[str, object]] = []
    for sample in samples:
        answer = predict_financial_answer(sample, max_context_chars=max_context_chars)
        predictions.append({
            "sample_id": sample.sample_id,
            "prediction": answer,
            "cited_source_ids": sample.source_ids[:1],
        })
    out_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in predictions) + ("\n" if predictions else ""), encoding="utf-8")
    return {
        "prediction_count": len(predictions),
        "output_path": str(out_path),
        "benchmark_path": str(benchmark_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def predict_financial_answer(sample: FinancialQASample, *, max_context_chars: int = 6000) -> str:
    context = "\n\n".join(sample.contexts)[:max_context_chars]
    prompt = (
        "You are answering a financial benchmark question. "
        "Use only the provided evidence. Return the shortest exact answer; "
        "do not include reasoning or extra prose.\n\n"
        f"Question:\n{sample.question}\n\n"
        f"Evidence:\n{context}\n\n"
        "Answer:"
    )
    return chat(
        prompt,
        system="You are a precise financial QA assistant. Answer only with the final value or phrase.",
        temperature=0,
        max_tokens=64,
    ).strip()
