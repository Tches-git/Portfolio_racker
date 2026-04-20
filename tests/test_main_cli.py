from __future__ import annotations

import types

import main


def test_main_defaults_to_analysis(monkeypatch):
    called = {}

    def fake_run_analysis(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_analysis", fake_run_analysis)

    assert main.main(["600519", "--eval"]) == 0
    assert called["argv"] == ["600519", "--eval"]


def test_main_dispatches_analyze_subcommand(monkeypatch):
    called = {}

    def fake_run_analysis(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_analysis", fake_run_analysis)

    assert main.main(["analyze", "000858"]) == 0
    assert called["argv"] == ["000858"]


def test_main_dispatches_script_subcommand(monkeypatch):
    monkeypatch.setattr(main, "_dispatch_script", lambda module_name, argv: 0 if module_name == "scripts.regression" and argv == ["--llm-judge"] else 1)

    assert main.main(["regression", "--llm-judge"]) == 0


def test_main_dispatches_web(monkeypatch):
    called = {}

    def fake_run_web(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(main, "_run_web", fake_run_web)

    assert main.main(["web", "--server.headless=true"]) == 0
    assert called["argv"] == ["--server.headless=true"]


def test_dispatch_script_calls_module_main(monkeypatch):
    module = types.SimpleNamespace(main=lambda argv: 7)
    monkeypatch.setattr(main.importlib, "import_module", lambda name: module)

    assert main._dispatch_script("scripts.ablation", ["--stocks", "600519"]) == 7


def test_analyze_parser_accepts_legacy_and_optional_flags():
    args = main.build_analyze_parser().parse_args(["600519", "--eval", "--mc-sims", "500"])

    assert args.code == "600519"
    assert args.eval is True
    assert args.mc_sims == 500
