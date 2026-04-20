"""数据源模块测试 — 解析逻辑测试（不调用外部API）"""
from __future__ import annotations

import pandas as pd
import pytest

from app.models import FinancialMetrics


class TestParseValue:
    """akshare_client._parse_value 解析测试"""

    def test_normal_number(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value("123.45") == pytest.approx(123.45)

    def test_with_unit_yi(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value("862.28亿") == pytest.approx(862.28)

    def test_with_unit_percent(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value("15.38%") == pytest.approx(15.38)

    def test_false_value(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value(False) == 0.0

    def test_none_value(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value(None) == 0.0

    def test_empty_string(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value("") == 0.0

    def test_dash(self):
        from app.data_source.akshare_client import _parse_value
        assert _parse_value("--") == 0.0


class TestValidateStockCode:
    """股票代码校验测试"""

    def test_valid_code(self):
        from app.data_source.akshare_client import _validate_stock_code
        assert _validate_stock_code("600519") == "600519"

    def test_code_with_spaces(self):
        from app.data_source.akshare_client import _validate_stock_code
        assert _validate_stock_code(" 600519 ") == "600519"

    def test_invalid_code_too_short(self):
        from app.data_source.akshare_client import _validate_stock_code
        with pytest.raises(ValueError):
            _validate_stock_code("123")

    def test_invalid_code_non_numeric(self):
        from app.data_source.akshare_client import _validate_stock_code
        with pytest.raises(ValueError):
            _validate_stock_code("abcdef")


class TestSafeFloat:
    """_safe_float 安全浮点数转换测试"""

    def test_normal(self):
        from app.data_source.akshare_client import _safe_float
        assert _safe_float("123.45") == pytest.approx(123.45)

    def test_none(self):
        from app.data_source.akshare_client import _safe_float
        assert _safe_float(None) == 0.0

    def test_nan_string(self):
        from app.data_source.akshare_client import _safe_float
        assert _safe_float("nan") == 0.0

    def test_dash(self):
        from app.data_source.akshare_client import _safe_float
        assert _safe_float("-") == 0.0


class TestPeriodHelpers:
    def test_period_to_eastmoney_date(self):
        from app.data_source.akshare_client import _period_to_eastmoney_date

        assert _period_to_eastmoney_date("2025-12-31") == "20251231"
        assert _period_to_eastmoney_date("2024Q3") == "20240930"
        assert _period_to_eastmoney_date("202406") == "20240630"
        assert _period_to_eastmoney_date("") is None

    def test_normalize_period(self):
        from app.data_source.akshare_client import _normalize_period

        assert _normalize_period("2025") == "2025-12-31"
        assert _normalize_period("2024Q1") == "2024-03-31"
        assert _normalize_period("20240930") == "2024-09-30"

    def test_calc_yoy_growth_normalizes_and_sorts(self):
        from app.data_source.akshare_client import _calc_yoy_growth

        metrics = [
            FinancialMetrics(code="600519", period="2024", revenue=100, net_profit=40),
            FinancialMetrics(code="600519", period="2025", revenue=120, net_profit=42),
        ]
        result = _calc_yoy_growth(metrics)
        assert result[0].period == "2025-12-31"
        assert result[0].revenue_yoy == pytest.approx(20.0)


class TestMetricSanitizers:
    def test_fill_balance_fields_recovers_missing_values(self):
        from app.data_source.akshare_client import _fill_balance_fields

        metric = FinancialMetrics(code="600519", period="2025-12-31", revenue=100, debt_ratio=40, total_assets=200)
        metric = _fill_balance_fields(metric)

        assert metric.total_liability == pytest.approx(80.0)
        assert metric.total_equity == pytest.approx(120.0)

    def test_sanitize_metrics_deduplicates_by_richer_period(self):
        from app.data_source.akshare_client import _sanitize_metrics

        metrics = [
            FinancialMetrics(code="600519", period="2025", revenue=100, net_profit=30),
            FinancialMetrics(code="600519", period="2025-12-31", revenue=100, net_profit=30, roe=25, gross_margin=90, debt_ratio=20),
        ]
        result = _sanitize_metrics(metrics)

        assert len(result) == 1
        assert result[0].period == "2025-12-31"
        assert result[0].roe == pytest.approx(25)

    def test_sanitize_metrics_filters_invalid_revenue_rows(self):
        from app.data_source.akshare_client import _sanitize_metrics

        metrics = [
            FinancialMetrics(code="600519", period="2025-12-31", revenue=0, net_profit=20),
            FinancialMetrics(code="600519", period="2024-12-31", revenue=100, net_profit=30),
        ]
        result = _sanitize_metrics(metrics)

        assert len(result) == 1
        assert result[0].period == "2024-12-31"


class TestEastmoneyHelpers:

    def test_normalize_eastmoney_columns(self):
        from app.data_source.akshare_client import _normalize_eastmoney_columns

        df = pd.DataFrame(columns=["��Ʊ����", "ÿ�ɾ�Ӫ�ֽ�����", "���ʲ�������", "����ë����"])
        normalized = _normalize_eastmoney_columns(df)
        assert "股票代码" in normalized.columns
        assert "每股经营现金流" in normalized.columns
        assert "净资产收益率" in normalized.columns
        assert "销售毛利率" in normalized.columns

    def test_load_industry_candidates_supports_string_map(self, monkeypatch):
        from app.data_source.akshare_client import _load_industry_candidates

        monkeypatch.setattr(
            "app.data_source.akshare_client.json.loads",
            lambda _: {"白酒": ["600519", "000858"]},
        )
        monkeypatch.setattr("app.data_source.akshare_client.Path.exists", lambda self: True)
        monkeypatch.setattr("app.data_source.akshare_client.Path.read_text", lambda self, encoding=None: "{}")

        candidates = _load_industry_candidates("白酒Ⅱ")
        assert candidates == [{"code": "600519"}, {"code": "000858"}]

    def test_enrich_with_eastmoney_handles_garbled_columns(self, monkeypatch):
        from app.data_source.akshare_client import _enrich_with_eastmoney

        class DummyAk:
            @staticmethod
            def stock_yjbb_em(date):
                return pd.DataFrame([
                    {"��Ʊ����": "600519", "ÿ�ɾ�Ӫ�ֽ�����": 2.5, "���ʲ�������": 31.2, "����ë����": 91.5}
                ])

        monkeypatch.setitem(__import__("sys").modules, "akshare", DummyAk)
        monkeypatch.setattr("app.data_source.akshare_client._read_cache", lambda key, max_age=3600: {"total_shares": 10})

        metrics = [FinancialMetrics(code="600519", period="2025-12-31")]
        enriched = _enrich_with_eastmoney("600519", metrics)

        assert enriched[0].cash_flow == pytest.approx(25.0)
        assert enriched[0].roe == pytest.approx(31.2)
        assert enriched[0].gross_margin == pytest.approx(91.5)

    def test_normalize_news_columns(self):
        from app.data_source.akshare_client import _normalize_news_columns

        df = pd.DataFrame(columns=["col0", "col1", "col2", "col3", "col4", "col5"])
        normalized = _normalize_news_columns(df)
        assert "新闻标题" in normalized.columns
        assert "新闻内容" in normalized.columns
        assert "发布时间" in normalized.columns
        assert "文章来源" in normalized.columns
        assert "新闻链接" in normalized.columns


class TestNewsHelpers:
    def test_clean_news_text_strips_html_and_truncates(self):
        from app.data_source.akshare_client import _clean_news_text

        cleaned = _clean_news_text("<b>标题</b>\n\t测试" + "a" * 300, max_len=20)
        assert "<b>" not in cleaned
        assert "\n" not in cleaned
        assert cleaned.endswith("...")

    def test_is_useful_news_item_filters_garbled_text(self):
        from app.data_source.akshare_client import _is_useful_news_item

        assert _is_useful_news_item("公司收到监管问询", "摘要正常") is True
        assert _is_useful_news_item("���ű���", "摘要正常") is False

    def test_dedupe_news_items_keeps_unique_titles(self):
        from app.data_source.akshare_client import _dedupe_news_items

        items = [
            {"title": "新闻A", "content": "内容1"},
            {"title": "新闻A", "content": "内容1"},
            {"title": "新闻B", "content": "内容2"},
        ]
        deduped = _dedupe_news_items(items, 5)
        assert [item["title"] for item in deduped] == ["新闻A", "新闻B"]

    def test_get_recent_news_filters_garbled_eastmoney(self, monkeypatch):
        from app.data_source.akshare_client import get_recent_news

        class DummyAk:
            @staticmethod
            def stock_news_em(symbol):
                return pd.DataFrame([
                    {"col0": 0, "col1": "���ű���", "col2": "乱码摘要", "col3": "2026-01-01", "col4": "东财", "col5": "http://a"},
                    {"col0": 1, "col1": "公司收到监管问询函", "col2": "关注信息披露与经营波动", "col3": "2026-01-02", "col4": "东财", "col5": "http://b"},
                ])

        monkeypatch.setitem(__import__("sys").modules, "akshare", DummyAk)
        news = get_recent_news("600519", count=5)
        assert len(news) == 1
        assert news[0]["title"] == "公司收到监管问询函"
        assert news[0]["channel"] == "eastmoney"
