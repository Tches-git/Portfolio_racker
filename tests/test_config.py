from __future__ import annotations

import importlib

import pytest

import app.config as config


def test_validate_runtime_config_reports_invalid_provider(monkeypatch):
    monkeypatch.setattr(config, "LLM_PROVIDER", "invalid")
    errors = config.validate_runtime_config()
    assert any("LLM_PROVIDER" in err for err in errors)


def test_validate_runtime_config_reports_bad_thresholds(monkeypatch):
    monkeypatch.setattr(config, "MAX_AGENT_STEPS", 0)
    monkeypatch.setattr(config, "MC_SIMULATIONS", 0)
    monkeypatch.setattr(config, "DCF_DEFAULT_WACC", 2.0)
    monkeypatch.setattr(config, "DCF_DEFAULT_TERMINAL_GROWTH", 3.0)
    errors = config.validate_runtime_config()
    assert any("MAX_AGENT_STEPS" in err for err in errors)
    assert any("MC_SIMULATIONS" in err for err in errors)
    assert any("DCF_DEFAULT_WACC" in err for err in errors)


def test_ensure_runtime_config_requires_api_key(monkeypatch):
    monkeypatch.setattr(config, "LLM_PROVIDER", "zhipu")
    monkeypatch.setattr(config, "ZHIPUAI_API_KEY", "")
    with pytest.raises(RuntimeError, match="ZHIPUAI_API_KEY"):
        config.ensure_runtime_config(require_api_key=True)
