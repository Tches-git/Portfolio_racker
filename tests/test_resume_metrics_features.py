from __future__ import annotations

from pathlib import Path

import app.api.server as server
from app.evals.agent_eval import evaluate_agent_tasks, expand_agent_tasks, load_agent_benchmark, run_agent_eval
from app.evals.financial_qa_eval import _answer_key_hit, evaluate_financial_qa, load_financial_qa_benchmark, load_financial_qa_predictions, run_financial_qa_eval
from app.evals.rag_eval import evaluate_rag_citations
from app.evals.tracking_benchmark_builder import build_real_tracking_benchmark, samples_from_source_items
from app.evals.tracking_eval import evaluate_tracking_pipeline, expand_samples, load_tracking_benchmark, run_tracking_eval
from app.finance.event_backtest import build_event_backtest
from app.tracking.models import MarketEvent
from app.db.repositories import save_user_events
from tests.helpers import multi_user_client


def _bars() -> list[dict]:
    return [
        {"date": f"2026-01-{day:02d}", "open": 100 + day, "high": 102 + day, "low": 99 + day, "close": 100 + day, "volume": 1000 + day}
        for day in range(1, 20)
    ]


def test_tracking_eval_loads_benchmark_and_outputs_metrics(tmp_path):
    samples = load_tracking_benchmark()
    result = evaluate_tracking_pipeline(samples)

    assert result["sample_count"] >= 20
    assert result["dedupe"]["f1"] >= 0
    assert result["event_type_macro_f1"] >= 0

    persisted = run_tracking_eval(output_dir=tmp_path)
    assert Path(str(persisted["json_path"])).exists()
    assert Path(str(persisted["markdown_path"])).exists()


def test_tracking_eval_supports_larger_reproducible_sample_set(tmp_path):
    samples = load_tracking_benchmark()
    expanded = expand_samples(samples, target_count=500)
    result = evaluate_tracking_pipeline(expanded)

    assert len(expanded) == 500
    assert result["sample_count"] == 500
    assert result["alert_positive_count"] > 0
    assert result["alert_negative_count"] > 0

    first = run_tracking_eval(output_dir=tmp_path, target_count=500)
    second = run_tracking_eval(output_dir=tmp_path, target_count=1000)
    assert first["sample_count"] == 500
    assert second["sample_count"] == 1000
    assert first["json_path"] != second["json_path"]
    assert Path(str(first["json_path"])).exists()
    assert Path(str(second["json_path"])).exists()


def test_agent_eval_loads_benchmark_and_outputs_metrics(tmp_path):
    tasks = load_agent_benchmark()
    result = evaluate_agent_tasks(tasks)

    assert result["sample_count"] >= 80
    assert result["task_success_rate"] >= 0
    assert result["required_tool_coverage"] > 0
    assert result["trace_completeness_rate"] > 0

    persisted = run_agent_eval(output_dir=tmp_path, target_count=48)
    assert persisted["sample_count"] == 48
    assert Path(str(persisted["json_path"])).exists()
    assert Path(str(persisted["markdown_path"])).exists()


def test_agent_eval_supports_larger_reproducible_sample_set(tmp_path):
    tasks = load_agent_benchmark()
    expanded = expand_agent_tasks(tasks, target_count=500)
    result = evaluate_agent_tasks(expanded)

    assert len(expanded) == 500
    assert result["sample_count"] == 500
    assert result["task_type_counts"]
    assert result["difficulty_counts"]

    first = run_agent_eval(output_dir=tmp_path, target_count=300)
    second = run_agent_eval(output_dir=tmp_path, target_count=500)
    assert first["sample_count"] == 300
    assert second["sample_count"] == 500
    assert first["json_path"] != second["json_path"]


def test_agent_eval_handles_empty_samples():
    result = evaluate_agent_tasks([])

    assert result["sample_count"] == 0
    assert result["task_success_rate"] == 0
    assert result["required_tool_coverage"] == 0


def test_real_tracking_benchmark_builder_uses_public_metadata(tmp_path):
    items = [
        ("600000", {"title": "公司发布年度报告 净利润增长", "summary": "年度报告披露利润增长", "source": "cninfo", "provider": "cninfo", "channel": "announcement", "time": "2026-04-01", "link": "https://example.test/a"}),
        ("600000", {"title": "公司收到监管问询函", "summary": "交易所要求说明事项", "source": "交易所", "provider": "exchange", "channel": "filing", "time": "2026-04-02", "link": "https://example.test/b"}),
    ]

    samples = samples_from_source_items(items)

    assert len(samples) == 2
    assert samples[0]["label_source"] == "heuristic_from_public_metadata"
    assert samples[0]["needs_human_review"] is True
    assert {sample["expected_event_type"] for sample in samples} >= {"earnings", "regulation"}


def test_build_real_tracking_benchmark_reads_cache(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "announcement_cninfo_600000_2.json").write_text(
        '{"items":[{"title":"公司回购股份实施进展公告","summary":"回购股份","source":"cninfo","provider":"cninfo","channel":"announcement","time":"2026-04-01","link":"https://example.test/r"}]}',
        encoding="utf-8",
    )
    output = tmp_path / "tracking_events_real.jsonl"

    result = build_real_tracking_benchmark(output_path=output, cache_dir=cache_dir, target_count=10)

    assert result.sample_count == 1
    assert output.exists()
    assert "tracking_events_real" in output.name


def test_financial_qa_eval_supports_public_dataset_shapes(tmp_path):
    benchmark = tmp_path / "financebench_subset.jsonl"
    benchmark.write_text(
        "\n".join([
            '{"id":"fb_1","doc_name":"10k_a","question":"What was revenue?","answer":"$10 million","evidence":"The company reported revenue of $10 million."}',
            '{"id":"finqa_1","qa":{"question":"净利润是多少？","answer":"5亿元"},"pre_text":["公司披露"],"table":[["净利润","5亿元"]],"post_text":["同比增长"]}',
            '{"table":[["Metric","Value"],["ROE","12%"]],"paragraphs":[{"text":"ROE was 12%."}],"questions":[{"uid":"tat_1","question":"What was ROE?","answer":"12%"}]}',
        ]),
        encoding="utf-8",
    )
    predictions = tmp_path / "predictions.jsonl"
    predictions.write_text(
        "\n".join([
            '{"sample_id":"fb_1","prediction":"$10 million","cited_source_ids":["10k_a"]}',
            '{"sample_id":"finqa_1","prediction":"5亿元","cited_source_ids":["finqa_doc_2"]}',
            '{"sample_id":"tat_1","prediction":"12%","cited_source_ids":["tatqa_doc_3"]}',
        ]),
        encoding="utf-8",
    )

    samples = load_financial_qa_benchmark(benchmark)
    preds = load_financial_qa_predictions(predictions)
    result = evaluate_financial_qa(samples, preds)
    persisted = run_financial_qa_eval(benchmark_path=benchmark, predictions_path=predictions, output_dir=tmp_path)

    assert len(samples) == 3
    assert result["answer_exact_match"] == 1.0
    assert result["answer_key_hit_rate"] == 1.0
    assert result["context_answer_hit_rate"] == 1.0
    assert persisted["sample_count"] == 3
    assert Path(str(persisted["json_path"])).exists()


def test_financial_qa_key_hit_handles_financial_answer_formats():
    assert _answer_key_hit("$1,577", "$1577.00")
    assert _answer_key_hit("8.738", "$8.70")
    assert _answer_key_hit("No; quick ratio is below 1x.", "No. The quick ratio was 0.96.")
    assert not _answer_key_hit("Cannot be determined", "-0.02")


def test_event_backtest_computes_windows():
    event = MarketEvent(event_id="e1", stock_code="600519", title="业绩增长", published_at="2026-01-03", event_type="earnings", impact_level="high")
    payload = build_event_backtest(stock_code="600519", events=[event], daily_bars=_bars())

    assert payload["matched_event_count"] == 1
    assert payload["items"][0]["returns"]["t1"] != 0
    assert payload["groups"][0]["event_count"] == 1


def test_event_backtest_api_is_user_scoped(monkeypatch):
    monkeypatch.setattr(server, "get_stock_daily_bars", lambda stock_code, days=180: _bars())
    with multi_user_client() as (client, _users, Session):
        with Session() as db:
            save_user_events(db, user_id="user-alice", events=[
                MarketEvent(event_id="alice-event", stock_code="600519", title="业绩增长", published_at="2026-01-03", event_type="earnings", impact_level="high")
            ])

        alice = client.get("/api/v1/stocks/600519/event-backtest", headers={"X-Test-User": "alice"})
        bob = client.get("/api/v1/stocks/600519/event-backtest", headers={"X-Test-User": "bob"})

    assert alice.status_code == 200
    assert alice.json()["matched_event_count"] == 1
    assert bob.status_code == 200
    assert bob.json()["matched_event_count"] == 0


def test_rag_eval_counts_citation_coverage():
    report = "公司收入增长 12%，据年报披露盈利改善。\n估值仍有上行空间，需关注风险。"
    refs = [{"title": "年报披露盈利改善", "source": "年报", "summary": "收入增长 12%"}]

    payload = evaluate_rag_citations(report, refs, stock_code="600519")

    assert payload["source_reference_count"] == 1
    assert payload["claim_count"] >= 1
    assert payload["citation_coverage_rate"] > 0


def test_quality_workbench_requires_login_and_returns_metrics():
    with multi_user_client() as (client, _users, _Session):
        response = client.get("/api/v1/ui/quality", headers={"X-Test-User": "alice"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["test_count"] >= 1
    assert payload["metrics"]
    assert "agent_eval" in payload
    assert "financial_qa_eval" in payload
