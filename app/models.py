"""金融研报系统数据模型"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PlanItem:
    """Agent 规划步骤"""
    step_id: str
    objective: str
    preferred_tool: str = ""
    status: str = "pending"  # pending / running / done / failed

@dataclass
class ToolCallRecord:
    """工具调用记录（用于 Agent 记忆）"""
    tool_name: str
    args: dict[str, Any] = field(default_factory=dict)
    observation: str = ""
    success: bool = True
    from_cache: bool = False
    attempts: int = 1

@dataclass
class StockProfile:
    """公司基本信息"""
    code: str
    name: str
    industry: str
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    total_shares: float = 0.0
    listing_date: str = ""

@dataclass
class FinancialMetrics:
    """核心财务指标"""
    code: str
    period: str  # 如 "2024Q3"
    revenue: float = 0.0          # 营收（亿元）
    net_profit: float = 0.0       # 净利润（亿元）
    revenue_yoy: float = 0.0     # 营收同比增速 %
    profit_yoy: float = 0.0      # 净利润同比增速 %
    roe: float = 0.0             # ROE %
    gross_margin: float = 0.0    # 毛利率 %
    debt_ratio: float = 0.0      # 资产负债率 %
    cash_flow: float = 0.0       # 经营现金流（亿元）
    total_assets: float = 0.0    # 总资产（亿元）
    total_equity: float = 0.0    # 股东权益（亿元）
    total_liability: float = 0.0 # 总负债（亿元）
    operating_cost: float = 0.0  # 营业成本（亿元）
    cash_and_equivalents: float = 0.0  # 货币资金（亿元）

    def summary(self) -> str:
        return (
            f"[{self.period}] 营收 {self.revenue:.1f}亿(YoY {self.revenue_yoy:+.1f}%) | "
            f"净利润 {self.net_profit:.1f}亿(YoY {self.profit_yoy:+.1f}%) | "
            f"ROE {self.roe:.1f}% | 毛利率 {self.gross_margin:.1f}% | 负债率 {self.debt_ratio:.1f}%"
        )

@dataclass
class RiskItem:
    """风险条目"""
    category: str   # financial / market / industry / news
    level: str      # high / medium / low
    description: str
    metric: str = ""
    value: str = ""
    evidence: str = ""
    transmission_path: str = ""
    impact: str = ""
    source: str = ""
    time: str = ""

@dataclass
class PeerCompany:
    """同行业对比公司"""
    code: str
    name: str
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    roe: float = 0.0
    gross_margin: float = 0.0
    net_margin: float = 0.0
    revenue: float = 0.0
    net_profit: float = 0.0
    revenue_yoy: float = 0.0

@dataclass
class DuPontResult:
    """杜邦分析结果"""
    period: str
    roe: float = 0.0              # ROE %
    net_margin: float = 0.0       # 净利率 %
    asset_turnover: float = 0.0   # 总资产周转率
    equity_multiplier: float = 0.0  # 权益乘数
    computed_roe: float = 0.0     # 分解后的ROE = net_margin * asset_turnover * equity_multiplier

@dataclass
class DCFResult:
    """DCF估值结果"""
    wacc: float = 0.0             # 加权平均资本成本 %
    terminal_growth: float = 0.0  # 永续增长率 %
    fcf_projections: list[dict] = field(default_factory=list)  # 未来5年FCF预测
    terminal_value: float = 0.0   # 终值（亿元）
    enterprise_value: float = 0.0 # 企业价值（亿元）
    equity_value: float = 0.0     # 股权价值（亿元）
    per_share_value: float = 0.0  # 每股价值（元）
    current_price: float = 0.0    # 当前价格（元）
    upside: float = 0.0           # 上涨空间 %
    base_growth_rate: float = 0.0
    sensitivity_matrix: list[list[float]] = field(default_factory=list)
    sensitivity_waccs: list[float] = field(default_factory=list)
    sensitivity_growth_rates: list[float] = field(default_factory=list)
    monte_carlo_summary: dict[str, float] = field(default_factory=dict)

@dataclass
class TrendResult:
    """趋势分析结果"""
    metric_name: str              # 指标名称，如"营收"、"净利润"
    periods: list[str] = field(default_factory=list)   # 年度列表
    values: list[float] = field(default_factory=list)  # 各年度值
    cagr: float = 0.0            # CAGR %
    trend_direction: str = ""     # "上升"/"下降"/"波动"

@dataclass
class AnalysisState:
    """分析流程状态"""
    stock_code: str = ""
    stock_name: str = ""
    profile: StockProfile | None = None
    metrics: list[FinancialMetrics] = field(default_factory=list)
    peers: list[PeerCompany] = field(default_factory=list)
    risks: list[RiskItem] = field(default_factory=list)
    news: list[dict[str, str]] = field(default_factory=list)
    sections: dict[str, str] = field(default_factory=dict)   # section_id -> 内容
    reviews: dict[str, dict] = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)
    dupont: list[DuPontResult] = field(default_factory=list)
    dcf: DCFResult | None = None
    trends: list[TrendResult] = field(default_factory=list)
    balance_sheets: list[dict] = field(default_factory=list)  # 资产负债表原始数据
    final_report: str = ""
    plan: list[PlanItem] = field(default_factory=list)
    tool_memory: list[ToolCallRecord] = field(default_factory=list)
    reflection: str = ""
    run_metrics: dict[str, Any] = field(default_factory=dict)

    def log(self, text: str) -> None:
        self.trace.append(text)
