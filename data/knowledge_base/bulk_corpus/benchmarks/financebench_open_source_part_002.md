# FinanceBench 样本：financebench_id_01148

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023_10K。
- 问题类型：domain-relevant；推理类型：Information extraction OR Logical reasoning OR。
- 问题：What industry does AMCOR primarily operate in?
- 标准答案：Amcor is a global leader in packaging production for various use cases.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Today, we are a global leader in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other products

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00684

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR information extraction。
- 问题：Does AMCOR have an improving gross margin profile as of FY2023? If gross margin is not a useful metric for a company like this, then state that and explain why.
- 标准答案：No. For AMCOR there has been a slight decline in gross margins by 0.8%.
- 答案依据：Gross Profit/Net Sales
2725/14694
2820/14544

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Amcor plc and Subsidiaries Consolidated Statements of Income ($ in millions, except per share data) For the years ended June 30, 2023 2022 2021 Net sales $ 14,694 $ 14,544 $ 12,861 Cost of sales (11,969) (11,724) (10,129) Gross profit 2,725 2,820 2,732

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01936

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What is the nature & purpose of AMCOR's restructuring liability as oF Q2 of FY2023 close?
- 标准答案：87% of the total restructuring liability is related Employee liabilities.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：($ in millions) Employee Costs Fixed Asset Related Costs Other Costs Total Restructuring Costs Liability balance at June 30, 2022 $ 97 $ 3 $ 18 $ 118 Net charges to earnings 2 2 Cash paid (16) (1) (8) (25) Reversal of unused amounts (2) (2) Liability balance at December 31, 2022 $ 81 $ 2 $ 10 $ 93

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01928

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What Was AMCOR's Adjusted Non GAAP EBITDA for FY 2023
- 标准答案：AMCOR's Adj. EBITDA was $2,018mn in FY 2023
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Twelve Months Ended June 30, 2022 Twelve Months Ended June 30, 2023 ($ million) EBITDA EBIT Net Income EPS (Diluted US cents)(1) EBITDA EBIT Net Income EPS (Diluted US cents)(1) Net income attributable to Amcor 805 805 805 52.9 1,048 1,048 1,048 70.5 Net income attributable to non-controlling interests 10 10 10 10 Tax expense 300 300 193 193 Interest expense, net 135 135 259 259 Depreciation and amortization 579 569 EBITDA, EBIT, Net income and EPS 1,829 1,250 805 52.9 2,080 1,510 1,048 70.5 2019 Bemis Integration Plan 37 37 37 2.5 Net loss on disposals(2) 10 10 10 0.7 Impact of hyperinflation 16 16 16 1.0 24 24 24 1.9 Property and other losses, net(3) 13 13 13 0.8 2 2 2 0.1 Russia-Ukraine conflict impacts(4) 200 200 200 13.2 (90) (90) (90) (6.0) Pension settlements 8 8 8 0.5 5 5 5 0.3 Other 4 4 4 0.3 (3) (3) (3) (0.3) Amortization of acquired intangibles (5) 163 163 10.7 160 160 10.8 Tax effect of above items (32) (2.1) (57) (4.0) Adjusted EBITDA, EBIT, Net income and EPS 2,117 1,701 1,224 80.5 2,018 1,608 1,089 73.3

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01930

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Amcor；文档：AMCOR_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：How much was the Real change in Sales for AMCOR in FY 2023 vs FY 2022, if we exclude the impact of FX movement, passthrough costs and one-off items?
- 标准答案：The Real Growth was flat in FY 2023 vs FY 2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Amcor, AMCOR_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Three Months Ended June 30 Twelve Months Ended June 30 ($ million) Flexibles Rigid Packaging Total Flexibles Rigid Packaging Total Net sales fiscal year 2023 2,777 897 3,673 11,154 3,540 14,694 Net sales fiscal year 2022 2,967 942 3,909 11,151 3,393 14,544 Reported Growth % (6) (5) (6) 4 1 FX % 1 (1) (4) (1) (3) Constant Currency Growth % (7) (4) (6) 4 5 4 Raw Material Pass Through % 1 1 5 8 5 Items affecting comparability % (3) (2) (2) (1) Comparable Constant Currency Growth % (5) (4) (5) 1 (3) Volume % (7) (6) (7) (3) (4) (3) Price/Mix % 2 2 2 4 1 3

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03069

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2015_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Answer the following question as if you are an equity research analyst and have lost internet connection so you do not have access to financial metric providers. According to the details clearly outlined within the P&L statement and the statement of cash flows, what is the FY2015 depreciation and amortization (D&A from cash flow statement) % margin for AMD?
- 标准答案：4.2%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: Net revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2015_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA Advanced Micro Devices, Inc. Consolidated Statements of Operations Year Ended December 26, 2015 December 27, 2014 December 28, 2013 (In millions, except per share amounts) Net revenue $ 3,991 $ 5,506 $ 5,299 Cost of sales 2,911 3,667 3,321 Gross margin 1,080 1,839 1,978 Research and development 947 1,072 1,201 Marketing, general and administrative 482 604 674 Amortization of acquired intangible assets 3 14 18 Restructuring and other special charges, net 129 71 30 Goodwill impairment charge 233 Legal settlements, net (48) Operating income (loss) (481) (155) 103 Interest expense (160) (177) (177) Other expense, net (5) (66) Loss before income taxes (646) (398) (74) Provision for income taxes 14 5 9 Net loss $ (660) $ (403) $ (83) Net loss per share Basic $ (0.84) $ (0.53) $ (0.11) Diluted $ (0.84) $ (0.53) $ (0.11) Shares used in per share calculation Basic 783 768 754 Diluted 783 768 754 See accompanying notes to consolidated financial statements. 54

证据 2：Advanced Micro Devices, Inc. Consolidated Statements of Cash Flows Year Ended December 26, 2015 December 27, 2014 December 28, 2013 (In millions) Cash flows from operating activities: Net loss $ (660) $ (403) $ (83) Adjustments to reconcile net loss to net cash used in operating activities: Depreciation and amortization 167 203 236 Net loss on disposal of property, plant and equipment 31 Stock-based compensation expense 63 81 91 Non-cash interest expense 11 17 25 Goodwill impairment charge 233 Restructuring and other special charges, net 83 14 Net loss on debt redemptions 61 1 Other (3) (13) (1) Changes in operating assets and liabilities: Accounts receivable 280 7 (200) Inventories (11) 199 (322) Prepayments and other - GLOBALFOUNDRIES 84 (113) Prepaid expenses and other assets (111) (7) (103) Accounts payables, accrued liabilities and other (156) (231) 266 Payable to GLOBALFOUNDRIES 27 (146) (89) Net cash used in operating activities (226) (98) (148) Cash flows from investing activities: Purchases of available-for-sale securities (227) (790) (1,043) Purchases of property, plant and equipment (96) (95) (84) Proceeds from sales and maturities of available-for-sale securities 462 873 1,344 Proceeds from sale of property, plant and equipment 8 238 Net cash provided by (used in) investing activities 147 (12) 455 Cash flows from financing activities: Proceeds from borrowings, net 100 1,155 55 Proceeds from issuance of common stock 5 4 3 Repayments of long-term debt and capital lease obligations (44) (1,115) (55) Other (2) 2 10 Net cash provided by financing activities 59 46 13 Net increase (decrease) in cash and cash equivalents (20) (64) 320 Cash and cash equivalents at beginning of year 805 869 549 Cash and cash equivalents at end of year $ 785 $ 805 $ 869 Supplemental disclosures of cash flow information: Cash paid during the year for: Interest $ 149 $ 138 $ 152 Income taxes $ 3 $ 7 $ 9 See accompanying notes to consolidated financial statements. 58

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00222

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Logical reasoning。
- 问题：Does AMD have a reasonably healthy liquidity profile based on its quick ratio for FY22? If the quick ratio is not relevant to measure liquidity, please state that and explain why.
- 标准答案：Yes. The quick ratio is 1.57, calculated as (cash and cash equivalents+Short term investments+Accounts receivable, net+receivables from related parties)/ (current liabilities).
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Balance Sheets December 31, 2022 December 25, 2021 (In millions, except par value amounts) ASSETS Current assets: Cash and cash equivalents $ 4,835 $ 2,535 Short-term investments 1,020 1,073 Accounts receivable, net 4,126 2,706 Inventories 3,771 1,955 Receivables from related parties 2 2 Prepaid expenses and other current assets 1,265 312 Total current assets 15,019 8,583 Property and equipment, net 1,513 702 Operating lease right-of-use assets 460 367 Goodwill 24,177 289 Acquisition-related intangibles 24,118 Investment: equity method 83 69 Deferred tax assets 58 931 Other non-current assets 2,152 1,478 Total assets $ 67,580 $ 12,419 LIABILITIES AND STOCKHOLDERS EQUITY Current liabilities: Accounts payable $ 2,493 $ 1,321 Payables to related parties 463 85 Accrued liabilities 3,077 2,424 Current portion of long-term debt, net 312 Other current liabilities 336 98 Total current liabilities 6,369 4,240 Long-term debt, net of current portion 2,467 1 Long-term operating lease liabilities 396 348 Deferred tax liabilities 1,934 12 Other long-term liabilities 1,664 321 Commitments and Contingencies (see Notes 16 and 17) Stockholders equity: Capital stock: Common stock, par value $0.01; shares authorized: 2,250; shares issued: 1,645 and 1,232; shares outstanding: 1,612 and 1,207 16 12 Additional paid-in capital 58,005 11,069 Treasury stock, at cost (shares held: 33 and 25) (3,099) (2,130) Accumulated deficit (131) (1,451) Accumulated other comprehensive loss (41) (3) Total stockholders equity 54,750 7,497 Total liabilities and stockholders equity $ 67,580 $ 12,419

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00995

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are the major products and services that AMD sells as of FY22?
- 标准答案：AMD sells server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and Adaptive System-on-Chip (SoC) products for data centers; CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers; discrete GPUs, and semi-custom SoC products and development services; and embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Overview We are a global semiconductor company primarily offering: server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and Adaptive System-on-Chip (SoC) products for data centers; CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers; discrete GPUs, and semi-custom SoC products and development services; and embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products. From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01198

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What drove revenue change as of the FY22 for AMD?
- 标准答案：In 2022, AMD reported Higher sales of their EPYC server processors, higher semi-custom product sales, and the inclusion of Xilinx embedded product sales
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Net revenue for 2022 was $23.6 billion, an increase of 44% compared to 2021 net revenue of $16.4 billion. The increase in net revenue was driven by a 64% increase in Data Center segment revenue primarily due to higher sales of our EPYC server processors, a 21% increase in Gaming segment revenue primarily due to higher semi-custom product sales, and a significant increase in Embedded segment revenue from the prior year period driven by the inclusion of Xilinx embedded product sales.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00917

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Numerical reasoning OR Logical reasoning。
- 问题：What drove operating margin change as of the FY22 for AMD? If operating margin is not a useful metric for a company like this, then please state that and explain why.
- 标准答案：The decrease in AMD's operating income was primarily driven by amortization of intangible assets associated with the Xilinx acquisition
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Operating income for 2022 was $1.3 billion compared to operating income of $3.6 billion for 2021. The decrease in operating income was primarily driven by amortization of intangible assets associated with the Xilinx acquisition.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01279

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for AMD in FY22?
- 标准答案：In 2022, AMD brought in the most cashflow from Operations
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Advanced Micro Devices, Inc. Consolidated Statements of Cash Flows Year Ended December 31, 2022 December 25, 2021 December 26, 2020 (In millions) Cash flows from operating activities: Net income $ 1,320 $ 3,162 $ 2,490 Adjustments to reconcile net income to net cash provided by operating activities: Depreciation and amortization 4,174 407 312 Stock-based compensation 1,081 379 274 Amortization of debt discount and issuance costs 5 14 Amortization of operating lease right-of-use assets 88 56 42 Amortization of inventory fair value adjustment 189 Loss on debt redemption, repurchase and conversion 7 54 Loss on sale or disposal of property and equipment 16 34 33 Deferred income taxes (1,505) 308 (1,223) (Gains) losses on equity investments, net 62 (56) (2) Other (14) (7) 8 Changes in operating assets and liabilities: Accounts receivable, net (1,091) (640) (219) Inventories (1,401) (556) (417) Receivables from related parties (13) 8 10 Prepaid expenses and other assets (1,197) (920) (231) Payables to related parties 379 7 (135) Accounts payable 931 801 (513) Accrued liabilities and other 546 526 574 Net cash provided by operating activities 3,565 3,521 1,071 Cash flows from investing activities: Purchases of property and equipment (450) (301) (294) Purchases of short-term investments (2,667) (2,056) (850) Proceeds from maturity of short-term investments 4,310 1,678 192 Cash received from acquisition of Xilinx 2,366 Acquisition of Pensando, net of cash acquired (1,544) Other (16) (7) Net cash provided by (used in) investing activities 1,999 (686) (952) Cash flows from financing activities: Proceeds from debt, net of issuance costs 991 200 Repayment of debt (312) (200) Proceeds from sales of common stock through employee equity plans 167 104 85 Repurchases of common stock (3,702) (1,762) Common stock repurchases for tax withholding on employee equity plans (406) (237) (78) Other (2) (1) Net cash (used in) provided by financing activities (3,264) (1,895) 6 Net increase in cash and cash equivalents 2,300 940 125 Cash and cash equivalents at beginning of year 2,535 1,595 1,470 Cash and cash equivalents at end of year $ 4,835 $ 2,535 $ 1,595

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00563

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：From FY21 to FY22, excluding Embedded, in which AMD reporting segment did sales proportionally increase the most?
- 标准答案：Data Center
- 答案依据：Data center: 
FY22: 6,043
FY21: 3,694 
6,043/3,694-1 = 63,59%

Client: 
FY22: 6,201
FY21: 6,887 
6,201/6,887-1 = -9,96%


Gaming: 
FY22: 6,805
FY21: 5,607 
6,805/5,607-1 = 21,37%

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Year Ended December 31, 2022 December 25, 2021 (In millions) Net revenue: Data Center $ 6,043 $ 3,694 Client 6,201 6,887 Gaming 6,805 5,607 Embedded 4,552 246 Total net revenue $ 23,601 $ 16,434 Operating income (loss): Data Center $ 1,848 $ 991 Client 1,190 2,088 Gaming 953 934 Embedded 2,252 44 All Other (4,979) (409) Total operating income (loss) $ 1,264 $ 3,648

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00757

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：AMD；文档：AMD_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Did AMD report customer concentration in FY22?
- 标准答案：Yes, one customer accounted for 16% of consolidated net revenue
- 答案依据：One customer ccounting for 16% of net evenue is a high customer concenration

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, AMD, AMD_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：One customer accounted for 16% of our consolidated net revenue for the year ended December 31, 2022. Sales to this customer consisted of sales of products from our Gaming segment. A loss of this customer would have a material adverse effect on our business.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00476

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Which debt securities are registered to trade on a national securities exchange under American Express' name as of 2022?
- 标准答案：There are none
- 答案依据：No debt securities are listed under the securities registered pursuant to Section 12(b) of the Act, which implies there are none

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Registrants telephone number, including area code: (212) 640-2000 Securities registered pursuant to Section 12(b) of the Act: Title of each class Trading Symbol(s) Name of each exchange on which registered Common Shares (par value $0.20 per Share) AXP New York Stock Exchange Securities registered pursuant to section 12(g) of the Act: None

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01028

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are the geographies that American Express primarily operates in as of 2022?
- 标准答案：United States, EMEA, APAC, and LACC
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：(Millions) United States EMEA APAC LACC Other Unallocated Consolidated 2022 Total revenues net of interest expense $ 41,396 $ 4,871 $ 3,835 $ 2,917 $ (157) $ 52,862 Pretax income (loss) from continuing operations 10,383 550 376 500 (2,224) 9,585 2021 Total revenues net of interest expense $ 33,103 $ 3,643 $ 3,418 $ 2,238 $ (22) $ 42,380 Pretax income (loss) from continuing operations 10,325 460 420 494 (1,010) 10,689 2020 Total revenues net of interest expense $ 28,263 $ 3,087 $ 3,271 $ 2,019 $ (553) $ 36,087 Pretax income (loss) from continuing operations 5,422 187 328 273 (1,914) 4,296

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00723

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR information extraction。
- 问题：Does AMEX have an improving operating margin profile as of 2022? If operating margin is not a useful metric for a company like this, then state that and explain why.
- 标准答案：Performance is not measured through operating margin
- 答案依据：It's a financial services company and performance is measured through the Net Interest Margin.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：CONSOLIDATED STATEMENTS OF INCOME Year Ended December 31 (Millions, except per share amounts) 2022 2021 2020 Revenues Non-interest revenues Discount revenue $ 30,739 $ 24,563 $ 19,435 Net card fees 6,070 5,195 4,664 Service fees and other revenue 4,521 3,316 2,702 Processed revenue 1,637 1,556 1,301 Total non-interest revenues 42,967 34,630 28,102 Interest income Interest on loans 11,967 8,850 9,779 Interest and dividends on investment securities 96 83 127 Deposits with banks and other 595 100 177 Total interest income 12,658 9,033 10,083 Interest expense Deposits 1,527 458 943 Long-term debt and other 1,236 825 1,155 Total interest expense 2,763 1,283 2,098 Net interest income 9,895 7,750 7,985 Total revenues net of interest expense 52,862 42,380 36,087 Provisions for credit losses Card Member receivables 627 (73) 1,015 Card Member loans 1,514 (1,155) 3,453 Other 41 (191) 262 Total provisions for credit losses 2,182 (1,419) 4,730 Total revenues net of interest expense after provisions for credit losses 50,680 43,799 31,357 Expenses Card Member rewards 14,002 11,007 8,041 Business development 4,943 3,762 3,051 Card Member services 2,959 1,993 1,230 Marketing 5,458 5,291 3,696 Salaries and employee benefits 7,252 6,240 5,718 Other, net 6,481 4,817 5,325 Total expenses 41,095 33,110 27,061 Pretax income 9,585 10,689 4,296 Income tax provision 2,071 2,629 1,161 Net income $ 7,514 $ 8,060 $ 3,135 Earnings per Common Share (Note 21) Basic $ 9.86 $ 10.04 $ 3.77 Diluted $ 9.85 $ 10.02 $ 3.77 Average common shares outstanding for earnings per common share: Basic 751 789 805 Diluted 752 790 806

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00720

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Numerical reasoning OR Logical reasoning。
- 问题：What drove gross margin change as of the FY2022 for American Express? If gross margin is not a useful metric for a company like this, then please state that and explain why.
- 标准答案：Performance is not measured through gross margin
- 答案依据：It's a financial services company and performance is measured through the Net Interest Margin.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：CONSOLIDATED STATEMENTS OF INCOME Year Ended December 31 (Millions, except per share amounts) 2022 2021 2020 Revenues Non-interest revenues Discount revenue $ 30,739 $ 24,563 $ 19,435 Net card fees 6,070 5,195 4,664 Service fees and other revenue 4,521 3,316 2,702 Processed revenue 1,637 1,556 1,301 Total non-interest revenues 42,967 34,630 28,102 Interest income Interest on loans 11,967 8,850 9,779 Interest and dividends on investment securities 96 83 127 Deposits with banks and other 595 100 177 Total interest income 12,658 9,033 10,083 Interest expense Deposits 1,527 458 943 Long-term debt and other 1,236 825 1,155 Total interest expense 2,763 1,283 2,098 Net interest income 9,895 7,750 7,985 Total revenues net of interest expense 52,862 42,380 36,087 Provisions for credit losses Card Member receivables 627 (73) 1,015 Card Member loans 1,514 (1,155) 3,453 Other 41 (191) 262 Total provisions for credit losses 2,182 (1,419) 4,730 Total revenues net of interest expense after provisions for credit losses 50,680 43,799 31,357 Expenses Card Member rewards 14,002 11,007 8,041 Business development 4,943 3,762 3,051 Card Member services 2,959 1,993 1,230 Marketing 5,458 5,291 3,696 Salaries and employee benefits 7,252 6,240 5,718 Other, net 6,481 4,817 5,325 Total expenses 41,095 33,110 27,061 Pretax income 9,585 10,689 4,296 Income tax provision 2,071 2,629 1,161 Net income $ 7,514 $ 8,060 $ 3,135 Earnings per Common Share (Note 21) Basic $ 9.86 $ 10.04 $ 3.77 Diluted $ 9.85 $ 10.02 $ 3.77 Average common shares outstanding for earnings per common share: Basic 751 789 805 Diluted 752 790 806

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01351

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：How much has the effective tax rate of American Express changed between FY2021 and FY2022?
- 标准答案：The effective tax rate for American Express has changed/dropped from 24.6% in FY 2021 to 21.6% in FY 2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：TABLE 1: SUMMARY OF FINANCIAL PERFORMANCE Years Ended December 31, Change Change (Millions, except percentages, per share amounts and where indicated) 2022 2021 2020 2022 vs. 2021 2021 vs. 2020 Selected Income Statement Data Total revenues net of interest expense $ 52,862 $ 42,380 $ 36,087 $ 10,482 25 % $ 6,293 17 % Provisions for credit losses 2,182 (1,419) 4,730 3,601 # (6,149) # Expenses 41,095 33,110 27,061 7,985 24 6,049 22 Pretax income 9,585 10,689 4,296 (1,104) (10) 6,393 # Income tax provision 2,071 2,629 1,161 (558) (21) 1,468 # Net income 7,514 8,060 3,135 (546) (7) 4,925 # Earnings per common share diluted $ 9.85 $ 10.02 $ 3.77 $ (0.17) (2)% $ 6.25 # % Common Share Statistics Cash dividends declared per common share $ 2.08 $ 1.72 $ 1.72 $ 0.36 21 % $ % Average common shares outstanding: Basic 751 789 805 (38) (5)% (16) (2)% Diluted 752 790 806 (38) (5)% (16) (2)% Selected Metrics and Ratios Network volumes (Billions) $ 1,552.8 $ 1,284.2 $ 1,037.8 $ 269 21 % $ 246 24 % Return on average equity 32.3 % 33.7 % 14.2 % Net interest income divided by average Card Member loans 10.4 % 10.2 % 10.7 % Net interest yield on average Card Member loans 10.6 % 10.7 % 11.5 % Effective tax rate 21.6 % 24.6 % 27.0 % Common Equity Tier 1 10.3 % 10.5 % 13.5 % Selected Balance Sheet Data Cash and cash equivalents $ 33,914 $ 22,028 $ 32,965 $ 11,886 54 % $ (10,937) (33)% Card Member receivables 57,613 53,645 43,701 3,968 7 9,944 23 Card Member loans 107,964 88,562 73,373 19,402 22 15,189 21 Customer deposits 110,239 84,382 86,875 25,857 31 (2,493) (3) Long-term debt $ 42,573 $ 38,675 $ 42,952 $ 3,898 10 % $ (4,277) (10)%

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01964

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What was the largest liability in American Express's Balance Sheet in 2022?
- 标准答案：Customer deposits
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：CONSOLIDATED BALANCE SHEETS December 31 (Millions, except share data) 2022 2021 Assets Cash and cash equivalents Cash and due from banks (includes restricted cash of consolidated variable interest entities: 2022, $5; 2021, $11) $ 5,510 $ 1,292 Interest-bearing deposits in other banks (includes securities purchased under resale agreements: 2022, $318; 2021, $463) 28,097 20,548 Short-term investment securities (includes restricted investments of consolidated variable interest entities: 2022, $54; 2021, $32) 307 188 Total cash and cash equivalents 33,914 22,028 Card Member receivables (includes gross receivables available to settle obligations of a consolidated variable interest entity: 2022, $5,193; 2021, $5,175), less reserves for credit losses: 2022, $229; 2021, $64 57,384 53,581 Card Member loans (includes gross loans available to settle obligations of a consolidated variable interest entity: 2022, $28,461; 2021, $26,587), less reserves for credit losses: 2022, $3,747; 2021, $3,305 104,217 85,257 Other loans, less reserves for credit losses: 2022, $59; 2021, $52 5,357 2,859 Investment securities 4,578 2,591 Premises and equipment, less accumulated depreciation and amortization: 2022, $9,850; 2021, $8,602 5,215 4,988 Other assets, less reserves for credit losses: 2022, $22; 2021, $25 17,689 17,244 Total assets $ 228,354 $ 188,548 Liabilities and Shareholders Equity Liabilities Customer deposits $ 110,239 $ 84,382 Accounts payable 12,133 10,574 Short-term borrowings 1,348 2,243 Long-term debt (includes debt issued by consolidated variable interest entities: 2022, $12,662; 2021, $13,803) 42,573 38,675 Other liabilities 37,350 30,497 Total liabilities $ 203,643 $ 166,371 Contingencies and Commitments (Note 12) Shareholders Equity Preferred shares, $1.66 par value, authorized 20 million shares; issued and outstanding 1,600 shares as of December 31, 2022 and 2021 (Note 16) Common shares, $0.20 par value, authorized 3.6 billion shares; issued and outstanding 743 million shares as of December 31, 2022 and 761 million shares as of December 31, 2021 149 153 Additional paid-in capital 11,493 11,495 Retained earnings 16,279 13,474 Accumulated other comprehensive income (loss) (3,210) (2,945) Total shareholders equity 24,711 22,177 Total liabilities and shareholders equity $ 228,354 $ 188,548

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01981

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Express；文档：AMERICANEXPRESS_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Was American Express able to retain card members during 2022?
- 标准答案：Yes
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Express, AMERICANEXPRESS_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Net card fees increased 17 percent year over-year, as new card acquisitions reached record levels in 2022 and Card Member retention remained high, demonstrating the impact of investments we have made in our premium value propositions

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_05718

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Water Works；文档：AMERICANWATERWORKS_2020_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：How much (in USD billions) did American Water Works pay out in cash dividends for FY2020? Compute or extract the answer by primarily using the details outlined in the statement of cash flows.
- 标准答案：$0.40
- 答案依据：The metric total cash dividends paid out was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Dividends paid.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Water Works, AMERICANWATERWORKS_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents American Water Works Company, Inc. and Subsidiary Companies Consolidated Statements of Cash Flows (In millions) For the Years Ended December 31, 2020 2019 2018 CASH FLOWS FROM OPERATING ACTIVITIES Net income $ 709 $ 621 $ 565 Adjustments to reconcile to net cash flows provided by operating activities: Depreciation and amortization 604 582 545 Deferred income taxes and amortization of investment tax credits 207 208 195 Provision for losses on accounts receivable 34 28 33 Loss (gain) on asset dispositions and purchases 34 (20) Impairment charge 57 Pension and non-pension postretirement benefits (14) 17 23 Other non-cash, net (20) (41) 20 Changes in assets and liabilities: Receivables and unbilled revenues (97) (25) (17) Pension and non-pension postretirement benefit contributions (39) (31) (22) Accounts payable and accrued liabilities (2) 66 25 Other assets and liabilities, net 44 (72) 22 Impact of Freedom Industries settlement activities (4) (40) Net cash provided by operating activities 1,426 1,383 1,386 CASH FLOWS FROM INVESTING ACTIVITIES Capital expenditures (1,822) (1,654) (1,586) Acquisitions, net of cash acquired (135) (235) (398) Proceeds from sale of assets 2 48 35 Removal costs from property, plant and equipment retirements, net (106) (104) (87) Net cash used in investing activities (2,061) (1,945) (2,036) CASH FLOWS FROM FINANCING ACTIVITIES Proceeds from long-term debt 1,334 1,530 1,358 Repayments of long-term debt (342) (495) (526) Proceeds from term loan 500 Net short-term borrowings with maturities less than three months (5) (178) 60 Issuance of common stock 183 Proceeds from issuances of employee stock plans and direct stock purchase plan, net of taxes paid of $17, $11 and $8 in 2020, 2019 and 2018, respectively 9 15 16 Advances and contributions in aid of construction, net of refunds of $24, $30 and $22 in 2020, 2019 and 2018, respectively 28 26 21 Debt issuance costs and make-whole premium on early debt redemption (15) (15) (22) Dividends paid (389) (353) (319) Anti-dilutive share repurchases (36) (45) Net cash provided by financing activities 1,120 494 726 Net increase (decrease) in cash, cash equivalents and restricted funds 485 (68) 76 Cash, cash equivalents and restricted funds at beginning of period 91 159 83 Cash, cash equivalents and restricted funds at end of period $ 576 $ 91 $ 159 Cash paid during the year for: Interest, net of capitalized amount $ 382 $ 383 $ 332 Income taxes, net of refunds of $2, $4 and $0 in 2020, 2019 and 2018, respectively $ 7 $ 12 $ 38 Non-cash investing activity: Capital expenditures acquired on account but unpaid as of year end $ 221 $ 235 $ 181 The accompanying notes are an integral part of these Consolidated Financial Statements. 84

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04254

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Water Works；文档：AMERICANWATERWORKS_2021_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Basing your judgments off of the cash flow statement and the income statement, what is American Water Works's FY2021 unadjusted operating income + depreciation and amortization from the cash flow statement (unadjusted EBITDA) in USD millions?
- 标准答案：$1832.00
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization.

Metric 2: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating income.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Water Works, AMERICANWATERWORKS_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents American Water Works Company, Inc. and Subsidiary Companies Consolidated Statements of Operations (In millions, except per share data) For the Years Ended December 31, 2021 2020 2019 Operating revenues $ 3,930 $ 3,777 $ 3,610 Operating expenses: Operation and maintenance 1,777 1,622 1,544 Depreciation and amortization 636 604 582 General taxes 321 303 280 Other (10) Total operating expenses, net 2,734 2,529 2,396 Operating income 1,196 1,248 1,214 Other income (expense): Interest expense (403) (397) (386) Interest income 4 2 4 Non-operating benefit costs, net 78 49 16 Gain or (loss) on sale of businesses 747 (44) Other, net 18 22 29 Total other income (expense) 444 (324) (381) Income before income taxes 1,640 924 833 Provision for income taxes 377 215 212 Net income attributable to common shareholders $ 1,263 $ 709 $ 621 Basic earnings per share: (a) Net income attributable to common shareholders $ 6.96 $ 3.91 $ 3.44 Diluted earnings per share: (a) Net income attributable to common shareholders $ 6.95 $ 3.91 $ 3.43 Weighted average common shares outstanding: Basic 182 181 181 Diluted 182 182 181 (a) Amounts may not calculate due to rounding. The accompanying notes are an integral part of these Consolidated Financial Statements. 84

证据 2：Table of Contents American Water Works Company, Inc. and Subsidiary Companies Consolidated Statements of Cash Flows (In millions) For the Years Ended December 31, 2021 2020 2019 CASH FLOWS FROM OPERATING ACTIVITIES Net income $ 1,263 $ 709 $ 621 Adjustments to reconcile to net cash flows provided by operating activities: Depreciation and amortization 636 604 582 Deferred income taxes and amortization of investment tax credits 230 207 208 Provision for losses on accounts receivable 37 34 28 (Gain) or loss on sale of businesses (747) 34 Pension and non-pension postretirement benefits (41) (14) 17 Other non-cash, net (23) (20) (41) Changes in assets and liabilities: Receivables and unbilled revenues (74) (97) (25) Pension and non-pension postretirement benefit contributions (40) (39) (31) Accounts payable and accrued liabilities 66 (2) 66 Other assets and liabilities, net 134 44 (76) Net cash provided by operating activities 1,441 1,426 1,383 CASH FLOWS FROM INVESTING ACTIVITIES Capital expenditures (1,764) (1,822) (1,654) Acquisitions, net of cash acquired (135) (135) (235) Proceeds from sale of assets, net of cash on hand 472 2 48 Removal costs from property, plant and equipment retirements, net (109) (106) (104) Net cash used in investing activities (1,536) (2,061) (1,945) CASH FLOWS FROM FINANCING ACTIVITIES Proceeds from long-term debt 1,118 1,334 1,530 Repayments of long-term debt (372) (342) (495) (Repayments of) proceeds from term loan (500) 500 Net short-term borrowings with maturities less than three months (198) (5) (178) (Remittances) proceeds from issuances of employee stock plans and direct stock purchase plan, net of taxes paid of $18, $17 and $11 in 2021, 2020 and 2019, respectively (1) 9 15 Advances and contributions in aid of construction, net of refunds of $25, $24 and $30 in 2021, 2020 and 2019, respectively 62 28 26 Debt issuance costs and make-whole premium on early debt redemption (26) (15) (15) Dividends paid (428) (389) (353) Anti-dilutive share repurchases (36) Net cash (used in) provided by financing activities (345) 1,120 494 Net (decrease) increase in cash, cash equivalents and restricted funds (440) 485 (68) Cash, cash equivalents and restricted funds at beginning of period 576 91 159 Cash, cash equivalents and restricted funds at end of period $ 136 $ 576 $ 91 Cash paid during the year for: Interest, net of capitalized amount $ 389 $ 382 $ 383 Income taxes, net of refunds of $6, $2 and $4 in 2021, 2020 and 2019, respectively $ 1 $ 7 $ 12 Non-cash investing activity: Capital expenditures acquired on account but unpaid as of year end $ 292 $ 221 $ 235 Seller promissory note from the sale of the Homeowner Services Group $ 720 $ $ Contingent cash payment from the sale of the Homeowner Services Group $ 75 $ $ The accompanying notes are an integral part of these Consolidated Financial Statements. 86

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00070

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：American Water Works；文档：AMERICANWATERWORKS_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Does American Water Works have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- 标准答案：No, American Water Works had negative working capital of -$1561M in FY 2022.
- 答案依据：Accounts receivable+Income tax receivable+Unbilled revenues+Materials and supplies+other-Accounts payable-Accrued liabilities-Accrued taxes
334+114+275+98+312-254-706-49

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, American Water Works, AMERICANWATERWORKS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：American Water Works Company, Inc. and Subsidiary Companies Consolidated Balance Sheets (In millions, except share and per share data) December 31, 2022 December 31, 2021 ASSETS Property, plant and equipment $ 29,736 $ 27,413 Accumulated depreciation (6,513) (6,329) Property, plant and equipment, net 23,223 21,084 Current assets: Cash and cash equivalents 85 116 Restricted funds 32 20 Accounts receivable, net of allowance for uncollectible accounts of $60 and $75, respectively 334 271 Income tax receivable 114 4 Unbilled revenues 275 248 Materials and supplies 98 57 Assets held for sale 683 Other 312 155 Total current assets 1,250 1,554

证据 2：American Water Works Company, Inc. and Subsidiary Companies Consolidated Balance Sheets (In millions, except share and per share data) December 31, 2022 December 31, 2021 CAPITALIZATION AND LIABILITIES Capitalization: Common stock ($0.01 par value; 500,000,000 shares authorized; 187,200,539 and 186,880,413 shares issued, respectively) $ 2 $ 2 Paid-in-capital 6,824 6,781 Retained earnings 1,267 925 Accumulated other comprehensive loss (23) (45) Treasury stock, at cost (5,342,477 and 5,269,324 shares, respectively) (377) (365) Total common shareholders' equity 7,693 7,298 Long-term debt 10,926 10,341 Redeemable preferred stock at redemption value 3 3 Total long-term debt 10,929 10,344 Total capitalization 18,622 17,642 Current liabilities: Short-term debt 1,175 584 Current portion of long-term debt 281 57 Accounts payable 254 235 Accrued liabilities 706 701 Accrued taxes 49 176 Accrued interest 91 88 Liabilities related to assets held for sale 83 Other 255 217 Total current liabilities 2,811 2,141

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02608

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2017_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：In agreement with the information outlined in the income statement, what is the FY2015 - FY2017 3 year average net profit margin (as a %) for Best Buy? Answer in units of percents and round to one decimal place.
- 标准答案：2.8%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total revenue. This metric was located in the 10K as a single line item named: Revenue.

Metric 2: Net income. This metric was located in the 10K as a single line item named: Net earnings attributable to Best Buy Co., Inc. shareholders.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Statements of Earnings $ and shares in millions, except per share amounts Fiscal Years Ended January 28, 2017 January 30, 2016 January 31, 2015 Revenue $ 39,403 $ 39,528 $ 40,339 Costofgoodssold 29,963 30,334 31,292 Restructuringchargescostofgoodssold 3 Grossprofit 9,440 9,191 9,047 Selling,generalandadministrativeexpenses 7,547 7,618 7,592 Restructuringcharges 39 198 5 Operatingincome 1,854 1,375 1,450 Otherincome(expense) Gainonsaleofinvestments 3 2 13 Investmentincomeandother 31 13 14 Interestexpense (72) (80) (90) Earningsfromcontinuingoperationsbeforeincometaxexpense 1,816 1,310 1,387 Incometaxexpense 609 503 141 Netearningsfromcontinuingoperations 1,207 807 1,246 Gain(loss)fromdiscontinuedoperations(Note2),netoftaxexpenseof$7,$1and$0 21 90 (11) Netearningsincludingnoncontrollinginterests 1,228 897 1,235 Netearningsfromdiscontinuedoperationsattributabletononcontrollinginterests (2) NetearningsattributabletoBestBuyCo.,Inc.shareholders $ 1,228 $ 897 $ 1,233 Basicearnings(loss)pershareattributabletoBestBuyCo.,Inc.shareholders Continuingoperations $ 3.79 $ 2.33 $ 3.57 Discontinuedoperations 0.07 0.26 (0.04) Basicearningspershare $ 3.86 $ 2.59 $ 3.53 Dilutedearnings(loss)pershareattributabletoBestBuyCo.,Inc.shareholders Continuingoperations $ 3.74 $ 2.30 $ 3.53 Discontinuedoperations 0.07 0.26 (0.04) Dilutedearningspershare $ 3.81 $ 2.56 $ 3.49 Weighted-averagecommonsharesoutstanding Basic 318.5 346.5 349.5 Diluted 322.6 350.7 353.6 SeeNotestoConsolidatedFinancialStatements. 54

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04417

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2019_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is the year end FY2019 total amount of inventories for Best Buy? Answer in USD millions. Base your judgments on the information provided primarily in the balance sheet.
- 标准答案：$5409.00
- 答案依据：The metric inventories was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Merchandise inventories.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Balance Sheets $ in millions, except per share and share amounts February 2, 2019 February 3, 2018 Assets Current assets Cashandcashequivalents $ 1,980 $ 1,101 Short-terminvestments 2,032 Receivables,net 1,015 1,049 Merchandiseinventories 5,409 5,209 Othercurrentassets 466 438 Totalcurrentassets 8,870 9,829 Property and equipment Landandbuildings 637 623 Leaseholdimprovements 2,119 2,327 Fixturesandequipment 5,865 5,410 Propertyundercapitalandfinancingleases 579 340 Grosspropertyandequipment 9,200 8,700 Lessaccumulateddepreciation 6,690 6,279 Netpropertyandequipment 2,510 2,421 Goodwill 915 425 Other assets 606 374 Total assets $ 12,901 $ 13,049 Liabilities and equity Current liabilities Accountspayable $ 5,257 $ 4,873 Unredeemedgiftcardliabilities 290 385 Deferredrevenue 446 453 Accruedcompensationandrelatedexpenses 482 561 Accruedliabilities 982 1,001 Currentportionoflong-termdebt 56 544 Totalcurrentliabilities 7,513 7,817 Long-term liabilities 750 809 Long-term debt 1,332 811 Contingencies and commitments (Note 13) Equity BestBuyCo.,Inc.Shareholders'Equity Preferredstock,$1.00parvalue:Authorized400,000shares;Issuedandoutstandingnone Commonstock,$0.10parvalue:Authorized1.0billionshares;Issuedandoutstanding265,703,000and 282,988,000shares,respectively 27 28 Additionalpaid-incapital Retainedearnings 2,985 3,270 Accumulatedothercomprehensiveincome 294 314 Totalequity 3,306 3,612 Total liabilities and equity $ 12,901 $ 13,049 SeeNotestoConsolidatedFinancialStatements. 50

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
