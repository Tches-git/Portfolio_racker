# 金融 Agent 任务评测语料



## 来源

- 本地 Agent 任务集：`data/benchmarks/agent_tasks.jsonl`

- 用途：多 Agent 工具覆盖、Trace 完整性、异常降级和引用要求评测。



## 任务条目

Agent 任务样本：任务 ID agent_001，任务类型 event_review，难度 medium。任务描述：根据近期重大公告判断是否需要更新研报，并说明影响路径。。期望工具：fetch_announcements, rag_query, risk_assessment。期望输出：事件摘要, 影响判断, 建议动作, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_002，任务类型 risk_review，难度 hard。任务描述：复核一条监管关注事件的风险等级，判断是否需要进入人工复核。。期望工具：fetch_exchange_filings, fetch_news, risk_assessment。期望输出：风险等级, 触发原因, 人工复核建议, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_003，任务类型 briefing_summary，难度 medium。任务描述：为组合生成当日研究简报，突出高影响事件和待处理事项。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：今日主题, 关键事件, 待处理事项, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_004，任务类型 market_explain，难度 medium。任务描述：解释单只股票当日明显波动，结合行情和公开信息给出可能原因。。期望工具：fetch_live_quotes, fetch_news, fetch_announcements。期望输出：行情变化, 可能原因, 风险提示, 数据状态。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_005，任务类型 portfolio_alert，难度 hard。任务描述：识别组合内多只股票同时出现的风险共振，并给出优先处理顺序。。期望工具：fetch_news, fetch_exchange_filings, risk_assessment。期望输出：受影响股票, 共振原因, 优先级, 建议动作。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_006，任务类型 data_fallback，难度 easy。任务描述：当行情源不可用时，给出降级后的研究结论和数据可用性提示。。期望工具：fetch_live_quotes, fetch_news, rag_query。期望输出：降级说明, 可用数据, 不确定性提示, 下一步动作。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_007，任务类型 report_update，难度 hard。任务描述：基于事件和历史研报判断是否需要更新估值假设。。期望工具：fetch_financials, dcf_valuation, rag_query。期望输出：需更新假设, 估值影响, 证据来源, 更新建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_008，任务类型 event_review，难度 medium。任务描述：对券商观点变化进行事件点评，区分事实、观点和可验证数据。。期望工具：fetch_broker_reports, fetch_live_quotes, rag_query。期望输出：事实摘要, 观点变化, 验证数据, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_009，任务类型 risk_review，难度 medium。任务描述：检查舆情风险是否已经传导到基本面假设。。期望工具：fetch_news, fetch_financials, risk_assessment。期望输出：舆情摘要, 基本面传导, 风险等级, 跟踪建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_010，任务类型 briefing_summary，难度 easy。任务描述：将组合事件压缩成适合开盘前阅读的简报。。期望工具：fetch_announcements, fetch_live_quotes, rag_query。期望输出：简报摘要, 风险事项, 机会线索, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_011，任务类型 market_explain，难度 medium。任务描述：在缺少新闻匹配时，基于行情和历史信息给出谨慎解释。。期望工具：fetch_live_quotes, fetch_news, trend_analysis。期望输出：行情描述, 解释边界, 不确定性提示, 后续观察。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_012，任务类型 portfolio_alert，难度 medium。任务描述：根据组合内公告密集度识别需要优先复核的公司。。期望工具：fetch_announcements, fetch_exchange_filings, risk_assessment。期望输出：复核名单, 触发依据, 优先级, 处理建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_013，任务类型 report_update，难度 medium。任务描述：围绕利润率变化更新研报中的经营质量判断。。期望工具：fetch_financials, trend_analysis, rag_query。期望输出：利润率变化, 经营质量判断, 来源引用, 更新段落。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_014，任务类型 event_review，难度 easy。任务描述：对一条业绩快报提炼核心信息并判断影响等级。。期望工具：fetch_announcements, fetch_financials, quantitative_scoring。期望输出：核心数据, 影响等级, 对比基准, 建议动作。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_015，任务类型 risk_review，难度 hard。任务描述：评估行业政策变化对组合持仓的潜在风险。。期望工具：fetch_news, rag_query, risk_assessment。期望输出：政策摘要, 影响范围, 风险等级, 复核建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_016，任务类型 data_fallback，难度 easy。任务描述：当公告源返回空结果时，生成可解释的空态结论。。期望工具：fetch_announcements, fetch_news, rag_query。期望输出：空态原因, 替代来源, 可信度提示, 下一步动作。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_017，任务类型 report_update，难度 hard。任务描述：更新可比公司估值部分，说明估值口径和局限。。期望工具：fetch_stock_profile, fetch_peers, comparable_valuation。期望输出：估值口径, 可比公司, 局限说明, 更新建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_018，任务类型 market_explain，难度 medium。任务描述：结合成交额变化解释事件后的市场关注度。。期望工具：fetch_live_quotes, fetch_news, rag_query。期望输出：成交变化, 关注度判断, 事件关联, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_019，任务类型 briefing_summary，难度 medium。任务描述：从多个事件中整理需要今日人工复核的事项。。期望工具：fetch_news, fetch_exchange_filings, risk_assessment。期望输出：复核事项, 触发规则, 优先级, 负责人建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_020，任务类型 portfolio_alert，难度 hard。任务描述：识别组合内高影响低置信事件，并提示不能直接下结论。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：低置信事件, 原因解释, 人工复核, 数据缺口。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_021，任务类型 event_review，难度 hard。任务描述：把公告、新闻和研报观点合并为一条事件点评。。期望工具：fetch_announcements, fetch_news, fetch_broker_reports。期望输出：多来源摘要, 一致结论, 分歧点, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_022，任务类型 risk_review，难度 medium。任务描述：判断财务指标恶化是否需要触发组合风险预警。。期望工具：fetch_financials, trend_analysis, risk_assessment。期望输出：指标变化, 风险原因, 预警建议, 跟踪指标。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_023，任务类型 data_fallback，难度 medium。任务描述：在券商研报源失败时，使用公开新闻和知识库给出保守总结。。期望工具：fetch_broker_reports, fetch_news, rag_query。期望输出：失败说明, 替代证据, 保守结论, 后续补采。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_024，任务类型 report_update，难度 medium。任务描述：根据风险事件生成研报风险提示段落，并保留证据来源。。期望工具：fetch_news, risk_assessment, rag_query。期望输出：风险段落, 传导路径, 缓释因素, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_025，任务类型 event_review，难度 medium。任务描述：判断同一事件的多条公告是否属于重复披露，并输出合并后的点评。。期望工具：fetch_announcements, rag_query。期望输出：重复判断, 合并摘要, 影响判断, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_026，任务类型 event_review，难度 hard。任务描述：在新闻标题夸张但公告证据不足时，给出保守事件点评。。期望工具：fetch_news, fetch_announcements, risk_assessment。期望输出：事实边界, 证据缺口, 影响判断, 建议动作。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_027，任务类型 event_review，难度 hard。任务描述：对高影响低置信事件进行复核，判断是否应进入预警队列。。期望工具：fetch_news, fetch_exchange_filings, rag_query。期望输出：置信度判断, 预警建议, 复核理由, 来源引用。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_028，任务类型 event_review，难度 medium。任务描述：对业绩说明会公告提取需要后续跟踪的问题。。期望工具：fetch_announcements, fetch_financials, rag_query。期望输出：公告摘要, 跟踪问题, 影响范围, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_029，任务类型 event_review，难度 medium。任务描述：根据回购或增持公告判断其对市场情绪的影响。。期望工具：fetch_announcements, fetch_live_quotes, rag_query。期望输出：事件摘要, 情绪影响, 局限说明, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_030，任务类型 event_review，难度 medium。任务描述：将经营数据公告转化为研报更新任务说明。。期望工具：fetch_announcements, fetch_financials, trend_analysis。期望输出：关键数据, 研报影响, 更新任务, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_031，任务类型 event_review，难度 hard。任务描述：对券商研报标题相近但结论不同的情况整理分歧点。。期望工具：fetch_broker_reports, rag_query。期望输出：共同事实, 分歧点, 需要验证数据, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_032，任务类型 event_review，难度 hard。任务描述：判断一条市场传闻是否足以触发研究任务。。期望工具：fetch_news, fetch_announcements, risk_assessment。期望输出：传闻来源, 证据强度, 触发判断, 人工复核。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_033，任务类型 risk_review，难度 hard。任务描述：在多个风险信号同时出现时，归纳主要风险主线。。期望工具：fetch_news, fetch_exchange_filings, risk_assessment。期望输出：风险主线, 影响链路, 优先级, 复核建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_034，任务类型 risk_review，难度 hard。任务描述：分析公告中的诉讼事项是否影响盈利假设。。期望工具：fetch_announcements, fetch_financials, risk_assessment。期望输出：诉讼摘要, 财务影响, 假设调整, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_035，任务类型 risk_review，难度 hard。任务描述：判断监管处罚是否需要降低事件置信度或提高影响等级。。期望工具：fetch_exchange_filings, fetch_news, risk_assessment。期望输出：监管事实, 影响等级, 置信度说明, 建议动作。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_036，任务类型 risk_review，难度 medium。任务描述：对供应链中断风险进行复核并输出监控指标。。期望工具：fetch_news, fetch_announcements, risk_assessment。期望输出：风险事件, 传导路径, 监控指标, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_037，任务类型 risk_review，难度 medium。任务描述：检查财务杠杆变化是否构成风险提示。。期望工具：fetch_financials, trend_analysis, risk_assessment。期望输出：杠杆变化, 风险等级, 证据来源, 跟踪建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_038，任务类型 risk_review，难度 hard。任务描述：对大额减值公告判断是否需要更新风险段落。。期望工具：fetch_announcements, fetch_financials, risk_assessment。期望输出：减值事项, 利润影响, 风险段落, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_039，任务类型 risk_review，难度 hard。任务描述：在缺少公告原文时，只基于二级来源给出低置信复核结论。。期望工具：fetch_announcements, fetch_news, rag_query。期望输出：低置信说明, 替代证据, 不能确认事项, 下一步动作。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_040，任务类型 risk_review，难度 hard。任务描述：识别政策变化对估值假设的下行风险。。期望工具：fetch_news, rag_query, dcf_valuation。期望输出：政策变化, 估值影响, 风险提示, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_041，任务类型 briefing_summary，难度 medium。任务描述：生成组合晨会简报，优先排列需要人工处理的事项。。期望工具：fetch_news, fetch_announcements, risk_assessment。期望输出：晨会摘要, 待处理事项, 优先级, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_042，任务类型 briefing_summary，难度 medium。任务描述：将前一日事件整理为适合盘后复盘的简报。。期望工具：fetch_live_quotes, fetch_news, fetch_announcements。期望输出：盘后摘要, 行情关联, 风险事项, 数据状态。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_043，任务类型 briefing_summary，难度 easy。任务描述：当组合暂无高影响事件时，生成清晰的无风险空态说明。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：空态说明, 已检查来源, 低影响事件, 后续观察。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_044，任务类型 briefing_summary，难度 medium。任务描述：从多只股票事件中提炼今日主题，并避免重复标题堆砌。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：今日主题, 代表事件, 去重说明, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_045，任务类型 briefing_summary，难度 medium。任务描述：为风险偏好较低的用户生成偏防守的组合简报。。期望工具：fetch_news, risk_assessment, rag_query。期望输出：防守视角, 风险排序, 建议动作, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_046，任务类型 briefing_summary，难度 medium。任务描述：在数据源部分失败时，生成带降级提示的每日简报。。期望工具：fetch_news, fetch_announcements, fetch_live_quotes。期望输出：简报摘要, 失败来源, 可用信息, 不确定性提示。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_047，任务类型 briefing_summary，难度 medium。任务描述：把公告、行情和风险预警合并成一页组合看板摘要。。期望工具：fetch_announcements, fetch_live_quotes, risk_assessment。期望输出：组合摘要, 风险队列, 行情信号, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_048，任务类型 briefing_summary，难度 medium。任务描述：判断今日是否需要生成组合级研报更新任务。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：触发判断, 关键证据, 任务建议, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_049，任务类型 market_explain，难度 medium。任务描述：解释单股上涨但无公告支持的情况，避免过度归因。。期望工具：fetch_live_quotes, fetch_news, fetch_announcements。期望输出：行情事实, 证据不足, 可能解释, 风险提示。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_050，任务类型 market_explain，难度 medium。任务描述：解释放量下跌并关联近期风险事件。。期望工具：fetch_live_quotes, fetch_news, risk_assessment。期望输出：行情变化, 风险关联, 影响判断, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_051，任务类型 market_explain，难度 hard。任务描述：判断行情异动是否只是行业同步波动。。期望工具：fetch_live_quotes, fetch_peers, fetch_news。期望输出：个股表现, 行业对比, 归因判断, 数据状态。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_052，任务类型 market_explain，难度 medium。任务描述：在实时行情接口失败时，用最近日线和公开消息给出解释边界。。期望工具：fetch_live_quotes, fetch_news, trend_analysis。期望输出：降级说明, 可用信息, 解释边界, 后续动作。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_053，任务类型 market_explain，难度 hard。任务描述：根据估值指标和事件判断上涨后的风险收益变化。。期望工具：fetch_live_quotes, dcf_valuation, risk_assessment。期望输出：估值状态, 事件影响, 风险收益, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_054，任务类型 market_explain，难度 medium。任务描述：判断成交额上升是否与研报观点变化有关。。期望工具：fetch_live_quotes, fetch_broker_reports, rag_query。期望输出：成交变化, 观点线索, 证据强度, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_055，任务类型 market_explain，难度 hard。任务描述：解释低波动但预警升高的反常情况。。期望工具：fetch_live_quotes, fetch_exchange_filings, risk_assessment。期望输出：行情状态, 预警原因, 反常解释, 复核建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_056，任务类型 market_explain，难度 hard。任务描述：在行情和新闻方向相反时，输出中性解释。。期望工具：fetch_live_quotes, fetch_news, rag_query。期望输出：冲突信号, 中性判断, 不确定性, 来源引用。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_057，任务类型 portfolio_alert，难度 hard。任务描述：根据组合内同一行业事件密集出现识别主题风险。。期望工具：fetch_news, fetch_announcements, fetch_peers。期望输出：主题风险, 影响股票, 优先级, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_058，任务类型 portfolio_alert，难度 medium。任务描述：把多个低影响事件聚合成组合级观察项。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：观察项, 聚合原因, 影响范围, 处理建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_059，任务类型 portfolio_alert，难度 hard。任务描述：识别组合中需要暂停自动下结论的低置信高影响事件。。期望工具：fetch_news, fetch_exchange_filings, risk_assessment。期望输出：低置信事件, 原因说明, 人工复核, 数据缺口。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_060，任务类型 portfolio_alert，难度 hard。任务描述：判断组合预警是否由单一数据源异常导致。。期望工具：fetch_news, fetch_announcements, fetch_live_quotes。期望输出：异常来源, 交叉验证, 预警结论, 降级说明。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_061，任务类型 portfolio_alert，难度 medium。任务描述：为组合风险队列生成一条可执行的处理顺序。。期望工具：risk_assessment, fetch_news, rag_query。期望输出：处理顺序, 优先级原因, 建议动作, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_062，任务类型 portfolio_alert，难度 easy。任务描述：当组合中没有持仓受到影响时，输出明确的无动作结论。。期望工具：fetch_news, fetch_announcements, risk_assessment。期望输出：无动作结论, 检查范围, 低风险说明, 后续观察。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_063，任务类型 portfolio_alert，难度 hard。任务描述：对同一风险事件影响多只股票的情况生成组合级摘要。。期望工具：fetch_news, fetch_peers, risk_assessment。期望输出：共同事件, 受影响范围, 风险排序, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_064，任务类型 portfolio_alert，难度 medium。任务描述：识别组合中需要触发研报更新的预警。。期望工具：fetch_announcements, risk_assessment, rag_query。期望输出：触发预警, 研报任务, 触发依据, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_065，任务类型 data_fallback，难度 easy。任务描述：行情、公告均不可用时，生成不能继续自动分析的明确提示。。期望工具：fetch_live_quotes, fetch_announcements。期望输出：失败来源, 停止原因, 用户提示, 重试建议。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_066，任务类型 data_fallback，难度 medium。任务描述：知识库检索为空时，仍要输出基于公开数据的有限结论。。期望工具：rag_query, fetch_news, fetch_financials。期望输出：检索空态, 可用数据, 有限结论, 不确定性。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_067，任务类型 data_fallback，难度 medium。任务描述：券商研报接口失败时，避免伪造机构观点。。期望工具：fetch_broker_reports, fetch_news, rag_query。期望输出：失败说明, 不能声称事项, 替代证据, 后续补采。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_068，任务类型 data_fallback，难度 hard。任务描述：财务数据缺口导致估值不可算时，给出替代分析路径。。期望工具：fetch_financials, dcf_valuation, comparable_valuation。期望输出：缺口说明, 估值限制, 替代路径, 用户提示。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_069，任务类型 data_fallback，难度 hard。任务描述：多个来源返回相互矛盾信息时，输出冲突处理说明。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：冲突信息, 可信来源, 暂缓结论, 复核动作。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_070，任务类型 data_fallback，难度 medium。任务描述：当上传文档解析失败时，要求回退到在线来源并提示解析状态。。期望工具：extract_document_summary, fetch_news, rag_query。期望输出：解析失败, 回退来源, 分析边界, 重传建议。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_071，任务类型 data_fallback，难度 medium。任务描述：当基金持仓工具失败时，不把机构行为作为结论依据。。期望工具：fetch_fund_holdings, fetch_news, risk_assessment。期望输出：工具失败, 剔除依据, 替代判断, 风险提示。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_072，任务类型 data_fallback，难度 medium。任务描述：当可比公司样本不足时，说明估值结论不可靠。。期望工具：fetch_peers, comparable_valuation, rag_query。期望输出：样本不足, 估值限制, 保守判断, 后续补充。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_073，任务类型 report_update，难度 medium。任务描述：根据季度经营数据更新研报核心观点。。期望工具：fetch_announcements, fetch_financials, trend_analysis。期望输出：核心变化, 观点更新, 引用证据, 更新段落。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_074，任务类型 report_update，难度 medium。任务描述：将风险事件转化为研报中的风险提示和跟踪指标。。期望工具：fetch_news, risk_assessment, rag_query。期望输出：风险提示, 跟踪指标, 传导路径, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_075，任务类型 report_update，难度 hard。任务描述：当估值模型输入不足时，更新研报中的估值限制说明。。期望工具：fetch_financials, dcf_valuation, rag_query。期望输出：输入缺口, 估值限制, 保守表述, 后续数据。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_076，任务类型 report_update，难度 hard。任务描述：根据行业政策变化更新研报投资逻辑。。期望工具：fetch_news, rag_query, risk_assessment。期望输出：政策影响, 投资逻辑, 风险因素, 来源引用。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_077，任务类型 report_update，难度 medium。任务描述：把事件点评输出改写为正式研报摘要。。期望工具：fetch_announcements, rag_query, trend_analysis。期望输出：研报摘要, 关键依据, 影响判断, 引用来源。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_078，任务类型 report_update，难度 medium。任务描述：根据券商观点变化更新外部一致预期描述。。期望工具：fetch_broker_reports, rag_query, fetch_live_quotes。期望输出：观点变化, 一致预期, 证据来源, 保守说明。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_079，任务类型 report_update，难度 easy。任务描述：在没有新增事件时，判断是否无需更新研报。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：无更新结论, 检查范围, 原因说明, 后续观察。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_080，任务类型 report_update，难度 hard。任务描述：对历史研报结论和新事件之间的冲突进行修订建议。。期望工具：fetch_news, fetch_financials, rag_query。期望输出：冲突点, 修订建议, 证据来源, 风险提示。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_081，任务类型 citation_audit，难度 medium。任务描述：检查事件点评是否每个关键判断都有来源支撑。。期望工具：rag_query, fetch_announcements, fetch_news。期望输出：缺失引用, 已支持判断, 补充来源, 修订建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_082，任务类型 citation_audit，难度 hard。任务描述：识别研报摘要中的无来源观点并要求改写。。期望工具：rag_query, fetch_broker_reports, fetch_financials。期望输出：无来源观点, 可引用证据, 改写建议, 可信度提示。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_083，任务类型 citation_audit，难度 hard。任务描述：当引用来源只有二级新闻时，降低结论置信度。。期望工具：fetch_news, fetch_announcements, rag_query。期望输出：来源等级, 置信度调整, 保守结论, 复核建议。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_084，任务类型 citation_audit，难度 hard。任务描述：对多来源结论进行交叉验证，标注一致与不一致之处。。期望工具：fetch_news, fetch_announcements, fetch_broker_reports。期望输出：一致结论, 分歧信息, 证据矩阵, 处理建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_085，任务类型 citation_audit，难度 medium。任务描述：判断 RAG 检索结果是否与当前问题相关。。期望工具：rag_query, fetch_news。期望输出：相关性判断, 无关来源, 替代检索词, 下一步动作。是否要求引用：True；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_086，任务类型 citation_audit，难度 medium。任务描述：检查行情解释是否错误引用了历史过期信息。。期望工具：fetch_live_quotes, rag_query, fetch_news。期望输出：时效性检查, 过期信息, 修订建议, 数据状态。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_087，任务类型 citation_audit，难度 medium。任务描述：在来源不足时生成人工复核工单而不是输出确定结论。。期望工具：fetch_announcements, fetch_news, rag_query。期望输出：来源不足, 工单内容, 人工复核, 暂缓结论。是否要求引用：False；是否要求降级：True。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。

Agent 任务样本：任务 ID agent_088，任务类型 citation_audit，难度 hard。任务描述：对生成研报中的数据口径进行引用一致性检查。。期望工具：fetch_financials, rag_query, extract_document_tables。期望输出：口径检查, 引用一致性, 异常项, 修订建议。是否要求引用：True；是否要求降级：False。该条目用于 PlannerAgent、RiskReviewAgent 和 CitationAuditAgent 的任务理解与评测。