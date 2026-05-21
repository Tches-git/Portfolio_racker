"""真实金融事件 benchmark 构建工具。

从公开公告、新闻、研报观点等来源的结构化缓存或实时采集结果中生成 JSONL
评测样本。这里不把“扩展样本”伪装成真实事件，只输出实际采集到的来源元数据，
后续可人工复核标签后作为 tracking-eval 的输入。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
from pathlib import Path
from typing import Iterable

from app.config import CACHE_DIR, PROJECT_ROOT

DEFAULT_REAL_TRACKING_BENCHMARK_PATH = PROJECT_ROOT / "data" / "benchmarks" / "tracking_events_real.jsonl"


@dataclass
class RealTrackingBuildResult:
    output_path: Path
    sample_count: int
    stock_codes: list[str]
    source_files: list[str]
    generated_at: str


def build_real_tracking_benchmark(
    *,
    output_path: Path = DEFAULT_REAL_TRACKING_BENCHMARK_PATH,
    stock_codes: list[str] | None = None,
    target_count: int = 150,
    include_live: bool = False,
    cache_dir: Path = CACHE_DIR,
) -> RealTrackingBuildResult:
    codes = [str(code).strip() for code in (stock_codes or []) if str(code).strip()]
    cache_items, source_files = load_cached_source_items(cache_dir=cache_dir, stock_codes=codes)
    live_items: list[tuple[str, dict]] = []
    if include_live:
        live_items = collect_live_source_items(codes or _stock_codes_from_cached_items(cache_items), limit=12)

    samples = samples_from_source_items([*cache_items, *live_items])
    if target_count > 0:
        samples = samples[:target_count]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(json.dumps(sample, ensure_ascii=False) for sample in samples) + ("\n" if samples else ""), encoding="utf-8")
    return RealTrackingBuildResult(
        output_path=output_path,
        sample_count=len(samples),
        stock_codes=sorted({str(sample.get("raw", {}).get("stock_code", "")) for sample in samples if sample.get("raw", {}).get("stock_code")}),
        source_files=source_files,
        generated_at=datetime.now().isoformat(timespec="seconds"),
    )


def load_cached_source_items(*, cache_dir: Path = CACHE_DIR, stock_codes: list[str] | None = None) -> tuple[list[tuple[str, dict]], list[str]]:
    code_filter = {str(code) for code in (stock_codes or []) if str(code)}
    items: list[tuple[str, dict]] = []
    source_files: list[str] = []
    if not cache_dir.exists():
        return items, source_files
    for path in sorted(cache_dir.glob("*.json")):
        stock_code = _infer_stock_code(path.name)
        if code_filter and stock_code not in code_filter:
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        records = payload.get("items") if isinstance(payload, dict) else payload
        if isinstance(records, dict):
            records = [records]
        if not isinstance(records, list):
            continue
        used = False
        for record in records:
            if not isinstance(record, dict):
                continue
            item = dict(record)
            item.setdefault("stock_code", stock_code)
            if _is_usable_source_item(item):
                items.append((stock_code, item))
                used = True
        if used:
            source_files.append(str(path))
    return items, source_files


def collect_live_source_items(stock_codes: list[str], *, limit: int = 8) -> list[tuple[str, dict]]:
    """按需实时采集公开来源。测试不依赖该函数，避免网络成为回归前提。"""
    from app.data_source.live_tools import fetch_announcements, fetch_broker_reports, fetch_exchange_filings
    from app.data_source.akshare_client import get_recent_news, get_stock_profile

    items: list[tuple[str, dict]] = []
    for code in stock_codes:
        try:
            profile = get_stock_profile(code)
            stock_name = profile.name
        except Exception:
            stock_name = code
        fetchers = (
            lambda: fetch_announcements(code, stock_name=stock_name, limit=limit),
            lambda: fetch_exchange_filings(code, stock_name=stock_name, limit=limit),
            lambda: fetch_broker_reports(code, stock_name=stock_name, limit=limit),
            lambda: get_recent_news(stock_name)[:limit] if stock_name else [],
        )
        for fetcher in fetchers:
            try:
                for item in fetcher() or []:
                    if isinstance(item, dict) and _is_usable_source_item(item):
                        payload = dict(item)
                        payload.setdefault("stock_code", code)
                        payload.setdefault("stock_name", stock_name)
                        items.append((code, payload))
            except Exception:
                continue
    return items


def samples_from_source_items(items: Iterable[tuple[str, dict]]) -> list[dict]:
    samples: list[dict] = []
    seen: set[str] = set()
    for stock_code, item in items:
        if not _is_usable_source_item(item):
            continue
        raw = _raw_event_payload(stock_code, item)
        identity = raw.get("link") or f"{raw.get('stock_code')}:{_normalize_title(raw.get('title', ''))}"
        if identity in seen:
            continue
        seen.add(identity)
        event_type = infer_event_type(raw)
        impact_level = infer_impact_level(raw, event_type=event_type)
        sample = {
            "raw": raw,
            "expected_event_type": event_type,
            "expected_impact_level": impact_level,
            "duplicate_group": _duplicate_group(raw, event_type=event_type),
            "should_alert": impact_level in {"high", "medium"} and not bool(item.get("is_placeholder")),
            "label_source": "heuristic_from_public_metadata",
            "needs_human_review": True,
        }
        samples.append(sample)
    return samples


def infer_event_type(raw: dict) -> str:
    title = f"{raw.get('title', '')} {raw.get('summary', '')}"
    channel = str(raw.get("channel") or "")
    evidence_type = str(raw.get("evidence_type") or "")
    if "broker" in channel or "研报" in title or "评级" in title or "目标价" in title:
        return "broker_view"
    if re.search(r"问询|监管|处罚|立案|调查|警示函", title):
        return "regulation"
    if "filing" in channel or "年报" in title or "季报" in title or "报告" in title:
        if _is_low_impact_disclosure(title):
            return "announcement"
        return "earnings"
    if "announcement" in channel or "公告" in title or "披露" in title:
        if re.search(r"问询|监管|处罚|立案|警示函", title):
            return "regulation"
        if re.search(r"回购|增持|减持|分红|权益分派", title):
            return "shareholder"
        return "announcement"
    if re.search(r"政策|补贴|行业|规划|办法|意见", title):
        return "industry_policy"
    if re.search(r"涨停|跌停|大涨|大跌|异动|成交|放量", title):
        return "market_move"
    if re.search(r"风险|违约|亏损|下滑|诉讼|舆情", title):
        return "risk_sentiment"
    if re.search(r"订单|产能|交付|中标|合同", title):
        return "capacity_order"
    if re.search(r"提价|降价|价格|产品", title):
        return "product_price"
    if evidence_type:
        return evidence_type
    return "news"


def infer_impact_level(raw: dict, *, event_type: str) -> str:
    text = f"{raw.get('title', '')} {raw.get('summary', '')}"
    if _is_low_impact_disclosure(text):
        return "low"
    if event_type in {"regulation", "risk_sentiment"}:
        return "high"
    if re.search(r"重大|净利润|业绩|亏损|违约|立案|处罚|回购股份|主要经营数据", text):
        return "high"
    if event_type in {"earnings", "industry_policy", "market_move", "broker_view", "announcement", "shareholder"}:
        return "medium"
    if re.search(r"增长|下降|增持|减持|分红|订单|中标|价格", text):
        return "medium"
    return "low"


def _raw_event_payload(stock_code: str, item: dict) -> dict:
    title = str(item.get("title") or item.get("name") or "").strip()
    summary = str(item.get("summary") or title).strip()
    return {
        "id": str(item.get("id") or _short_hash(f"{stock_code}:{title}:{item.get('time', '')}:{item.get('link', '')}")),
        "stock_code": str(item.get("stock_code") or stock_code),
        "stock_name": str(item.get("stock_name") or ""),
        "title": title,
        "summary": summary[:240],
        "source": str(item.get("source") or item.get("provider") or ""),
        "provider": str(item.get("provider") or item.get("source") or ""),
        "channel": str(item.get("channel") or ""),
        "time": str(item.get("time") or item.get("date") or ""),
        "link": str(item.get("link") or item.get("url") or ""),
        "evidence_type": str(item.get("evidence_type") or ""),
    }


def _is_usable_source_item(item: dict) -> bool:
    if item.get("is_placeholder"):
        return False
    title = str(item.get("title") or item.get("name") or "").strip()
    return len(title) >= 6


def _duplicate_group(raw: dict, *, event_type: str) -> str:
    return _short_hash(
        f"{raw.get('stock_code')}:{str(raw.get('time', ''))[:10]}:{event_type}:{_canonical_event_title(str(raw.get('title', '')))}"
    )


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", "", str(title).lower())


def _canonical_event_title(title: str) -> str:
    text = _normalize_title(title)
    text = re.sub(r"^[\u4e00-\u9fa5A-Za-z0-9]+关于", "关于", text)
    text = re.sub(r"（英文版|英文|摘要|全文|修订版|更新后）", "", text)
    text = re.sub(r"(202[0-9]年)?(年度|第一季度|半年度|第三季度)", "", text)
    text = re.sub(r"[：:，,。.（）()《》\\-—_\\s]", "", text)
    return text[:40]


def _is_low_impact_disclosure(text: str) -> bool:
    return bool(re.search(
        r"独立董事述职|董事会审计委员会|会议决议|股东大会|公司章程|制度|ESG|环境、社会及治理|社会责任|英文版|摘要|法律意见书|募集说明书|上市保荐|内部控制|审计报告|财务报表附注",
        text,
        flags=re.IGNORECASE,
    ))


def _short_hash(value: str) -> str:
    return md5(value.encode("utf-8")).hexdigest()[:16]


def _infer_stock_code(filename: str) -> str:
    match = re.search(r"(\d{6})", filename)
    return match.group(1) if match else ""


def _stock_codes_from_cached_items(items: list[tuple[str, dict]]) -> list[str]:
    return sorted({code for code, _item in items if code})
