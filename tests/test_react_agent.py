from __future__ import annotations

import app.agent.react_agent as react_mod
from app.models import AblationConfig, AnalysisState, PlanItem


def test_react_agent_reflects_and_supplements(monkeypatch):
    plan = [PlanItem(step_id="S1", objective="获取信息", preferred_tool="fetch_stock_profile")]
    main_steps = [react_mod.AgentStep(step_num=1, action="fetch_stock_profile", action_input={}, observation="ok")]
    extra_steps = [react_mod.AgentStep(step_num=2, action="fetch_news", action_input={}, observation="news")]

    monkeypatch.setattr(react_mod, "_make_tools", lambda state: [])
    monkeypatch.setattr(react_mod, "format_tools_prompt", lambda tools: "tools")
    monkeypatch.setattr(react_mod.ReActAgent, "_plan", lambda self, task, tools_prompt: plan)
    monkeypatch.setattr(react_mod.ReActAgent, "_act", lambda self, task, tools, tools_prompt, plan_text, state: (main_steps, "初始结论"))
    monkeypatch.setattr(
        react_mod.ReActAgent,
        "_reflect",
        lambda self, task, plan_text, steps, answer, state: {
            "is_complete": False,
            "missing_items": ["近期新闻"],
            "quality_score": 6,
            "summary": "需要补充新闻",
        },
    )
    monkeypatch.setattr(
        react_mod.ReActAgent,
        "_supplement",
        lambda self, missing, tools, tools_prompt, plan_text, state, steps: (extra_steps, "补充后的结论"),
    )

    events: list[str] = []
    agent = react_mod.ReActAgent(on_step=lambda event, detail, info: events.append(event))
    result = agent.run("task", AnalysisState(stock_code="600519"))

    assert result.answer == "补充后的结论"
    assert result.total_steps == 2
    assert result.reflection == "需要补充新闻"
    assert "reflecting" in events
    assert "reflection_done" in events


def test_react_agent_skips_supplement_when_complete(monkeypatch):
    plan = [PlanItem(step_id="S1", objective="获取信息", preferred_tool="fetch_stock_profile")]
    main_steps = [react_mod.AgentStep(step_num=1, action="fetch_stock_profile", action_input={}, observation="ok")]

    monkeypatch.setattr(react_mod, "_make_tools", lambda state: [])
    monkeypatch.setattr(react_mod, "format_tools_prompt", lambda tools: "tools")
    monkeypatch.setattr(react_mod.ReActAgent, "_plan", lambda self, task, tools_prompt: plan)
    monkeypatch.setattr(react_mod.ReActAgent, "_act", lambda self, task, tools, tools_prompt, plan_text, state: (main_steps, "最终结论"))
    monkeypatch.setattr(
        react_mod.ReActAgent,
        "_reflect",
        lambda self, task, plan_text, steps, answer, state: {
            "is_complete": True,
            "quality_score": 8,
            "summary": "已完成",
        },
    )

    called = {"supplement": False}

    def _supplement(*args, **kwargs):
        called["supplement"] = True
        return [], ""

    monkeypatch.setattr(react_mod.ReActAgent, "_supplement", _supplement)

    agent = react_mod.ReActAgent()
    result = agent.run("task", AnalysisState(stock_code="600519"))

    assert result.answer == "最终结论"
    assert result.total_steps == 1
    assert result.reflection == "已完成"
    assert called["supplement"] is False


def test_react_agent_skips_reflection_when_disabled(monkeypatch):
    plan = [PlanItem(step_id="S1", objective="获取信息", preferred_tool="fetch_stock_profile")]
    main_steps = [react_mod.AgentStep(step_num=1, action="fetch_stock_profile", action_input={}, observation="ok")]

    monkeypatch.setattr(react_mod, "_make_tools", lambda state: [])
    monkeypatch.setattr(react_mod, "format_tools_prompt", lambda tools: "tools")
    monkeypatch.setattr(react_mod.ReActAgent, "_plan", lambda self, task, tools_prompt: plan)
    monkeypatch.setattr(react_mod.ReActAgent, "_act", lambda self, task, tools, tools_prompt, plan_text, state: (main_steps, "最终结论"))

    called = {"reflect": False}

    def _reflect(*args, **kwargs):
        called["reflect"] = True
        return {"summary": "不应执行"}

    monkeypatch.setattr(react_mod.ReActAgent, "_reflect", _reflect)

    events: list[str] = []
    agent = react_mod.ReActAgent(
        on_step=lambda event, detail, info: events.append(event),
        ablation_config=AblationConfig(enable_reflection=False),
    )
    result = agent.run("task", AnalysisState(stock_code="600519"))

    assert result.answer == "最终结论"
    assert result.total_steps == 1
    assert result.reflection == ""
    assert called["reflect"] is False
    assert "reflecting" not in events
    assert "reflection_done" in events
