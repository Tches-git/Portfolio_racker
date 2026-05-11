# 金融消息追踪平台升级方案

## 一、目标定位

当前项目的核心能力是 A 股金融研报生成。下一阶段不建议推倒重来，而是把它升级为：

**金融消息追踪平台：持续跟踪股票、行业、公告、新闻、研报观点和市场异动，把碎片消息转成可检索、可解释、可追踪的研究事件流，并在必要时触发深度研报更新。**

这样可以保留现有能力：

- ReAct Agent 研究与写作链路
- RAG 与 Graph RAG 检索能力
- 金融工具链、DCF、风险识别、量化评分
- 历史记忆与报告对比
- FastAPI + Next.js 产品前端
- 质量评测、回归、质量门禁

平台升级的核心不是“多做一个新闻页”，而是形成：

```text
消息采集 -> 事件标准化 -> 去重聚合 -> 影响分析 -> 时间线/预警 -> 研究任务/研报更新
```

## 二、产品形态

### 1. 自选股/组合监控

用户可以维护关注股票池，例如：

- 白酒组合
- 银行组合
- 新能源组合
- 半导体组合
- 自定义重点跟踪股票

系统定时或手动抓取：

- 公司公告
- 交易所披露
- 新闻
- 券商研报摘要
- 行情快照
- 异动信息

每只股票形成自己的消息流和事件时间线。

### 2. 消息聚合与去重

同一事件可能来自多个来源，例如“贵州茅台提价”可能同时出现在公告、新闻和研报点评中。

平台需要把这些碎片合并成一个结构化事件，并保留：

- 原始标题
- 来源渠道
- 发布时间
- 链接
- 摘要
- 可信度
- 是否来自 fallback 来源
- 相关来源列表

### 3. 事件分类与影响判断

消息进入系统后，需要被归类为研究事件。

建议事件类型：

- `earnings`：业绩/预告/快报
- `announcement`：公司公告
- `filing`：交易所披露
- `regulation`：监管/问询/处罚
- `shareholder`：股东变动/回购/减持
- `product_price`：产品价格/提价/降价
- `capacity_order`：产能/订单/交付
- `industry_policy`：行业政策
- `risk_sentiment`：风险舆情
- `broker_view`：券商观点/评级
- `market_move`：行情异动
- `other`：其他

每个事件需要输出：

- 影响方向：利好 / 利空 / 中性 / 不确定
- 影响等级：高 / 中 / 低
- 影响范围：基本面 / 估值 / 短期情绪 / 行业景气 / 风险暴露
- 置信度
- 一句话解释“为什么重要”

### 4. 风险与机会雷达

每只股票需要能快速看到：

- 近 24 小时高影响事件
- 近 7 天核心利好
- 近 7 天核心风险
- 反复出现的风险主题
- 和历史研报观点是否冲突
- 是否建议重新生成研报

这部分可以复用现有：

- `app.finance.risk_model`
- `app.memory`
- `app.evals`
- `app.agent.orchestrator`

### 5. 研究任务中心

消息追踪不只是展示信息，还应该触发研究任务。

典型任务：

- 解释一条公告的影响
- 总结过去 7 天某只股票的重要事件
- 判断新事件是否改变估值假设
- 判断新事件是否改变投资建议
- 基于最近事件更新研报

这能把“消息平台”和“研报生成器”自然连接起来。

## 三、建议架构

新增一条 `Tracking Pipeline`：

```text
数据源抓取
  ↓
消息标准化
  ↓
去重/聚合
  ↓
事件分类
  ↓
影响分析
  ↓
时间线/预警/任务
  ↓
触发深度研报或更新摘要
```

建议新增模块：

```text
app/
  tracking/
    __init__.py
    models.py          # MarketEvent / Watchlist / Alert 等模型
    sources.py         # 多来源消息抓取适配
    normalizer.py      # 统一消息结构
    deduper.py         # 标题/内容/时间窗口去重
    classifier.py      # 事件分类、情绪、影响方向
    impact.py          # 对财务/估值/风险/投资观点的影响判断
    timeline.py        # 股票/行业事件时间线
    alerts.py          # 预警规则
    briefing.py        # 每日/每股简报生成
    jobs.py            # 定时/批量追踪任务
```

当前已落地/建议保留的 API：

```text
GET  /api/v1/events
GET  /api/v1/events?mode=history
GET  /api/v1/events/{event_id}
GET  /api/v1/stocks/{stock_code}/events
GET  /api/v1/alerts
GET  /api/v1/briefing/daily
POST /api/v1/watchlists
GET  /api/v1/watchlists
POST /api/v1/events/{event_id}/analyze
```

建议新增前端页面：

```text
frontend/src/app/events/page.tsx
frontend/src/app/events/[eventId]/page.tsx
frontend/src/app/watchlist/page.tsx
frontend/src/app/alerts/page.tsx
frontend/src/app/briefing/page.tsx
frontend/src/app/stocks/[stockCode]/timeline/page.tsx
```

## 四、核心数据模型

### MarketEvent

```python
@dataclass
class MarketEvent:
    event_id: str
    stock_code: str
    stock_name: str
    title: str
    summary: str
    source: str
    provider: str
    url: str
    published_at: str
    collected_at: str
    event_type: str
    sentiment: str        # positive / negative / neutral / uncertain
    impact_level: str     # high / medium / low
    impact_scope: str     # fundamentals / valuation / sentiment / industry / risk
    confidence: float
    reason: str
    related_sources: list[dict]
    is_duplicate: bool = False
    parent_event_id: str = ""
```

### Watchlist

```python
@dataclass
class Watchlist:
    watchlist_id: str
    name: str
    stock_codes: list[str]
    description: str = ""
    created_at: str = ""
    updated_at: str = ""
```

### Alert

```python
@dataclass
class TrackingAlert:
    alert_id: str
    stock_code: str
    event_id: str
    alert_type: str       # high_impact / repeated_risk / thesis_conflict / report_refresh
    title: str
    message: str
    severity: str         # high / medium / low
    status: str           # open / acknowledged / resolved
    created_at: str
```

## 五、MVP 实施方案

### Phase 1：消息事件流

目标：先把项目从“只生成研报”升级为“能持续展示金融事件流”。

范围：

- 新增 `MarketEvent` 数据结构
- 复用现有 `live_tools` 获取公告、新闻、行情、研报来源
- 新增 `normalizer`，统一转成事件
- 新增简单去重逻辑
- 新增 `/api/v1/events`
- 新增 `/api/v1/stocks/{stock_code}/events`
- 前端新增消息流页面和单股票事件时间线

验收标准：

- 可以看到全市场事件列表
- 可以按股票查看事件时间线
- 每条事件有来源、时间、摘要、类型
- 不影响现有研报生成、runs、exports
- 全量测试通过

### Phase 2：事件分类与影响分析

当前进展：已扩展规则分类，覆盖业绩、公告、监管、行业政策、市场异动、研报观点、风险舆情，并在事件详情页展示影响等级、影响方向、影响范围、置信度和判断理由。

目标：让事件不只是消息，而是研究对象。

范围：

- 新增 `classifier.py`
- 基于规则 + LLM fallback 判断事件类型
- 输出影响方向、影响等级、影响范围、置信度
- 新增“为什么重要”解释
- 事件详情页展示影响分析

验收标准：

- 每条事件都有分类和影响标签
- 高影响事件可以被筛选
- 分类失败时有明确降级状态
- 事件分析结果可被后续研报更新链路读取

### Phase 3：Watchlist 与预警中心

当前进展：已完成轻量预警中心和 Watchlist 闭环，支持默认组合、创建组合、组合级事件/预警概览，并暴露 `/api/v1/watchlists`、`/api/v1/alerts` 与前端 `/watchlist`、`/alerts` 页面。

目标：让用户围绕关注股票持续追踪。

范围：

- 新增 watchlist 模型和 API
- 新增组合/自选股页面
- 新增高影响事件 alert
- 新增重复风险 alert
- 新增研报更新建议 alert
- 运行任务中心接入事件触发入口

验收标准：

- 用户可以维护关注股票列表
- 预警中心可以展示待处理事件
- 高影响事件可以触发“生成点评”或“更新研报”
- 股票详情页可以展示近期风险/机会雷达

### Phase 4：每日简报与研究闭环

当前进展：已完成每日简报骨架和事件触发研究入口，支持关键事件、风险/利空统计、今日主题、人工复核事件、建议动作，并可从事件详情/预警/简报触发研报更新任务。

目标：形成完整研究工作流。

范围：

- 新增每日简报 `briefing.py`
- 支持按全市场、watchlist、单股票生成简报
- 支持基于事件生成轻量点评
- 支持基于事件触发研报更新
- 将事件和历史 memory 对比，识别观点漂移

验收标准：

- 可以生成“今日最重要的 5 件事”
- 可以生成单股票最近 7 天事件摘要
- 可以判断是否需要更新研报
- 事件能沉淀到 memory 或 report context

### Phase 5：事件历史沉淀

当前进展：已新增轻量本地事件历史，采集事件会写入 `tracking_events.json`，支持按股票、来源、事件类型、影响等级和时间范围查询，并可通过 `/api/v1/events?mode=history` 查看历史事件。

后续方向：

- 将历史查询接入更多图表和趋势统计
- 增加事件与历史研报观点的漂移对比
- 将事件历史从 JSON 平滑迁移到 SQLite

## 六、前端页面设计建议

### 首页：追踪工作台

首屏应从“生成研报”调整为“今日金融追踪工作台”。

核心区块：

- 今日新增事件数
- 高影响事件数
- 需要复核的股票数
- 建议更新研报的股票数
- 最新高影响事件
- 自选股事件概览
- 最近运行任务

### 事件流页面

支持筛选：

- 股票代码
- 行业
- 来源
- 事件类型
- 影响方向
- 影响等级
- 时间范围

每条事件卡片展示：

- 标题
- 股票
- 来源
- 发布时间
- 类型标签
- 影响标签
- 一句话解释
- 相关来源数

### 股票事件时间线

展示：

- 按时间排序的事件
- 高影响事件突出显示
- 同类事件聚合
- 风险/机会分组
- 触发研报更新按钮

### 预警中心

展示：

- 高影响事件
- 重复风险
- 和历史投资观点冲突的事件
- 需要人工复核的低置信事件
- 建议更新研报的股票

### 每日简报

展示：

- 全市场简报
- 自选股简报
- 行业简报
- 单股票简报

## 七、评测与质量指标

新增指标：

### 数据与来源指标

- `event_count`
- `source_count`
- `source_coverage`
- `duplicate_event_rate`
- `fallback_source_rate`

### 分类与影响指标

- `classified_event_rate`
- `high_impact_event_count`
- `low_confidence_event_count`
- `event_type_distribution`
- `sentiment_distribution`

### 预警指标

- `alert_count`
- `high_severity_alert_count`
- `repeated_risk_alert_count`
- `report_refresh_suggestion_count`

### 研究闭环指标

- `event_to_report_reference_count`
- `event_absorption_rate`
- `thesis_conflict_count`
- `report_refresh_trigger_rate`

## 八、技术风险与约束

### 1. 数据源稳定性

免费公开源字段变化频繁，需要：

- 缓存
- fallback
- 错误分类
- 来源降级披露

### 2. 去重难度

同一事件可能标题不同、来源不同、发布时间不同。MVP 阶段先使用轻量策略：

- 股票代码一致
- 标题关键词相似
- 发布时间在固定窗口内
- 事件类型一致

后续再引入 embedding 相似度。

### 3. LLM 成本

不要对每条消息都调用 LLM。建议：

- 规则优先
- 只对高价值/低置信事件调用 LLM
- 批量分类
- 缓存分类结果

### 4. 平台边界

平台应定位为研究辅助，不应输出确定性投资建议。所有页面要保留：

- 来源信息
- 置信度
- 数据降级说明
- 人工复核入口

## 九、推荐第一步

最建议先做：

**Phase 1：消息事件流 + 单股票事件时间线。**

具体任务：

1. 新建 `app/tracking/models.py`
2. 新建 `app/tracking/normalizer.py`
3. 将现有 `live_tools` 的公告、新闻、研报、行情结果转成 `MarketEvent`
4. 新增 `/api/v1/events`
5. 新增 `/api/v1/stocks/{stock_code}/events`
6. 前端新增 `/events`
7. 前端新增 `/stocks/[stockCode]/timeline`
8. 补测试：normalizer、API route、前端 contract

这一步完成后，项目就会从“单次研报生成器”变成“有持续追踪入口的金融研究平台”。
