# 评测与 Benchmark 接入说明

本项目的评测分为三层，简历中应明确区分，避免把项目内样本写成公开权威 benchmark。

## 1. 真实事件样本

从公开公告、新闻、研报观点等来源元数据生成事件样本：

```bash
python main.py build-tracking-benchmark \
  --stock-codes 600519,300750,002594,000858,600036 \
  --target-count 150 \
  --live
```

输出默认写入：

```text
data/benchmarks/tracking_events_real.jsonl
```

评测真实样本时不要做扩展：

```bash
python main.py tracking-eval \
  --benchmark data/benchmarks/tracking_events_real.jsonl \
  --no-expand
```

注意：该文件由公开来源元数据和启发式规则生成，字段 `needs_human_review=true` 表示标签仍需人工复核。简历中可以写“构建真实事件初始样本与复核流程”，不要写成“150 条人工标注事件”。

## 2. 公共金融 QA/RAG Benchmark

仓库不直接内置 FinanceBench、FinQA、TAT-QA 数据本体。建议从官方来源下载后抽取本地子集，再运行：

```bash
python main.py finance-qa-predict \
  --benchmark data/benchmarks/public/financebench_open_source_full.jsonl \
  --limit 50 \
  --output output/evals/financebench_50_predictions.jsonl

python main.py finance-qa-eval \
  --benchmark data/benchmarks/public/financebench_open_source_full.jsonl \
  --predictions output/evals/financebench_50_predictions.jsonl \
  --limit 50
```

评测会同时输出严格 `Exact Match`、`Token-F1` 和更适合金额/Yes-No/短语答案的 `关键答案命中率`。简历中优先写清楚样本来源和规模，不要把 smoke 子集结果包装成完整 FinanceBench 分数。

最近一次本地实测口径：

- FinanceBench open-source 公开文件：150 条样本已接入本地评测流程。
- 完整 150 条无预测评测：仅统计检索上下文覆盖，答案命中率为 68.0%。
- 50 条预测子集：关键答案命中率 76.0%，相对同一子集上下文答案命中率 72.0% 提升 4.0 个百分点；严格 Exact Match 26.0%，Token-F1 39.9%，引用覆盖率 100.0%。
- 上述结果是本地 open-source 子集评测，不等同完整 FinanceBench 官方榜单成绩。

支持的输入形态：

- FinanceBench 风格：`id/question/answer/evidence/doc_name`
- FinQA 风格：`id/qa/pre_text/table/post_text`
- TAT-QA 风格：`table/paragraphs/questions`
- 通用 JSONL：`sample_id/question/answer/context/source_ids`

没有 `--predictions` 时，评测只统计上下文答案命中，不计算真实生成准确率。

## 3. 项目内 Agent 任务评测

Agent 任务集位于：

```text
data/benchmarks/agent_tasks.jsonl
```

当前包含 80+ 条任务模板，覆盖事件点评、风险复核、组合预警、行情解释、数据源降级、研报更新和引用审计等场景：

```bash
python main.py agent-eval
python main.py agent-eval --target-count 500
```

该评测是项目内金融研究 Agent 任务评测，不等同 GAIA、SWE-bench 等公开通用 Agent benchmark。
