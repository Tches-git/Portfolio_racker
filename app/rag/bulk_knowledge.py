"""批量知识语料导入：公共 benchmark、A 股证券目录、缓存事件和行情序列。"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import CACHE_DIR, DATA_DIR, KNOWLEDGE_DOCS_DIR

BENCHMARK_DIR = DATA_DIR / "benchmarks"
DEFAULT_OUTPUT_DIR = KNOWLEDGE_DOCS_DIR / "bulk_corpus"
IMPORT_MANIFEST_PATH = DATA_DIR / "bulk_knowledge_import_manifest.json"


@dataclass(frozen=True)
class BulkKnowledgeImportResult:
    imported_count: int
    output_paths: list[Path]
    manifest_path: Path
    corpus_counts: dict[str, int]


def import_bulk_knowledge(
    *,
    include_universe: bool = True,
    include_benchmarks: bool = True,
    include_cache_items: bool = True,
    include_daily_bars: bool = True,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    cache_dir: Path = CACHE_DIR,
    benchmark_dir: Path = BENCHMARK_DIR,
    manifest_path: Path = IMPORT_MANIFEST_PATH,
) -> BulkKnowledgeImportResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    corpus_counts: dict[str, int] = {}

    if include_universe:
        paths, count = _write_stock_universe_corpus(cache_dir=cache_dir, output_dir=output_dir / "stock_universe")
        output_paths.extend(paths)
        corpus_counts["stock_universe"] = count

    if include_benchmarks:
        paths, counts = _write_benchmark_corpus(benchmark_dir=benchmark_dir, output_dir=output_dir / "benchmarks")
        output_paths.extend(paths)
        corpus_counts.update(counts)

    if include_cache_items:
        paths, count = _write_cache_item_corpus(cache_dir=cache_dir, output_dir=output_dir / "cache_items")
        output_paths.extend(paths)
        corpus_counts["cache_items"] = count

    if include_daily_bars:
        paths, count = _write_daily_bar_corpus(cache_dir=cache_dir, output_dir=output_dir / "daily_bars")
        output_paths.extend(paths)
        corpus_counts["daily_bars"] = count

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "output_dir": str(output_dir),
        "imported_count": len(output_paths),
        "corpus_counts": corpus_counts,
        "outputs": [str(path) for path in output_paths],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return BulkKnowledgeImportResult(
        imported_count=len(output_paths),
        output_paths=output_paths,
        manifest_path=manifest_path,
        corpus_counts=corpus_counts,
    )


def render_stock_universe_entry(item: dict[str, Any]) -> str:
    code = str(item.get("code") or "").zfill(6)
    name = str(item.get("name") or "").strip()
    aliases = str(item.get("aliases") or "").strip()
    exchange = _guess_exchange(code)
    market = _guess_market_board(code)
    alias_text = f"；别名/拼音线索：{aliases}" if aliases else ""
    return (
        f"证券主数据条目：股票代码 {code}，证券简称 {name}，交易场所 {exchange}，板块线索 {market}{alias_text}。"
        f"该条目用于 A 股 RAG 中的股票名称/代码消歧、组合创建、行情检索、公告归属、事件归并、研报生成和任务追踪。"
        f"常见检索词包括：{name}、{code}、{exchange}、{market}、A股、上市公司、证券简称、股票代码。"
        f"当用户只输入简称、代码或组合股票池时，可以用该条目把自然语言标的映射到标准六位代码。"
        f"使用边界：本条目只提供证券主数据和检索索引，不提供实时价格、财务结论或投资建议；实时行情和公告仍以工具接口及交易所披露为准。"
    )


def render_financebench_sample(sample: dict[str, Any]) -> str:
    evidence_parts = []
    for idx, evidence in enumerate(sample.get("evidence") or [], start=1):
        if not isinstance(evidence, dict):
            continue
        text = _clean_text(str(evidence.get("evidence_text") or ""))
        if text:
            evidence_parts.append(f"证据 {idx}：{text}")
    evidence_text = "\n\n".join(evidence_parts) or "暂无证据文本"
    return f"""# FinanceBench 样本：{sample.get('financebench_id') or sample.get('id') or 'unknown'}

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：{sample.get('company') or '未标注'}；文档：{sample.get('doc_name') or '未标注'}。
- 问题类型：{sample.get('question_type') or '未标注'}；推理类型：{sample.get('question_reasoning') or '未标注'}。
- 问题：{sample.get('question') or '未提供'}
- 标准答案：{sample.get('answer') or '未提供'}
- 答案依据：{sample.get('justification') or '未提供'}

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, {sample.get('company') or ''}, {sample.get('doc_name') or ''}, {sample.get('question_type') or ''}, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
{evidence_text}

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
"""


def _write_stock_universe_corpus(*, cache_dir: Path, output_dir: Path) -> tuple[list[Path], int]:
    payload = _read_json(cache_dir / "stock_a_code_name_directory.json")
    items = payload.get("items", []) if isinstance(payload, dict) else []
    items = [item for item in items if isinstance(item, dict) and item.get("code") and item.get("name")]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    batch_size = 200
    for batch_index in range(0, len(items), batch_size):
        batch = items[batch_index:batch_index + batch_size]
        lines = [
            "# A股证券主数据目录",
            "",
            "## 来源",
            "- 本地 A 股代码名称缓存：`data/cache/stock_a_code_name_directory.json`",
            "- 用途：股票名称/代码消歧、组合创建、行情检索和事件归属。",
            "",
            "## 使用边界",
            "- 本目录只提供证券主数据索引，不提供实时行情、财务结论或投资建议。",
            "- 股票简称、上市状态和板块信息可能变化，正式使用应结合最新交易所和行情接口。",
            "",
            "## 证券条目",
        ]
        lines.extend(render_stock_universe_entry(item) for item in batch)
        output_path = output_dir / f"a_share_directory_part_{batch_index // batch_size + 1:03d}.md"
        output_path.write_text("\n\n".join(lines), encoding="utf-8")
        output_paths.append(output_path)
    return output_paths, len(items)


def _write_benchmark_corpus(*, benchmark_dir: Path, output_dir: Path) -> tuple[list[Path], dict[str, int]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    counts: dict[str, int] = {}

    financebench_path = benchmark_dir / "public" / "financebench_open_source_full.jsonl"
    financebench_samples = _read_jsonl(financebench_path)
    counts["financebench"] = len(financebench_samples)
    for index in range(0, len(financebench_samples), 25):
        batch = financebench_samples[index:index + 25]
        text = "\n\n---\n\n".join(render_financebench_sample(sample) for sample in batch)
        output_path = output_dir / f"financebench_open_source_part_{index // 25 + 1:03d}.md"
        output_path.write_text(text, encoding="utf-8")
        output_paths.append(output_path)

    tracking_samples = _read_jsonl(benchmark_dir / "tracking_events_real.jsonl")
    counts["tracking_events_real"] = len(tracking_samples)
    if tracking_samples:
        output_path = output_dir / "tracking_events_real_corpus.md"
        output_path.write_text(_render_tracking_events(tracking_samples), encoding="utf-8")
        output_paths.append(output_path)

    agent_tasks = _read_jsonl(benchmark_dir / "agent_tasks.jsonl")
    counts["agent_tasks"] = len(agent_tasks)
    if agent_tasks:
        output_path = output_dir / "agent_tasks_corpus.md"
        output_path.write_text(_render_agent_tasks(agent_tasks), encoding="utf-8")
        output_paths.append(output_path)

    return output_paths, counts


def _write_cache_item_corpus(*, cache_dir: Path, output_dir: Path) -> tuple[list[Path], int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    source_files = []
    for pattern in (
        "announcement_cninfo_*.json",
        "filing_cninfo_*.json",
        "broker_reports_*.json",
        "research_eastmoney_*.json",
    ):
        source_files.extend(sorted(cache_dir.glob(pattern)))
    entries: list[str] = []
    seen: set[str] = set()
    for path in source_files:
        for item in _extract_items(path):
            key = f"{path.name}::{item.get('title') or item.get('summary')}::{item.get('time')}"
            if key in seen:
                continue
            seen.add(key)
            entries.append(_render_cache_item(path.name, item))
    output_paths: list[Path] = []
    for index in range(0, len(entries), 120):
        batch = entries[index:index + 120]
        output_path = output_dir / f"cache_items_part_{index // 120 + 1:03d}.md"
        output_path.write_text("\n\n---\n\n".join(batch), encoding="utf-8")
        output_paths.append(output_path)
    return output_paths, len(entries)


def _write_daily_bar_corpus(*, cache_dir: Path, output_dir: Path) -> tuple[list[Path], int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    count = 0
    for path in sorted(cache_dir.glob("daily_bars_*.json")):
        items = _extract_items(path)
        if not items:
            continue
        count += len(items)
        stock_code = _stock_code_from_filename(path.name)
        rows = [
            f"# 日线行情序列：{stock_code}",
            "",
            "## 来源",
            f"- 本地行情缓存：`data/cache/{path.name}`",
            "",
            "## 关键事实",
            f"- 股票代码：{stock_code}；样本数：{len(items)}。",
            "- 该条目用于 RAG 理解近期价格区间、涨跌幅、成交额和换手率，不替代实时行情接口。",
            "",
            "## 日线条目",
        ]
        for item in items:
            rows.append(
                "日线行情："
                f"{stock_code} 在 {item.get('date') or '未知日期'} 开盘 {_fmt(item.get('open'))}，最高 {_fmt(item.get('high'))}，"
                f"最低 {_fmt(item.get('low'))}，收盘 {_fmt(item.get('close'))}，涨跌幅 {_fmt(item.get('change_pct'))}%，"
                f"成交量 {_fmt(item.get('volume'))}，成交额 {_fmt(item.get('amount'))}，换手率 {_fmt(item.get('turnover'))}%。"
                "该条目适合用于事件回测、趋势解释、波动复核和行情上下文补充；正式研报应以最新行情接口复核。"
            )
        output_path = output_dir / f"{path.stem}.md"
        output_path.write_text("\n\n".join(rows), encoding="utf-8")
        output_paths.append(output_path)
    return output_paths, count


def _render_tracking_events(samples: list[dict[str, Any]]) -> str:
    rows = [
        "# 真实金融事件 benchmark 语料",
        "",
        "## 来源",
        "- 本地真实事件样本：`data/benchmarks/tracking_events_real.jsonl`",
        "- 用途：事件分类、影响等级、预警命中和去重评测。",
        "",
        "## 使用边界",
        "- 样本来自公开公告/新闻元数据和启发式标注，部分条目仍需人工复核。",
        "",
        "## 事件条目",
    ]
    for sample in samples:
        raw = sample.get("raw") or {}
        rows.append(
            "真实事件样本："
            f"股票 {raw.get('stock_name') or raw.get('stock_code') or '未标注'}，标题《{raw.get('title') or '未命名事件'}》，"
            f"摘要：{raw.get('summary') or '暂无摘要'}。来源 {raw.get('source') or raw.get('provider') or '公开来源'}，"
            f"时间 {raw.get('time') or '未记录'}，链接 {raw.get('link') or '无'}。"
            f"标注事件类型 {sample.get('expected_event_type')}，影响等级 {sample.get('expected_impact_level')}，"
            f"是否应触发预警 {sample.get('should_alert')}，去重组 {sample.get('duplicate_group')}。"
            "该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。"
        )
    return "\n\n".join(rows)


def _render_agent_tasks(samples: list[dict[str, Any]]) -> str:
    rows = [
        "# 金融 Agent 任务评测语料",
        "",
        "## 来源",
        "- 本地 Agent 任务集：`data/benchmarks/agent_tasks.jsonl`",
        "- 用途：多 Agent 工具覆盖、Trace 完整性、异常降级和引用要求评测。",
        "",
        "## 任务条目",
    ]
    for sample in samples:
        rows.append(
            "Agent 任务样本："
            f"任务 ID {sample.get('task_id')}，任务类型 {sample.get('task_type')}，难度 {sample.get('difficulty')}。"
            f"任务描述：{sample.get('prompt')}。"
            f"期望工具：{', '.join(sample.get('expected_tools') or [])}。"
            f"期望输出：{', '.join(sample.get('expected_outputs') or [])}。"
            f"是否要求引用：{sample.get('requires_citation')}；是否要求降级：{sample.get('requires_fallback')}。"
            "该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。"
        )
    return "\n\n".join(rows)


def _render_cache_item(source_file: str, item: dict[str, Any]) -> str:
    stock_code = str(item.get("stock_code") or _stock_code_from_filename(source_file) or "").strip()
    title = str(item.get("title") or item.get("summary") or "未命名事项").strip()
    source = str(item.get("source") or item.get("provider") or "公开来源").strip()
    channel = str(item.get("channel") or _channel_from_filename(source_file)).strip()
    link = str(item.get("link") or item.get("url") or "").strip()
    return f"""# 公开缓存条目：{stock_code} {title}

## 来源
- 本地缓存文件：`data/cache/{source_file}`
- 原始来源：{source}
- 链接：{link or '无'}

## 关键事实
- 股票代码：{stock_code or '未标注'}；渠道：{channel}；时间：{item.get('time') or item.get('published_at') or '未记录'}。
- 标题：{title}
- 摘要：{item.get('summary') or title}
- 证据类型：{item.get('evidence_type') or '未标注'}；检索模式：{item.get('retrieval_mode') or 'cache'}。

## 投研关注点
- 该条目可用于识别公告、研报观点或披露文件中的研究主题、事件触发原因和市场关注焦点。
- 对同一股票的多条条目应结合时间顺序、来源类型和事件影响等级综合判断。

## RAG 检索关键词
{stock_code}, {title}, {source}, {channel}, 公告, 研报观点, 事件, 风险, 预警

## 使用边界
- 本条目是缓存摘要，不包含完整公告或完整研报正文；正式引用应回到原始公告、交易所披露或公开来源链接。
"""


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            rows.append(payload)
    return rows


def _extract_items(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return [item for item in payload["items"] if isinstance(item, dict)]
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def _guess_exchange(code: str) -> str:
    if code.startswith(("600", "601", "603", "605", "688", "689", "900")):
        return "上海证券交易所"
    if code.startswith(("000", "001", "002", "003", "300", "301", "200")):
        return "深圳证券交易所"
    if code.startswith(("8", "9")):
        return "北京证券交易所"
    return "A股市场"


def _guess_market_board(code: str) -> str:
    if code.startswith("688"):
        return "科创板"
    if code.startswith(("300", "301")):
        return "创业板"
    if code.startswith(("8", "9")):
        return "北交所"
    if code.startswith(("002", "003")):
        return "深市中小板/主板"
    if code.startswith(("600", "601", "603", "605")):
        return "沪市主板"
    return "A股"


def _stock_code_from_filename(filename: str) -> str:
    match = re.search(r"(\d{6})", filename)
    return match.group(1) if match else ""


def _channel_from_filename(filename: str) -> str:
    if "announcement" in filename:
        return "announcement"
    if "filing" in filename:
        return "filing"
    if "broker" in filename or "research" in filename:
        return "broker_report"
    return "cache"


def _clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _fmt(value: Any) -> str:
    if value in (None, ""):
        return "--"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)
