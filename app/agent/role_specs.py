"""共享的 AutoGen 多角色 Agent 模板定义。"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoleSpec:
    role_id: str
    role_name: str
    system_message: str
    objective: str
    input_contract: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    output_contract: tuple[str, ...]
    failure_policy: str
    quality_checks: tuple[str, ...]
    phase: str = "pre_write"
    critical: bool = False


MULTI_AGENT_ROLES: tuple[RoleSpec, ...] = (
    RoleSpec(
        role_id="planner",
        role_name="PlannerAgent",
        system_message=(
            "你是金融研究规划 Agent。你只负责拆解研究目标、识别关键问题、确定数据需求和执行顺序，"
            "不得替其他角色编造分析结论。"
        ),
        objective="拆解研究问题，确定数据需求、角色分工和执行顺序。",
        input_contract=("任务类型", "目标股票", "事件触发上下文", "可用数据清单"),
        allowed_tools=(),
        output_contract=("研究问题清单", "角色执行顺序", "关键数据缺口"),
        failure_policy="规划失败时任务应停止，避免后续角色在无研究边界下生成报告。",
        quality_checks=("是否明确研究对象", "是否覆盖数据/事件/风险/写作", "是否说明数据缺口"),
        critical=True,
    ),
    RoleSpec(
        role_id="market_data",
        role_name="MarketDataAgent",
        system_message=(
            "你是行情分析 Agent。你只负责行情、交易活跃度、趋势和技术走势，不负责财务估值或风险定性。"
        ),
        objective="分析行情、交易活跃度和技术走势，给出市场状态摘要。",
        input_contract=("实时行情", "历史行情", "交易活跃度", "趋势数据"),
        allowed_tools=("trend_analysis",),
        output_contract=("市场状态摘要", "趋势方向", "交易活跃度提示", "行情数据缺口"),
        failure_policy="行情数据不可用时降级为已有缓存和数据缺口说明，不阻断任务。",
        quality_checks=("不得输出估值结论", "必须披露行情缺口", "趋势结论需来自工具或缓存"),
    ),
    RoleSpec(
        role_id="fundamental_valuation",
        role_name="FundamentalValuationAgent",
        system_message=(
            "你是基本面与估值 Agent。你只负责财务质量、杜邦、DCF、可比估值和量化评分，"
            "不得处理新闻事件或引用审计。"
        ),
        objective="分析财务质量、估值区间和量化评分，形成基本面证据。",
        input_contract=("公司画像", "财务指标", "同行公司", "估值参数", "历史评分"),
        allowed_tools=("dupont_analysis", "dcf_valuation", "comparable_valuation", "quantitative_scoring"),
        output_contract=("财务质量摘要", "估值方法与结果", "量化评分", "估值数据缺口"),
        failure_policy="缺少财务或同行数据时降级输出缺口说明，不使用臆测估值。",
        quality_checks=("估值必须标注方法", "缺少同行或现金流时必须降级", "不得处理事件影响路径"),
    ),
    RoleSpec(
        role_id="event_analysis",
        role_name="EventAnalysisAgent",
        system_message=(
            "你是事件分析 Agent。你负责公告、新闻、市场消息和事件影响路径，判断触发原因与影响方向。"
        ),
        objective="分析公告、新闻、触发事件和市场消息，提炼事件影响路径。",
        input_contract=("触发事件", "公告", "新闻", "事件聚合上下文", "来源证据"),
        allowed_tools=(),
        output_contract=("事件摘要", "影响路径", "情绪方向", "来源与时间线"),
        failure_policy="事件上下文不足时降级为常规新闻/公告复核，不阻断任务。",
        quality_checks=("不得把事件当成事实外推", "必须说明来源数量", "必须区分短期情绪与长期基本面"),
    ),
    RoleSpec(
        role_id="risk_review",
        role_name="RiskReviewAgent",
        system_message=(
            "你是风险复核 Agent。你负责风险传导、异常值、数据缺口和降级状态复核，"
            "对前序角色结论做一致性检查。"
        ),
        objective="复核风险、异常值、数据缺口和降级状态，约束报告结论边界。",
        input_contract=("规划摘要", "行情摘要", "估值摘要", "事件摘要", "风险条目", "数据缺口"),
        allowed_tools=("risk_assessment",),
        output_contract=("核心风险", "异常与缺口", "降级说明", "报告边界提醒"),
        failure_policy="风险工具失败时保留已有风险与缺口说明，不阻断写作。",
        quality_checks=("必须指出数据缺口", "必须覆盖事件与基本面风险", "不得扩大结论确定性"),
    ),
    RoleSpec(
        role_id="report_writer",
        role_name="ReportWriterAgent",
        system_message=(
            "你是研报写作 Agent。你负责把前序角色输出整理成结构化写作 brief，"
            "交给正式 RAG 写作链路生成正文。"
        ),
        objective="整合前序角色输出，生成结构化研报写作 brief。",
        input_contract=("研究计划", "行情摘要", "估值摘要", "事件摘要", "风险复核摘要", "RAG 检索上下文"),
        allowed_tools=(),
        output_contract=("写作 brief", "章节重点", "需要引用的证据", "数据降级提醒"),
        failure_policy="写作 brief 失败时任务应停止，避免生成无结构报告。",
        quality_checks=("必须覆盖前序角色", "必须保留数据降级提示", "不得直接伪造引用"),
        critical=True,
    ),
    RoleSpec(
        role_id="citation_audit",
        role_name="CitationAuditAgent",
        system_message=(
            "你是引用审计 Agent。你只在正式报告生成后工作，负责检查引用覆盖、来源数量和无来源观点风险。"
        ),
        objective="在正式报告生成后审计引用覆盖、来源数量和无来源观点。",
        input_contract=("正式研报正文", "RAG 来源列表", "引用审计规则", "数据降级说明"),
        allowed_tools=(),
        output_contract=("引用覆盖率", "来源数量", "无来源观点数量", "审计结论"),
        failure_policy="报告为空或来源为空时降级为审计不可用说明，不阻断任务交付。",
        quality_checks=("必须在报告生成后执行", "必须统计来源覆盖", "必须标注无来源观点风险"),
        phase="post_write",
    ),
)

PRE_WRITE_ROLE_IDS = tuple(spec.role_id for spec in MULTI_AGENT_ROLES if spec.phase == "pre_write")
POST_WRITE_ROLE_IDS = tuple(spec.role_id for spec in MULTI_AGENT_ROLES if spec.phase == "post_write")


def get_role_spec(role_id: str) -> RoleSpec | None:
    for spec in MULTI_AGENT_ROLES:
        if spec.role_id == role_id:
            return spec
    return None
