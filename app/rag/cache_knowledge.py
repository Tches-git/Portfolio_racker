"""将本地公开数据缓存整理成 RAG 知识文档。"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import CACHE_DIR, DATA_DIR, KNOWLEDGE_DOCS_DIR

DEFAULT_OUTPUT_DIR = KNOWLEDGE_DOCS_DIR / "stock_cache"
IMPORT_MANIFEST_PATH = DATA_DIR / "knowledge_cache_import_manifest.json"


@dataclass(frozen=True)
class StockCacheKnowledgeResult:
    imported_count: int
    output_paths: list[Path]
    stock_codes: list[str]
    manifest_path: Path


def import_stock_cache_knowledge(
    *,
    stock_codes: list[str] | None = None,
    limit: int = 0,
    cache_dir: Path = CACHE_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    manifest_path: Path = IMPORT_MANIFEST_PATH,
) -> StockCacheKnowledgeResult:
    codes = _select_stock_codes(stock_codes=stock_codes, limit=limit, cache_dir=cache_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for code in codes:
        payload = build_stock_cache_payload(code, cache_dir=cache_dir)
        if not payload:
            continue
        markdown = render_stock_cache_markdown(payload)
        output_path = output_dir / f"{code}_{_slugify(payload['name'])}.md"
        output_path.write_text(markdown, encoding="utf-8")
        output_paths.append(output_path)

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cache_dir": str(cache_dir),
        "output_dir": str(output_dir),
        "stock_codes": codes,
        "imported_count": len(output_paths),
        "outputs": [str(path) for path in output_paths],
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return StockCacheKnowledgeResult(
        imported_count=len(output_paths),
        output_paths=output_paths,
        stock_codes=codes,
        manifest_path=manifest_path,
    )


def build_stock_cache_payload(code: str, *, cache_dir: Path = CACHE_DIR) -> dict[str, Any] | None:
    profile = _read_json(cache_dir / f"profile_{code}.json")
    if not isinstance(profile, dict):
        return None
    name = str(profile.get("name") or code).strip()
    industry = str(profile.get("industry") or "未分类").strip()
    return {
        "code": code,
        "name": name,
        "industry": industry,
        "profile": profile,
        "quote": _read_json(cache_dir / f"live_quote_{code}.json") or {},
        "announcements": _read_items(cache_dir, [
            f"announcement_cninfo_{code}_12.json",
            f"announcement_cninfo_{code}_5.json",
            f"announcement_{code}_5.json",
        ]),
        "broker_views": _read_items(cache_dir, [
            f"broker_reports_{code}_12.json",
            f"broker_reports_{code}_5.json",
            f"research_eastmoney_{code}_12.json",
            f"research_eastmoney_{code}_5.json",
        ]),
        "metrics": _read_json(cache_dir / f"metrics_ths_{code}.json") or {},
        "industry_keywords": _industry_keywords(industry, name),
        "analysis_focus": _industry_focus(industry),
    }


def render_stock_cache_markdown(payload: dict[str, Any]) -> str:
    code = str(payload["code"])
    name = str(payload["name"])
    industry = str(payload["industry"])
    profile = payload.get("profile") or {}
    quote = payload.get("quote") or {}
    announcements = _dedupe_items(payload.get("announcements") or [])[:12]
    broker_views = _dedupe_items(payload.get("broker_views") or [])[:12]
    keywords = ", ".join(dict.fromkeys([name, code, industry, *payload.get("industry_keywords", [])]))
    announcement_lines = _format_item_lines(announcements, fallback="暂无公告缓存")
    broker_lines = _format_item_lines(broker_views, fallback="暂无券商观点缓存")
    focus_lines = "\n".join(f"- {item}" for item in payload.get("analysis_focus", []))
    market_prefix = "sh" if code.startswith("6") else "sz"
    cache_time = _format_ts(profile.get("_ts") or quote.get("_ts"))

    return f"""# A股公司知识快照：{name}（{code}）

## 来源
- 本地公开数据缓存：`data/cache/profile_{code}.json`
- 公告缓存：`data/cache/announcement_cninfo_{code}_*.json`
- 研报观点标题缓存：`data/cache/broker_reports_{code}_*.json`、`data/cache/research_eastmoney_{code}_*.json`
- 巨潮资讯公告检索：https://www.cninfo.com.cn/new/disclosure/stock?stockCode={code}
- 东方财富行情入口：https://quote.eastmoney.com/{market_prefix}{code}.html

## 关键事实
- 公司名称：{name}；股票代码：{code}；行业标签：{industry}。
- 当前缓存画像显示：市值约 {_fmt(profile.get("market_cap"))} 亿元，PE {_fmt(profile.get("pe_ratio"))}，PB {_fmt(profile.get("pb_ratio"))}，股本 {_fmt(profile.get("total_shares"))} 亿股。
- 行情快照显示：价格 {_fmt(quote.get("price") or profile.get("current_price"))}，行情来源 `{quote.get("provider") or "akshare/cache"}`，更新时间 {quote.get("time") or cache_time or "未记录"}。
- 该知识条目来自项目已采集缓存，适合让 RAG 在研报生成前快速获得公司、行业、公告和观点标题背景。

## 近期公告/事件证据
{announcement_lines}

## 近期券商观点标题
{broker_lines}

## 投研关注点
{focus_lines}
- 对 {name} 的研报生成应优先交叉验证最新公告、行情变化、财务指标和事件上下文，避免只依据单一缓存标题下结论。

## RAG 检索关键词
{keywords}

## 使用边界
- 本条目是对公开缓存的摘要索引，不包含完整公告或完整研报正文，不替代原始披露文件。
- 券商观点部分只保存标题、机构和日期，用于识别市场关注主题，不代表项目或作者观点。
- 市值、PE、PB、价格等缓存字段可能过期，正式研报必须结合实时行情和最新公告复核。
- 如需引用事实，应优先使用公告链接、交易所披露、公司年报或当前工具返回的结构化数据。
"""


def _select_stock_codes(*, stock_codes: list[str] | None, limit: int, cache_dir: Path) -> list[str]:
    if stock_codes:
        codes = [_normalize_code(code) for code in stock_codes if _normalize_code(code)]
    else:
        codes = sorted(path.stem.removeprefix("profile_") for path in cache_dir.glob("profile_*.json"))
    if limit > 0:
        return codes[:limit]
    return codes


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_items(cache_dir: Path, filenames: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for filename in filenames:
        payload = _read_json(cache_dir / filename)
        if isinstance(payload, dict) and isinstance(payload.get("items"), list):
            items.extend(item for item in payload["items"] if isinstance(item, dict))
        elif isinstance(payload, list):
            items.extend(item for item in payload if isinstance(item, dict))
    return items


def _format_item_lines(items: list[dict[str, Any]], *, fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    lines = []
    for item in items:
        title = str(item.get("title") or item.get("summary") or "未命名事项").strip()
        time = str(item.get("time") or item.get("published_at") or "时间未记录").strip()
        source = str(item.get("source") or item.get("provider") or "公开来源").strip()
        link = str(item.get("link") or item.get("url") or "").strip()
        suffix = f"；链接：{link}" if link else ""
        lines.append(f"- {time}｜{source}｜{title}{suffix}")
    return "\n".join(lines)


def _dedupe_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for item in items:
        key = f"{item.get('title') or item.get('summary')}::{item.get('time')}"
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _industry_focus(industry: str) -> list[str]:
    text = industry.lower()
    if "银行" in industry:
        return ["净息差、资产质量、不良生成、拨备覆盖、资本充足率和财富管理收入是银行股的核心变量。", "需要区分规模扩张、息差修复和信用成本下降对利润的不同贡献。"]
    if "保险" in industry or "证券" in industry:
        return ["金融机构分析应关注投资收益、负债成本、权益市场波动、偿付能力和监管资本约束。", "保险公司还需要拆分新业务价值、代理人队伍、综合成本率和资产负债匹配。"]
    if "房地产" in industry or "地产" in industry:
        return ["地产公司应关注销售回款、拿地强度、融资成本、债务到期、存货减值和交付风险。", "行业政策、城市能级和资产负债表修复决定风险判断的边界。"]
    if "电池" in industry or "汽车" in industry:
        return ["新能源链条应重点跟踪销量、价格战、产能利用率、单车盈利、电池材料价格和海外政策。", "需要把收入增长拆分为量、价、结构和海外贡献，避免只看销量。"]
    if "白酒" in industry or "饮料" in industry or "食品" in industry:
        return ["消费品分析应关注品牌力、渠道库存、批价、费用投放、现金回款和消费场景。", "白酒等高毛利业务需要额外复核渠道利润和合同负债。"]
    if "医药" in industry:
        return ["医药公司应关注研发管线、集采降价、医保谈判、专利悬崖、销售费用和合规风险。", "创新药与仿制药、器械、CXO 等子行业的估值锚不同。"]
    if "半导体" in industry or "电子" in industry or "计算机" in industry or "通信" in industry or "安全" in industry:
        return ["科技公司应关注订单景气、产品迭代、研发强度、客户集中度、库存周期和国产替代节奏。", "网络安全和软件类公司还应复核项目验收、回款、应收账款和递延收入。"]
    if "电力" in industry or "能源" in industry or "煤" in industry or "有色" in industry or "矿" in industry:
        return ["周期和能源企业应关注商品价格、产量、成本曲线、资本开支、长协比例和分红能力。", "需要区分价格弹性和资源禀赋带来的盈利稳定性。"]
    return ["研报应先确认商业模式、行业景气、竞争格局、财务质量、估值锚和风险事件。", "重点复核收入增长是否能转化为现金流和股东回报。"]


def _industry_keywords(industry: str, name: str) -> list[str]:
    keywords = [industry, "公告", "行情", "研报观点", "财务质量", "风险事件", "估值"]
    focus_text = " ".join(_industry_focus(industry))
    keywords.extend(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]{2,}", focus_text))
    if name:
        keywords.append(name)
    return keywords[:32]


def _fmt(value: Any) -> str:
    if value in (None, ""):
        return "--"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def _format_ts(value: Any) -> str:
    if not value:
        return ""
    try:
        return datetime.fromtimestamp(float(value)).isoformat(timespec="seconds")
    except Exception:
        return str(value)


def _normalize_code(code: str) -> str:
    value = re.sub(r"\D", "", str(code or ""))
    return value.zfill(6) if value else ""


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff_-]+", "-", value)
    return value.strip("-") or "stock"
