"""在线工具层：公告 / 行情 / 券商研报 / 文件归档。"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from hashlib import md5

from app.config import CACHE_TTL_DEFAULT
from app.data_source.akshare_client import _read_cache, _write_cache, get_recent_news, get_stock_profile

logger = logging.getLogger("fin.live_tools")


def fetch_live_quotes(stock_code: str) -> dict:
    cache_key = f"live_quote_{stock_code}"
    cached = _read_cache(cache_key, max_age=300)
    if cached:
        return dict(cached)
    profile = get_stock_profile(stock_code)
    payload = {
        "title": f"{profile.name} 实时行情快照",
        "time": datetime.now().isoformat(),
        "source": "akshare_profile",
        "provider": "akshare",
        "channel": "live_quote",
        "retrieval_mode": "api",
        "evidence_type": "quote",
        "is_placeholder": False,
        "link": "",
        "price": profile.current_price,
        "pe_ratio": profile.pe_ratio,
        "pb_ratio": profile.pb_ratio,
        "market_cap": profile.market_cap,
        "stock_code": stock_code,
    }
    _write_cache(cache_key, payload)
    return payload


def fetch_announcements(stock_code: str, stock_name: str = "", limit: int = 5) -> list[dict[str, str]]:
    items = _fetch_cninfo_announcements(stock_code=stock_code, limit=limit)
    if not items:
        items = _build_news_backed_items(stock_code=stock_code, stock_name=stock_name, limit=limit, channel="announcement", source="news_fallback")
    return [
        _normalize_source_item(item, channel="announcement", stock_code=stock_code)
        for item in items[:limit]
    ]


def fetch_exchange_filings(stock_code: str, stock_name: str = "", limit: int = 5) -> list[dict[str, str]]:
    items = _fetch_cninfo_filings(stock_code=stock_code, limit=limit)
    if not items:
        items = _build_news_backed_items(stock_code=stock_code, stock_name=stock_name, limit=limit, channel="filing", source="news_fallback")
    return [
        _normalize_source_item(item, channel="filing", stock_code=stock_code)
        for item in items[:limit]
    ]


def fetch_broker_reports(stock_code: str, stock_name: str = "", limit: int = 5) -> list[dict[str, str]]:
    cache_key = f"broker_reports_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    profile = get_stock_profile(stock_code)
    company = stock_name or profile.name or stock_code
    items = [
        _normalize_source_item(item, channel="broker_report", stock_code=stock_code)
        for item in _fetch_eastmoney_research_reports(stock_code=stock_code, limit=limit)
    ]
    if not items:
        items = [
            _normalize_source_item(item, channel="broker_report", stock_code=stock_code)
            for item in _build_news_backed_items(
                stock_code=stock_code,
                stock_name=company,
                limit=limit,
                channel="broker_report",
                source="broker_report_fallback",
            )[:limit]
        ]
    if not items:
        items = [
            _normalize_source_item(
                {
                    "title": f"{company} 券商观点汇总（占位）",
                    "time": datetime.now().isoformat(),
                    "source": "internal_placeholder",
                    "provider": "internal",
                    "channel": "broker_report",
                    "retrieval_mode": "placeholder",
                    "link": "",
                    "summary": f"当前仓库尚未接入外部券商研报 API，已保留 {company} 的在线工具接口与来源占位。",
                    "is_placeholder": True,
                },
                channel="broker_report",
                stock_code=stock_code,
            )
        ]
    _write_cache(cache_key, {"items": items})
    return items[:limit]


def extract_document_tables(document) -> list[dict]:
    return list(getattr(document, "tables", []) or [])


def _fetch_eastmoney_research_reports(*, stock_code: str, limit: int) -> list[dict[str, str]]:
    cache_key = f"research_eastmoney_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    try:
        import akshare as ak

        df = ak.stock_research_report_em(symbol=stock_code)
        if df is None or getattr(df, "empty", True):
            return []
        items: list[dict[str, str]] = []
        for _, row in df.head(limit).iterrows():
            title = _pick_first_value(row, ["报告名称", "报告标题", "标题", "研究报告名称", "title"])
            if not title:
                continue
            org = _pick_first_value(row, ["机构", "机构名称", "研究机构", "券商", "source"])
            analyst = _pick_first_value(row, ["分析师", "作者", "研究员"])
            rating = _pick_first_value(row, ["评级", "投资评级", "评级变动"])
            time_str = _pick_first_value(row, ["报告日期", "日期", "发布时间", "time"])
            link = _pick_first_value(row, ["报告链接", "链接", "url", "URL"])
            summary_parts = [part for part in [org, analyst, rating] if part]
            items.append({
                "title": title,
                "time": time_str,
                "source": org or "eastmoney_research",
                "provider": "eastmoney_research",
                "channel": "broker_report",
                "retrieval_mode": "api",
                "link": link,
                "summary": " | ".join(summary_parts) or title,
                "evidence_type": "broker_view",
                "is_placeholder": False,
            })
        _write_cache(cache_key, {"items": items})
        return items
    except Exception as exc:
        logger.warning("东财研报抓取失败 [%s]: %s", stock_code, exc)
        return []


def fetch_fund_holdings(stock_code: str, limit: int = 5) -> list[dict[str, str]]:
    cache_key = f"fund_holdings_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    try:
        import akshare as ak

        df = ak.stock_report_fund_hold(symbol=stock_code)
        if df is None or getattr(df, "empty", True):
            return []
        items: list[dict[str, str]] = []
        for _, row in df.head(limit).iterrows():
            fund_name = _pick_first_value(row, ["基金简称", "基金名称", "名称", "fund"])
            if not fund_name:
                continue
            period = _pick_first_value(row, ["报告期", "持仓日期", "日期", "time"])
            shares = _pick_first_value(row, ["持股数", "持股数量", "持仓数量"])
            ratio = _pick_first_value(row, ["占流通股比例", "持股比例", "占净值比例", "比例"])
            items.append(_normalize_source_item({
                "title": f"{fund_name} 持有 {stock_code}",
                "time": period,
                "source": "eastmoney_fund_hold",
                "provider": "eastmoney_fund_hold",
                "channel": "fund_holding",
                "retrieval_mode": "api",
                "link": "",
                "summary": f"持股数 {shares or '--'}，比例 {ratio or '--'}",
                "evidence_type": "institutional_holding",
                "is_placeholder": False,
            }, channel="fund_holding", stock_code=stock_code))
        _write_cache(cache_key, {"items": items})
        return items
    except Exception as exc:
        logger.warning("基金持仓抓取失败 [%s]: %s", stock_code, exc)
        return []


def extract_document_summary(document) -> dict[str, str]:
    text_blocks = list(getattr(document, "text_blocks", []) or [])
    title = getattr(document, "title", "文档")
    metadata = dict(getattr(document, "metadata", {}) or {})
    summary = " ".join(text_blocks[:3])[:280] if text_blocks else "未解析到正文，可能需要 OCR 或更高质量 PDF。"
    return {
        "title": title,
        "summary": summary,
        "source_type": getattr(document, "source_type", "unknown"),
        "parse_status": metadata.get("parse_status", "success"),
    }


def _fetch_cninfo_announcements(*, stock_code: str, limit: int) -> list[dict[str, str]]:
    cache_key = f"announcement_cninfo_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    try:
        import akshare as ak

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=180)).strftime("%Y%m%d")
        df = ak.stock_zh_a_disclosure_report_cninfo(symbol=stock_code, start_date=start_date, end_date=end_date)
        items = _map_cninfo_rows(df, limit=limit, channel="announcement")
        _write_cache(cache_key, {"items": items})
        return items
    except Exception as exc:
        logger.warning("CNInfo 公告抓取失败 [%s]: %s", stock_code, exc)
        return []


def _fetch_cninfo_filings(*, stock_code: str, limit: int) -> list[dict[str, str]]:
    cache_key = f"filing_cninfo_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    try:
        import akshare as ak

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
        df = ak.stock_zh_a_disclosure_report_cninfo(symbol=stock_code, category="年报", start_date=start_date, end_date=end_date)
        items = _map_cninfo_rows(df, limit=limit, channel="filing")
        _write_cache(cache_key, {"items": items})
        return items
    except Exception as exc:
        logger.warning("CNInfo 披露抓取失败 [%s]: %s", stock_code, exc)
        return []


def _map_cninfo_rows(df, *, limit: int, channel: str) -> list[dict[str, str]]:
    if df is None or getattr(df, "empty", True):
        return []
    rows: list[dict[str, str]] = []
    for _, row in df.head(limit).iterrows():
        title = _pick_first_value(row, ["公告标题", "公告名称", "标题", "公告内容", "�������"])
        time_str = _pick_first_value(row, ["公告时间", "时间", "日期", "����ʱ��"])
        link = _pick_first_value(row, ["公告链接", "链接", "url", "��������"])
        security_name = _pick_first_value(row, ["名称", "简称", "股票简称", "���"])
        if not title:
            continue
        rows.append({
            "title": title,
            "time": str(time_str),
            "source": "cninfo",
            "provider": "cninfo",
            "channel": channel,
            "retrieval_mode": "api",
            "link": str(link),
            "summary": f"{security_name} {title}".strip(),
            "evidence_type": "announcement_update" if channel == "announcement" else "filing_report",
            "is_placeholder": False,
        })
    return rows


def _pick_first_value(row, keys: list[str]) -> str:
    for key in keys:
        try:
            value = row.get(key, "")
        except Exception:
            value = ""
        if value is not None and str(value).strip() and str(value).strip().lower() != "nan":
            return str(value).strip()
    return ""


def _build_news_backed_items(*, stock_code: str, stock_name: str, limit: int, channel: str, source: str) -> list[dict[str, str]]:
    cache_key = f"{channel}_{stock_code}_{limit}"
    cached = _read_cache(cache_key, max_age=CACHE_TTL_DEFAULT)
    if cached and isinstance(cached.get("items"), list):
        return list(cached["items"])
    company = stock_name or stock_code
    news = get_recent_news(company, count=limit)
    items = [
        {
            "title": item.get("title", ""),
            "time": item.get("time", ""),
            "source": item.get("source", source),
            "provider": item.get("channel", source),
            "channel": channel,
            "retrieval_mode": "fallback_news",
            "link": item.get("url", ""),
            "summary": item.get("content", ""),
            "evidence_type": "news_summary",
            "is_placeholder": False,
        }
        for item in news[:limit]
    ]
    _write_cache(cache_key, {"items": items})
    return items


def _normalize_source_item(item: dict[str, str], *, channel: str, stock_code: str) -> dict[str, str]:
    title = item.get("title", "")
    time_str = item.get("time", "")
    source = item.get("source", "")
    provider = item.get("provider", source or "unknown")
    retrieval_mode = item.get("retrieval_mode", "api")
    is_placeholder = bool(item.get("is_placeholder", False))
    evidence_type = item.get("evidence_type")
    if not evidence_type or evidence_type == "news_summary":
        evidence_type = _infer_evidence_type(channel, title, retrieval_mode=retrieval_mode)
    return {
        **item,
        "id": item.get("id", _stable_id(title, time_str, source, channel=channel)),
        "channel": channel,
        "provider": provider,
        "retrieval_mode": retrieval_mode,
        "evidence_type": evidence_type,
        "stock_code": stock_code,
        "is_placeholder": is_placeholder,
    }


def _infer_evidence_type(channel: str, title: str, *, retrieval_mode: str = "api") -> str:
    title = title or ""
    if channel == "announcement":
        if any(keyword in title for keyword in ("问询", "处罚", "监管", "风险")):
            return "announcement_risk"
        return "announcement_update"
    if channel == "filing":
        if any(keyword in title for keyword in ("年报", "半年报", "季报")):
            return "filing_report"
        return "filing_disclosure"
    if channel == "broker_report":
        if retrieval_mode == "fallback_news":
            return "broker_news_fallback"
        return "broker_view"
    if channel == "fund_holding":
        return "institutional_holding"
    return "source_note"


def _stable_id(*parts: str, channel: str) -> str:
    raw = "::".join([channel, *parts])
    return md5(raw.encode("utf-8", errors="ignore")).hexdigest()[:16]
