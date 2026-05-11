from __future__ import annotations

import logging

from app.data_source.live_tools import fetch_announcements, fetch_broker_reports, fetch_exchange_filings, fetch_fund_holdings, fetch_live_quotes


def test_fetch_live_quotes_uses_profile(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools.get_stock_profile", lambda code: type("P", (), {"name": "贵州茅台", "market_cap": 25000, "current_price": 1688.0, "pe_ratio": 25.5, "pb_ratio": 8.2})())
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    written = {}
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda key, data: written.setdefault(key, data))

    quote = fetch_live_quotes("600519")

    assert quote["channel"] == "live_quote"
    assert quote["provider"] == "akshare"
    assert quote["retrieval_mode"] == "api"
    assert quote["price"] == 1688.0
    assert quote["pe_ratio"] == 25.5
    assert written


def test_fetch_announcements_uses_cninfo_when_available(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "app.data_source.live_tools._fetch_cninfo_announcements",
        lambda stock_code, limit: [{"title": "年度股东大会通知", "time": "2026-03-01", "source": "cninfo", "provider": "cninfo", "retrieval_mode": "api", "link": "http://cninfo/a", "summary": "平安银行 年度股东大会通知", "evidence_type": "announcement_update", "is_placeholder": False}],
    )
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda *args, **kwargs: [])

    announcements = fetch_announcements("000001", "平安银行", limit=1)

    assert announcements[0]["provider"] == "cninfo"
    assert announcements[0]["retrieval_mode"] == "api"
    assert announcements[0]["evidence_type"] == "announcement_update"


def test_fetch_announcements_and_filings_fallback_to_news(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._fetch_cninfo_announcements", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.data_source.live_tools._fetch_cninfo_filings", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda name, count=5: [{"title": "收到问询函", "time": "2026-01-01", "source": "东财", "url": "http://a", "content": "披露摘要", "channel": "eastmoney"}])

    announcements = fetch_announcements("600519", "贵州茅台", limit=1)
    filings = fetch_exchange_filings("600519", "贵州茅台", limit=1)

    assert announcements[0]["channel"] == "announcement"
    assert announcements[0]["provider"] == "eastmoney"
    assert announcements[0]["retrieval_mode"] == "fallback_news"
    assert announcements[0]["evidence_type"] == "announcement_risk"
    assert filings[0]["channel"] == "filing"
    assert filings[0]["evidence_type"] == "filing_disclosure"


def test_fetch_exchange_filings_uses_cninfo_when_available(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "app.data_source.live_tools._fetch_cninfo_filings",
        lambda stock_code, limit: [{"title": "2025年年度报告", "time": "2026-03-20", "source": "cninfo", "provider": "cninfo", "retrieval_mode": "api", "link": "http://cninfo/f", "summary": "平安银行 2025年年度报告", "evidence_type": "filing_report", "is_placeholder": False}],
    )
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda *args, **kwargs: [])

    filings = fetch_exchange_filings("000001", "平安银行", limit=1)

    assert filings[0]["provider"] == "cninfo"
    assert filings[0]["evidence_type"] == "filing_report"


def test_fetch_broker_reports_prefers_eastmoney_research(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools.get_stock_profile", lambda code: type("P", (), {"name": "贵州茅台"})())
    monkeypatch.setattr(
        "app.data_source.live_tools._fetch_eastmoney_research_reports",
        lambda stock_code, limit: [{"title": "盈利预测上调", "time": "2026-01-03", "source": "中信证券", "provider": "eastmoney_research", "channel": "broker_report", "retrieval_mode": "api", "link": "http://r", "summary": "中信证券 | 买入", "evidence_type": "broker_view", "is_placeholder": False}],
    )
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda *args, **kwargs: [])

    reports = fetch_broker_reports("600519", "贵州茅台", limit=1)

    assert reports[0]["provider"] == "eastmoney_research"
    assert reports[0]["retrieval_mode"] == "api"
    assert reports[0]["evidence_type"] == "broker_view"


def test_fetch_broker_reports_prefers_news_fallback(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools.get_stock_profile", lambda code: type("P", (), {"name": "贵州茅台"})())
    monkeypatch.setattr("app.data_source.live_tools._fetch_eastmoney_research_reports", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda name, count=5: [{"title": "机构上调盈利预测", "time": "2026-01-03", "source": "东财", "url": "http://broker", "content": "机构观点摘要", "channel": "eastmoney"}])

    reports = fetch_broker_reports("600519", "贵州茅台", limit=1)

    assert reports[0]["channel"] == "broker_report"
    assert reports[0]["is_placeholder"] is False
    assert reports[0]["retrieval_mode"] == "fallback_news"
    assert reports[0]["evidence_type"] == "broker_news_fallback"


def test_fetch_broker_reports_returns_placeholder_when_no_external_api(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools.get_stock_profile", lambda code: type("P", (), {"name": "贵州茅台"})())
    monkeypatch.setattr("app.data_source.live_tools._fetch_eastmoney_research_reports", lambda *args, **kwargs: [])
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda *args, **kwargs: [])

    reports = fetch_broker_reports("600519", "贵州茅台", limit=1)

    assert reports[0]["channel"] == "broker_report"
    assert reports[0]["is_placeholder"] is True
    assert reports[0]["retrieval_mode"] == "placeholder"
    assert "占位" in reports[0]["summary"]


def test_fetch_fund_holdings_maps_akshare_rows(monkeypatch):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools._write_cache", lambda *args, **kwargs: None)

    class FakeDf:
        empty = False
        def head(self, limit):
            return self
        def iterrows(self):
            yield 0, {"基金简称": "测试基金", "报告期": "2025Q4", "持股数": "100万", "持股比例": "1.2%"}

    monkeypatch.setattr("akshare.stock_report_fund_hold", lambda symbol: FakeDf())

    holdings = fetch_fund_holdings("600519", limit=1)

    assert holdings[0]["channel"] == "fund_holding"
    assert holdings[0]["provider"] == "eastmoney_fund_hold"
    assert holdings[0]["evidence_type"] == "institutional_holding"


def test_fetch_announcements_logs_cninfo_failure(monkeypatch, caplog):
    monkeypatch.setattr("app.data_source.live_tools._read_cache", lambda *args, **kwargs: None)
    monkeypatch.setattr("app.data_source.live_tools.get_recent_news", lambda *args, **kwargs: [])

    def fail_fetch(*args, **kwargs):
        raise RuntimeError("cninfo down")

    monkeypatch.setattr("akshare.stock_zh_a_disclosure_report_cninfo", fail_fetch)

    with caplog.at_level(logging.WARNING, logger="fin.live_tools"):
        announcements = fetch_announcements("600519", "贵州茅台", limit=1)

    assert announcements == []
    assert "CNInfo 公告抓取失败" in caplog.text
