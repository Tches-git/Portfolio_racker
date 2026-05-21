"""RAG 引用可信度评测。"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from app.config import OUTPUT_DIR, PROJECT_ROOT


def evaluate_rag_citations(report: str, source_refs: list[dict] | None = None, *, stock_code: str = "") -> dict[str, object]:
    refs = [item for item in (source_refs or []) if isinstance(item, dict)]
    claims = _extract_claims(report)
    supported = [claim for claim in claims if _claim_has_support(claim, refs)]
    unsupported = [claim for claim in claims if claim not in supported]
    source_reference_count = len(refs)
    citation_coverage_rate = len(supported) / len(claims) if claims else (1.0 if refs else 0.0)
    retrieval_topk_hit_rate = _retrieval_hit_rate(refs)
    rerank_selected_count = sum(1 for ref in refs if ref.get("rerank_score") not in (None, ""))
    return {
        "stock_code": stock_code,
        "claim_count": len(claims),
        "supported_claim_count": len(supported),
        "unsupported_claim_count": len(unsupported),
        "citation_coverage_rate": round(citation_coverage_rate, 4),
        "source_reference_count": source_reference_count,
        "retrieval_topk_hit_rate": round(retrieval_topk_hit_rate, 4),
        "rerank_selected_count": rerank_selected_count,
        "unsupported_claims": unsupported[:20],
    }


def run_rag_eval(*, stock_code: str, output_dir: Path | None = None) -> dict[str, object]:
    out_dir = output_dir or OUTPUT_DIR / "evals"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = _find_latest_report(stock_code)
    source_refs = _find_source_refs(stock_code, report_path)
    report = report_path.read_text(encoding="utf-8") if report_path else ""
    result = evaluate_rag_citations(report, source_refs, stock_code=stock_code)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    json_path = out_dir / f"rag_eval_{stock_code}_{timestamp}.json"
    md_path = out_dir / f"rag_eval_{stock_code}_{timestamp}.md"
    result = {
        **result,
        "report_path": str(report_path or ""),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "json_path": str(json_path),
        "markdown_path": str(md_path),
    }
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(format_rag_eval_markdown(result), encoding="utf-8")
    return result


def format_rag_eval_markdown(result: dict[str, object]) -> str:
    return "\n".join([
        f"# RAG 引用可信度评测 — {result.get('stock_code', '')}",
        "",
        f"- 报告路径：{result.get('report_path', '') or '未找到'}",
        f"- 核心观点数：**{result.get('claim_count', 0)}**",
        f"- 来源引用数：**{result.get('source_reference_count', 0)}**",
        f"- 引用覆盖率：**{float(result.get('citation_coverage_rate', 0)):.1%}**",
        f"- 无来源观点数：**{result.get('unsupported_claim_count', 0)}**",
        f"- 检索 Top-K 命中率：**{float(result.get('retrieval_topk_hit_rate', 0)):.1%}**",
        f"- Rerank 选中数：**{result.get('rerank_selected_count', 0)}**",
        "",
        "## 简历口径",
        "对研报核心观点进行来源绑定和引用覆盖率统计，用于说明 RAG 生成链路的可追溯性。",
    ]) + "\n"


def _extract_claims(report: str) -> list[str]:
    lines = []
    for raw in report.splitlines():
        line = raw.strip().lstrip("-*0123456789.、 ")
        if len(line) < 16:
            continue
        if line.startswith("#") or line.startswith("|"):
            continue
        if any(keyword in line for keyword in ("预计", "增长", "下降", "风险", "估值", "评级", "收入", "利润", "现金流", "ROE", "毛利率", "%", "亿元", "倍")):
            lines.append(line[:220])
    return lines


def _claim_has_support(claim: str, refs: list[dict]) -> bool:
    if re.search(r"\[\d+\]|来源|据|公告|年报|研报|披露", claim):
        return True
    tokens = [token for token in re.split(r"[，。；：:、\s]+", claim) if len(token) >= 3]
    if not tokens or not refs:
        return False
    ref_text = "\n".join(f"{ref.get('title', '')} {ref.get('summary', '')} {ref.get('source', '')}" for ref in refs)
    matched = sum(1 for token in tokens[:8] if token in ref_text)
    return matched >= 2


def _retrieval_hit_rate(refs: list[dict]) -> float:
    if not refs:
        return 0.0
    hits = sum(1 for ref in refs if ref.get("title") and (ref.get("source") or ref.get("provider")))
    return hits / len(refs)


def _find_latest_report(stock_code: str) -> Path | None:
    candidates = _artifact_candidates(f"report_{stock_code}_*.md")
    return candidates[0] if candidates else None


def _find_source_refs(stock_code: str, report_path: Path | None) -> list[dict]:
    source_candidates = _artifact_candidates(f"sources_{stock_code}_*.json")
    if report_path:
        report_suffix = report_path.stem.replace(f"report_{stock_code}_", "")
        matched = [item for item in source_candidates if report_suffix in item.stem]
        source_candidates = matched or source_candidates
    if not source_candidates:
        return []
    try:
        payload = json.loads(source_candidates[0].read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "source_refs", "sources"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _artifact_candidates(pattern: str) -> list[Path]:
    seen: set[Path] = set()
    candidates: list[Path] = []
    for root in (OUTPUT_DIR, PROJECT_ROOT):
        for item in root.glob(f"**/{pattern}"):
            if item in seen or not item.is_file():
                continue
            seen.add(item)
            candidates.append(item)
    return sorted(candidates, key=lambda item: item.stat().st_mtime, reverse=True)
