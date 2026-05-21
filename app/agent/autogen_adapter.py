"""AutoGen AgentChat 运行时适配层。

该模块只负责把项目现有 OpenAI-compatible 配置转换为 AutoGen 的模型客户端。
真实多角色流程在 ``multi_agent.py`` 中保持同步、可测试；当 AutoGen 依赖未安装时，
系统仍能通过本地降级流程完成任务并保留相同 trace 结构。
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.config import LLM_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL
from app.agent.role_specs import MULTI_AGENT_ROLES


@dataclass
class AutoGenRuntime:
    """AutoGen 运行时信息。"""

    available: bool
    mode: str
    model: str
    base_url: str = ""
    error: str = ""
    model_client: Any | None = None
    agents: list[Any] | None = None


def create_autogen_runtime() -> AutoGenRuntime:
    """创建 AutoGen AgentChat runtime。

    返回值永远可用：依赖不存在或模型配置缺失时不会抛错，而是返回
    ``available=False``，由多 Agent 工作流记录降级状态。
    """

    if not OPENAI_API_KEY:
        return AutoGenRuntime(
            available=False,
            mode="autogen_graphflow_fallback",
            model=LLM_MODEL,
            base_url=OPENAI_BASE_URL,
            error="OPENAI_API_KEY 未配置，AutoGen runtime 已降级为本地编排",
        )

    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
    except Exception as exc:
        return AutoGenRuntime(
            available=False,
            mode="autogen_graphflow_fallback",
            model=LLM_MODEL,
            base_url=OPENAI_BASE_URL,
            error=f"AutoGen 依赖不可用: {exc}",
        )

    kwargs: dict[str, Any] = {"model": LLM_MODEL, "api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    if _requires_custom_model_info(LLM_MODEL):
        kwargs["model_info"] = {
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "gpt-5",
            "structured_output": True,
            "multiple_system_messages": True,
        }
    try:
        client = OpenAIChatCompletionClient(**kwargs)
    except Exception as exc:
        return AutoGenRuntime(
            available=False,
            mode="autogen_graphflow_fallback",
            model=LLM_MODEL,
            base_url=OPENAI_BASE_URL,
            error=f"AutoGen client 初始化失败: {exc}",
        )
    return AutoGenRuntime(
        available=True,
        mode="autogen_graphflow",
        model=LLM_MODEL,
        base_url=OPENAI_BASE_URL,
        model_client=client,
        agents=_build_agentchat_agents(client),
    )


def _requires_custom_model_info(model: str) -> bool:
    normalized = (model or "").lower()
    known_prefixes = ("gpt-4", "gpt-3.5", "o1", "o3", "o4", "chatgpt")
    return not normalized.startswith(known_prefixes)


def _build_agentchat_agents(model_client: Any) -> list[Any]:
    try:
        from autogen_agentchat.agents import AssistantAgent
    except Exception:
        return []
    agents: list[Any] = []
    for spec in MULTI_AGENT_ROLES:
        system_message = (
            f"{spec.system_message}\n\n"
            f"目标：{spec.objective}\n"
            f"输入契约：{'；'.join(spec.input_contract)}\n"
            f"工具边界：{', '.join(spec.allowed_tools) if spec.allowed_tools else '不调用工具'}\n"
            f"输出契约：{'；'.join(spec.output_contract)}\n"
            f"失败策略：{spec.failure_policy}\n"
            f"质量检查：{'；'.join(spec.quality_checks)}"
        )
        agents.append(
            AssistantAgent(
                name=spec.role_name,
                model_client=model_client,
                description=spec.objective,
                system_message=system_message,
            )
        )
    return agents
