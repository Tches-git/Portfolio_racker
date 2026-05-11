# 项目改进建议

> 本文档列出了金融研报智能分析系统的改进建议，按优先级排列。不涉及 API Key 安全问题（需单独处理）。
> 
> 状态标记：✅ 已修复 | ⚠️ 部分修复 | ❌ 未解决

---

## P0 - 必须修复

### 1. ✅ 异常被静默吞掉

**状态：已修复**

所有 `except Exception: pass` 模式已替换为 `logger.warning()` 记录异常。`akshare_client.py` 和 `knowledge_base.py` 中的全部异常处理点已添加日志输出。全项目已无 bare `except: pass`（仅 `config.py` 中 `dotenv` 可选导入的 `pass` 属正常模式）。

---

## P1 - 高优先级

### 2. ⚠️ 测试覆盖不足

**状态：部分修复** — 测试文件从 5 个增至 9 个，但核心模块仍有缺口。

**已覆盖（新增）：**

| 测试文件 | 覆盖模块 |
|----------|----------|
| `test_circuit_breaker.py` | 熔断器状态机（CLOSED/OPEN/HALF_OPEN） |
| `test_llm.py` | LLM 重试逻辑、JSON 解析、Provider 拒绝处理 |
| `test_reranker.py` | 重排序缓存命中 |
| `test_valuation.py` | 蒙特卡洛 DCF 分布特性、百分位排序 |

**仍缺失测试的模块：**

| 模块 | 文件 | 重要程度 |
|------|------|----------|
| ReAct Agent | `app/agent/react_agent.py` | 极高 — 核心推理引擎 |
| 编排器 | `app/agent/orchestrator.py` | 高 — 流程控制中枢 |
| Tracer | `app/utils/tracer.py` | 中 |
| 记忆存储 | `app/memory/store.py` | 中 |
| 记忆对比 | `app/memory/comparator.py` | 中 |

**建议：**
- 优先为 `react_agent.py` 编写 mock 测试，验证规划/执行/反思三阶段流转
- 为 `orchestrator.py` 编写集成测试，mock 数据源和 LLM 调用

---

### 3. ⚠️ 清理死代码

**状态：部分修复** — `async_fetch.py` 已删除，`app/agents/` 目录中的桩文件已删除，但目录本身（含空 `__init__.py` 和 `__pycache__`）仍存在。

**待处理：**
- 删除整个 `app/agents/` 目录（含 `__init__.py` 和 `__pycache__`）

---

### 4. ❌ Token 限制管理缺失

**状态：未解决**

**风险点：**

- `app/agent/orchestrator.py` 报告生成 prompt 嵌入所有财务表格、研究结论、RAG 上下文、历史数据，总量可能超出模型上下文窗口
- `app/agent/react_agent.py` 文本模式已有滑动窗口（保留最后 12 条消息），但 Function Calling 模式无上下文裁剪
- 观测结果截断为 3000 字符，但字符数不等于 token 数

**建议：**
- 引入 token 计数工具（如 `tiktoken` 或按中文字符 1:1.5 估算）
- 在调用前检查总 token 数，超限时按优先级截断：先截 RAG 上下文 → 再截历史数据 → 最后截财务细节
- 为 Function Calling 模式添加与文本模式类似的上下文裁剪机制

---

## P2 - 中优先级

### 5. ✅ 线程安全问题

**状态：已修复**

- `app/llm.py`：`TokenStats` 已添加 `threading.Lock()`，`record()` 和 `summary()` 均在锁内操作。Provider 单例使用 `_provider_lock` 双重检查锁定。
- `app/rag/reranker.py`：`_rerank_cache_lock` 保护所有缓存读写和淘汰操作。
- `app/utils/tracer.py`：`_lock` 一致保护 span stack、spans 列表、record 方法、summary 快照。全局活跃 tracer 有独立的 `_tracer_lock`。

**遗留注意事项：** `orchestrator.py` 的 `_prefetch_data` 中线程内直接修改 `state` 字段，当前因 `.result()` 等待而碰巧安全，但设计上脆弱。如果未来修改执行顺序需注意。

---

### 6. ✅ 蒙特卡洛模拟性能优化

**状态：已修复**

`valuation.py` 的蒙特卡洛 DCF 已完全 numpy 向量化：
- 增长率矩阵通过广播计算
- FCF 矩阵使用 `np.cumprod`
- 折现因子向量化
- 无 Python for 循环遍历模拟次数

---

### 7. ✅ URL 注入风险

**状态：已修复**

`akshare_client.py` 已导入 `from urllib.parse import quote`，新闻查询 URL 使用 `quote(name)` 编码。

---

### 8. ❌ YoY 增长率计算逻辑重复

**状态：未解决**

同一段同比增长率计算逻辑仍在 `akshare_client.py` 中出现 3 次：
- `_fetch_ths_financials` 约第 309-317 行
- `_enrich_with_eastmoney` 约第 468-477 行
- `_fetch_sina_financials` 约第 569-578 行

**建议：** 提取为私有方法：
```python
def _calc_yoy_growth(self, metrics: list[FinancialMetrics]) -> None:
    """为财务数据列表计算同比增长率"""
    for curr in metrics:
        curr_year = curr.period[:4]
        prev_period = str(int(curr_year) - 1) + curr.period[4:]
        prev = next((m for m in metrics if m.period == prev_period), None)
        if prev and prev.revenue > 0 and curr.revenue_yoy == 0:
            curr.revenue_yoy = round((curr.revenue / prev.revenue - 1) * 100, 2)
        if prev and prev.net_profit and curr.profit_yoy == 0:
            curr.profit_yoy = round((curr.net_profit / prev.net_profit - 1) * 100, 2)
```

---

### 9. ⚠️ LLM Provider 响应缺少防御性检查

**状态：部分修复** — 智谱 Provider 已修复，OpenAI Provider 未修复。

- `zhipu_provider.py`：已添加 `choices` 空值检查和 `content` 空值检查 ✅
- `openai_provider.py`：仍直接访问 `resp.choices[0].message.content`，无空值防御 ❌

**建议：** 在 `openai_provider.py` 的 `chat` 和 `chat_with_tools` 方法中添加与智谱 Provider 相同的防御检查：
```python
if not getattr(resp, "choices", None):
    raise ValueError("LLM 返回空 choices")
content = resp.choices[0].message.content
if not content:
    raise ValueError("LLM 返回空响应")
```

---

### 10. ⚠️ 数据预取与工具执行双重路径

**状态：当前实现可接受，但存在维护风险**

`orchestrator.py` 的 `_prefetch_data` 将结果写入 `state.tool_memory`，后续 Agent 工具调用可命中缓存。设计上是双路径，但通过缓存机制避免了重复请求。如果未来修改工具函数的返回格式或参数，需同步修改预取逻辑。

---

## P3 - 低优先级

### 11. ✅ 魔法数字散落各处

**状态：大部分已修复**

`config.py` 已集中定义 18+ 参数，包括缓存 TTL、熔断器参数、嵌入批大小、DCF/蒙特卡洛参数等，均支持环境变量覆盖。

**仍硬编码的次要值：**
- `embeddings.py`：`batch_size = 16` 未使用 `config.EMBED_BATCH_SIZE`
- `react_agent.py`：`max_steps=15` 默认值、观测截断 `3000` 字符

---

### 12. ✅ 输出文件互相覆盖

**状态：已修复**

旧 Python Web 入口已移除；CLI 与 API 统一通过 `app.exports.storage.save_output_files()` 按股票代码和时间戳写入导出物，避免固定文件名覆盖。

**建议：** 文件名加入股票代码和时间戳：
```python
filename = f"report_{stock_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
```

---

### 13. ❌ RAG 查询未并行化

**状态：未解决**

`orchestrator.py` 的 `_write_report_with_rag` 中 5 个主题 RAG 查询仍串行执行。

**建议：** 使用 `ThreadPoolExecutor` 并行执行：
```python
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(kb.query, q, top_k=3, candidate_k=10, use_rerank=True): q for q in queries}
    rag_results = {f.result(): futures[f] for f in as_completed(futures)}
```

---

### 14. ❌ Prompt 注入防护

**状态：未解决**

外部数据（新闻标题、财务数据、知识库文档）直接嵌入 LLM prompt，无任何隔离。

**涉及位置：**
- `app/agent/orchestrator.py`：研究任务和报告生成 prompt
- `app/finance/risk_model.py`：新闻标题和内容注入风险评估 prompt
- `app/rag/reranker.py`：文档内容嵌入重排序 prompt（已截断至 300 字符，降低了攻击面）

**建议：**
- 对外部文本添加分隔标记：`<external_data>...</external_data>`
- 在 system prompt 中指示模型仅将标记内容作为数据处理
- 对新闻标题做基本清洗（去除异常长度、特殊控制字符）

---

### 15. ⚠️ 工具函数成功/失败不可区分

**状态：部分修复**

`execute_tool` 包装层已区分四种状态（成功、缓存命中 `[缓存]`、关键失败 `[关键工具失败]`、非关键失败 `[非关键]`），`Tool` dataclass 新增 `critical` 字段。但单个工具函数内部仍返回 `f"获取失败: {e}"` 字符串，无法程序化区分成功与失败。

**建议：** 工具函数在失败时抛出异常，由 `execute_tool` 统一捕获并格式化：
```python
# 工具函数
def fetch_stock_profile(stock_code: str) -> str:
    profile = client.get_stock_profile(stock_code)  # 失败自然抛异常
    return format_profile(profile)

# execute_tool 捕获
try:
    result = tool.func(**args)
except Exception as e:
    result = f"[{'关键工具失败' if tool.critical else '非关键'}] {tool.name}: {e}"
```

---

### 16. ⚠️ Web/API 访问控制仍需部署层治理

**状态：部分修复**

旧 Python Web 应用已移除；当前 Web 入口切换为 FastAPI + Next.js。API 层已有基础 actor/role header 用于运行治理，但面向非本地部署时仍需要网关、认证或反向代理访问控制。

**建议（若部署到非本地环境）：**
- API 网关或反向代理（Nginx）层面的 Basic Auth / OAuth
- 为 `/api/v1/runs*` 增加真实用户鉴权与限流
- 按用户/工作区隔离运行任务与额度

---

## 改进进度总览

| 状态 | 数量 | 项目编号 |
|------|------|----------|
| ✅ 已修复 | 6 | #1, #5, #6, #7, #11, #12 |
| ⚠️ 部分修复 | 6 | #2, #3, #9, #10, #15, #16 |
| ❌ 未解决 | 4 | #4, #8, #13, #14 |

---

*文档创建：2026-04-09 | 最后更新：2026-04-10*
