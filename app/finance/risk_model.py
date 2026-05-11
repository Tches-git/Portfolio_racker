"""风险评估模型 — 基于财务指标和新闻的多维风险识别（行业感知阈值）"""
from __future__ import annotations

import logging
import re

from app.models import FinancialMetrics, RiskItem, StockProfile

logger = logging.getLogger("fin.risk")

_INDUSTRY_THRESHOLDS: dict[str, dict] = {
    "银行": {"debt_ratio_high": 92, "debt_ratio_warn": 90, "pe_high": 15, "pe_warn": 10},
    "房地产": {"debt_ratio_high": 80, "debt_ratio_warn": 75, "pe_high": 30, "pe_warn": 20},
    "非银金融": {"debt_ratio_high": 85, "debt_ratio_warn": 80, "pe_high": 40, "pe_warn": 25},
    "证券": {"debt_ratio_high": 80, "debt_ratio_warn": 75, "pe_high": 30, "pe_warn": 20},
    "保险": {"debt_ratio_high": 88, "debt_ratio_warn": 85, "pe_high": 25, "pe_warn": 15},
}

_DEFAULT_THRESHOLDS: dict = {
    "debt_ratio_high": 70, "debt_ratio_warn": 55,
    "pe_high": 80, "pe_warn": 50,
}

_NEWS_RULES = [
    {
        "keywords": ["处罚", "立案", "调查", "问询", "违规", "行政监管", "罚款"],
        "level": "high",
        "description": "监管或合规负面事件升温，可能扰动经营节奏与市场预期",
        "transmission_path": "监管处置或合规整改 → 业务推进放缓/新增成本上升 → 利润率与估值承压",
        "impact": "净利率、估值中枢、市场情绪",
    },
    {
        "keywords": ["召回", "事故", "质量问题", "食品安全", "停产", "停工", "爆雷"],
        "level": "high",
        "description": "产品或生产事件可能损伤品牌与交付能力",
        "transmission_path": "产品/生产事件 → 销售受阻或渠道信心下滑 → 收入增速与毛利率承压",
        "impact": "营收增速、毛利率、品牌声誉",
    },
    {
        "keywords": ["减持", "解禁", "诉讼", "仲裁", "违约", "债务"],
        "level": "medium",
        "description": "资本运作或法律纠纷事件可能放大股价波动与融资压力",
        "transmission_path": "减持/诉讼/债务事件 → 风险偏好下降或融资成本上升 → 估值与现金流预期承压",
        "impact": "估值波动、融资能力、现金流预期",
    },
    {
        "keywords": ["降价", "价格战", "需求疲软", "消费疲软", "销量下滑", "去库存"],
        "level": "medium",
        "description": "需求或价格压力可能削弱收入增长与盈利弹性",
        "transmission_path": "需求转弱/价格竞争加剧 → 销量或单价承压 → 收入增速和利润率回落",
        "impact": "营收增速、净利率、库存周转",
    },
]


def _get_threshold(industry: str) -> dict:
    """根据行业名称获取对应阈值"""
    for key, val in _INDUSTRY_THRESHOLDS.items():
        if key in industry:
            return val
    return _DEFAULT_THRESHOLDS


def _sanitize_external_text(text: str, *, max_len: int = 200) -> str:
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def _wrap_external_text(text: str) -> str:
    cleaned = _sanitize_external_text(text)
    return f"<external_data>{cleaned}</external_data>" if cleaned else ""


def _build_risk(category: str, level: str, description: str, *, metric: str = "", value: str = "", evidence: str = "", transmission_path: str = "", impact: str = "", source: str = "", time: str = "") -> RiskItem:
    return RiskItem(
        category=category,
        level=level,
        description=description,
        metric=metric,
        value=value,
        evidence=evidence,
        transmission_path=transmission_path,
        impact=impact,
        source=source,
        time=time,
    )


def assess_financial_risks(profile: StockProfile, metrics: list[FinancialMetrics]) -> list[RiskItem]:
    """基于财务指标识别风险（使用行业感知阈值）"""
    risks: list[RiskItem] = []
    if not metrics:
        risks.append(_build_risk(
            "financial", "high", "无法获取财务数据，信息披露存疑",
            evidence="缺少核心财务报表数据",
            transmission_path="关键财务信息缺失 → 无法验证经营质量与估值假设 → 研究结论可靠性下降",
            impact="报告可信度、估值判断",
            source="financial_metrics",
        ))
        return risks

    m = metrics[0]
    industry = profile.industry if profile else ""
    t = _get_threshold(industry)

    if m.debt_ratio > t["debt_ratio_high"]:
        risks.append(_build_risk(
            "financial", "high",
            f"资产负债率 {m.debt_ratio:.1f}% 超过行业警戒线 {t['debt_ratio_high']}%，存在偿债风险",
            metric="debt_ratio", value=f"{m.debt_ratio:.1f}%",
            evidence=f"最新资产负债率 {m.debt_ratio:.1f}%",
            transmission_path="杠杆水平过高 → 利息负担与再融资压力上升 → 盈利与现金流安全边际收窄",
            impact="偿债能力、净利率、现金流安全性",
            source="financial_metrics",
        ))
    elif m.debt_ratio > t["debt_ratio_warn"]:
        risks.append(_build_risk(
            "financial", "medium",
            f"资产负债率 {m.debt_ratio:.1f}% 偏高（行业警戒线 {t['debt_ratio_warn']}%）",
            metric="debt_ratio", value=f"{m.debt_ratio:.1f}%",
            evidence=f"最新资产负债率 {m.debt_ratio:.1f}%",
            transmission_path="杠杆抬升 → 财务弹性下降 → 后续扩张和分红空间受限",
            impact="财务弹性、融资能力",
            source="financial_metrics",
        ))

    if m.profit_yoy < -30:
        risks.append(_build_risk(
            "financial", "high", f"净利润同比下滑 {m.profit_yoy:.1f}%，盈利恶化严重",
            metric="profit_yoy", value=f"{m.profit_yoy:.1f}%",
            evidence=f"最新净利润同比 {m.profit_yoy:.1f}%",
            transmission_path="盈利快速下滑 → 现金创造与估值锚弱化 → 市场预期下修",
            impact="净利润、估值中枢、市场预期",
            source="financial_metrics",
        ))
    elif m.profit_yoy < -10:
        risks.append(_build_risk(
            "financial", "medium", f"净利润同比下滑 {m.profit_yoy:.1f}%",
            metric="profit_yoy", value=f"{m.profit_yoy:.1f}%",
            evidence=f"最新净利润同比 {m.profit_yoy:.1f}%",
            transmission_path="利润增长放缓或下滑 → 盈利弹性减弱 → 估值支撑走弱",
            impact="盈利弹性、估值支撑",
            source="financial_metrics",
        ))

    if m.cash_flow < 0:
        risks.append(_build_risk(
            "financial", "high", f"经营现金流为负 {m.cash_flow:.1f}亿，造血能力不足",
            metric="cash_flow", value=f"{m.cash_flow:.1f}亿",
            evidence=f"最新经营现金流 {m.cash_flow:.1f}亿",
            transmission_path="经营现金流转负 → 外部融资依赖提升 → 投资与分红能力承压",
            impact="现金流安全边际、资本开支、分红能力",
            source="financial_metrics",
        ))

    if m.roe < 3:
        risks.append(_build_risk(
            "financial", "medium", f"ROE 仅 {m.roe:.1f}%，资本回报率低",
            metric="roe", value=f"{m.roe:.1f}%",
            evidence=f"最新 ROE {m.roe:.1f}%",
            transmission_path="资本回报偏低 → 内生增长效率不足 → 长期估值中枢受压",
            impact="资本回报、长期估值",
            source="financial_metrics",
        ))

    if profile and profile.pe_ratio > t["pe_high"]:
        risks.append(_build_risk(
            "market", "high", f"动态 PE {profile.pe_ratio:.1f} 倍，远超行业均值，估值泡沫风险",
            metric="pe_ratio", value=f"{profile.pe_ratio:.1f}",
            evidence=f"当前动态 PE {profile.pe_ratio:.1f} 倍",
            transmission_path="估值显著抬升 → 对业绩兑现要求更高 → 一旦低于预期股价波动放大",
            impact="估值回撤风险、股价波动",
            source="market_quote",
        ))
    elif profile and profile.pe_ratio > t["pe_warn"]:
        risks.append(_build_risk(
            "market", "medium", f"动态 PE {profile.pe_ratio:.1f} 倍，估值偏高",
            metric="pe_ratio", value=f"{profile.pe_ratio:.1f}",
            evidence=f"当前动态 PE {profile.pe_ratio:.1f} 倍",
            transmission_path="估值处于偏高区间 → 安全边际收窄 → 对短期波动更敏感",
            impact="安全边际、短期波动",
            source="market_quote",
        ))

    if len(metrics) >= 3:
        roe_values = [mt.roe for mt in metrics[:3]]
        if all(roe_values[i] < roe_values[i + 1] for i in range(len(roe_values) - 1)):
            risks.append(_build_risk(
                "financial", "medium",
                f"ROE 连续 {len(roe_values)} 期下滑（{roe_values[-1]:.1f}%→{roe_values[0]:.1f}%），盈利能力可能正在恶化",
                metric="roe_trend", value=f"{roe_values[-1]:.1f}%→{roe_values[0]:.1f}%",
                evidence=f"近 {len(roe_values)} 期 ROE 依次为 {' / '.join(f'{v:.1f}%' for v in reversed(roe_values))}",
                transmission_path="ROE 持续回落 → 盈利质量或资产效率下行 → 估值溢价收缩",
                impact="盈利质量、估值溢价",
                source="financial_metrics",
            ))

    return risks


def assess_news_risks(news: list[dict[str, str]], stock_name: str) -> list[RiskItem]:
    """基于新闻关键词识别可落地风险，并输出证据与传导路径"""
    if not news:
        return []

    risks: list[RiskItem] = []
    seen_titles: set[str] = set()
    for item in news[:8]:
        title = _sanitize_external_text(item.get("title", ""), max_len=120)
        content = _sanitize_external_text(item.get("content", ""), max_len=180)
        text = f"{title} {content}"
        normalized_title = title.lower()
        if not title or normalized_title in seen_titles:
            continue
        seen_titles.add(normalized_title)
        wrapped_title = _wrap_external_text(title)
        wrapped_content = _wrap_external_text(content)
        for rule in _NEWS_RULES:
            if any(keyword in text for keyword in rule["keywords"]):
                evidence = f"新闻标题：{wrapped_title}" if wrapped_title else ""
                if wrapped_content:
                    evidence = f"{evidence}；摘要：{wrapped_content}" if evidence else f"摘要：{wrapped_content}"
                risks.append(_build_risk(
                    "news",
                    rule["level"],
                    rule["description"],
                    evidence=evidence,
                    transmission_path=rule["transmission_path"],
                    impact=rule["impact"],
                    source=item.get("source") or item.get("channel") or "news",
                    time=item.get("time", ""),
                ))
                break
    return risks
