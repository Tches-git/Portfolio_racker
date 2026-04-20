"""标签页配置。"""
from __future__ import annotations

RESULT_GROUPS = [
    ("总览", [("核心摘要", "summary"), ("研报正文", "report")]),
    ("分析", [("原始数据", "data"), ("估值模型", "valuation"), ("趋势图表", "trends")]),
    ("诊断", [("运行指标", "metrics"), ("Agent推理链", "agent"), ("RAG记录", "rag"), ("历史记录", "history")]),
]

TAB_SPECS = [item for _, items in RESULT_GROUPS for item in items]


def get_tab_labels() -> list[str]:
    return [label for label, _ in TAB_SPECS]


def get_result_groups() -> list[tuple[str, list[tuple[str, str]]]]:
    return RESULT_GROUPS
