# 真实金融事件 benchmark 语料



## 来源

- 本地真实事件样本：`data/benchmarks/tracking_events_real.jsonl`

- 用途：事件分类、影响等级、预警命中和去重评测。



## 使用边界

- 样本来自公开公告/新闻元数据和启发式标注，部分条目仍需人工复核。



## 事件条目

真实事件样本：股票 000002，标题《关于就深铁集团220亿股东借款签署补充协议暨日常关联交易公告》，摘要：万科A 关于就深铁集团220亿股东借款签署补充协议暨日常关联交易公告。来源 cninfo，时间 2026-05-13 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225302554&orgId=gssz0000002&announcementTime=2026-05-13 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 f08346f396e6a7e8。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于深铁集团向公司提供25亿元股东借款额度并由公司提供担保暨日常关联交易公告》，摘要：万科A 关于深铁集团向公司提供25亿元股东借款额度并由公司提供担保暨日常关联交易公告。来源 cninfo，时间 2026-05-13 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225302553&orgId=gssz0000002&announcementTime=2026-05-13 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 991ae29807f3f0e1。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《第二十届董事会第三十四次会议决议公告》，摘要：万科A 第二十届董事会第三十四次会议决议公告。来源 cninfo，时间 2026-05-13 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225302552&orgId=gssz0000002&announcementTime=2026-05-13 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 3322dc02b5d1bfbe。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于在交易商协会披露《关于2023年度第二期中期票据本息偿付安排的公告》的提示性公告》，摘要：万科A 关于在交易商协会披露《关于2023年度第二期中期票据本息偿付安排的公告》的提示性公告。来源 cninfo，时间 2026-05-12 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225292213&orgId=gssz0000002&announcementTime=2026-05-12 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 12f0df57c4be8253。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于在交易商协会披露《关于2023年度第二期中期票据2026年第一次持有人会议的答复公告》的提示性公告》，摘要：万  科Ａ 关于在交易商协会披露《关于2023年度第二期中期票据2026年第一次持有人会议的答复公告》的提示性公告。来源 cninfo，时间 2026-05-10 17:03:32，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225287344&orgId=gssz0000002&announcementTime=2026-05-10 17:03:32。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 e6517a9ee46f8b6e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于制定2026年度公司董事、高级管理人员薪酬方案的公告》，摘要：万科A 关于制定2026年度公司董事、高级管理人员薪酬方案的公告。来源 cninfo，时间 2026-05-09 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225286480&orgId=gssz0000002&announcementTime=2026-05-09 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 ca1f1023847806ae。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《万科企业股份有限公司董事、高级管理人员薪酬管理制度》，摘要：万科A 万科企业股份有限公司董事、高级管理人员薪酬管理制度。来源 cninfo，时间 2026-05-09 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225286479&orgId=gssz0000002&announcementTime=2026-05-09 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 ad0b7aebe2aadaf4。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于召开2025年度股东会的通知》，摘要：万科A 关于召开2025年度股东会的通知。来源 cninfo，时间 2026-05-09 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225286478&orgId=gssz0000002&announcementTime=2026-05-09 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 3ee0d1fb9dbbe492。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《第二十届董事会第三十三次会议决议公告》，摘要：万科A 第二十届董事会第三十三次会议决议公告。来源 cninfo，时间 2026-05-09 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225286477&orgId=gssz0000002&announcementTime=2026-05-09 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 6fd78e85772a39ef。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于按照《香港上市规则》公布2026年4月证券变动月报表的公告》，摘要：万科A 关于按照《香港上市规则》公布2026年4月证券变动月报表的公告。来源 cninfo，时间 2026-05-07 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225279799&orgId=gssz0000002&announcementTime=2026-05-07 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b40790ed3907576a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《关于公开挂牌转让环山集团股份有限公司股权的公告》，摘要：万科A 关于公开挂牌转让环山集团股份有限公司股权的公告。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225264064&orgId=gssz0000002&announcementTime=2026-04-30 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 936ec77d9cbe6a18。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000002，标题《第二十届董事会第三十二次会议决议公告》，摘要：万科A 第二十届董事会第三十二次会议决议公告。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000002&announcementId=1225264063&orgId=gssz0000002&announcementTime=2026-04-30 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 ef92a97ada7c4b3f。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于完成发行于2027年到期的86.24亿港元及于2033年到期的86.24亿港元可转换为公司H股的公司债券的公告》，摘要：美的集团 关于完成发行于2027年到期的86.24亿港元及于2033年到期的86.24亿港元可转换为公司H股的公司债券的公告。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225304414&orgId=9900005965&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 2310aa830336d29d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于为全资子公司提供担保的公告》，摘要：美的集团 关于为全资子公司提供担保的公告。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225304413&orgId=9900005965&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 a15e4d7f1845dd5b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于拟根据一般性授权发行于2027年到期的86.24亿港元及于2033年到期的86.24亿港元可转换为公司H股的公司债券的公告》，摘要：美的集团 关于拟根据一般性授权发行于2027年到期的86.24亿港元及于2033年到期的86.24亿港元可转换为公司H股的公司债券的公告。来源 cninfo，时间 2026-05-07 08:00:31，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225280951&orgId=9900005965&announcementTime=2026-05-07 08:00:31。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 467210fb8a13fb25。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于对下属控股子公司担保额度调剂的公告》，摘要：美的集团 关于对下属控股子公司担保额度调剂的公告。来源 cninfo，时间 2026-05-07 08:00:31，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225280950&orgId=9900005965&announcementTime=2026-05-07 08:00:31。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 0898c71cffdb5628。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《第五届董事会第十五次会议决议公告》，摘要：美的集团 第五届董事会第十五次会议决议公告。来源 cninfo，时间 2026-05-07 08:00:31，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225280949&orgId=9900005965&announcementTime=2026-05-07 08:00:31。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 2a8013eef00a6200。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于以集中竞价交易方式回购A股股份进展情况的公告》，摘要：美的集团 关于以集中竞价交易方式回购A股股份进展情况的公告。来源 cninfo，时间 2026-05-07 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225279156&orgId=9900005965&announcementTime=2026-05-07 00:00:00。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 3dc983dfc08a64b4。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《公司章程修正案(2026年4月）》，摘要：美的集团 公司章程修正案(2026年4月）。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259076&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 dae5c002dc3fe83b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《公司章程（2026年4月）》，摘要：美的集团 公司章程（2026年4月）。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259075&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 a718146dba3e8f7b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《北京市嘉源律师事务所关于美的集团股份有限公司回购注销部分限制性股票的法律意见书》，摘要：美的集团 北京市嘉源律师事务所关于美的集团股份有限公司回购注销部分限制性股票的法律意见书。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259074&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 shareholder，影响等级 low，是否应触发预警 False，去重组 cda083683be09285。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《董事会薪酬与考核委员会关于公司限制性股票激励计划回购注销相关事项的核查意见》，摘要：美的集团 董事会薪酬与考核委员会关于公司限制性股票激励计划回购注销相关事项的核查意见。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259073&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 6231c13b0cd4565e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《关于对2022年和2023年限制性股票激励计划部分激励股份回购注销的公告》，摘要：美的集团 关于对2022年和2023年限制性股票激励计划部分激励股份回购注销的公告。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259072&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 1a097764333a4d1c。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000333，标题《独立董事提名人声明与承诺》，摘要：美的集团 独立董事提名人声明与承诺。来源 cninfo，时间 2026-04-30 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000333&announcementId=1225259071&orgId=9900005965&announcementTime=2026-04-30 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 2d0edbbe859b0bc0。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《关于拟续聘会计师事务所的公告》，摘要：泸州老窖 关于拟续聘会计师事务所的公告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240685&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b3d265978eccaad5。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（李良琛）》，摘要：泸州老窖 2025年度独立董事述职报告（李良琛）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240684&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 c074eb0b17f04514。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（陈国祥）》，摘要：泸州老窖 2025年度独立董事述职报告（陈国祥）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240683&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 577e7cd95c93b416。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（李国旺）》，摘要：泸州老窖 2025年度独立董事述职报告（李国旺）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240682&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 502d90ab61decc76。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（陈有安）》，摘要：泸州老窖 2025年度独立董事述职报告（陈有安）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240681&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 2e931517784676dd。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（益智）》，摘要：泸州老窖 2025年度独立董事述职报告（益智）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240680&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 88ceffd2089b2fc2。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度独立董事述职报告（吕先锫）》，摘要：泸州老窖 2025年度独立董事述职报告（吕先锫）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240679&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 6719ba83498a63c3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年环境、社会及治理（ESG）报告（英文版）》，摘要：泸州老窖 2025年环境、社会及治理（ESG）报告（英文版）。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240678&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 4c53f916139eec84。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年环境、社会及治理（ESG）报告》，摘要：泸州老窖 2025年环境、社会及治理（ESG）报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240677&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 4c53f916139eec84。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《内部控制审计报告》，摘要：泸州老窖 内部控制审计报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240676&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 d08faa5325b42782。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《2025年度内部控制评价报告》，摘要：泸州老窖 2025年度内部控制评价报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240675&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 32b9b318db049b78。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000568，标题《关于募集资金2025年度存放与使用情况的专项报告》，摘要：泸州老窖 关于募集资金2025年度存放与使用情况的专项报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000568&announcementId=1225240674&orgId=gssz0000568&announcementTime=2026-04-29。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 fef4887fd8a84e47。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《关于回购股份事项前十大股东及前十大无限售条件股东持股情况的公告》，摘要：五 粮 液 关于回购股份事项前十大股东及前十大无限售条件股东持股情况的公告。来源 cninfo，时间 2026-05-12 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225292435&orgId=gssz0000858&announcementTime=2026-05-12 00:00:00。标注事件类型 shareholder，影响等级 high，是否应触发预警 True，去重组 47f0069f84cf2255。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2026年第一次临时股东会议案资料》，摘要：五 粮 液 2026年第一次临时股东会议案资料。来源 cninfo，时间 2026-05-12 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225292434&orgId=gssz0000858&announcementTime=2026-05-12 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 936ef651862ea767。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《关于2026年第一次临时股东会增加临时提案暨股东会补充通知的公告》，摘要：五 粮 液 关于2026年第一次临时股东会增加临时提案暨股东会补充通知的公告。来源 cninfo，时间 2026-05-07 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225280482&orgId=gssz0000858&announcementTime=2026-05-07 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 0998ee4b9667b9f2。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《关于四川省宜宾五粮液集团有限公司增持公司股票计划的公告》，摘要：五 粮 液 关于四川省宜宾五粮液集团有限公司增持公司股票计划的公告。来源 cninfo，时间 2026-05-07 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225280481&orgId=gssz0000858&announcementTime=2026-05-07 00:00:00。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 d93e2d6c1d8b4a82。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2025年半年度报告（更新后）》，摘要：五 粮 液 2025年半年度报告（更新后）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273126&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 ec604f3245436488。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2025年第一季度报告（更新后）》，摘要：五 粮 液 2025年第一季度报告（更新后）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273125&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 ec604f3245436488。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2025年半年度报告摘要（更新后）》，摘要：五 粮 液 2025年半年度报告摘要（更新后）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273124&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 d22b582504b30d3e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2025年第三季度报告（更新后）》，摘要：五 粮 液 2025年第三季度报告（更新后）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273123&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 ec604f3245436488。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《关于前期会计差错更正的公告》，摘要：五 粮 液 关于前期会计差错更正的公告。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273122&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 e51b67d155f724f9。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《2025年度涉及财务公司关联交易的存款、贷款等金融业务的专项说明》，摘要：五 粮 液 2025年度涉及财务公司关联交易的存款、贷款等金融业务的专项说明。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273121&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b98c908efe07809d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《独立董事2025年度述职报告（侯水平）》，摘要：五 粮 液 独立董事2025年度述职报告（侯水平）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273120&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 b258d3041fa92baa。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 000858，标题《独立董事2025年度述职报告（罗华伟）》，摘要：五 粮 液 独立董事2025年度述职报告（罗华伟）。来源 cninfo，时间 2026-04-30 18:20:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=000858&announcementId=1225273119&orgId=gssz0000858&announcementTime=2026-04-30 18:20:27。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 43a1068a5c77453a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度权益分派实施公告》，摘要：海康威视 2025年度权益分派实施公告。来源 cninfo，时间 2026-05-14，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225303075&orgId=9900012688&announcementTime=2026-05-14。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 67c082e99310b92d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《国浩律师（杭州）事务所关于公司2025年度股东会之法律意见书》，摘要：海康威视 国浩律师（杭州）事务所关于公司2025年度股东会之法律意见书。来源 cninfo，时间 2026-05-09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225285784&orgId=9900012688&announcementTime=2026-05-09。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 6567292de66bf73e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度股东会决议公告》，摘要：海康威视 2025年度股东会决议公告。来源 cninfo，时间 2026-05-09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225285783&orgId=9900012688&announcementTime=2026-05-09。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 c3ff560b5137b9bb。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度环境、社会和公司治理（ESG）报告（英文版）》，摘要：海康威视 2025年度环境、社会和公司治理（ESG）报告（英文版）。来源 cninfo，时间 2026-04-25，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225184924&orgId=9900012688&announcementTime=2026-04-25。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 4c74927a1eb5a452。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年年度报告（英文版）》，摘要：海康威视 2025年年度报告（英文版）。来源 cninfo，时间 2026-04-25，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225184923&orgId=9900012688&announcementTime=2026-04-25。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 8ee8d638b57009d5。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《关于拟变更会计师事务所的公告》，摘要：海康威视 关于拟变更会计师事务所的公告。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123097&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 6c52e0a5801670b1。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2026年一季度报告（英文版）》，摘要：海康威视 2026年一季度报告（英文版）。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123096&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 3a067377b9cf007d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《独立董事关于公司涉及财务公司关联交易的存贷款等金融业务的专项意见》，摘要：海康威视 独立董事关于公司涉及财务公司关联交易的存贷款等金融业务的专项意见。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123095&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 91529893b3dd550c。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度董事会工作报告》，摘要：海康威视 2025年度董事会工作报告。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123094&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 f11629a35fdf8d58。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《关于与中国电子科技财务有限公司开展金融服务业务的风险处置预案》，摘要：海康威视 关于与中国电子科技财务有限公司开展金融服务业务的风险处置预案。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123093&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 7718d32c1c70ec77。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度独立董事述职报告（谭小芬）》，摘要：海康威视 2025年度独立董事述职报告（谭小芬）。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123092&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 d4c97a8b76a22fa3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002415，标题《2025年度独立董事述职报告（吴晓波）》，摘要：海康威视 2025年度独立董事述职报告（吴晓波）。来源 cninfo，时间 2026-04-18，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002415&announcementId=1225123091&orgId=9900012688&announcementTime=2026-04-18。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 6a59a721580997a5。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《2022年股票期权激励计划第三个行权期可行权激励对象名单》，摘要：立讯精密 2022年股票期权激励计划第三个行权期可行权激励对象名单。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225303286&orgId=9900014448&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b78a16acc129fafa。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《2022年股票期权激励计划人员名单（调整后）》，摘要：立讯精密 2022年股票期权激励计划人员名单（调整后）。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225303285&orgId=9900014448&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b34e2676d0ec0c26。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《2022年股票期权激励计划注销股票期权数量及人员名单》，摘要：立讯精密 2022年股票期权激励计划注销股票期权数量及人员名单。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225303284&orgId=9900014448&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 30cce883b2809f52。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《关于2022年股票期权激励计划第三个行权期采用自主行权模式的提示性公告》，摘要：立讯精密 关于2022年股票期权激励计划第三个行权期采用自主行权模式的提示性公告。来源 cninfo，时间 2026-05-14 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225303283&orgId=9900014448&announcementTime=2026-05-14 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 fffa79e8ecd58e39。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《关于股份回购进展情况的公告》，摘要：立讯精密 关于股份回购进展情况的公告。来源 cninfo，时间 2026-05-07 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225279805&orgId=9900014448&announcementTime=2026-05-07 00:00:00。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 23350a9adfe07a89。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《关于部分股票期权注销完成的公告》，摘要：立讯精密 关于部分股票期权注销完成的公告。来源 cninfo，时间 2026-05-06 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225274028&orgId=9900014448&announcementTime=2026-05-06 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9a6ed969fcd109b7。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《关于2021年股票期权激励计划首次授予第四个行权期采用自主行权模式的提示性公告》，摘要：立讯精密 关于2021年股票期权激励计划首次授予第四个行权期采用自主行权模式的提示性公告。来源 cninfo，时间 2026-05-06 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225274027&orgId=9900014448&announcementTime=2026-05-06 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 844e708ad8deb1a7。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《2026年半年度业绩预告》，摘要：立讯精密 2026年半年度业绩预告。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225250030&orgId=9900014448&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 high，是否应触发预警 True，去重组 1e1ebc1d4e7893f3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《董事会秘书工作细则（2026年4月）》，摘要：立讯精密 董事会秘书工作细则（2026年4月）。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225249998&orgId=9900014448&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 2cf7bbf09e1750e5。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《控股子公司管理制度（2026年4月）》，摘要：立讯精密 控股子公司管理制度（2026年4月）。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225249997&orgId=9900014448&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 748075add890351b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《总经理工作细则（2026年4月）》，摘要：立讯精密 总经理工作细则（2026年4月）。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225249996&orgId=9900014448&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b3429f31935dd7a9。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002475，标题《内幕信息知情人管理制度（2026年4月）》，摘要：立讯精密 内幕信息知情人管理制度（2026年4月）。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002475&announcementId=1225249995&orgId=9900014448&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 2f8e85c4445ea84c。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（股份发行人及根据《上市规则》第十九B章上市的香港预托证券发行人的证券变动月报表）》，摘要：比亚迪 H股公告（股份发行人及根据《上市规则》第十九B章上市的香港预托证券发行人的证券变动月报表）。来源 cninfo，时间 2026-05-06 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225277521&orgId=gshk0001211&announcementTime=2026-05-06 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9eca8ac46d3adc7e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《2026年4月产销快报》，摘要：比亚迪 2026年4月产销快报。来源 cninfo，时间 2026-05-06 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225277520&orgId=gshk0001211&announcementTime=2026-05-06 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 a3c8f838cafabb04。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《提名委员会实施细则（2026年4月）》，摘要：比亚迪 提名委员会实施细则（2026年4月）。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225233075&orgId=gshk0001211&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 ab59d87d7941d65d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《关于聘任公司副总裁的公告》，摘要：比亚迪 关于聘任公司副总裁的公告。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225233074&orgId=gshk0001211&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 09bd84f1ec39c5f1。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《第八届董事会第二十三次会议决议公告》，摘要：比亚迪 第八届董事会第二十三次会议决议公告。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225233073&orgId=gshk0001211&announcementTime=2026-04-29 00:00:00。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 84f59112c8662c73。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《2026年一季度报告》，摘要：比亚迪 2026年一季度报告。来源 cninfo，时间 2026-04-29 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225233071&orgId=gshk0001211&announcementTime=2026-04-29 00:00:00。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 6d6ffe3feb16df3b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（于二零二六年六月九日举行的股东周年大会（「股东周年大会」）或其任何续会适用的H股持有人代表委任表格）》，摘要：比亚迪 H股公告（于二零二六年六月九日举行的股东周年大会（「股东周年大会」）或其任何续会适用的H股持有人代表委任表格）。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147072&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 53db2c9893f7087c。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（截至二零二五年十二月三十一日止年度之末期股息(更新)）》，摘要：比亚迪 H股公告（截至二零二五年十二月三十一日止年度之末期股息(更新)）。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147071&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 c835abd34b6f9c71。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（股东周年大会通告）》，摘要：比亚迪 H股公告（股东周年大会通告）。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147070&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 19edc92782061794。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（通函）》，摘要：比亚迪 H股公告（通函）。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147069&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 422a799a7e7d495a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《H股公告（暂停办理过户登记）》，摘要：比亚迪 H股公告（暂停办理过户登记）。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147068&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b58891bcd8b3cd04。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 002594，标题《关于召开2025年度股东会的通知》，摘要：比亚迪 关于召开2025年度股东会的通知。来源 cninfo，时间 2026-04-23 00:00:00，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=002594&announcementId=1225147067&orgId=gshk0001211&announcementTime=2026-04-23 00:00:00。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 c546e8a0b851752a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《关于控股股东无偿捐赠部分公司股份的进展公告》，摘要：宁德时代 关于控股股东无偿捐赠部分公司股份的进展公告。来源 cninfo，时间 2026-05-11 18:48:08，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225292100&orgId=GD165627&announcementTime=2026-05-11 18:48:08。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9d2673c1bd245f17。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《H股公告（截至2026年4月30日止股份发行人的证券变动月报表）》，摘要：宁德时代 H股公告（截至2026年4月30日止股份发行人的证券变动月报表）。来源 cninfo，时间 2026-05-07 18:48:09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225282726&orgId=GD165627&announcementTime=2026-05-07 18:48:09。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 7d55dcca204a9b7f。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《关于完成配售H股的公告》，摘要：宁德时代 关于完成配售H股的公告。来源 cninfo，时间 2026-04-30 20:42:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225274804&orgId=GD165627&announcementTime=2026-04-30 20:42:27。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 016c43b10f4cd443。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《H股公告（翌日披露报表）》，摘要：宁德时代 H股公告（翌日披露报表）。来源 cninfo，时间 2026-04-30 20:42:27，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225274803&orgId=GD165627&announcementTime=2026-04-30 20:42:27。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 f429d4b0aea9b7b0。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《关于2026年度第二期绿色科技创新债券发行完成的公告》，摘要：宁德时代 关于2026年度第二期绿色科技创新债券发行完成的公告。来源 cninfo，时间 2026-04-30 20:42:09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225274805&orgId=GD165627&announcementTime=2026-04-30 20:42:09。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 fa2705bcf4488d10。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《关于根据一般性授权配售新H股的公告》，摘要：宁德时代 关于根据一般性授权配售新H股的公告。来源 cninfo，时间 2026-04-28 08:12:58，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225223116&orgId=GD165627&announcementTime=2026-04-28 08:12:58。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b50181910865e430。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《第四届董事会第十六次会议决议公告》，摘要：宁德时代 第四届董事会第十六次会议决议公告。来源 cninfo，时间 2026-04-28 08:12:58，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225223115&orgId=GD165627&announcementTime=2026-04-28 08:12:58。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0c309be055e241a7。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《中信建投证券股份有限公司关于宁德时代新能源科技股份有限公司股东向特定机构投资者询价转让股份的核查报告》，摘要：宁德时代 中信建投证券股份有限公司关于宁德时代新能源科技股份有限公司股东向特定机构投资者询价转让股份的核查报告。来源 cninfo，时间 2026-04-23 21:36:49，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225173667&orgId=GD165627&announcementTime=2026-04-23 21:36:49。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 783dfdab0114afc9。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《中国国际金融股份有限公司关于宁德时代新能源科技股份有限公司股东向特定机构投资者询价转让股份的核查报告》，摘要：宁德时代 中国国际金融股份有限公司关于宁德时代新能源科技股份有限公司股东向特定机构投资者询价转让股份的核查报告。来源 cninfo，时间 2026-04-23 21:36:49，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225173666&orgId=GD165627&announcementTime=2026-04-23 21:36:49。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 783dfdab0114afc9。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《股东询价转让结果报告书暨持股5%以上股东持有权益比例降至5%以下的权益变动提示性公告》，摘要：宁德时代 股东询价转让结果报告书暨持股5%以上股东持有权益比例降至5%以下的权益变动提示性公告。来源 cninfo，时间 2026-04-23 21:36:49，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225173665&orgId=GD165627&announcementTime=2026-04-23 21:36:49。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 65265aae7b93763d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《简式权益变动报告书》，摘要：宁德时代 简式权益变动报告书。来源 cninfo，时间 2026-04-23 21:36:49，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225173664&orgId=GD165627&announcementTime=2026-04-23 21:36:49。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 5a7abfad81f09e92。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 300750，标题《关于授予2026年A股员工持股计划预留份额的公告》，摘要：宁德时代 关于授予2026年A股员工持股计划预留份额的公告。来源 cninfo，时间 2026-04-22 19:14:29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=300750&announcementId=1225150151&orgId=GD165627&announcementTime=2026-04-22 19:14:29。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 47e81e09c41da3d0。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于执行董事及行长离任的公告》，摘要：招商银行 招商银行股份有限公司关于执行董事及行长离任的公告。来源 cninfo，时间 2026-05-01，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225272650&orgId=gssh0600036&announcementTime=2026-05-01。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9fbe889940897e49。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司董事会决议公告》，摘要：招商银行 招商银行股份有限公司董事会决议公告。来源 cninfo，时间 2026-05-01，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225272642&orgId=gssh0600036&announcementTime=2026-05-01。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 d09cbd8a9ff9d819。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司董事会决议公告》，摘要：招商银行 招商银行股份有限公司董事会决议公告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225231670&orgId=gssh0600036&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 16b664332d6d7ee2。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司2026年第一季度第三支柱报告》，摘要：招商银行 招商银行股份有限公司2026年第一季度第三支柱报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225231665&orgId=gssh0600036&announcementTime=2026-04-29。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 0d64d2dbb810576c。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于独立非执行董事辞任的公告》，摘要：招商银行 招商银行股份有限公司关于独立非执行董事辞任的公告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225231620&orgId=gssh0600036&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b1dd7c3dc56c080f。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司2026年第一季度报告》，摘要：招商银行 招商银行股份有限公司2026年第一季度报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225231394&orgId=gssh0600036&announcementTime=2026-04-29。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 eb9e6c6fd160ddce。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《[H股公告]招商银行股份有限公司伦敦分行在招商银行股份有限公司的50亿美元中期票据计划下发行于2029年到期的人民币30亿元票息为1.73%的票据》，摘要：招商银行 [H股公告]招商银行股份有限公司伦敦分行在招商银行股份有限公司的50亿美元中期票据计划下发行于2029年到期的人民币30亿元票息为1.73%的票据。来源 cninfo，时间 2026-04-23，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225149847&orgId=gssh0600036&announcementTime=2026-04-23。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 498ff5ddcf0012b4。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于优先股全部赎回及摘牌完成的公告》，摘要：招商银行 招商银行股份有限公司关于优先股全部赎回及摘牌完成的公告。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225111786&orgId=gssh0600036&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 68420ff951f37ed3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《[H股公告]招商银行股份有限公司董事会会议召开日期》，摘要：招商银行 [H股公告]招商银行股份有限公司董事会会议召开日期。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225110226&orgId=gssh0600036&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9c40b632df461b11。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于无固定期限资本债券发行完毕的公告》，摘要：招商银行 招商银行股份有限公司关于无固定期限资本债券发行完毕的公告。来源 cninfo，时间 2026-04-16，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225107247&orgId=gssh0600036&announcementTime=2026-04-16。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 61e64f0869d1c217。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于优先股停牌的提示性公告》，摘要：招商银行 招商银行股份有限公司关于优先股停牌的提示性公告。来源 cninfo，时间 2026-04-10，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225087446&orgId=gssh0600036&announcementTime=2026-04-10。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 b0e1deb35c885bac。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600036，标题《招商银行股份有限公司关于优先股全部赎回及摘牌的公告》，摘要：招商银行 招商银行股份有限公司关于优先股全部赎回及摘牌的公告。来源 cninfo，时间 2026-04-10，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600036&announcementId=1225087441&orgId=gssh0600036&announcementTime=2026-04-10。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 5aa899a574203bf0。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药关于获得药物临床试验批准通知书的公告》，摘要：恒瑞医药 恒瑞医药关于获得药物临床试验批准通知书的公告。来源 cninfo，时间 2026-05-14，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225304597&orgId=gssh0600276&announcementTime=2026-05-14。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 e5c00ec2374f128b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药关于与百时美施贵宝公司签署战略合作及许可协议的公告》，摘要：恒瑞医药 恒瑞医药关于与百时美施贵宝公司签署战略合作及许可协议的公告。来源 cninfo，时间 2026-05-12，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225300018&orgId=gssh0600276&announcementTime=2026-05-12。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 91d357c9dc7ddce1。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药关于获得药物临床试验批准通知书的公告》，摘要：恒瑞医药 恒瑞医药关于获得药物临床试验批准通知书的公告。来源 cninfo，时间 2026-05-09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225284384&orgId=gssh0600276&announcementTime=2026-05-09。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 59eb610761ef1abf。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药关于获得药物临床试验批准通知书的公告》，摘要：恒瑞医药 恒瑞医药关于获得药物临床试验批准通知书的公告。来源 cninfo，时间 2026-05-09，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225284366&orgId=gssh0600276&announcementTime=2026-05-09。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 59eb610761ef1abf。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药关于回购公司A股股份的进展公告》，摘要：恒瑞医药 恒瑞医药关于回购公司A股股份的进展公告。来源 cninfo，时间 2026-05-08，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225281541&orgId=gssh0600276&announcementTime=2026-05-08。标注事件类型 shareholder，影响等级 medium，是否应触发预警 True，去重组 cead523661434193。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《H股公告-证券变动月报表》，摘要：恒瑞医药 H股公告-证券变动月报表。来源 cninfo，时间 2026-05-08，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225281536&orgId=gssh0600276&announcementTime=2026-05-08。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 e83f9507e42f05bf。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《薪酬与考核委员会实施细则（2026年4月修订）》，摘要：恒瑞医药 薪酬与考核委员会实施细则（2026年4月修订）。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225260061&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 5a4e212db39de7df。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《审计委员会实施细则（2026年4月修订）》，摘要：恒瑞医药 审计委员会实施细则（2026年4月修订）。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225260028&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 1a20019d415391a1。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《投资者关系管理制度（2026年4月修订）》，摘要：恒瑞医药 投资者关系管理制度（2026年4月修订）。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225259996&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 01def2e5cc2de440。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《恒瑞医药第十届董事会第三次会议决议公告》，摘要：恒瑞医药 恒瑞医药第十届董事会第三次会议决议公告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225259969&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 f826615458ab412f。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《提名委员会实施细则（2026年4月修订）》，摘要：恒瑞医药 提名委员会实施细则（2026年4月修订）。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225259959&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 23b5d64576c9eaf4。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600276，标题《信息披露事务管理制度（2026年4月修订）》，摘要：恒瑞医药 信息披露事务管理制度（2026年4月修订）。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600276&announcementId=1225259888&orgId=gssh0600276&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0792b702a05a7b14。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台关于回购股份实施进展的公告》，摘要：贵州茅台 贵州茅台关于回购股份实施进展的公告。来源 cninfo，时间 2026-05-08，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225282650&orgId=gssh0600519&announcementTime=2026-05-08。标注事件类型 shareholder，影响等级 high，是否应触发预警 True，去重组 9478266efd634e91。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台关于召开2025年度及2026年第一季度业绩说明会的公告》，摘要：贵州茅台 贵州茅台关于召开2025年度及2026年第一季度业绩说明会的公告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225228128&orgId=gssh0600519&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 high，是否应触发预警 True，去重组 27e0bad30fd1a8c3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2026年第一季度主要经营数据公告》，摘要：贵州茅台 贵州茅台2026年第一季度主要经营数据公告。来源 cninfo，时间 2026-04-25，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225188174&orgId=gssh0600519&announcementTime=2026-04-25。标注事件类型 announcement，影响等级 high，是否应触发预警 True，去重组 e3d4e73f9cb6ca88。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2026年第一季度报告》，摘要：贵州茅台 贵州茅台2026年第一季度报告。来源 cninfo，时间 2026-04-25，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225187851&orgId=gssh0600519&announcementTime=2026-04-25。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 8604dc308c90aaed。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年度独立董事述职报告（王鑫）》，摘要：贵州茅台 贵州茅台2025年度独立董事述职报告（王鑫）。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114747&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 e32198ad4e81bf15。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台关于贵州茅台集团财务有限公司的风险评估报告》，摘要：贵州茅台 贵州茅台关于贵州茅台集团财务有限公司的风险评估报告。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114745&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 03c5b2983a48f400。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年度董事会审计委员会履职情况报告》，摘要：贵州茅台 贵州茅台2025年度董事会审计委员会履职情况报告。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114743&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 359758ef1b82b360。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年年度报告》，摘要：贵州茅台 贵州茅台2025年年度报告。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114741&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 5c1975ff927d612f。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年环境、社会及治理（ESG）报告（英文版）》，摘要：贵州茅台 贵州茅台2025年环境、社会及治理（ESG）报告（英文版）。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114738&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 e89e8d099f562c17。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台第四届董事会2026年度第六次会议决议公告》，摘要：贵州茅台 贵州茅台第四届董事会2026年度第六次会议决议公告。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114735&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 659124b13ce44f6a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年年度报告（英文版）》，摘要：贵州茅台 贵州茅台2025年年度报告（英文版）。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114733&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0b5800893af94f86。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600519，标题《贵州茅台2025年年度报告摘要》，摘要：贵州茅台 贵州茅台2025年年度报告摘要。来源 cninfo，时间 2026-04-17，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600519&announcementId=1225114731&orgId=gssh0600519&announcementTime=2026-04-17。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0b5800893af94f86。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年年度股东会资料》，摘要：长江电力 长江电力2025年年度股东会资料。来源 cninfo，时间 2026-05-01，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225271752&orgId=gssh0600900&announcementTime=2026-05-01。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 df8e803d4bb9d0bf。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力董事会审计委员会2025年度对会计师事务所履行监督职责情况的报告》，摘要：长江电力 长江电力董事会审计委员会2025年度对会计师事务所履行监督职责情况的报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262575&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 6032c4ecb17e27d0。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年度涉及财务公司关联交易的存款、贷款等金融业务的专项说明》，摘要：长江电力 长江电力2025年度涉及财务公司关联交易的存款、贷款等金融业务的专项说明。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262503&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 8faf452277098256。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年度环境、社会和公司治理报告》，摘要：长江电力 长江电力2025年度环境、社会和公司治理报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262474&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 f78ce77513e05f71。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年度环境、社会和公司治理报告摘要》，摘要：长江电力 长江电力2025年度环境、社会和公司治理报告摘要。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262440&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 55ddbd2c6c7da427。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力董事会关于独立董事独立性自查情况的专项意见》，摘要：长江电力 长江电力董事会关于独立董事独立性自查情况的专项意见。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262342&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 598fbae76109bf73。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年内部控制评价报告》，摘要：长江电力 长江电力2025年内部控制评价报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262326&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 1e86de5799de620e。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力关于三峡财务有限责任公司的风险持续评估报告》，摘要：长江电力 长江电力关于三峡财务有限责任公司的风险持续评估报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262318&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 63fab853f44831f7。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年度内部控制审计报告》，摘要：长江电力 长江电力2025年度内部控制审计报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262300&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 f70f6ac190aefa1b。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力董事会审计委员会2025年度工作报告》，摘要：长江电力 长江电力董事会审计委员会2025年度工作报告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262291&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0b80a87e5c77b6dc。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力2025年度非经营性资金占用及其他关联资金往来的专项说明》，摘要：长江电力 长江电力2025年度非经营性资金占用及其他关联资金往来的专项说明。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262255&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 cebc443ffad75858。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 600900，标题《长江电力第六届董事会第五十三次会议决议公告》，摘要：长江电力 长江电力第六届董事会第五十三次会议决议公告。来源 cninfo，时间 2026-04-30，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=600900&announcementId=1225262227&orgId=gssh0600900&announcementTime=2026-04-30。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 0706cef9606e6630。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《关于参加“2026年陕西辖区上市公司投资者集体接待日暨2025年度业绩说明会”的公告》，摘要：隆基绿能 关于参加“2026年陕西辖区上市公司投资者集体接待日暨2025年度业绩说明会”的公告。来源 cninfo，时间 2026-05-13，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225300448&orgId=9900022338&announcementTime=2026-05-13。标注事件类型 announcement，影响等级 high，是否应触发预警 True，去重组 a0253dc2f126f1d3。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《关于提供担保的进展公告》，摘要：隆基绿能 关于提供担保的进展公告。来源 cninfo，时间 2026-05-11，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225287204&orgId=9900022338&announcementTime=2026-05-11。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 41f742dd5733d111。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《2025年年度股东会会议资料》，摘要：隆基绿能 2025年年度股东会会议资料。来源 cninfo，时间 2026-05-08，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225281750&orgId=9900022338&announcementTime=2026-05-08。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 9e98f1d003b30a31。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《2025年度非经营性资金占用及其他关联资金往来情况的专项说明》，摘要：隆基绿能 2025年度非经营性资金占用及其他关联资金往来情况的专项说明。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225251685&orgId=9900022338&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 medium，是否应触发预警 True，去重组 7f7fb9770c7e3a1d。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《第六届董事会独立董事专门会议2026年第一次会议决议》，摘要：隆基绿能 第六届董事会独立董事专门会议2026年第一次会议决议。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225251684&orgId=9900022338&announcementTime=2026-04-29。标注事件类型 announcement，影响等级 low，是否应触发预警 False，去重组 4add46cdc3cbb01a。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。

真实事件样本：股票 601012，标题《关于2025年度会计师事务所履职情况的评估报告》，摘要：隆基绿能 关于2025年度会计师事务所履职情况的评估报告。来源 cninfo，时间 2026-04-29，链接 http://www.cninfo.com.cn/new/disclosure/detail?stockCode=601012&announcementId=1225251683&orgId=9900022338&announcementTime=2026-04-29。标注事件类型 earnings，影响等级 medium，是否应触发预警 True，去重组 0720f4a38fc66e17。该条目用于金融事件处理 Pipeline 和多 Agent 事件分析角色的评测与检索增强。