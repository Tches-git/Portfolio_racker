"""金融数据接口 — akshare 同花顺 + 新浪/腾讯行情 + 本地缓存"""
from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests

from app.config import (
    CACHE_DIR,
    CACHE_TTL_DEFAULT,
    CACHE_TTL_FINANCIALS,
    CACHE_TTL_PROFILE,
    CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
)
from app.models import FinancialMetrics, PeerCompany, StockProfile
from app.utils.circuit_breaker import CircuitBreaker, CircuitOpenError

logger = logging.getLogger("fin.data")

HEADERS = {"Referer": "https://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}


def _recent_report_dates(n: int = 4) -> list[str]:
    """生成最近 n 个财报期截止日（格式 YYYYMMDD），按时间倒序"""
    now = datetime.now()
    dates: list[str] = []
    for year_offset in range(3):
        y = now.year - year_offset
        for m, d in [(9, 30), (6, 30), (3, 31), (12, 31)]:
            if datetime(y, m, d) <= now:
                dates.append(f"{y}{m:02d}{d:02d}")
            if len(dates) >= n:
                return dates
    return dates


_sina_breaker = CircuitBreaker(
    "sina_api",
    failure_threshold=CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    recovery_timeout=CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
)
_tencent_breaker = CircuitBreaker(
    "tencent_api",
    failure_threshold=CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    recovery_timeout=CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
)
_ths_breaker = CircuitBreaker(
    "ths_akshare",
    failure_threshold=CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    recovery_timeout=CIRCUIT_BREAKER_RECOVERY_TIMEOUT,
)


def _cache_path(key: str) -> Path:
    return CACHE_DIR / f"{key}.json"


def _read_cache(key: str, max_age: int = CACHE_TTL_DEFAULT) -> dict | None:
    """读取缓存"""
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - data.get("_ts", 0) < max_age:
            return data
    except Exception as e:
        logger.warning(f"读取缓存失败 [{key}]: {e}")
    return None


def _write_cache(key: str, data: dict) -> None:
    data = {**data, "_ts": time.time()}
    try:
        _cache_path(key).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        logger.warning(f"写入缓存失败 [{key}]: {e}")


def _market_prefix(code: str) -> str:
    if code.startswith(("6", "9")):
        return "sh" + code
    return "sz" + code


def _validate_stock_code(code: str) -> str:
    """校验并清洗股票代码"""
    code = str(code).strip()
    if not re.match(r"^\d{6}$", code):
        raise ValueError(f"无效的股票代码: {code}（应为6位数字）")
    return code


def _safe_float(val) -> float:
    if val is None:
        return 0.0
    s = str(val).strip().replace(",", "")
    if s.lower() in {"", "nan", "none", "-", "--"}:
        return 0.0
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def _parse_value(val) -> float:
    """解析同花顺的值（如 '862.28亿'、'15.38%'、False）"""
    if val is False or val is None or str(val).strip() in ("", "False", "None", "--"):
        return 0.0
    s = str(val).replace("亿", "").replace("%", "").replace(",", "").strip()
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def _normalize_period(period: str) -> str:
    period = str(period).strip()
    if not period:
        return ""
    if re.fullmatch(r"\d{4}", period):
        return f"{period}-12-31"
    q_match = re.fullmatch(r"(\d{4})Q([1-4])", period, re.IGNORECASE)
    if q_match:
        suffix = {"1": "03-31", "2": "06-30", "3": "09-30", "4": "12-31"}[q_match.group(2)]
        return f"{q_match.group(1)}-{suffix}"
    ym_match = re.fullmatch(r"(\d{4})(\d{2})", period)
    if ym_match:
        suffix = {"03": "03-31", "06": "06-30", "09": "09-30", "12": "12-31"}.get(ym_match.group(2))
        if suffix:
            return f"{ym_match.group(1)}-{suffix}"
    if re.fullmatch(r"\d{8}", period):
        return f"{period[:4]}-{period[4:6]}-{period[6:8]}"
    return period


def _sort_metrics(metrics: list[FinancialMetrics]) -> list[FinancialMetrics]:
    metrics.sort(key=lambda m: _normalize_period(m.period), reverse=True)
    return metrics


def _calc_yoy_growth(metrics: list[FinancialMetrics], *, overwrite_existing: bool = False) -> list[FinancialMetrics]:
    """统一计算同比增速"""
    if not metrics:
        return metrics
    period_map = {_normalize_period(m.period): m for m in metrics}
    for curr in metrics:
        normalized = _normalize_period(curr.period)
        curr.period = normalized or curr.period
        curr_year = curr.period[:4]
        prev_period = f"{int(curr_year) - 1}{curr.period[4:]}"
        prev = period_map.get(prev_period)
        if prev and prev.revenue > 0 and (overwrite_existing or curr.revenue_yoy == 0):
            curr.revenue_yoy = round((curr.revenue / prev.revenue - 1) * 100, 2)
        if prev and prev.net_profit > 0 and (overwrite_existing or curr.profit_yoy == 0):
            curr.profit_yoy = round((curr.net_profit / prev.net_profit - 1) * 100, 2)
    return _sort_metrics(metrics)


def _clip_financial_values(m: FinancialMetrics) -> FinancialMetrics:
    m.revenue_yoy = max(-100, min(m.revenue_yoy, 500))
    m.profit_yoy = max(-100, min(m.profit_yoy, 500))
    m.roe = max(-200, min(m.roe, 200))
    m.gross_margin = max(-50, min(m.gross_margin, 100))
    m.debt_ratio = max(0, min(m.debt_ratio, 100))
    return m


def _count_metric_fields(m: FinancialMetrics) -> int:
    fields = [
        m.revenue, m.net_profit, m.revenue_yoy, m.profit_yoy, m.roe,
        m.gross_margin, m.debt_ratio, m.cash_flow, m.total_assets,
        m.total_equity, m.total_liability,
    ]
    return sum(1 for value in fields if value not in (0, 0.0, "", None))


def _fill_balance_fields(m: FinancialMetrics) -> FinancialMetrics:
    if m.total_assets < 0:
        m.total_assets = 0.0
    if m.total_liability < 0:
        m.total_liability = 0.0
    if m.debt_ratio > 0:
        ratio = m.debt_ratio / 100
        if m.total_assets > 0 and m.total_liability == 0:
            m.total_liability = round(m.total_assets * ratio, 2)
        if m.total_assets > 0 and m.total_equity == 0 and ratio < 1:
            m.total_equity = round(m.total_assets * (1 - ratio), 2)
        if m.total_equity > 0 and m.total_assets == 0 and ratio < 1:
            m.total_assets = round(m.total_equity / (1 - ratio), 2)
        if m.total_liability > 0 and m.total_assets == 0 and ratio > 0:
            m.total_assets = round(m.total_liability / ratio, 2)
    if m.total_assets > 0 and m.total_equity > 0 and m.total_liability == 0:
        m.total_liability = round(max(m.total_assets - m.total_equity, 0), 2)
    if m.total_assets > 0 and m.total_liability > 0 and m.total_equity == 0:
        m.total_equity = round(m.total_assets - m.total_liability, 2)
    if m.total_equity > 0 and m.total_liability > 0 and m.total_assets == 0:
        m.total_assets = round(m.total_equity + m.total_liability, 2)
    if m.total_assets > 0 and m.total_equity > m.total_assets:
        m.total_equity = 0.0
        m.total_liability = 0.0
    if m.total_assets > 0 and m.total_liability > m.total_assets:
        m.total_equity = 0.0
        m.total_liability = 0.0
    return m


def _sanitize_metrics(metrics: list[FinancialMetrics], *, require_revenue: bool = True) -> list[FinancialMetrics]:
    sanitized: dict[str, FinancialMetrics] = {}
    for m in metrics:
        m.period = _normalize_period(m.period) or m.period
        if require_revenue and m.revenue <= 0:
            continue
        m = _fill_balance_fields(m)
        m = _clip_financial_values(m)
        existing = sanitized.get(m.period)
        if existing is None or _count_metric_fields(m) >= _count_metric_fields(existing):
            sanitized[m.period] = m
    cleaned = list(sanitized.values())
    _sort_metrics(cleaned)
    return _calc_yoy_growth(cleaned)


def get_stock_profile(code: str) -> StockProfile:
    """获取公司基本信息（新浪行情 + 腾讯财务）"""
    code = _validate_stock_code(code)
    cached = _read_cache(f"profile_{code}", max_age=CACHE_TTL_PROFILE)
    if cached and cached.get("name"):
        return StockProfile(**{k: v for k, v in cached.items() if k != "_ts"})

    symbol = _market_prefix(code)
    name = code
    pe, pb, market_cap, industry, total_shares = 0.0, 0.0, 0.0, "未知", 0.0
    current_price = 0.0

    try:
        def _fetch_sina_quote():
            url = f"https://hq.sinajs.cn/list={symbol}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.encoding = "gbk"
            return r.text.split('"')[1].split(",")

        parts = _sina_breaker.call(_fetch_sina_quote)
        name = parts[0]
    except CircuitOpenError as e:
        logger.warning(f"新浪行情熔断跳过: {e}")
    except Exception as e:
        logger.warning(f"新浪行情失败: {e}")

    try:
        def _fetch_tencent_quote():
            url = f"https://qt.gtimg.cn/q={symbol}"
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.encoding = "gbk"
            return r.text.split("~")

        parts = _tencent_breaker.call(_fetch_tencent_quote)
        if len(parts) > 46:
            name = parts[1] if parts[1] else name
            current_price = _safe_float(parts[3])
            market_cap = _safe_float(parts[45])
            pe = _safe_float(parts[39])
            pb = _safe_float(parts[46])
            if current_price > 0 and market_cap > 0:
                total_shares = round(market_cap / current_price, 4)
    except CircuitOpenError as e:
        logger.warning(f"腾讯接口熔断跳过: {e}")
    except Exception as e:
        logger.warning(f"腾讯接口失败: {e}")

    try:
        import akshare as ak

        for date_str in _recent_report_dates(4):
            try:
                df_yjbb = ak.stock_yjbb_em(date=date_str)
                if df_yjbb is not None and not df_yjbb.empty:
                    row = df_yjbb[df_yjbb["股票代码"] == code]
                    if not row.empty:
                        ind = str(row.iloc[0].get("所处行业", "")).strip()
                        if ind and ind not in ("nan", ""):
                            industry = ind
                            break
            except Exception as e:
                logger.warning(f"东财行业检测失败 [{date_str}]: {e}")
    except Exception as e:
        logger.warning(f"东财行业检测初始化失败: {e}")

    if industry in ("未知", ""):
        try:
            url = f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/{code}.phtml"
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.encoding = "gbk"
            m = re.search(r"所属行业.*?<td.*?>(.*?)</td>", r.text, re.DOTALL)
            if m:
                ind = m.group(1).strip()
                if ind and not ind.startswith("@"):
                    industry = ind
        except Exception as e:
            logger.warning(f"新浪行业回退失败 [{code}]: {e}")

    profile = StockProfile(
        code=code,
        name=name,
        industry=industry,
        market_cap=market_cap,
        pe_ratio=pe,
        pb_ratio=pb,
        total_shares=total_shares,
        listing_date="",
    )
    _write_cache(
        f"profile_{code}",
        {
            "code": code,
            "name": name,
            "industry": industry,
            "market_cap": market_cap,
            "pe_ratio": pe,
            "pb_ratio": pb,
            "total_shares": total_shares,
            "listing_date": "",
        },
    )
    return profile


def get_financial_metrics(code: str) -> list[FinancialMetrics]:
    """获取财务指标"""
    code = _validate_stock_code(code)
    cached = _read_cache(f"metrics_ths_{code}", max_age=CACHE_TTL_FINANCIALS)
    if cached and cached.get("items"):
        items = cached["items"]
        if items and items[0].get("revenue", 0) > 0:
            return [FinancialMetrics(**item) for item in items]

    try:
        metrics = _ths_breaker.call(_fetch_ths_financials, code)
        if metrics:
            metrics = _enrich_with_eastmoney(code, metrics)
            metrics = _sanitize_metrics(metrics)
        if metrics:
            _write_cache(f"metrics_ths_{code}", {"items": [_metrics_to_dict(m) for m in metrics]})
        return metrics
    except CircuitOpenError as e:
        logger.warning(f"同花顺熔断跳过: {e}，直接走新浪回退")
    except Exception as e:
        logger.warning(f"同花顺财务数据获取失败: {e}，尝试新浪回退")

    try:
        metrics = _fetch_sina_financials(code)
        if metrics:
            metrics = _sanitize_metrics(metrics)
            _write_cache(f"metrics_ths_{code}", {"items": [_metrics_to_dict(m) for m in metrics]})
        return metrics
    except Exception as e:
        logger.warning(f"新浪财务数据也失败: {e}")
        return []


def _fetch_ths_financials(code: str) -> list[FinancialMetrics]:
    """从同花顺获取年度+季度财务摘要"""
    import akshare as ak

    all_metrics: list[FinancialMetrics] = []
    seen_periods: set[str] = set()

    try:
        df_yearly = ak.stock_financial_abstract_ths(symbol=code, indicator="按年度")
        if df_yearly is not None and not df_yearly.empty:
            for _, row in df_yearly.tail(5).iterrows():
                period = str(row.get("报告期", ""))
                if not period or period in seen_periods:
                    continue
                seen_periods.add(period)
                m = _ths_row_to_metrics(code, period, row)
                if m.revenue > 0:
                    all_metrics.append(m)
    except Exception as e:
        logger.warning(f"同花顺年度数据失败: {e}")

    try:
        df_quarter = ak.stock_financial_abstract_ths(symbol=code, indicator="按报告期")
        if df_quarter is not None and not df_quarter.empty:
            current_year = datetime.now().year
            for _, row in df_quarter.iterrows():
                period = str(row.get("报告期", ""))
                if not period or period in seen_periods:
                    continue
                try:
                    year = int(period[:4])
                    if year < current_year - 1:
                        continue
                except (ValueError, IndexError):
                    continue
                if period.endswith("12-31") and period[:4] in [p[:4] for p in seen_periods if p.endswith("12-31")]:
                    continue
                seen_periods.add(period)
                m = _ths_row_to_metrics(code, period, row)
                if m.revenue > 0:
                    all_metrics.append(m)
    except Exception as e:
        logger.warning(f"同花顺季度数据失败: {e}")

    return _sanitize_metrics(all_metrics)


def _ths_row_to_metrics(code: str, period: str, row) -> FinancialMetrics:
    revenue = _parse_value(row.get("营业总收入", 0))
    net_profit = _parse_value(row.get("净利润", 0))
    revenue_yoy = _parse_value(row.get("营业总收入同比增长率", 0))
    profit_yoy = _parse_value(row.get("净利润同比增长率", 0))
    roe = _parse_value(row.get("净资产收益率", 0))
    gross_margin = _parse_value(row.get("销售毛利率", 0))
    debt_ratio = _parse_value(row.get("资产负债率", 0))
    bvps = _parse_value(row.get("每股净资产", 0))
    cash_per_share = _parse_value(row.get("每股经营现金流", 0))

    total_equity = 0.0
    total_assets = 0.0
    total_liability = 0.0
    total_shares = 0.0
    if bvps > 0:
        profile_cache = _read_cache(f"profile_{code}")
        total_shares = profile_cache.get("total_shares", 0) if profile_cache else 0
        if total_shares > 0:
            total_equity = round(bvps * total_shares, 2)
            if 0 < debt_ratio < 100:
                total_assets = round(total_equity / (1 - debt_ratio / 100), 2)
                total_liability = round(total_assets - total_equity, 2)

    return FinancialMetrics(
        code=code,
        period=period,
        revenue=revenue,
        net_profit=net_profit,
        revenue_yoy=revenue_yoy,
        profit_yoy=profit_yoy,
        roe=roe,
        gross_margin=gross_margin,
        debt_ratio=debt_ratio,
        cash_flow=round(cash_per_share * total_shares, 2) if cash_per_share else 0.0,
        total_assets=total_assets,
        total_equity=total_equity,
        total_liability=total_liability,
    )


def _metrics_to_dict(m: FinancialMetrics) -> dict:
    return {
        "code": m.code,
        "period": m.period,
        "revenue": m.revenue,
        "net_profit": m.net_profit,
        "revenue_yoy": m.revenue_yoy,
        "profit_yoy": m.profit_yoy,
        "roe": m.roe,
        "gross_margin": m.gross_margin,
        "debt_ratio": m.debt_ratio,
        "cash_flow": m.cash_flow,
        "total_assets": m.total_assets,
        "total_equity": m.total_equity,
        "total_liability": m.total_liability,
        "operating_cost": m.operating_cost,
        "cash_and_equivalents": m.cash_and_equivalents,
    }


def _normalize_eastmoney_columns(df):
    try:
        df = df.copy()
        rename_map = {}
        for col in df.columns:
            raw = str(col)
            if "股票代码" in raw or "��Ʊ����" in raw:
                rename_map[col] = "股票代码"
            elif "每股经营现金流" in raw or "ÿ�ɾ�Ӫ�ֽ�����" in raw:
                rename_map[col] = "每股经营现金流"
            elif "净资产收益率" in raw or "���ʲ�������" in raw:
                rename_map[col] = "净资产收益率"
            elif "销售毛利率" in raw or "����ë����" in raw:
                rename_map[col] = "销售毛利率"
        if rename_map:
            df = df.rename(columns=rename_map)
        return df
    except Exception:
        return df


def _period_to_eastmoney_date(period: str) -> str | None:
    period = str(period).strip()
    if not period:
        return None
    if "-" in period and len(period) >= 10:
        return period.replace("-", "")[:8]
    if len(period) == 8 and period.isdigit():
        return period
    if len(period) >= 6 and period[:4].isdigit() and period[-2:].upper().startswith("Q"):
        quarter = period[-1]
        mapping = {"1": "0331", "2": "0630", "3": "0930", "4": "1231"}
        suffix = mapping.get(quarter)
        if suffix:
            return period[:4] + suffix
    if len(period) >= 6 and period[:4].isdigit() and period[-2:].isdigit():
        mapping = {"03": "0331", "06": "0630", "09": "0930", "12": "1231"}
        suffix = mapping.get(period[-2:])
        if suffix:
            return period[:4] + suffix
    return None


def _enrich_with_eastmoney(code: str, metrics: list[FinancialMetrics]) -> list[FinancialMetrics]:
    """补充东财字段"""
    try:
        import akshare as ak

        eastmoney_cache: dict[str, object] = {}
        profile_cache = _read_cache(f"profile_{code}")
        total_shares = profile_cache.get("total_shares", 0) if profile_cache else 0

        for m in metrics:
            date_str = _period_to_eastmoney_date(m.period)
            if not date_str:
                continue
            try:
                if date_str not in eastmoney_cache:
                    eastmoney_cache[date_str] = _normalize_eastmoney_columns(ak.stock_yjbb_em(date=date_str))
                df = eastmoney_cache[date_str]
                if df is None or getattr(df, "empty", True):
                    continue
                if "股票代码" not in df.columns:
                    continue
                row = df[df["股票代码"].astype(str).str.zfill(6) == code]
                if row.empty:
                    continue
                row = row.iloc[0]
                cash_ps = _safe_float(row.get("每股经营现金流"))
                if cash_ps and m.cash_flow == 0 and total_shares > 0:
                    m.cash_flow = round(cash_ps * total_shares, 2)
                roe_val = _safe_float(row.get("净资产收益率"))
                if roe_val and m.roe == 0:
                    m.roe = round(roe_val, 2)
                gm_val = _safe_float(row.get("销售毛利率"))
                if gm_val and m.gross_margin == 0:
                    m.gross_margin = round(gm_val, 2)
            except Exception as e:
                logger.warning(f"东财逐期增强失败 [{m.period}]: {e}")
    except Exception as e:
        logger.warning(f"东财业绩报表补充失败: {e}")

    return _sanitize_metrics(metrics, require_revenue=False)


def _fetch_sina_financials(code: str) -> list[FinancialMetrics]:
    """新浪财报回退（简化版）"""
    return []


def _fetch_page(url: str) -> str:
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.encoding = "gbk"
            return r.text
        except Exception:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                raise


def _parse_sina_table(html: str) -> dict[str, list[float]]:
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
    result: dict[str, list[float]] = {}
    for row_html in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.DOTALL)
        if not cells:
            continue
        label = re.sub(r"<.*?>", "", cells[0]).strip().replace("\xa0", "")
        if not label:
            continue
        values = []
        for cell in cells[1:5]:
            clean = re.sub(r"<.*?>", "", cell).strip().replace(",", "").replace("\xa0", "")
            values.append(_safe_float(clean))
        result[label] = values
    return result


def _get_table_val(data: dict[str, list[float]], key: str, col: int) -> float:
    if key in data and col < len(data[key]):
        return data[key][col]
    for k, v in data.items():
        if key.rstrip("(%)") in k and col < len(v):
            return v[col]
    return 0.0


def _load_industry_candidates(industry: str) -> list[dict[str, str]]:
    map_path = Path(__file__).parent.parent.parent / "data" / "industry_map.json"
    if not map_path.exists():
        return []
    try:
        industry_map = json.loads(map_path.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning(f"读取行业映射失败: {e}")
        return []

    normalized = industry.replace("Ⅰ", "").replace("Ⅱ", "").replace("Ⅲ", "").strip()
    candidates = industry_map.get(industry) or industry_map.get(normalized) or []
    normalized_items: list[dict[str, str]] = []
    for item in candidates:
        if isinstance(item, str):
            normalized_items.append({"code": item})
        elif isinstance(item, dict) and item.get("code"):
            normalized_items.append({"code": str(item["code"])})
    return normalized_items


def get_peer_companies(industry: str, exclude_code: str = "", top_n: int = 5) -> list[PeerCompany]:
    """获取同行业公司（从行业映射文件）+ 关键财务指标"""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    candidates = [c for c in _load_industry_candidates(industry) if c.get("code") != exclude_code][: top_n * 2]
    peers: list[PeerCompany] = []

    def _build_peer(item: dict) -> PeerCompany | None:
        try:
            profile = get_stock_profile(item["code"])
            metrics = get_financial_metrics(item["code"])
            latest = metrics[0] if metrics else FinancialMetrics(code=item["code"], period="")
            net_margin = round(latest.net_profit / latest.revenue * 100, 1) if latest.revenue > 0 else 0.0
            return PeerCompany(
                code=item["code"],
                name=profile.name,
                market_cap=profile.market_cap,
                pe_ratio=profile.pe_ratio,
                pb_ratio=profile.pb_ratio,
                roe=latest.roe,
                gross_margin=latest.gross_margin,
                net_margin=net_margin,
                revenue=latest.revenue,
                net_profit=latest.net_profit,
                revenue_yoy=latest.revenue_yoy,
            )
        except Exception as e:
            logger.warning(f"构建同行公司失败 [{item.get('code', '')}]: {e}")
            return None

    with ThreadPoolExecutor(max_workers=min(6, max(1, len(candidates)))) as pool:
        futures = [pool.submit(_build_peer, item) for item in candidates]
        for future in as_completed(futures):
            peer = future.result()
            if peer is not None:
                peers.append(peer)

    peers.sort(key=lambda p: p.market_cap, reverse=True)
    return peers[:top_n]


def _normalize_news_columns(df):
    try:
        df = df.copy()
        rename_map = {}
        for idx, col in enumerate(df.columns):
            raw = str(col)
            if "新闻标题" in raw or "���ű���" in raw or idx == 1:
                rename_map[col] = "新闻标题"
            elif "发布时间" in raw or "����ʱ��" in raw or idx == 3:
                rename_map[col] = "发布时间"
            elif "文章来源" in raw or "������Դ" in raw or idx == 4:
                rename_map[col] = "文章来源"
            elif "新闻链接" in raw or ("��������" in raw and idx >= 5) or idx == 5:
                rename_map[col] = "新闻链接"
            elif "新闻内容" in raw or ("��������" in raw and idx == 2) or idx == 2:
                rename_map[col] = "新闻内容"
        if rename_map:
            df = df.rename(columns=rename_map)
        return df
    except Exception:
        return df


def _clean_news_text(text: str, *, max_len: int = 240) -> str:
    text = re.sub(r"<.*?>", "", str(text or ""))
    text = text.replace("\u3000", " ").replace("&nbsp;", " ")
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" -|•：:;；，,。.!！?？")
    if len(text) > max_len:
        text = text[:max_len].rstrip() + "..."
    return text


def _looks_garbled_text(text: str) -> bool:
    text = str(text or "").strip()
    if not text:
        return True
    bad_markers = ("���", "����", "��", "锟", "鈥", "�")
    return any(marker in text for marker in bad_markers)


def _is_useful_news_item(title: str, content: str) -> bool:
    title = str(title or "").strip()
    content = str(content or "").strip()
    if not title or len(title) < 4:
        return False
    if _looks_garbled_text(title):
        return False
    if content and _looks_garbled_text(content):
        return False
    return True


def _normalize_news_item(title: str, content: str = "", time_str: str = "", source: str = "", url: str = "", channel: str = "") -> dict[str, str]:
    return {
        "title": _clean_news_text(title, max_len=120),
        "content": _clean_news_text(content, max_len=220),
        "time": _clean_news_text(time_str, max_len=40),
        "source": _clean_news_text(source, max_len=40),
        "url": _clean_news_text(url, max_len=200),
        "channel": channel,
    }


def _dedupe_news_items(items: list[dict[str, str]], count: int) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for item in items:
        title = item.get("title", "")
        content = item.get("content", "")
        key = (title, content[:80])
        if not title or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
        if len(deduped) >= count:
            break
    return deduped


def get_recent_news(name: str, count: int = 5) -> list[dict[str, str]]:
    """获取新闻，优先东财新闻接口，失败后回退新浪搜索"""
    try:
        import akshare as ak

        symbol_match = re.search(r"\((\d{6})\)", name)
        symbol = symbol_match.group(1) if symbol_match else ""
        if not symbol and re.fullmatch(r"\d{6}", name.strip()):
            symbol = name.strip()
        if symbol:
            df = _normalize_news_columns(ak.stock_news_em(symbol=symbol))
            if df is not None and not getattr(df, "empty", True):
                news = []
                for _, row in df.iterrows():
                    title = _clean_news_text(row.get("新闻标题", ""), max_len=120)
                    content = _clean_news_text(row.get("新闻内容", ""), max_len=220)
                    tm = _clean_news_text(row.get("发布时间", ""), max_len=40)
                    source = _clean_news_text(row.get("文章来源", ""), max_len=40)
                    link = _clean_news_text(row.get("新闻链接", ""), max_len=200)
                    if _is_useful_news_item(title, content):
                        news.append(_normalize_news_item(title, content, tm, source, link, "eastmoney"))
                news = _dedupe_news_items(news, count)
                if news:
                    return news
    except Exception as e:
        logger.warning(f"东财新闻获取失败 [{name}]: {e}")

    try:
        url = f"https://search.sina.com.cn/news?q={quote(name)}&c=news&sort=time"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.encoding = "utf-8"
        titles = re.findall(r"<h2><a.*?>(.*?)</a></h2>", r.text)
        summaries = re.findall(r'<p class="content">(.*?)</p>', r.text)
        times = re.findall(r'<span class="fgray_time">(.*?)</span>', r.text)
        news = []
        for i, title in enumerate(titles):
            clean_title = _clean_news_text(title, max_len=120)
            summary = _clean_news_text(summaries[i], max_len=220) if i < len(summaries) else ""
            tm = _clean_news_text(times[i], max_len=40) if i < len(times) else ""
            if _is_useful_news_item(clean_title, summary):
                news.append(_normalize_news_item(clean_title, summary, tm, channel="sina_search"))
        return _dedupe_news_items(news, count)
    except Exception as e:
        logger.warning(f"获取新闻失败 [{name}]: {e}")
        return []
