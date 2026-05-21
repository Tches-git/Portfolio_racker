# FinanceBench 样本：financebench_id_03029

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2018_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is the FY2018 capital expenditure amount (in USD millions) for 3M? Give a response to the question by relying on the details shown in the cash flow statement.
- 标准答案：$1577.00
- 答案依据：The metric capital expenditures was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Purchases of property, plant and equipment (PP&E).

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents 3M Company and Subsidiaries Consolidated Statement of Cash Flow s Years ended December 31 (Millions) 2018 2017 2016 Cash Flows from Operating Activities Net income including noncontrolling interest $ 5,363 $ 4,869 $ 5,058 Adjustments to reconcile net income including noncontrolling interest to net cash provided by operating activities Depreciation and amortization 1,488 1,544 1,474 Company pension and postretirement contributions (370) (967) (383) Company pension and postretirement expense 410 334 250 Stock-based compensation expense 302 324 298 Gain on sale of businesses (545) (586) (111) Deferred income taxes (57) 107 7 Changes in assets and liabilities Accounts receivable (305) (245) (313) Inventories (509) (387) 57 Accounts payable 408 24 148 Accrued income taxes (current and long-term) 134 967 101 Other net 120 256 76 Net cash provided by (used in) operating activities 6,439 6,240 6,662 Cash Flows from Investing Activities Purchases of property, plant and equipment (PP&E) (1,577) (1,373) (1,420) Proceeds from sale of PP&E and other assets 262 49 58 Acquisitions, net of cash acquired 13 (2,023) (16) Purchases of marketable securities and investments (1,828) (2,152) (1,410) Proceeds from maturities and sale of marketable securities and investments 2,497 1,354 1,247 Proceeds from sale of businesses, net of cash sold 846 1,065 142 Other net 9 (6) (4) Net cash provided by (used in) investing activities 222 (3,086) (1,403) Cash Flows from Financing Activities Change in short-term debt net (284) 578 (797) Repayment of debt (maturities greater than 90 days) (1,034) (962) (992) Proceeds from debt (maturities greater than 90 days) 2,251 1,987 2,832 Purchases of treasury stock (4,870) (2,068) (3,753) Proceeds from issuance of treasury stock pursuant to stock option and benefit plans 485 734 804 Dividends paid to shareholders (3,193) (2,803) (2,678) Other net (56) (121) (42) Net cash provided by (used in) financing activities (6,701) (2,655) (4,626) Effect of exchange rate changes on cash and cash equivalents (160) 156 (33) Net increase (decrease) in cash and cash equivalents (200) 655 600 Cash and cash equivalents at beginning of year 3,053 2,398 1,798 Cash and cash equivalents at end of period $ 2,853 $ 3,053 $ 2,398 The accompanying Notes to Consolidated Financial Statements are an integral part of this statement. 60

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04672

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2018_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：Assume that you are a public equities analyst. Answer the following question by primarily using information that is shown in the balance sheet: what is the year end FY2018 net PPNE for 3M? Answer in USD billions.
- 标准答案：$8.70
- 答案依据：The metric ppne, net was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Property, plant and equipment â net.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents 3M Company and Subsidiaries Consolidated Balance Shee t At December 31 December 31, December 31, (Dollars in millions, except per share amount) 2018 2017 Assets Current assets Cash and cash equivalents $ 2,853 $ 3,053 Marketable securities current 380 1,076 Accounts receivable net of allowances of $95 and $103 5,020 4,911 Inventories Finished goods 2,120 1,915 Work in process 1,292 1,218 Raw materials and supplies 954 901 Total inventories 4,366 4,034 Prepaids 741 937 Other current assets 349 266 Total current assets 13,709 14,277 Property, plant and equipment 24,873 24,914 Less: Accumulated depreciation (16,135) (16,048) Property, plant and equipment net 8,738 8,866 Goodwill 10,051 10,513 Intangible assets net 2,657 2,936 Other assets 1,345 1,395 Total assets $ 36,500 $ 37,987 Liabilities Current liabilities Short-term borrowings and current portion of long-term debt $ 1,211 $ 1,853 Accounts payable 2,266 1,945 Accrued payroll 749 870 Accrued income taxes 243 310 Other current liabilities 2,775 2,709 Total current liabilities 7,244 7,687 Long-term debt 13,411 12,096 Pension and postretirement benefits 2,987 3,620 Other liabilities 3,010 2,962 Total liabilities $ 26,652 $ 26,365 Commitments and contingencies (Note 16) Equity 3M Company shareholders equity: Common stock par value, $.01 par value $ 9 $ 9 Shares outstanding - 2018: 576,575,168 Shares outstanding - 2017: 594,884,237 Additional paid-in capital 5,643 5,352 Retained earnings 40,636 39,115 Treasury stock (29,626) (25,887) Accumulated other comprehensive income (loss) (6,866) (7,026) Total 3M Company shareholders equity 9,796 11,563 Noncontrolling interest 52 59 Total equity $ 9,848 $ 11,622 Total liabilities and equity $ 36,500 $ 37,987 The accompanying Notes to Consolidated Financial Statements are an integral part of this statement. 58

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00499

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning)。
- 问题：Is 3M a capital-intensive business based on FY2022 data?
- 标准答案：No, the company is managing its CAPEX and Fixed Assets pretty efficiently, which is evident from below key metrics:
CAPEX/Revenue Ratio: 5.1%
Fixed assets/Total Assets: 20%
Return on Assets= 12.4%
- 答案依据：CAPEX/Revenue
Fixed Assets/Total Assets
ROA=Net Income/Total Assets

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：3M Company and Subsidiaries Consolidated Statement of Income Years ended December 31 (Millions, except per share amounts) 2022 2021 2020 Net sales $ 34,229 $ 35,355 $ 32,184

证据 2：3M Company and Subsidiaries Consolidated Balance Sheet At December 31 (Dollars in millions, except per share amount) 2022 2021 Assets Current assets Cash and cash equivalents $ 3,655 $ 4,564 Marketable securities current 238 201 Accounts receivable net of allowances of $174 and $189 4,532 4,660 Inventories Finished goods 2,497 2,196 Work in process 1,606 1,577 Raw materials and supplies 1,269 1,212 Total inventories 5,372 4,985 Prepaids 435 654 Other current assets 456 339 Total current assets 14,688 15,403 Property, plant and equipment 25,998 27,213 Less: Accumulated depreciation (16,820) (17,784) Property, plant and equipment net 9,178 9,429 Operating lease right of use assets 829 858 Goodwill 12,790 13,486 Intangible assets net 4,699 5,288 Other assets 4,271 2,608 Total assets $ 46,455 $ 47,072

证据 3：3M Company and Subsidiaries Consolidated Statement of Cash Flows Years ended December 31 (Millions) 2022 2021 2020 Cash Flows from Operating Activities Net income including noncontrolling interest $ 5,791 $ 5,929 $ 5,453 Adjustments to reconcile net income including noncontrolling interest to net cash provided by operating activities Depreciation and amortization 1,831 1,915 1,911 Long-lived and indefinite-lived asset impairment expense 618 6 Goodwill impairment expense 271 Company pension and postretirement contributions (158) (180) (156) Company pension and postretirement expense 178 206 322 Stock-based compensation expense 263 274 262 Gain on business divestitures (2,724) (389) Deferred income taxes (663) (166) (165) Changes in assets and liabilities Accounts receivable (105) (122) 165 Inventories (629) (903) (91) Accounts payable 111 518 252 Accrued income taxes (current and long-term) (47) (244) 132 Other net 854 227 411 Net cash provided by (used in) operating activities 5,591 7,454 8,113 Cash Flows from Investing Activities Purchases of property, plant and equipment (PP&E) (1,749) (1,603) (1,501)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01226

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Numerical reasoning OR Logical reasoning。
- 问题：What drove operating margin change as of FY2022 for 3M? If operating margin is not a useful metric for a company like this, then please state that and explain why.
- 标准答案：Operating Margin for 3M in FY2022 has decreased by 1.7% primarily due to: 
-Decrease in gross Margin
-mostly one-off charges including Combat Arms Earplugs litigation, impairment related to exiting PFAS manufacturing, costs related to exiting Russia and divestiture-related restructuring
charges
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：SG&A, measured as a percent of sales, increased in 2022 when compared to the same period last year. SG&A was impacted by increased special item costs for significant litigation primarily related to steps toward resolving Combat Arms Earplugs litigation (discussed in Note 16) resulting in a 2022 second quarter pre-tax charge of approximately $1.2 billion, certain impairment costs related to exiting PFAS manufacturing (see Note 15), costs related to exiting Russia (see Note 15), divestiture-related restructuring charges (see Note 5), and continued investment in key growth initiatives. These increases were partially offset by restructuring benefits and ongoing general 3M cost management.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01865

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：If we exclude the impact of M&A, which segment has dragged down 3M's overall growth in 2022?
- 标准答案：The consumer segment shrunk by 0.9% organically.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Worldwide Sales Change By Business Segment Organic sales Acquisitions Divestitures Translation Total sales change Safety and Industrial 1.0 % % % (4.2) % (3.2) % Transportation and Electronics 1.2 (0.5) (4.6) (3.9) Health Care 3.2 (1.4) (3.8) (2.0) Consumer (0.9) (0.4) (2.6) (3.9) Total Company 1.2 (0.5) (3.9) (3.2)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00807

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2023Q2_10Q。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Logical reasoning。
- 问题：Does 3M have a reasonably healthy liquidity profile based on its quick ratio for Q2 of FY2023? If the quick ratio is not relevant to measure liquidity, please state that and explain why.
- 标准答案：No. The quick ratio for 3M was 0.96 by Jun'23 close, which needs a bit of an improvement to touch the 1x mark
- 答案依据：Quick Ratio= (Total current assets-Total inventories)/Total current liabilities
(15,754-5,280)/10,936

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2023Q2_10Q, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：3M Company and Subsidiaries Consolidated Balance Sheet (Unaudited) (Dollars in millions, except per share amount) June 30, 2023 December 31, 2022 Assets Current assets Cash and cash equivalents $ 4,258 $ 3,655 Marketable securities current 56 238 Accounts receivable net of allowances of $160 and $174 4,947 4,532 Inventories Finished goods 2,526 2,497 Work in process 1,527 1,606 Raw materials and supplies 1,227 1,269 Total inventories 5,280 5,372 Prepaids 674 435 Other current assets 539 456 Total current assets 15,754 14,688 Property, plant and equipment 26,459 25,998 Less: Accumulated depreciation (17,248) (16,820) Property, plant and equipment net 9,211 9,178 Operating lease right of use assets 812 829 Goodwill 12,869 12,790 Intangible assets net 4,470 4,699 Other assets 5,764 4,271 Total assets $ 48,880 $ 46,455 Liabilities Current liabilities Short-term borrowings and current portion of long-term debt $ 3,033 $ 1,938 Accounts payable 3,231 3,183 Accrued payroll 785 692 Accrued income taxes 172 259 Operating lease liabilities current 244 261 Other current liabilities 3,471 3,190 Total current liabilities 10,936 9,523

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00941

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2023Q2_10Q。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Which debt securities are registered to trade on a national securities exchange under 3M's name as of Q2 of 2023?
- 标准答案：Following debt securities registered under 3M's name are listed to trade on the New York Stock Exchange:
-1.500% Notes due 2026 (Trading Symbol: MMM26)
-1.750% Notes due 2030 (Trading Symbol: MMM30)
-1.500% Notes due 2031 (Trading Symbol: MMM31)
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2023Q2_10Q, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Title of each class Trading Symbol(s) Name of each exchange on which registered Common Stock, Par Value $.01 Per Share MMM New York Stock Exchange MMM Chicago Stock Exchange, Inc. 1.500% Notes due 2026 MMM26 New York Stock Exchange 1.750% Notes due 2030 MMM30 New York Stock Exchange 1.500% Notes due 2031 MMM31 New York Stock Exchange

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01858

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：3M；文档：3M_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Does 3M maintain a stable trend of dividend distribution?
- 标准答案：Yes, not only they distribute the dividends on a routine basis, 3M has also been increasing the per share dividend for consecutive 65 years
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, 3M, 3M_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：This marked the 65th consecutive year of dividend increases for 3M.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02987

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Activision Blizzard；文档：ACTIVISIONBLIZZARD_2019_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2019 fixed asset turnover ratio for Activision Blizzard? Fixed asset turnover ratio is defined as: FY2019 revenue / (average PP&E between FY2018 and FY2019). Round your answer to two decimal places. Base your judgments on the information provided primarily in the statement of income and the statement of financial position.
- 标准答案：24.26
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total revenue. This metric was located in the 10K as a single line item named: Total net revenues.

Metric 2: Ppne, net. This metric was located in the 10K as a single line item named: Property and equipment, net.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Activision Blizzard, ACTIVISIONBLIZZARD_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents ACTIVISION BLIZZARD, INC. AND SUBSIDIARIES CONSOLIDATED BALANCE SHEETS (Amounts in millions, except share data) At December 31, 2019 At December 31, 2018 Assets Current assets: Cash and cash equivalents $ 5,794 $ 4,225 Accounts receivable, net of allowances of $132 and $190, at December 31, 2019 and December 31, 2018, respectively 848 1,035 Inventories, net 32 43 Software development 322 264 Other current assets 296 539 Total current assets 7,292 6,106 Software development 54 65 Property and equipment, net 253 282 Deferred income taxes, net 1,293 458 Other assets 658 482 Intangible assets, net 531 735 Goodwill 9,764 9,762 Total assets $ 19,845 $ 17,890 Liabilities and Shareholders Equity Current liabilities: Accounts payable $ 292 $ 253 Deferred revenues 1,375 1,493 Accrued expenses and other liabilities 1,248 896 Total current liabilities 2,915 2,642 Long-term debt, net 2,675 2,671 Deferred income taxes, net 505 18 Other liabilities 945 1,167 Total liabilities 7,040 6,498 Commitments and contingencies (Note 23) Shareholders equity: Common stock, $0.000001 par value, 2,400,000,000 shares authorized, 1,197,436,644 and 1,192,093,991 shares issued at December 31, 2019 and December 31, 2018, respectively Additional paid-in capital 11,174 10,963 Less: Treasury stock, at cost, 428,676,471 shares at December 31, 2019 and December 31, 2018 (5,563) (5,563) Retained earnings 7,813 6,593 Accumulated other comprehensive loss (619) (601) Total shareholders equity 12,805 11,392 Total liabilities and shareholders equity $ 19,845 $ 17,890 The accompanying notes are an integral part of these Consolidated Financial Statements. F-4

证据 2：Table of Contents ACTIVISION BLIZZARD, INC. AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF OPERATIONS (Amounts in millions, except per share data) For the Years Ended December 31, 2019 2018 2017 Net revenues Product sales $ 1,975 $ 2,255 $ 2,110 Subscription, licensing, and other revenues 4,514 5,245 4,907 Total net revenues 6,489 7,500 7,017 Costs and expenses Cost of revenuesproduct sales: Product costs 656 719 733 Software royalties, amortization, and intellectual property licenses 240 371 300 Cost of revenuessubscription, licensing, and other revenues: Game operations and distribution costs 965 1,028 984 Software royalties, amortization, and intellectual property licenses 233 399 484 Product development 998 1,101 1,069 Sales and marketing 926 1,062 1,378 General and administrative 732 822 745 Restructuring and related costs 132 10 15 Total costs and expenses 4,882 5,512 5,708 Operating income 1,607 1,988 1,309 Interest and other expense (income), net (Note 18) (26) 71 146 Loss on extinguishment of debt 40 12 Income before income tax expense 1,633 1,877 1,151 Income tax expense 130 29 878 Net income $ 1,503 $ 1,848 $ 273 Earnings per common share Basic $ 1.96 $ 2.43 $ 0.36 Diluted $ 1.95 $ 2.40 $ 0.36 Weighted-average number of shares outstanding Basic 767 762 754 Diluted 771 771 766 The accompanying notes are an integral part of these Consolidated Financial Statements. F-5

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_07966

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Activision Blizzard；文档：ACTIVISIONBLIZZARD_2019_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2017 - FY2019 3 year average of capex as a % of revenue for Activision Blizzard? Answer in units of percents and round to one decimal place. Calculate (or extract) the answer from the statement of income and the cash flow statement.
- 标准答案：1.9%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Capital expenditures. This metric was located in the 10K as a single line item named: Capital expenditures.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: Total net revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Activision Blizzard, ACTIVISIONBLIZZARD_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents ACTIVISION BLIZZARD, INC. AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF OPERATIONS (Amounts in millions, except per share data) For the Years Ended December 31, 2019 2018 2017 Net revenues Product sales $ 1,975 $ 2,255 $ 2,110 Subscription, licensing, and other revenues 4,514 5,245 4,907 Total net revenues 6,489 7,500 7,017 Costs and expenses Cost of revenuesproduct sales: Product costs 656 719 733 Software royalties, amortization, and intellectual property licenses 240 371 300 Cost of revenuessubscription, licensing, and other revenues: Game operations and distribution costs 965 1,028 984 Software royalties, amortization, and intellectual property licenses 233 399 484 Product development 998 1,101 1,069 Sales and marketing 926 1,062 1,378 General and administrative 732 822 745 Restructuring and related costs 132 10 15 Total costs and expenses 4,882 5,512 5,708 Operating income 1,607 1,988 1,309 Interest and other expense (income), net (Note 18) (26) 71 146 Loss on extinguishment of debt 40 12 Income before income tax expense 1,633 1,877 1,151 Income tax expense 130 29 878 Net income $ 1,503 $ 1,848 $ 273 Earnings per common share Basic $ 1.96 $ 2.43 $ 0.36 Diluted $ 1.95 $ 2.40 $ 0.36 Weighted-average number of shares outstanding Basic 767 762 754 Diluted 771 771 766 The accompanying notes are an integral part of these Consolidated Financial Statements. F-5

证据 2：Table of Contents ACTIVISION BLIZZARD, INC. AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF CASH FLOWS (Amounts in millions) For the Years Ended December 31, 2019 2018 2017 Cash flows from operating activities: Net income $ 1,503 $ 1,848 $ 273 Adjustments to reconcile net income to net cash provided by operating activities: Deferred income taxes (352) (35) (181) Provision for inventories 6 6 33 Non-cash operating lease cost 64 Depreciation and amortization 328 509 888 Amortization of capitalized software development costs and intellectual property licenses (1) 225 489 311 Loss on extinguishment of debt 40 12 Share-based compensation expense (2) 166 209 176 Unrealized gain on equity investment (Note 10) (38) Other 51 7 40 Changes in operating assets and liabilities, net of effect from business acquisitions: Accounts receivable, net 182 (114) (165) Inventories 7 (5) (26) Software development and intellectual property licenses (275) (372) (301) Other assets 164 (51) (97) Deferred revenues (154) (122) 220 Accounts payable 31 (65) 85 Accrued expenses and other liabilities (77) (554) 945 Net cash provided by operating activities 1,831 1,790 2,213 Cash flows from investing activities: Proceeds from maturities of available-for-sale investments 153 116 80 Purchases of available-for-sale investments (65) (209) (135) Capital expenditures (116) (131) (155) Other investing activities 6 (6) 3 Net cash used in investing activities (22) (230) (207) Cash flows from financing activities: Proceeds from issuance of common stock to employees 105 99 178 Tax payment related to net share settlements on restricted stock units (59) (94) (56) Dividends paid (283) (259) (226) Proceeds from debt issuances, net of discounts 3,741 Repayment of long-term debt (1,740) (4,251) Premium payment for early redemption of note (25) Other financing activities (1) (10) Net cash used in financing activities (237) (2,020) (624) Effect of foreign exchange rate changes on cash and cash equivalents (3) (31) 76 Net increase (decrease) in cash and cash equivalents and restricted cash 1,569 (491) 1,458 Cash and cash equivalents and restricted cash at beginning of period 4,229 4,720 3,262 Cash and cash equivalents and restricted cash at end of period $ 5,798 $ 4,229 $ 4,720 (1) Excludes deferral and amortization of share-based compensation expense. (2) Includes the net effects of capitalization, deferral, and amortization of share-based compensation expense. The accompanying notes are an integral part of these Consolidated Financial Statements. F-8

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04735

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Adobe；文档：ADOBE_2015_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：You are an investment banker and your only resource(s) to answer the following question is (are): the statement of financial position and the cash flow statement. Here's the question: what is the FY2015 operating cash flow ratio for Adobe? Operating cash flow ratio is defined as: cash from operations / total current liabilities. Round your answer to two decimal places.
- 标准答案：0.66
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cash from operations. This metric was located in the 10K as a single line item named: Net cash provided by operating activities.

Metric 2: Total current liabilities. This metric was located in the 10K as a single line item named: Total current liabilities.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Adobe, ADOBE_2015_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：59 ADOBE SYSTEMS INCORPORATED CONSOLIDATED BALANCE SHEETS (In thousands, except par value) November 27, 2015 November 28, 2014 ASSETS Current assets: Cash and cash equivalents.................................................................................................................... $ 876,560 $ 1,117,400 Short-term investments ........................................................................................................................ 3,111,524 2,622,091 Trade receivables, net of allowances for doubtful accounts of $7,293 and $7,867, respectively........ 672,006 591,800 Deferred income taxes.......................................................................................................................... 95,279 Prepaid expenses and other current assets ........................................................................................... 161,802 175,758 Total current assets.......................................................................................................................... 4,821,892 4,602,328 Property and equipment, net................................................................................................................... 787,421 785,123 Goodwill ................................................................................................................................................. 5,366,881 4,721,962 Purchased and other intangibles, net....................................................................................................... 510,007 469,662 Investment in lease receivable................................................................................................................ 80,439 80,439 Other assets............................................................................................................................................. 159,832 126,315 Total assets...................................................................................................................................... $ 11,726,472 $ 10,785,829 LIABILITIES AND STOCKHOLDERS EQUITY Current liabilities: Trade payables...................................................................................................................................... $ 93,307 $ 68,377 Accrued expenses................................................................................................................................. 678,364 683,866 Debt and capital lease obligations........................................................................................................ 603,229 Accrued restructuring........................................................................................................................... 1,520 17,120 Income taxes payable........................................................................................................................... 6,165 23,920 Deferred revenue.................................................................................................................................. 1,434,200 1,097,923 Total current liabilities.................................................................................................................... 2,213,556 2,494,435 Long-term liabilities: Debt and capital lease obligations........................................................................................................ 1,907,231 911,086 Deferred revenue.................................................................................................................................. 51,094 57,401 Accrued restructuring........................................................................................................................... 3,214 5,194 Income taxes payable........................................................................................................................... 256,129 125,746 Deferred income taxes.......................................................................................................................... 208,209 342,315 Other liabilities..................................................................................................................................... 85,459 73,747 Total liabilities................................................................................................................................ 4,724,892 4,009,924 Commitments and contingencies Stockholders equity: Preferred stock, $0.0001 par value; 2,000 shares authorized; none issued.......................................... Common stock, $0.0001 par value; 900,000 shares authorized; 600,834 shares issued; 497,809 and 497,484 shares outstanding, respectively...................................................................... 61 61 Additional paid-in-capital .................................................................................................................... 4,184,883 3,778,495 Retained earnings................................................................................................................................. 7,253,431 6,924,294 Accumulated other comprehensive income (loss) ............................................................................... (169,080) (8,094) Treasury stock, at cost (103,025 and 103,350 shares, respectively), net of reissuances...................... (4,267,715) (3,918,851) Total stockholders equity............................................................................................................... 7,001,580 6,775,905 Total liabilities and stockholders equity........................................................................................ $ 11,726,472 $ 10,785,829 See accompanying Notes to Consolidated Financial Statements.

证据 2：63 ADOBE SYSTEMS INCORPORATED CONSOLIDATED STATEMENTS OF CASH FLOWS (In thousands) Years Ended November 27, 2015 November 28, 2014 November 29, 2013 Cash flows from operating activities: Net income..................................................................................................................... $ 629,551 $ 268,395 $ 289,985 Adjustments to reconcile net income to net cash provided by operating activities: Depreciation, amortization and accretion................................................................. 339,473 313,590 321,227 Stock-based compensation ....................................................................................... 335,859 333,701 328,987 Deferred income taxes.............................................................................................. (69,657) (26,089) 29,704 Gain on the sale of property ..................................................................................... (21,415) Write down of assets held for sale............................................................................ 23,151 Unrealized (gains) losses on investments................................................................. (9,210) (74) 5,665 Tax benefit from stock-based compensation............................................................ 68,133 53,225 25,290 Excess tax benefits from stock-based compensation................................................ (68,153) (53,235) (40,619) Other non-cash items................................................................................................ 1,216 1,889 5,654 Changes in operating assets and liabilities, net of acquired assets and assumed liabilities: Trade receivables, net ............................................................................................ (79,502) 7,928 33,649 Prepaid expenses and other current assets ............................................................. (7,701) (1,918) (55,509) Trade payables ....................................................................................................... 22,870 6,211 7,132 Accrued expenses................................................................................................... (5,944) 37,544 41,828 Accrued restructuring............................................................................................. (16,620) 8,871 (6,949) Income taxes payable............................................................................................. 29,801 11,006 (58,875) Deferred revenue.................................................................................................... 320,801 326,438 201,366 Net cash provided by operating activities......................................................... 1,469,502 1,287,482 1,151,686 Cash flows from investing activities: Purchases of short-term investments ............................................................................. (2,064,833) (2,014,186) (2,058,058) Maturities of short-term investments............................................................................. 371,790 272,076 360,485 Proceeds from sales of short-term investments ............................................................. 1,176,476 1,443,577 1,449,961 Acquisitions, net of cash acquired ................................................................................. (826,004) (29,802) (704,589) Purchases of property and equipment............................................................................ (184,936) (148,332) (188,358) Proceeds from sale of property ...................................................................................... 57,779 24,260 Purchases of long-term investments, intangibles and other assets ................................ (22,779) (17,572) (67,737) Proceeds from sale of long-term investments................................................................ 4,149 3,532 6,233 Net cash used for investing activities ............................................................... (1,488,358) (490,707) (1,177,803) Cash flows from financing activities: Purchases of treasury stock............................................................................................ (625,000) (600,000) (1,100,000) Proceeds from issuance of treasury stock...................................................................... 164,270 227,841 598,194 Cost of issuance of treasury stock.................................................................................. (186,373) (173,675) (97,418) Excess tax benefits from stock-based compensation..................................................... 68,153 53,235 40,619 Proceeds from debt and capital lease obligations .......................................................... 989,280 25,703 Repayment of debt and capital lease obligations........................................................... (602,189) (14,684) (25,879) Debt issuance costs ........................................................................................................ (8,828) (357) Net cash used for financing activities............................................................... (200,687) (507,283) (559,138) Effect of foreign currency exchange rates on cash and cash equivalents......................... (21,297) (6,648) (5,241) Net increase (decrease) in cash and cash equivalents....................................................... (240,840) 282,844 (590,496) Cash and cash equivalents at beginning of year............................................................... 1,117,400 834,556 1,425,052 Cash and cash equivalents at end of year ......................................................................... $ 876,560 $ 1,117,400 $ 834,556 Supplemental disclosures: Cash paid for income taxes, net of refunds.................................................................... $ 203,010 $ 20,140 $ 129,701 Cash paid for interest ..................................................................................................... $ 56,014 $ 68,886 $ 64,843 Non-cash investing activities: Investment in lease receivable applied to building purchase......................................... $ $ 126,800 $ Issuance of common stock and stock awards assumed in business acquisitions........... $ 677 $ 21 $ 1,160 See accompanying Notes to Consolidated Financial Statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_07507

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Adobe；文档：ADOBE_2016_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Adobe's year-over-year change in unadjusted operating income from FY2015 to FY2016 (in units of percents and round to one decimal place)? Give a solution to the question by using the income statement.
- 标准答案：65.4%
- 答案依据：The metric unadjusted operating income was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Operating income. The final step was to execute the desired percent change calculation on unadjusted operating income.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Adobe, ADOBE_2016_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents 62 ADOBE SYSTEMS INCORPORATED CONSOLIDATED STATEMENTS OF INCOME (In thousands, except per share data) Years Ended December 2, 2016 November 27, 2015 November 28, 2014 Revenue: Subscription $ 4,584,833 $ 3,223,904 $ 2,076,584 Product 800,498 1,125,146 1,627,803 Services and support 469,099 446,461 442,678 Total revenue 5,854,430 4,795,511 4,147,065 Cost of revenue: Subscription 461,860 409,194 335,432 Product 68,917 90,035 97,099 Services and support 289,131 245,088 189,549 Total cost of revenue 819,908 744,317 622,080 Gross profit 5,034,522 4,051,194 3,524,985 Operating expenses: Research and development 975,987 862,730 844,353 Sales and marketing 1,910,197 1,683,242 1,652,308 General and administrative 577,710 531,919 543,332 Restructuring and other charges (1,508) 1,559 19,883 Amortization of purchased intangibles 78,534 68,649 52,424 Total operating expenses 3,540,920 3,148,099 3,112,300 Operating income 1,493,602 903,095 412,685 Non-operating income (expense): Interest and other income (expense), net 13,548 33,909 7,267 Interest expense (70,442) (64,184) (59,732) Investment gains (losses), net (1,570) 961 1,156 Total non-operating income (expense), net (58,464) (29,314) (51,309) Income before income taxes 1,435,138 873,781 361,376 Provision for income taxes 266,356 244,230 92,981 Net income $ 1,168,782 $ 629,551 $ 268,395 Basic net income per share $ 2.35 $ 1.26 $ 0.54 Shares used to compute basic net income per share 498,345 498,764 497,867 Diluted net income per share $ 2.32 $ 1.24 $ 0.53 Shares used to compute diluted net income per share 504,299 507,164 508,480 See accompanying Notes to Consolidated Financial Statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03856

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Adobe；文档：ADOBE_2017_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2017 operating cash flow ratio for Adobe? Operating cash flow ratio is defined as: cash from operations / total current liabilities. Round your answer to two decimal places. Please utilize information provided primarily within the balance sheet and the cash flow statement.
- 标准答案：0.83
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cash from operations. This metric was located in the 10K as a single line item named: Net cash provided by operating activities.

Metric 2: Total current liabilities. This metric was located in the 10K as a single line item named: Total current liabilities.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Adobe, ADOBE_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents 57 ADOBE SYSTEMS INCORPORATED CONSOLIDATED BALANCE SHEETS (In thousands, except par value) December 1, 2017 December 2, 2016 ASSETS Current assets: Cash and cash equivalents $ 2,306,072 $ 1,011,315 Short-term investments 3,513,702 3,749,985 Trade receivables, net of allowances for doubtful accounts of $9,151 and $6,214, respectively 1,217,968 833,033 Prepaid expenses and other current assets 210,071 245,441 Total current assets 7,247,813 5,839,774 Property and equipment, net 936,976 816,264 Goodwill 5,821,561 5,406,474 Purchased and other intangibles, net 385,658 414,405 Investment in lease receivable 80,439 Other assets 143,548 139,890 Total assets $ 14,535,556 $ 12,697,246 LIABILITIES AND STOCKHOLDERS EQUITY Current liabilities: Trade payables $ 113,538 $ 88,024 Accrued expenses 993,773 739,630 Income taxes payable 14,196 38,362 Deferred revenue 2,405,950 1,945,619 Total current liabilities 3,527,457 2,811,635 Long-term liabilities: Debt and capital lease obligations 1,881,421 1,892,200 Deferred revenue 88,592 69,131 Income taxes payable 173,088 184,381 Deferred income taxes 279,941 217,660 Other liabilities 125,188 97,404 Total liabilities 6,075,687 5,272,411 Commitments and contingencies Stockholders equity: Preferred stock, $0.0001 par value; 2,000 shares authorized; none issued Common stock, $0.0001 par value; 900,000 shares authorized; 600,834 shares issued; 491,262 and 494,254 shares outstanding, respectively 61 61 Additional paid-in-capital 5,082,195 4,616,331 Retained earnings 9,573,870 8,114,517 Accumulated other comprehensive income (loss) (111,821) (173,602) Treasury stock, at cost (109,572 and 106,580 shares, respectively), net of reissuances (6,084,436) (5,132,472) Total stockholders equity 8,459,869 7,424,835 Total liabilities and stockholders equity $ 14,535,556 $ 12,697,246 See accompanying Notes to Consolidated Financial Statements.

证据 2：Table of Contents 61 ADOBE SYSTEMS INCORPORATED CONSOLIDATED STATEMENTS OF CASH FLOWS (In thousands) Years Ended December 1, 2017 December 2, 2016 November 27, 2015 Cash flows from operating activities: Net income $ 1,693,954 $ 1,168,782 $ 629,551 Adjustments to reconcile net income to net cash provided by operating activities: Depreciation, amortization and accretion 325,997 331,535 339,473 Stock-based compensation 451,451 349,912 335,859 Deferred income taxes 51,605 24,222 (69,657) Gain on the sale of property (21,415) Unrealized (gains) losses on investments (5,494) 3,145 (9,210) Excess tax benefits from stock-based compensation (75,105) (68,153) Other non-cash items 4,625 2,022 1,216 Changes in operating assets and liabilities, net of acquired assets and assumed liabilities: Trade receivables, net (187,173) (160,416) (79,502) Prepaid expenses and other current assets 28,040 (71,021) (7,701) Trade payables (45,186) (6,281) 22,870 Accrued expenses 154,125 64,978 (22,564) Income taxes payable (34,493) 43,115 97,934 Deferred revenue 475,402 524,840 320,801 Net cash provided by operating activities 2,912,853 2,199,728 1,469,502 Cash flows from investing activities: Purchases of short-term investments (1,931,011) (2,285,222) (2,064,833) Maturities of short-term investments 759,737 769,228 371,790 Proceeds from sales of short-term investments 1,393,929 860,849 1,176,476 Acquisitions, net of cash acquired (459,626) (48,427) (826,004) Purchases of property and equipment (178,122) (203,805) (184,936) Proceeds from sale of property 57,779 Purchases of long-term investments, intangibles and other assets (29,918) (58,433) (22,779) Proceeds from sale of long-term investments 2,134 5,777 4,149 Net cash used for investing activities (442,877) (960,033) (1,488,358) Cash flows from financing activities: Purchases of treasury stock (1,100,000) (1,075,000) (625,000) Proceeds from issuance of treasury stock 158,351 145,697 164,270 Taxes paid related to net share settlement of equity awards (240,126) (236,400) (186,373) Excess tax benefits from stock-based compensation 75,105 68,153 Proceeds from debt issuance 989,280 Repayment of debt and capital lease obligations (1,960) (108) (602,189) Debt issuance costs (8,828) Net cash used for financing activities (1,183,735) (1,090,706) (200,687) Effect of foreign currency exchange rates on cash and cash equivalents 8,516 (14,234) (21,297) Net increase (decrease) in cash and cash equivalents 1,294,757 134,755 (240,840) Cash and cash equivalents at beginning of year 1,011,315 876,560 1,117,400 Cash and cash equivalents at end of year $ 2,306,072 $ 1,011,315 $ 876,560 Supplemental disclosures: Cash paid for income taxes, net of refunds $ 396,668 $ 249,884 $ 203,010 Cash paid for interest $ 69,430 $ 66,193 $ 56,014 Non-cash investing activities: Investment in lease receivable applied to building purchase $ 80,439 $ $ Issuance of common stock and stock awards assumed in business acquisitions $ 10,348 $ $ 677 See accompanying Notes to Consolidated Financial Statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00438

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Adobe；文档：ADOBE_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR information extraction。
- 问题：Does Adobe have an improving operating margin profile as of FY2022? If operating margin is not a useful metric for a company like this, then state that and explain why.
- 标准答案：No the operating margins of Adobe have recently declined from 36.8% in FY 2021 to 34.6% in FY2022. A drop by 2.2% in a year.
- 答案依据：6098/16388
5802/14573

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Adobe, ADOBE_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：ADOBE INC. CONSOLIDATED STATEMENTS OF INCOME (In millions, except per share data) Years Ended December 2, 2022 December 3, 2021 November 27, 2020 Revenue: Subscription $ 16,388 $ 14,573 $ 11,626 Product 532 555 507 Services and other 686 657 735 Total revenue 17,606 15,785 12,868 Cost of revenue: Subscription 1,646 1,374 1,108 Product 35 41 36 Services and other 484 450 578 Total cost of revenue 2,165 1,865 1,722 Gross profit 15,441 13,920 11,146 Operating expenses: Research and development 2,987 2,540 2,188 Sales and marketing 4,968 4,321 3,591 General and administrative 1,219 1,085 968 Amortization of intangibles 169 172 162 Total operating expenses 9,343 8,118 6,909 Operating income 6,098 5,802 4,237

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00591

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Adobe；文档：ADOBE_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Does Adobe have an improving Free cashflow conversion as of FY2022?
- 标准答案：Yes, the FCF conversion (using net income as the denominator) for Adobe has improved by ~13% from 143% in 2021 to 156% in 2022
- 答案依据：FCF Conversion: (Net cash provided by operating activities - Purchases of property and equipment)/Net income
(7838-442)/4756
(7230-348)/4822

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Adobe, ADOBE_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：ADOBE INC. CONSOLIDATED STATEMENTS OF CASH FLOWS (In millions) Years Ended December 2, 2022 December 3, 2021 November 27, 2020 Cash flows from operating activities: Net income $ 4,756 $ 4,822 $ 5,260 Adjustments to reconcile net income to net cash provided by operating activities: Depreciation, amortization and accretion 856 788 757 Stock-based compensation 1,440 1,069 909 Reduction of operating lease right-of-use assets 83 73 87 Deferred income taxes 328 183 (1,501) Unrealized losses (gains) on investments, net 29 (4) (11) Other non-cash items 10 7 40 Changes in operating assets and liabilities, net of acquired assets and assumed liabilities: Trade receivables, net (198) (430) 106 Prepaid expenses and other assets (94) (475) (288) Trade payables 66 (20) 96 Accrued expenses and other liabilities 7 162 86 Income taxes payable 19 2 (72) Deferred revenue 536 1,053 258 Net cash provided by operating activities 7,838 7,230 5,727 Cash flows from investing activities: Purchases of short-term investments (909) (1,533) (1,071) Maturities of short-term investments 683 877 915 Proceeds from sales of short-term investments 270 191 167 Acquisitions, net of cash acquired (126) (2,682) Purchases of property and equipment (442) (348) (419) Purchases of long-term investments, intangibles and other assets (46) (42) (15) Proceeds from sales of long-term investments and other assets 9 Net cash used for investing activities (570) (3,537) (414)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01319

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AES Corporation；文档：AES_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What is the quantity of restructuring costs directly outlined in AES Corporation's income statements for FY2022? If restructuring costs are not explicitly outlined then state 0.
- 标准答案：0
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AES Corporation, AES_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Statements of Operations Years ended December 31, 2022, 2021, and 2020 2022 2021 2020 (in millions, except per share amounts) Revenue: Regulated $ 3,538 $ 2,868 $ 2,661 Non-Regulated 9,079 8,273 6,999 Total revenue 12,617 11,141 9,660 Cost of Sales: Regulated (3,162) (2,448) (2,235) Non-Regulated (6,907) (5,982) (4,732) Total cost of sales (10,069) (8,430) (6,967) Operating margin 2,548 2,711 2,693 General and administrative expenses (207) (166) (165) Interest expense (1,117) (911) (1,038) Interest income 389 298 268 Loss on extinguishment of debt (15) (78) (186) Other expense (68) (60) (53) Other income 102 410 75 Loss on disposal and sale of business interests (9) (1,683) (95) Goodwill impairment expense (777) Asset impairment expense (763) (1,575) (864) Foreign currency transaction gains (losses) (77) (10) 55 Other non-operating expense (175) (202) INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE TAXES AND EQUITY IN EARNINGS OF AFFILIATES (169) (1,064) 488 Income tax benefit (expense) (265) 133 (216) Net equity in losses of affiliates (71) (24) (123) INCOME (LOSS) FROM CONTINUING OPERATIONS (505) (955) 149 Gain from disposal of discontinued businesses, net of income tax expense of $0, $1, and $0, respectively 4 3 NET INCOME (LOSS) (505) (951) 152 Less: Net loss (income) attributable to noncontrolling interests and redeemable stock of subsidiaries (41) 542 (106) NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION $ (546) $ (409) $ 46

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00540

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AES Corporation；文档：AES_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- 标准答案：AES has converted inventory 9.5 times in FY 2022.
- 答案依据：Cost of sales/Inventory
10069/1055

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AES Corporation, AES_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Balance Sheets December 31, 2022 and 2021 2022 2021 (in millions, except share and per share data) ASSETS CURRENT ASSETS Cash and cash equivalents $ 1,374 $ 943 Restricted cash 536 304 Short-term investments 730 232 Accounts receivable, net of allowance for doubtful accounts of $5 and $5, respectively 1,799 1,418 Inventory 1,055 604

证据 2：Consolidated Statements of Operations Years ended December 31, 2022, 2021, and 2020 2022 2021 2020 (in millions, except per share amounts) Revenue: Regulated $ 3,538 $ 2,868 $ 2,661 Non-Regulated 9,079 8,273 6,999 Total revenue 12,617 11,141 9,660 Cost of Sales: Regulated (3,162) (2,448) (2,235) Non-Regulated (6,907) (5,982) (4,732) Total cost of sales (10,069) (8,430) (6,967)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_10420

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AES Corporation；文档：AES_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Based on the information provided primarily in the statement of financial position and the statement of income, what is AES's FY2022 return on assets (ROA)? ROA is defined as: FY2022 net income / (average total assets between FY2021 and FY2022). Round your answer to two decimal places.
- 标准答案：-0.02
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Net income. This metric was located in the 10K as a single line item named: NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION.

Metric 2: Total assets. This metric was located in the 10K as a single line item named: TOTAL ASSETS.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AES Corporation, AES_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：128 Consolidated Balance Sheets December 31, 2022 and 2021 2022 2021 (in millions, except share and per share data) ASSETS CURRENT ASSETS Cash and cash equivalents $ 1,374 $ 943 Restricted cash 536 304 Short-term investments 730 232 Accounts receivable, net of allowance for doubtful accounts of $5 and $5, respectively 1,799 1,418 Inventory 1,055 604 Prepaid expenses 98 142 Other current assets, net of CECL allowance of $2 and $0, respectively 1,533 897 Current held-for-sale assets 518 816 Total current assets 7,643 5,356 NONCURRENT ASSETS Property, Plant and Equipment: Land 470 426 Electric generation, distribution assets and other 26,599 25,552 Accumulated depreciation (8,651) (8,486) Construction in progress 4,621 2,414 Property, plant and equipment, net 23,039 19,906 Other Assets: Investments in and advances to affiliates 952 1,080 Debt service reserves and other deposits 177 237 Goodwill 362 1,177 Other intangible assets, net of accumulated amortization of $434 and $385, respectively 1,841 1,450 Deferred income taxes 319 409 Loan receivable, net of allowance of $26 1,051 Other noncurrent assets, net of allowance of $51 and $23, respectively 2,979 2,188 Noncurrent held-for-sale assets 1,160 Total other assets 7,681 7,701 TOTAL ASSETS $ 38,363 $ 32,963 LIABILITIES AND EQUITY CURRENT LIABILITIES Accounts payable $ 1,730 $ 1,153 Accrued interest 249 182 Accrued non-income taxes 249 266 Accrued and other liabilities 2,151 1,205 Non-recourse debt, including $416 and $302, respectively, related to variable interest entities 1,758 1,367 Current held-for-sale liabilities 354 559 Total current liabilities 6,491 4,732 NONCURRENT LIABILITIES Recourse debt 3,894 3,729 Non-recourse debt, including $2,295 and $2,223, respectively, related to variable interest entities 17,846 13,603 Deferred income taxes 1,139 977 Other noncurrent liabilities 3,168 3,358 Noncurrent held-for-sale liabilities 740 Total noncurrent liabilities 26,047 22,407 Commitments and Contingencies (see Notes 12 and 13) Redeemable stock of subsidiaries 1,321 1,257 EQUITY THE AES CORPORATION STOCKHOLDERS EQUITY Preferred stock (without par value, 50,000,000 shares authorized; 1,043,050 issued and outstanding at December 31, 2022 and December 31, 2021) 838 838 Common stock ($0.01 par value, 1,200,000,000 shares authorized; 818,790,001 issued and 668,743,464 outstanding at December 31, 2022 and 818,717,043 issued and 666,793,625 outstanding at December 31, 2021) 8 8 Additional paid-in capital 6,688 7,106 Accumulated deficit (1,635) (1,089) Accumulated other comprehensive loss (1,640) (2,220) Treasury stock, at cost (150,046,537 and 151,923,418 shares at December 31, 2022 and December 31, 2021, respectively) (1,822) (1,845) Total AES Corporation stockholders equity 2,437 2,798 NONCONTROLLING INTERESTS 2,067 1,769 Total equity 4,504 4,567 TOTAL LIABILITIES AND EQUITY $ 38,363 $ 32,963 See Accompanying Notes to Consolidated Financial Statements.

证据 2：129 Consolidated Statements of Operations Years ended December 31, 2022, 2021, and 2020 2022 2021 2020 (in millions, except per share amounts) Revenue: Regulated $ 3,538 $ 2,868 $ 2,661 Non-Regulated 9,079 8,273 6,999 Total revenue 12,617 11,141 9,660 Cost of Sales: Regulated (3,162) (2,448) (2,235) Non-Regulated (6,907) (5,982) (4,732) Total cost of sales (10,069) (8,430) (6,967) Operating margin 2,548 2,711 2,693 General and administrative expenses (207) (166) (165) Interest expense (1,117) (911) (1,038) Interest income 389 298 268 Loss on extinguishment of debt (15) (78) (186) Other expense (68) (60) (53) Other income 102 410 75 Loss on disposal and sale of business interests (9) (1,683) (95) Goodwill impairment expense (777) Asset impairment expense (763) (1,575) (864) Foreign currency transaction gains (losses) (77) (10) 55 Other non-operating expense (175) (202) INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE TAXES AND EQUITY IN EARNINGS OF AFFILIATES (169) (1,064) 488 Income tax benefit (expense) (265) 133 (216) Net equity in losses of affiliates (71) (24) (123) INCOME (LOSS) FROM CONTINUING OPERATIONS (505) (955) 149 Gain from disposal of discontinued businesses, net of income tax expense of $0, $1, and $0, respectively 4 3 NET INCOME (LOSS) (505) (951) 152 Less: Net loss (income) attributable to noncontrolling interests and redeemable stock of subsidiaries (41) 542 (106) NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION $ (546) $ (409) $ 46 AMOUNTS ATTRIBUTABLE TO THE AES CORPORATION COMMON STOCKHOLDERS: Income (loss) from continuing operations, net of tax $ (546) $ (413) $ 43 Income from discontinued operations, net of tax 4 3 NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION $ (546) $ (409) $ 46 BASIC EARNINGS PER SHARE: Income (loss) from continuing operations attributable to The AES Corporation common stockholders, net of tax $ (0.82) $ (0.62) $ 0.06 Income from discontinued operations attributable to The AES Corporation common stockholders, net of tax 0.01 0.01 NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION COMMON STOCKHOLDERS $ (0.82) $ (0.61) $ 0.07 DILUTED EARNINGS PER SHARE: Income (loss) from continuing operations attributable to The AES Corporation common stockholders, net of tax $ (0.82) $ (0.62) $ 0.06 Income from discontinued operations attributable to The AES Corporation common stockholders, net of tax 0.01 0.01 NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION COMMON STOCKHOLDERS $ (0.82) $ (0.61) $ 0.07 See Accompanying Notes to Consolidated Financial Statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_06655

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amazon；文档：AMAZON_2017_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Amazon's FY2017 days payable outstanding (DPO)? DPO is defined as: 365 * (average accounts payable between FY2016 and FY2017) / (FY2017 COGS + change in inventory between FY2016 and FY2017). Round your answer to two decimal places. Address the question by using the line items and information shown within the balance sheet and the P&L statement.
- 标准答案：93.86
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Accounts payable. This metric was located in the 10K as a single line item named: Accounts payable.

Metric 2: Inventories. This metric was located in the 10K as a single line item named: Inventories.

Metric 3: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of sales.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amazon, AMAZON_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents AMAZON.COM, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (in millions, except per share data) Year Ended December 31, 2015 2016 2017 Net product sales $ 79,268 $ 94,665 $ 118,573 Net service sales 27,738 41,322 59,293 Total net sales 107,006 135,987 177,866 Operating expenses: Cost of sales 71,651 88,265 111,934 Fulfillment 13,410 17,619 25,249 Marketing 5,254 7,233 10,069 Technology and content 12,540 16,085 22,620 General and administrative 1,747 2,432 3,674 Other operating expense, net 171 167 214 Total operating expenses 104,773 131,801 173,760 Operating income 2,233 4,186 4,106 Interest income 50 100 202 Interest expense (459) (484) (848) Other income (expense), net (256) 90 346 Total non-operating income (expense) (665) (294) (300) Income before income taxes 1,568 3,892 3,806 Provision for income taxes (950) (1,425) (769) Equity-method investment activity, net of tax (22) (96) (4) Net income $ 596 $ 2,371 $ 3,033 Basic earnings per share $ 1.28 $ 5.01 $ 6.32 Diluted earnings per share $ 1.25 $ 4.90 $ 6.15 Weighted-average shares used in computation of earnings per share: Basic 467 474 480 Diluted 477 484 493 See accompanying notes to consolidated financial statements. 38

证据 2：Table of Contents AMAZON.COM, INC. CONSOLIDATED BALANCE SHEETS (in millions, except per share data) December 31, 2016 2017 ASSETS Current assets: Cash and cash equivalents $ 19,334 $ 20,522 Marketable securities 6,647 10,464 Inventories 11,461 16,047 Accounts receivable, net and other 8,339 13,164 Total current assets 45,781 60,197 Property and equipment, net 29,114 48,866 Goodwill 3,784 13,350 Other assets 4,723 8,897 Total assets $ 83,402 $ 131,310 LIABILITIES AND STOCKHOLDERS EQUITY Current liabilities: Accounts payable $ 25,309 $ 34,616 Accrued expenses and other 13,739 18,170 Unearned revenue 4,768 5,097 Total current liabilities 43,816 57,883 Long-term debt 7,694 24,743 Other long-term liabilities 12,607 20,975 Commitments and contingencies (Note 7) Stockholders equity: Preferred stock, $0.01 par value: Authorized shares 500 Issued and outstanding shares none Common stock, $0.01 par value: Authorized shares 5,000 Issued shares 500 and 507 Outstanding shares 477 and 484 5 5 Treasury stock, at cost (1,837) (1,837) Additional paid-in capital 17,186 21,389 Accumulated other comprehensive loss (985) (484) Retained earnings 4,916 8,636 Total stockholders equity 19,285 27,709 Total liabilities and stockholders equity $ 83,402 $ 131,310 See accompanying notes to consolidated financial statements. 40

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_08135

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amazon；文档：AMAZON_2017_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Amazon's year-over-year change in revenue from FY2016 to FY2017 (in units of percents and round to one decimal place)? Calculate what was asked by utilizing the line items clearly shown in the statement of income.
- 标准答案：30.8%
- 答案依据：The metric total revenue was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total net sales. The final step was to execute the desired percent change calculation on total revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amazon, AMAZON_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents AMAZON.COM, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (in millions, except per share data) Year Ended December 31, 2015 2016 2017 Net product sales $ 79,268 $ 94,665 $ 118,573 Net service sales 27,738 41,322 59,293 Total net sales 107,006 135,987 177,866 Operating expenses: Cost of sales 71,651 88,265 111,934 Fulfillment 13,410 17,619 25,249 Marketing 5,254 7,233 10,069 Technology and content 12,540 16,085 22,620 General and administrative 1,747 2,432 3,674 Other operating expense, net 171 167 214 Total operating expenses 104,773 131,801 173,760 Operating income 2,233 4,186 4,106 Interest income 50 100 202 Interest expense (459) (484) (848) Other income (expense), net (256) 90 346 Total non-operating income (expense) (665) (294) (300) Income before income taxes 1,568 3,892 3,806 Provision for income taxes (950) (1,425) (769) Equity-method investment activity, net of tax (22) (96) (4) Net income $ 596 $ 2,371 $ 3,033 Basic earnings per share $ 1.28 $ 5.01 $ 6.32 Diluted earnings per share $ 1.25 $ 4.90 $ 6.15 Weighted-average shares used in computation of earnings per share: Basic 467 474 480 Diluted 477 484 493 See accompanying notes to consolidated financial statements. 38

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_08286

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amazon；文档：AMAZON_2019_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：By drawing conclusions from the information stated only in the income statement, what is Amazon's FY2019 net income attributable to shareholders (in USD millions)?
- 标准答案：$11588.00
- 答案依据：The metric net income was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Net income.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amazon, AMAZON_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents AMAZON.COM, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (in millions, except per share data) Year Ended December 31, 2017 2018 2019 Net product sales $ 118,573 $ 141,915 $ 160,408 Net service sales 59,293 90,972 120,114 Total net sales 177,866 232,887 280,522 Operating expenses: Cost of sales 111,934 139,156 165,536 Fulfillment 25,249 34,027 40,232 Technology and content 22,620 28,837 35,931 Marketing 10,069 13,814 18,878 General and administrative 3,674 4,336 5,203 Other operating expense (income), net 214 296 201 Total operating expenses 173,760 220,466 265,981 Operating income 4,106 12,421 14,541 Interest income 202 440 832 Interest expense (848) (1,417) (1,600) Other income (expense), net 346 (183) 203 Total non-operating income (expense) (300) (1,160) (565) Income before income taxes 3,806 11,261 13,976 Provision for income taxes (769) (1,197) (2,374) Equity-method investment activity, net of tax (4) 9 (14) Net income $ 3,033 $ 10,073 $ 11,588 Basic earnings per share $ 6.32 $ 20.68 $ 23.46 Diluted earnings per share $ 6.15 $ 20.14 $ 23.01 Weighted-average shares used in computation of earnings per share: Basic 480 487 494 Diluted 493 500 504 See accompanying notes to consolidated financial statements. 38

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03882

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2020_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is Amcor's year end FY2020 net AR (in USD millions)? Address the question by adopting the perspective of a financial analyst who can only use the details shown within the balance sheet.
- 标准答案：$1616.00
- 答案依据：The metric accounts receivable, net was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Trade receivables, net.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Amcor plc and Subsidiaries Consolidated Balance Sheet (in millions) As of June 30, 2020 2019 Assets Current assets: Cash and cash equivalents $ 742.6 $ 601.6 Trade receivables, net 1,615.9 1,864.3 Inventories, net 1,831.9 1,953.8 Prepaid expenses and other current assets 344.3 374.3 Assets held for sale 416.1 Total current assets 4,534.7 5,210.1 Non-current assets: Investments in affiliated companies 77.7 98.9 Property, plant and equipment, net 3,614.8 3,975.0 Operating lease assets 525.3 Deferred tax assets 135.4 190.9 Other intangible assets, net 1,994.3 2,306.8 Goodwill 5,339.3 5,156.0 Employee benefit assets 43.4 40.2 Other non-current assets 177.2 187.1 Total non-current assets 11,907.4 11,954.9 Total assets $ 16,442.1 $ 17,165.0 Liabilities Current liabilities: Current portion of long-term debt $ 11.1 $ 5.4 Short-term debt 195.2 788.8 Trade payables 2,170.8 2,303.4 Accrued employee costs 476.5 378.4 Other current liabilities 1,120.0 1,044.9 Liabilities held for sale 20.9 Total current liabilities 3,973.6 4,541.8 Non-current liabilities: Long-term debt, less current portion 6,028.4 5,309.0 Operating lease liabilities 465.7 Deferred tax liabilities 672.4 1,011.7 Employee benefit obligations 391.7 386.8 Other non-current liabilities 223.2 241.0 Total non-current liabilities 7,781.4 6,948.5 Total liabilities 11,755.0 11,490.3 Commitments and contingencies (See Note 19) Shareholders' Equity Amcor plc shareholders equity: Ordinary shares ($0.01 par value): Authorized (9,000.0 shares) Issued (1,568.5 and 1,625.9 shares, respectively) 15.7 16.3 Additional paid-in capital 5,480.0 6,007.5 Retained earnings 246.5 323.7 Accumulated other comprehensive income (loss) (1,049.3) (722.4) Treasury shares (6.7 and 1.4 shares, respectively) (67.0) (16.1) Total Amcor plc shareholders' equity 4,625.9 5,609.0 Non-controlling interest 61.2 65.7 Total shareholders' equity 4,687.1 5,674.7 Total liabilities and shareholders' equity $ 16,442.1 $ 17,165.0 See accompanying notes to consolidated financial statements. 50

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01935

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2022_8K_dated-2022-07-01。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What was the key agenda of the AMCOR's 8k filing dated 1st July 2022?
- 标准答案：Amcor Finance (USA), Inc. and Amcor Flexibles North America, Inc., entered into supplemental indentures relating to Guaranteed Senior Notes due 2026 and 2028. This involved the substitution of the Substitute Issuer (Amcor Flexibles North America) for the Former Issuer (Amcor Finance) and the assumption of covenants under the indentures. (In essence a novation agreement)
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2022_8K_dated-2022-07-01, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：On June 30, 2022, Amcor Finance (USA), Inc. (the Former Issuer) and Amcor Flexibles North America, Inc. (the Substitute Issuer), each a wholly-owned subsidiary of Amcor plc (the Company), entered into a (i) Second Supplemental Indenture (the Second Supplemental Indenture) with the Trustee (as defined below) with respect to the Indenture, dated as of April 28, 2016 (as amended and/or supplemented to date, the 2016 Indenture and, together with the Second Supplemental Indenture, the 2016 Indenture), among the Former Issuer, the guarantors party thereto and Deutsche Bank Trust Company Americas, as trustee (the Trustee), governing the Former Issuers (a) 3.625% Guaranteed Senior Notes due 2026 (the 2026 Notes) and (b) 4.500% Guaranteed Senior Notes due 2028 (the 2028 Notes and, together with the 2026 Notes, the Existing Notes) and (ii) First Supplemental Indenture (the First Supplemental Indenture and, together with the Second Supplemental Indenture, the Supplemental Indentures) with the Trustee with respect to the Indenture, dated as of June 13, 2019 (as amended and/or supplemented to date, the 2019 Indenture and, together with the First Supplemental Indenture, the 2019 Indenture and, together with the 2016 Indenture, the Indentures), among the Former Issuer, the guarantors party thereto and the Trustee, governing the Former Issuers (a) 3.625% Guaranteed Senior Notes due 2026 (the New 2026 Notes) and (b) 4.500% Guaranteed Senior Notes due 2028 (the New 2028 Notes and, together with the New 2026 Notes, the New Notes), in each case, relating to the substitution of the Substitute Issuer for the Former Issuer and the assumption by the Substitute Issuer of the covenants of the Former Issuer under the Indentures. As disclosed in the Companys Current Report on Form 8-K, filed with the Securities and Exchange Commission (the SEC) on June 17, 2019, the New Notes were issued in June 2019 following the completion of the Former Issuers exchange offer to certain eligible holders of the Existing Notes.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00799

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Has AMCOR's quick ratio improved or declined between FY2023 and FY2022? If the quick ratio is not something that a financial analyst would ask about a company like this, then state that and explain why.
- 标准答案：The quick ratio has slightly improved from 0.67 times to 0.69 times between FY 2023 and FY 2022.(3.4% jump)
- 答案依据：Quick Ratio= (Total current assets-(Raw materials and supplies+Work in process and finished goods))/Total current liabilities
(5308-992-1221)/4476
(5853-1114-1325)/5103

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Amcor plc and Subsidiaries Consolidated Balance Sheets ($ in millions, except share and per share data) As of June 30, 2023 2022 Assets Current assets: Cash and cash equivalents $ 689 $ 775 Trade receivables, net of allowance for credit losses of $21 and $25, respectively 1,875 1,935 Inventories, net Raw materials and supplies 992 1,114 Work in process and finished goods 1,221 1,325 Prepaid expenses and other current assets 531 512 Assets held for sale, net 192 Total current assets 5,308 5,853 Non-current assets: Property, plant, and equipment, net 3,762 3,646 Operating lease assets 533 560 Deferred tax assets 134 130 Other intangible assets, net 1,524 1,657 Goodwill 5,366 5,285 Employee benefit assets 67 89 Other non-current assets 309 206 Total non-current assets 11,695 11,573 Total assets $ 17,003 $ 17,426 Liabilities Current liabilities: Current portion of long-term debt $ 13 $ 14 Short-term debt 80 136 Trade payables 2,690 3,073 Accrued employee costs 396 471 Other current liabilities 1,297 1,344 Liabilities held for sale 65 Total current liabilities 4,476 5,103 Non-current liabilities: Long-term debt, less current portion 6,653 6,340 Operating lease liabilities 463 493 Deferred tax liabilities 616 677 Employee benefit obligations 224 201 Other non-current liabilities 481 471 Total non-current liabilities 8,437 8,182 Total liabilities $ 12,913 $ 13,285 Commitments and contingencies (See Note 20) Shareholders' Equity Amcor plc shareholders equity: Ordinary shares ($0.01 par value): Authorized (9,000 million shares) Issued (1,448 and 1,489 million shares, respectively) $ 14 $ 15 Additional paid-in capital 4,021 4,431 Retained earnings 865 534 Accumulated other comprehensive loss (862) (880) Treasury shares (1 and 2 million shares, respectively) (12) (18) Total Amcor plc shareholders' equity 4,026 4,082 Non-controlling interests 64 59 Total shareholders' equity 4,090 4,141 Total liabilities and shareholders' equity $ 17,003 $ 17,426 See accompanying notes to consolidated financial statements. 5

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01079

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are major acquisitions that AMCOR has done in FY2023, FY2022 and FY2021?
- 标准答案：Amcor completed these acquisitions during FY2023:
-100% equity interest of a flexibles manufacturing company in the Czech Republic
- 100% equity interest in a medical device packaging manufacturing site in
Shanghai, China.
-acquisition of a New Zealand-based leading manufacturer of state-of-the-art, automated protein
packaging machines.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：On August 1, 2022, the Company completed the acquisition of 100% equity interest in a Czech Republic company that operates a world-class flexible packaging manufacturing plant. The purchase consideration of $59 million included a deferred portion of $5 million that was paid in the first quarter of fiscal year 2024. The acquisition is part of the Company's Flexibles reportable segment and resulted in the recognition of acquired identifiable net assets of $36 million and goodwill of $23 million. Goodwill is not deductible for tax purposes. The fair values of the identifiable net assets acquired and goodwill are based on the Company's best estimate as of June 30, 2023. On March 17, 2023, the Company completed the acquisition of 100% equity interest in a medical device packaging manufacturing site in Shanghai, China. The purchase consideration of $60 million is subject to customary post-closing adjustments. The consideration includes contingent consideration of $20 million, to be earned and paid in cash over the three years following the acquisition date, subject to meeting certain performance targets. The acquisition is part of the Company's Flexibles reportable segment and resulted in the recognition of acquired identifiable net assets of $21 million and goodwill of $39 million. Goodwill is not deductible for tax purposes. The fair values of the contingent consideration, identifiable net assets acquired, and goodwill are based on the Company's best estimate as of June 30, 2023, and are considered preliminary. The Company aims to complete the purchase price allocation as soon as practicable but no later than one year from the date of the acquisition. On May 31, 2023, the Company completed the acquisition of a New Zealand based leading manufacturer of state-of-the-art, automated protein packaging machines. The purchase consideration of $45 million is subject to customary post-closing adjustments. The consideration includes contingent consideration of $13 million, to be earned and paid in cash over the two years following the acquisition date, subject to meeting certain performance targets. The acquisition is part of the Company's Flexibles reportable segment and resulted in the recognition of acquired identifiable net assets of $9 million and goodwill of $36 million. Goodwill is deductible for tax purposes. The fair values of the contingent consideration, identifiable net assets acquired, and goodwill are based on the Company's best estimate as of June 30, 2023, and are considered preliminary. The Company aims to complete the purchase price allocation as soon as practicable but no later than one year from the date of the acquisition.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
