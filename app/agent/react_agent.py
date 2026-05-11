"""ReAct Agent — Planning + Acting + Reflection 三阶段推理"""
from __future__ import annotations
import json
import logging
import re
from dataclasses import dataclass, field
from typing import Callable

from app.config import MAX_AGENT_STEPS, MAX_OBSERVATION_TOKENS, MAX_TOOL_HISTORY_MESSAGES
from app.llm import chat, chat_json, chat_with_tools
from app.models import AblationConfig, AnalysisState, PlanItem
from app.agent.tools import (
    Tool, _make_tools, format_tools_prompt,
    execute_tool, tools_to_function_specs,
)

logger = logging.getLogger("fin.agent.react")

StepCallback = Callable[[str, str, dict], None]


@dataclass
class AgentStep:
    """单步推理记录"""
    step_num: int
    thought: str = ""
    action: str = ""
    action_input: dict = field(default_factory=dict)
    observation: str = ""
    from_cache: bool = False


@dataclass
class AgentResult:
    """Agent 执行结果"""
    answer: str
    steps: list[AgentStep] = field(default_factory=list)
    total_steps: int = 0
    plan: list[PlanItem] = field(default_factory=list)
    reflection: str = ""


PLANNING_PROMPT = """你是一个专业的金融研究Agent。请对以下研究任务进行规划。

## 任务
{task}

请输出 JSON 格式的研究计划，包含 5-10 个步骤。每个步骤包含：
- step_id: 步骤编号 (如 "S1")
- objective: 该步骤的目标
- preferred_tool: 推荐使用的工具名称

## 可用工具
{tools_prompt}

## 输出格式
```json
[
  {{"step_id": "S1", "objective": "获取公司基本信息", "preferred_tool": "fetch_stock_profile"}},
  {{"step_id": "S2", "objective": "获取多年财务数据", "preferred_tool": "fetch_financials"}}
]
```

注意：合理规划顺序，先采集数据再做分析。"""


REACT_SYSTEM = """你是一个专业的金融研究Agent。你通过\"思考-行动-观察\"循环来完成任务。

## 推理格式（严格遵守）

每一步必须按以下格式输出：

Thought: [你的思考过程，分析当前信息，决定下一步行动]
Action: [工具名称]
Action Input: [JSON格式的参数，如 {{"code": "600519"}} 或 {{}}]

当你收集了足够信息可以回答时，输出：

Thought: [最终总结思考]
Final Answer: [你的最终分析结论]

## 重要规则
1. 每次只能调用一个工具
2. Action Input 必须是合法 JSON
3. 根据观察结果决定下一步，不要重复调用已成功的工具
4. 如果工具结果显示 [缓存]，说明已有该数据，直接使用即可
5. 充分利用 rag_query 工具获取专业金融知识来辅助分析

## Final Answer 要求
你的最终回答必须是一份 **2000字以上的深度分析结论**，不要只罗列数字。具体要求：

### 必须覆盖的分析维度（缺一不可）：
1. **商业模式定性**：公司靠什么赚钱？护城河是什么？与竞争对手的本质差异是什么？
2. **增长逻辑拆解**：营收增长靠量还是靠价？利润增长靠经营杠杆还是降本？增长是否可持续？拐点在哪？
3. **盈利质量判断**：经营现金流能否覆盖净利润？应收账款/存货是否异常？是否存在利润粉饰迹象？
4. **杜邦分析解读**：ROE是靠高利润率（品牌溢价）、高周转（运营效率）、还是高杠杆（财务冒险）驱动的？这种模式是否健康可持续？
5. **估值锚定**：DCF隐含的增长预期与实际增长能力是否匹配？相对同行的PE/PB溢价是否合理？
6. **风险传导路径**：不要只列风险名称，要分析\"如果A发生→导致B→对财务指标C产生X%的影响\"
7. **明确投资建议**：给出买入/持有/卖出判断，附核心理由和关键假设

### 分析质量标准：
- 每个论点必须引用至少一个具体数字
- 禁止使用空洞套话
- 对比分析必须有对比对象（同行/历史/行业均值）
- 趋势判断必须有时间维度

## 研究计划
{plan_text}

## 已完成的步骤
{memory_text}

{tools_prompt}
"""


REFLECTION_PROMPT = """你是一个资深金融研究主管。请审查以下研究过程和结果。

## 研究任务
{task}

## 研究计划
{plan_text}

## Agent 推理步骤
{steps_text}

## 当前结论
{conclusion}

## 已采集数据概览
- 公司信息: {has_profile}
- 财务数据: {n_metrics} 期
- 同行对比: {n_peers} 家
- 新闻: {n_news} 条
- 杜邦分析: {has_dupont}
- DCF估值: {has_dcf}
- 趋势分析: {has_trends}
- 风险评估: {n_risks} 项
- 量化评分: {has_scores}
- RAG知识: {has_rag}

## 请回答以下问题（JSON 格式）：
```json
{{
  "is_complete": true/false,
  "missing_items": ["缺失项1", "缺失项2"],
  "quality_score": 1-10,
  "suggestions": ["建议1", "建议2"],
  "summary": "整体评价"
}}
```"""


class ReActAgent:
    """三阶段推理 Agent：Planning → Acting → Reflection"""

    def __init__(self, role: str = "research", max_steps: int = MAX_AGENT_STEPS,
                 on_step: StepCallback | None = None, ablation_config: AblationConfig | None = None):
        self.role = role
        self.max_steps = max_steps
        self.on_step = on_step or (lambda *_: None)
        self.ablation_config = ablation_config or AblationConfig()

    def run(self, task: str, state: AnalysisState) -> AgentResult:
        tools = _make_tools(state)
        tools_prompt = format_tools_prompt(tools)

        self.on_step("planning", "正在制定研究计划...", {"role": self.role})
        plan = self._plan(task, tools_prompt)
        state.plan = plan

        plan_text = "\n".join(f"- [{p.step_id}] {p.objective} → {p.preferred_tool}" for p in plan)
        self.on_step("plan_ready", f"研究计划: {len(plan)} 步", {"plan": [{"id": p.step_id, "obj": p.objective} for p in plan]})

        steps, answer = self._act(task, tools, tools_prompt, plan_text, state)

        if not self.ablation_config.enable_reflection:
            state.reflection = ""
            self.on_step("reflection_done", "反思已跳过（消融实验）", {"reflection": {}})
            return AgentResult(answer=answer, steps=steps, total_steps=len(steps), plan=plan, reflection="")

        self.on_step("reflecting", "正在反思研究质量...", {"role": self.role})
        reflection = self._reflect(task, plan_text, steps, answer, state)
        state.reflection = reflection.get("summary", "")

        if not reflection.get("is_complete", True) and len(steps) < self.max_steps - 2:
            missing = reflection.get("missing_items", [])
            if missing:
                self.on_step("补充研究", f"发现缺失: {', '.join(missing[:3])}", {})
                extra_steps, extra_answer = self._supplement(missing, tools, tools_prompt, plan_text, state, steps)
                steps.extend(extra_steps)
                if extra_answer:
                    answer = extra_answer

        self.on_step("reflection_done", f"质量评分: {reflection.get('quality_score', '?')}/10", {"reflection": reflection})
        return AgentResult(answer=answer, steps=steps, total_steps=len(steps), plan=plan, reflection=reflection.get("summary", ""))

    def _plan(self, task: str, tools_prompt: str) -> list[PlanItem]:
        prompt = PLANNING_PROMPT.format(task=task, tools_prompt=tools_prompt)
        try:
            result = chat_json(prompt, temperature=0.1, max_tokens=1024)
            if isinstance(result, list):
                return [
                    PlanItem(
                        step_id=item.get("step_id", f"S{i + 1}"),
                        objective=item.get("objective", ""),
                        preferred_tool=item.get("preferred_tool", ""),
                    )
                    for i, item in enumerate(result)
                ]
        except Exception as e:
            logger.warning(f"规划失败: {e}")
        return [
            PlanItem("S1", "获取公司基本信息", "fetch_stock_profile"),
            PlanItem("S2", "获取多年财务数据", "fetch_financials"),
            PlanItem("S3", "获取同行业公司", "fetch_peers"),
            PlanItem("S4", "获取近期新闻", "fetch_news"),
            PlanItem("S5", "杜邦分析", "dupont_analysis"),
            PlanItem("S6", "DCF估值+蒙特卡洛", "dcf_valuation"),
            PlanItem("S7", "可比公司估值", "comparable_valuation"),
            PlanItem("S8", "趋势分析", "trend_analysis"),
            PlanItem("S9", "风险评估", "risk_assessment"),
            PlanItem("S10", "量化评分", "quantitative_scoring"),
        ]

    def _act(self, task: str, tools: list[Tool], tools_prompt: str,
             plan_text: str, state: AnalysisState) -> tuple[list[AgentStep], str]:
        try:
            return self._act_function_calling(task, tools, plan_text, state)
        except Exception as e:
            logger.warning(f"Function calling 模式失败，回退到文本模式: {e}")
            return self._act_text_mode(task, tools, tools_prompt, plan_text, state)

    def _truncate_observation(self, text: str) -> str:
        max_chars = max(200, int(MAX_OBSERVATION_TOKENS * 1.5))
        return text[:max_chars]

    def _trim_function_call_messages(self, messages: list[dict]) -> list[dict]:
        if len(messages) <= MAX_TOOL_HISTORY_MESSAGES:
            return messages
        return [messages[0], messages[1], *messages[-(MAX_TOOL_HISTORY_MESSAGES - 2):]]

    def _act_function_calling(self, task: str, tools: list[Tool],
                              plan_text: str, state: AnalysisState) -> tuple[list[AgentStep], str]:
        tool_specs = tools_to_function_specs(tools)
        messages = [
            {"role": "system", "content": (
                "你是一个专业的金融研究Agent。按照研究计划逐步执行分析。\n\n"
                f"## 研究计划\n{plan_text}\n\n"
                "根据计划调用合适的工具，完成所有步骤后给出综合结论。\n\n"
                "## 最终结论要求\n"
                "完成所有工具调用后，你的最终回答必须是一份深度分析结论，而不是数据摘要。"
            )},
            {"role": "user", "content": task},
        ]
        steps: list[AgentStep] = []

        for step_num in range(1, self.max_steps + 1):
            messages = self._trim_function_call_messages(messages)
            self.on_step("thinking", f"Step {step_num}: 推理中...", {"step": step_num, "role": self.role})
            result = chat_with_tools(messages, tool_specs, temperature=0.3)

            if result["type"] == "message":
                return steps, result["content"]

            if result["type"] == "tool_call":
                tool_name = result["tool"]
                tool_args = result["arguments"]
                step = AgentStep(step_num=step_num, action=tool_name, action_input=tool_args)
                self.on_step("action", f"调用工具: {tool_name}", {"step": step_num, "tool": tool_name, "input": tool_args})

                observation = execute_tool(tools, tool_name, tool_args, state=state)
                step.observation = observation
                step.from_cache = observation.startswith("[缓存]")
                self.on_step("observation", f"工具返回: {observation[:200]}...", {"step": step_num, "result_length": len(observation)})
                steps.append(step)

                observation_text = self._truncate_observation(observation)
                raw_msg = result.get("raw_message")
                if raw_msg and hasattr(raw_msg, "tool_calls") and raw_msg.tool_calls:
                    tc = raw_msg.tool_calls[0]
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [{
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }],
                    })
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": observation_text})
                else:
                    messages.append({"role": "assistant", "content": f"调用工具 {tool_name}，参数: {json.dumps(tool_args, ensure_ascii=False)}"})
                    messages.append({"role": "user", "content": f"工具返回结果:\n{observation_text}"})

        return steps, "达到最大推理步数"

    def _act_text_mode(self, task: str, tools: list[Tool], tools_prompt: str,
                       plan_text: str, state: AnalysisState) -> tuple[list[AgentStep], str]:
        memory_text = self._format_memory(state)
        system = REACT_SYSTEM.format(plan_text=plan_text, memory_text=memory_text, tools_prompt=tools_prompt)
        messages = [task]
        steps: list[AgentStep] = []

        for step_num in range(1, self.max_steps + 1):
            if len(messages) > 13:
                full_prompt = messages[0] + "\n\n[...之前的推理步骤已省略...]\n\n" + "\n\n".join(messages[-12:])
            else:
                full_prompt = "\n\n".join(messages)
            self.on_step("thinking", f"Step {step_num}: 推理中...", {"step": step_num, "role": self.role})
            response = chat(full_prompt, system=system, temperature=0.3, max_tokens=2048)
            step = AgentStep(step_num=step_num)

            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|Final Answer:|$)", response, re.DOTALL)
            if thought_match:
                step.thought = thought_match.group(1).strip()

            final_match = re.search(r"Final Answer:\s*(.*)", response, re.DOTALL)
            if final_match:
                steps.append(step)
                self.on_step("final", step.thought, {"step": step_num})
                return steps, final_match.group(1).strip()

            action_match = re.search(r"Action:\s*(\w+)", response)
            input_match = re.search(r"Action Input:\s*(\{.*?\})", response, re.DOTALL)
            if not action_match:
                logger.warning(f"未解析到 Action: {response[:200]}")
                messages.append(f"Agent 输出格式错误:\n{response}")
                continue

            tool_name = action_match.group(1).strip()
            tool_args = {}
            if input_match:
                try:
                    tool_args = json.loads(input_match.group(1))
                except json.JSONDecodeError:
                    tool_args = {}

            step.action = tool_name
            step.action_input = tool_args
            self.on_step("action", f"调用工具: {tool_name}", {"step": step_num, "tool": tool_name, "input": tool_args})

            observation = execute_tool(tools, tool_name, tool_args, state=state)
            step.observation = observation
            step.from_cache = observation.startswith("[缓存]")
            self.on_step("observation", f"工具返回: {observation[:200]}...", {"step": step_num, "result_length": len(observation)})
            steps.append(step)

            observation_text = self._truncate_observation(observation)
            messages.append(response)
            messages.append(f"Observation: {observation_text}")

        return steps, "达到最大推理步数，未能完成分析"

    def _reflect(self, task: str, plan_text: str, steps: list[AgentStep], answer: str, state: AnalysisState) -> dict:
        steps_text = "\n\n".join(
            f"Step {s.step_num}\nThought: {s.thought}\nAction: {s.action}\nInput: {json.dumps(s.action_input, ensure_ascii=False)}\nObservation: {self._truncate_observation(s.observation)}"
            for s in steps[:10]
        )
        prompt = REFLECTION_PROMPT.format(
            task=task,
            plan_text=plan_text,
            steps_text=steps_text,
            conclusion=answer[:1500],
            has_profile="是" if state.profile else "否",
            n_metrics=len(state.metrics),
            n_peers=len(state.peers),
            n_news=len(state.news),
            has_dupont="是" if state.dupont else "否",
            has_dcf="是" if state.dcf else "否",
            has_trends="是" if state.trends else "否",
            n_risks=len(state.risks),
            has_scores="是" if state.sections.get("scores") else "否",
            has_rag="是" if any("rag" in r.tool_name for r in state.tool_memory) else "否",
        )
        try:
            result = chat_json(prompt, temperature=0.1, max_tokens=768)
            if isinstance(result, dict):
                return result
        except Exception as e:
            logger.warning(f"反思失败: {e}")
        return {"is_complete": True, "quality_score": 7, "summary": "研究已基本完成"}

    def _supplement(self, missing: list[str], tools: list[Tool],
                    tools_prompt: str, plan_text: str,
                    state: AnalysisState, existing_steps: list[AgentStep]) -> tuple[list[AgentStep], str]:
        supplement_task = (
            f"以下研究项目尚未完成，请补充：\n" + "\n".join(f"- {m}" for m in missing[:3]) + "\n\n请调用相应工具完成这些分析，然后给出 Final Answer。"
        )
        try:
            return self._supplement_function_calling(supplement_task, tools, plan_text, state, existing_steps)
        except Exception as e:
            logger.warning(f"补充研究 function calling 失败，回退文本模式: {e}")
        return self._supplement_text_mode(supplement_task, tools, tools_prompt, plan_text, state, existing_steps)

    def _supplement_function_calling(self, task: str, tools: list[Tool], plan_text: str,
                                     state: AnalysisState, existing_steps: list[AgentStep]) -> tuple[list[AgentStep], str]:
        tool_specs = tools_to_function_specs(tools)
        messages = [
            {"role": "system", "content": "你是一个专业的金融研究Agent。请补充完成未完成的研究项目。\n\n" f"## 研究计划\n{plan_text}\n\n调用合适的工具完成补充分析，然后给出综合结论。"},
            {"role": "user", "content": task},
        ]
        steps: list[AgentStep] = []
        start_num = len(existing_steps) + 1

        for step_num in range(start_num, start_num + 3):
            messages = self._trim_function_call_messages(messages)
            result = chat_with_tools(messages, tool_specs, temperature=0.3)
            if result["type"] == "message":
                return steps, result["content"]
            if result["type"] == "tool_call":
                tool_name = result["tool"]
                tool_args = result["arguments"]
                step = AgentStep(step_num=step_num, action=tool_name, action_input=tool_args)
                observation = execute_tool(tools, tool_name, tool_args, state=state)
                step.observation = observation
                steps.append(step)
                observation_text = self._truncate_observation(observation)
                raw_msg = result.get("raw_message")
                if raw_msg and hasattr(raw_msg, "tool_calls") and raw_msg.tool_calls:
                    tc = raw_msg.tool_calls[0]
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [{"id": tc.id, "type": "function", "function": {"name": tc.function.name, "arguments": tc.function.arguments}}],
                    })
                    messages.append({"role": "tool", "tool_call_id": tc.id, "content": observation_text})
                else:
                    messages.append({"role": "assistant", "content": f"调用工具 {tool_name}"})
                    messages.append({"role": "user", "content": f"工具返回结果:\n{observation_text}"})
        return steps, ""

    def _supplement_text_mode(self, task: str, tools: list[Tool], tools_prompt: str,
                              plan_text: str, state: AnalysisState, existing_steps: list[AgentStep]) -> tuple[list[AgentStep], str]:
        memory_text = self._format_memory(state)
        system = REACT_SYSTEM.format(plan_text=plan_text, memory_text=memory_text, tools_prompt=tools_prompt)
        messages = [task]
        steps: list[AgentStep] = []
        start_num = len(existing_steps) + 1

        for step_num in range(start_num, start_num + 3):
            full_prompt = "\n\n".join(messages)
            response = chat(full_prompt, system=system, temperature=0.3, max_tokens=1536)
            step = AgentStep(step_num=step_num)
            thought_match = re.search(r"Thought:\s*(.*?)(?=Action:|Final Answer:|$)", response, re.DOTALL)
            if thought_match:
                step.thought = thought_match.group(1).strip()
            final_match = re.search(r"Final Answer:\s*(.*)", response, re.DOTALL)
            if final_match:
                steps.append(step)
                return steps, final_match.group(1).strip()
            action_match = re.search(r"Action:\s*(\w+)", response)
            input_match = re.search(r"Action Input:\s*(\{.*?\})", response, re.DOTALL)
            if not action_match:
                messages.append(f"Agent 输出格式错误:\n{response}")
                continue
            tool_name = action_match.group(1).strip()
            tool_args = {}
            if input_match:
                try:
                    tool_args = json.loads(input_match.group(1))
                except json.JSONDecodeError:
                    tool_args = {}
            step.action = tool_name
            step.action_input = tool_args
            observation = execute_tool(tools, tool_name, tool_args, state=state)
            step.observation = observation
            steps.append(step)
            messages.append(response)
            messages.append(f"Observation: {self._truncate_observation(observation)}")
        return steps, ""

    def _format_memory(self, state: AnalysisState) -> str:
        if not state.tool_memory:
            return "暂无已完成步骤"
        lines = []
        for record in state.tool_memory[-10:]:
            status = "成功" if record.success else "失败"
            lines.append(f"- {record.tool_name}: {status}")
        return "\n".join(lines)
