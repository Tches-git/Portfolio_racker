from __future__ import annotations

from app.ui.tabs import get_result_groups, get_tab_labels


def test_get_tab_labels_contains_summary_and_report():
    labels = get_tab_labels()

    assert labels[0] == "核心摘要"
    assert "研报正文" in labels
    assert labels[-1] == "历史记录"


def test_get_result_groups_organizes_tabs_by_layer():
    groups = get_result_groups()

    assert groups[0][0] == "总览"
    assert [label for label, _ in groups[0][1]] == ["核心摘要", "研报正文"]
    assert groups[-1][0] == "诊断"
