# FinanceBench 样本：financebench_id_00685

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2023_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Logical reasoning。
- 问题：Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why.
- 标准答案：Yes, the margins have been consistent, there has been a minor decline of 1.1% in gross margins between FY2022 and FY2023.
- 答案依据：Gross Profit/Revenue
9912/46298
11640/51761

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Statements of Earnings $ and shares in millions, except per share amounts Fiscal Years Ended January 28, 2023 January 29, 2022 January 30, 2021 Revenue $ 46,298 $ 51,761 $ 47,262 Cost of sales 36,386 40,121 36,689 Gross profit 9,912 11,640 10,573 Selling, general and administrative expenses 7,970 8,635 7,928 Restructuring charges 147 (34) 254 Operating income 1,795 3,039 2,391 Other income (expense): Investment income and other 28 10 38 Interest expense (35) (25) (52) Earnings before income tax expense and equity in income of affiliates 1,788 3,024 2,377 Income tax expense 370 574 579 Equity in income of affiliates 1 4 - Net earnings $ 1,419 $ 2,454 $ 1,798

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01077

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2023_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are major acquisitions that Best Buy has done in FY2023, FY2022 and FY2021?
- 标准答案：Best Buy closed two acquisitions, both these companies were already partially owned by Best Buy, but Best Buy acquired all outstanding shares of these two companies during FY 2022: (1) Current Health Ltd and (2) Two Peaks, LLC d/b/a Yardbird Furniture
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Acquisitions Current Health Ltd. In fiscal 2022, we acquired all of the outstanding shares of Current Health Ltd. (Current Health), a care-at-home technology platform, on November 2, 2021, for net cash consideration of $389 million. The acquired assets included $351 million of goodwill that was assigned to our Best Buy Health reporting unit and was deductible for income tax purposes. The acquisition is aligned with our focus in virtual care to enable people in their homes to connect seamlessly with their health care providers and is included in our Domestic reportable segment and Services revenue category. The acquisition was accounted for using the acquisition method of accounting for business combinations and was not material to the results of operations. Two Peaks, LLC d/b/a Yardbird Furniture In fiscal 2022, we acquired all of the outstanding shares of Two Peaks, LLC d/b/a Yardbird Furniture (Yardbird), a direct-to-consumer outdoor furniture company, on November 4, 2021, for net cash consideration of $79 million. The acquired assets included $47 million of goodwill that was assigned to our Best Buy Domestic reporting unit and was deductible for income tax purposes. The acquisition expands our assortment in categories like outdoor living, as more and more consumers look to make over or upgrade their outdoor living spaces. The acquisition was accounted for using the acquisition method of accounting for business combinations and was not material to the results of our operations.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01275

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2023_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Best Buy in FY2023?
- 标准答案：Best Buy generated the most cash flow from operating activities in FY 2023 ($1.8 bn)
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Statements of Cash Flows $ in millions Fiscal Years Ended January 28, 2023 January 29, 2022 January 30, 2021 Operating activities Net earnings $ 1,419 $ 2,454 $ 1,798 Adjustments to reconcile net earnings to total cash provided by operating activities: Depreciation and amortization 918 869 839 Restructuring charges 147 (34) 254 Stock-based compensation 138 141 135 Deferred income taxes 51 14 (36) Other, net 12 11 3 Changes in operating assets and liabilities, net of acquired assets and liabilities: Receivables (103) 17 73 Merchandise inventories 809 (328) (435) Other assets (21) (14) (51) Accounts payable (1,099) (201) 1,676 Income taxes 36 (156) 173 Other liabilities (483) 479 498 Total cash provided by operating activities 1,824 3,252 4,927 Investing activities Additions to property and equipment, net of $35, $46 and $32, respectively, of non-cash capital expenditures (930) (737) (713) Purchases of investments (46) (233) (620) Sales of investments 7 66 546 Acquisitions, net of cash acquired - (468) - Other, net 7 - (1) Total cash used in investing activities (962) (1,372) (788) Financing activities Repurchase of common stock (1,014) (3,502) (312) Issuance of common stock 16 29 28 Dividends paid (789) (688) (568) Borrowings of debt - - 1,892 Repayments of debt (19) (133) (1,916) Other, net - (3) - Total cash used in financing activities (1,806) (4,297) (876) Effect of exchange rate changes on cash (8) (3) 7 Increase (decrease) in cash, cash equivalents and restricted cash (952) (2,420) 3,270 Cash, cash equivalents and restricted cash at beginning of period 3,205 5,625 2,355 Cash, cash equivalents and restricted cash at end of period $ 2,253 $ 3,205 $ 5,625

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00288

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2024Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Was there any drop in Cash & Cash equivalents between FY 2023 and Q2 of FY2024?
- 标准答案：Yes, there was a decline of ~42% between FY2023 and Q2 of FY 2024.
- 答案依据：1093/1874-1

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2024Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：July 29, 2023 July 30, 2022 July 29, 2023 July 30, 2022 Operating income $ 348 $ 371 $ 659 $ 833 % of revenue 3.6 % 3.6 % 3.5 % 4.0 % Intangible asset amortization(1) 21 22 41 44 Restructuring charges(2) (7) 34 (16) 35 Non-GAAP operating income $ 362 $ 427 $ 684 $ 912 % of revenue 3.8 % 4.1 % 3.6 % 4.3 % Effective tax rate 26.1 % 15.6 % 24.8 % 20.5 % Intangible asset amortization(1) (0.4)% 0.4 % 0.4 % 0.2 % Restructuring charges(2) 0.4 % 0.7 % (0.1)% 0.1 % Loss on investments 0.5 % -% -% -% Non-GAAP effective tax rate 26.6 % 16.7 % 25.1 % 20.8 % Diluted EPS $ 1.25 $ 1.35 $ 2.36 $ 2.85 Intangible asset amortization(1) 0.10 0.10 0.18 0.19 Restructuring charges(2) (0.03) 0.15 (0.07) 0.15 Loss on investments - - 0.02 - Gain on sale of subsidiary, net(3) (0.10) - (0.10) - Income tax impact of non-GAAP adjustments(4) - (0.06) (0.02) (0.08) Non-GAAP diluted EPS $ 1.22 $ 1.54 $ 2.37 $ 3.11 For additional information regarding the nature of charges discussed below, refer to Note 1, Basis of Presentation, Note 2, Restructuring, and Note 3, Goodwill and Intangible Assets, of the Notes to Condensed Consolidated Financial Statements, included in this Quarterly Report on Form 10-Q. (1) Represents the non-cash amortization of definite-lived intangible assets associated with acquisitions, including customer relationships, tradenames and developed technology assets. (2) Represents charges related to employee termination benefits and subsequent adjustments from higher-than-expected employee retention related to previously planned organizational changes. (3) Represents the gain on sale of a Mexico subsidiary subsequent to our exit from operations in Mexico. (4) The non-GAAP adjustments primarily relate to the U.S. and Mexico. As such, the forecasted annual income tax charge on the U.S. non-GAAP adjustments is calculated using the statutory tax rate of 24.5%. There is no forecasted annual income tax benefit for Mexico non-GAAP items, as there is no forecasted annual tax expense on the income in the calculation of GAAP income tax expense. Our non-GAAP operating income rates decreased in the second quarter and first six months of fiscal 2024, primarily due to unfavorable SG&A rates, partially offset by favorable gross profit rates. Our non-GAAP effective tax rate increased in the second quarter of fiscal 2024, primarily due to the prior year resolution of certain discrete tax matters. Our non- GAAP effective tax rate increased in the first six months of fiscal 2024, primarily due to the prior year resolution of certain discrete tax matters and decreased tax benefits from stock-based compensation, partially offset by the impact of lower pre-tax earnings. Our non-GAAP diluted EPS decreased in the second quarter and first six months of fiscal 2024, primarily due to the decreases in non-GAAP operating income. Liquidity and Capital Resources We closely manage our liquidity and capital resources. Our liquidity requirements depend on key variables, including the level of investment required to support our business strategies, the performance of our business, capital expenditures, dividends, credit facilities, short-term borrowing arrangements and working capital management. We modify our approach to managing these variables as changes in our operating environment arise. For example, capital expenditures and share repurchases are a component of our cash flow and capital management strategy, which, to a large extent, we can adjust in response to economic and other changes in our business environment. We have a disciplined approach to capital allocation, which focuses on investing in key priorities that support our strategy. Cash and cash equivalents were as follows ($ in millions): July 29, 2023 January 28, 2023 July 30, 2022 Cash and cash equivalents $ 1,093 $ 1,874 $ 840

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00460

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2024Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Was there any change in the number of Best Buy stores between Q2 of FY2024 and FY2023?
- 标准答案：Yes, there is decline in number stores by 1.32% from 982 stores in Q2 FY 2023 to 969 by the end of Q2 FY2024.
- 答案依据：969/982-1

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2024Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：iscal 2024 was primarily driven by comparable sales declines in appliances, home theater, computing and mobile phones, partially offset by comparable sales growth in gaming. Online revenue of $2.8 billion and $5.5 billion in the second quarter and first six months of fiscal 2024 decreased 7.1% and 9.7% on a comparable basis, respectively. These decreases in revenue were primarily due to the reasons described above and within the Consolidated Results section, above. Domestic segment stores open at the beginning and end of the second quarters of fiscal 2024 and fiscal 2023 were as follows: Fiscal 2024 Fiscal 2023 Total Stores at Beginning of Second Quarter Stores Opened Stores Closed Total Stores at End of Second Quarter Total Stores at Beginning of Second Quarter Stores Opened Stores Closed Total Stores at End of Second Quarter Best Buy 908 - (1) 907 931 1 (2) 930 Outlet Centers 20 1 (1) 20 16 2 - 18 Pacific Sales 20 - - 20 21 - - 21 Yardbird 18 4 - 22 9 4 - 13 Total 966 5 (2) 969 977 7 (2) 982

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01902

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Best Buy；文档：BESTBUY_2024Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which Best Buy product category performed the best (by top line) in the domestic (USA) Market during Q2 of FY2024?
- 标准答案：The entertainment segment experienced the highest growth of 9% during Q2 FY2024, primarily from gaming division.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Best Buy, BESTBUY_2024Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Computing and Mobile Phones: The 6.4% comparable sales decline was driven primarily by computing, mobile phones and tablets. Consumer Electronics: The 5.7% comparable sales decline was driven primarily by home theater, partially offset by comparable sales growth in headphones and portable speakers. Appliances: The 16.1% comparable sales decline was driven primarily by large appliances. Entertainment: The 9.0% comparable sales growth was driven primarily by gaming, partially offset by comparable sales declines in virtual reality and drones. Services: The 7.6% comparable sales growth was driven primarily by the cumulative growth in our paid membership base

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04660

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Block；文档：BLOCK_2016_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Considering the data in the balance sheet, what is Block's (formerly known as Square) FY2016 working capital ratio? Define working capital ratio as total current assets divided by total current liabilities. Round your answer to two decimal places.
- 标准答案：1.73
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total current liabilities. This metric was located in the 10K as a single line item named: Total current liabilities.

Metric 2: Total current assets. This metric was located in the 10K as a single line item named: Total current assets.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Block, BLOCK_2016_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：SQUARE,INC. CONSOLIDATEDBALANCESHEETS (In thousands, except share and per share data) December31, 2016 2015 Assets Currentassets: Cashandcashequivalents $ 452,030 $ 461,329 Short-terminvestments 59,901 Restrictedcash 22,131 13,537 Settlementsreceivable 321,102 142,727 Customerfundsheld 43,574 9,446 Loansheldforsale 42,144 604 Merchantcashadvancereceivable,net 4,212 36,473 Othercurrentassets 56,331 41,447 Totalcurrentassets 1,001,425 705,563 Propertyandequipment,net 88,328 87,222 Goodwill 57,173 56,699 Acquiredintangibleassets,net 19,292 26,776 Long-terminvestments 27,366 Restrictedcash 14,584 14,686 Otherassets 3,194 3,826 Totalassets $ 1,211,362 $ 894,772 LiabilitiesandStockholdersEquity Currentliabilities: Accountspayable $ 12,602 $ 18,869 Customerspayable 388,058 215,365 Customerfundsobligation 43,574 9,446 Accruedtransactionlosses 20,064 17,176 Accruedexpenses 39,543 44,401 Othercurrentliabilities 73,623 28,945 Totalcurrentliabilities 577,464 334,202 Debt(Note11) Otherliabilities 57,745 52,522 Totalliabilities 635,209 386,724 Commitmentsandcontingencies(Note16) Stockholdersequity: Preferredstock,$0.0000001parvalue:100,000,000sharesauthorizedatDecember31,2016andDecember31,2015.None issuedandoutstandingatDecember31,2016andDecember31,2015. ClassAcommonstock,$0.0000001parvalue:1,000,000,000sharesauthorizedatDecember31,2016andDecember31,2015; 198,746,620and31,717,133issuedandoutstandingatDecember31,2016andDecember31,2015,respectively. ClassBcommonstock,$0.0000001parvalue:500,000,000sharesauthorizedatDecember31,2016andDecember31,2015; 165,800,756and303,232,312issuedandoutstandingatDecember31,2016andDecember31,2015,respectively. Additionalpaid-incapital 1,357,381 1,116,882 Accumulatedothercomprehensiveloss (1,989) (1,185) Accumulateddeficit (779,239) (607,649) Totalstockholdersequity 576,153 508,048 Totalliabilitiesandstockholdersequity $ 1,211,362 $ 894,772 Seeaccompanyingnotestoconsolidatedfinancialstatements. 68

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03838

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Block；文档：BLOCK_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2019 - FY2020 total revenue growth rate for Block (formerly known as Square)? Answer in units of percents and round to one decimal place. Approach the question asked by assuming the standpoint of an investment banking analyst who only has access to the statement of income.
- 标准答案：101.5%
- 答案依据：The metric total revenue was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total net revenue. The final step was to execute the desired percent change calculation on total revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Block, BLOCK_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：SQUARE, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (In thousands, except per share data) Year Ended December 31, 2020 2019 2018 Revenue: Transaction-basedrevenue $ 3,294,978 $ 3,081,074 $ 2,471,451 Subscriptionandservices-basedrevenue 1,539,403 1,031,456 591,706 Hardwarerevenue 91,654 84,505 68,503 Bitcoinrevenue 4,571,543 516,465 166,517 Totalnetrevenue 9,497,578 4,713,500 3,298,177 Costofrevenue: Transaction-basedcosts 1,911,848 1,937,971 1,558,562 Subscriptionandservices-basedcosts 222,712 234,270 169,884 Hardwarecosts 143,901 136,385 94,114 Bitcoincosts 4,474,534 508,239 164,827 Amortizationofacquiredtechnology 11,174 6,950 7,090 Totalcostofrevenue 6,764,169 2,823,815 1,994,477 Grossprofit 2,733,409 1,889,685 1,303,700 Operatingexpenses: Productdevelopment 881,826 670,606 497,479 Salesandmarketing 1,109,670 624,832 411,151 Generalandadministrative 579,203 436,250 339,245 Transactionandloanlosses 177,670 126,959 88,077 Amortizationofacquiredcustomerassets 3,855 4,481 4,362 Totaloperatingexpenses 2,752,224 1,863,128 1,340,314 Operatingincome(loss) (18,815) 26,557 (36,614) Gainonsaleofassetgroup (373,445) Interestexpense,net 56,943 21,516 17,982 Otherexpense(income),net (291,725) 273 (18,469) Income(loss)beforeincometax 215,967 378,213 (36,127) Provisionforincometaxes 2,862 2,767 2,326 Netincome(loss) $ 213,105 $ 375,446 $ (38,453) Netincome(loss)pershare: Basic $ 0.48 $ 0.88 $ (0.09) Diluted $ 0.44 $ 0.81 $ (0.09) Weighted-averagesharesusedtocomputenetincome(loss)pershare: Basic 443,126 424,999 405,731 Diluted 482,167 466,076 405,731 Seeaccompanyingnotestoconsolidatedfinancialstatements. 85

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_07661

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Block；文档：BLOCK_2020_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：Using the cash flow statement, answer the following question to the best of your abilities: how much did Block (formerly known as Square) generate in cash flow from operating activities in FY2020? Answer in USD millions.
- 标准答案：$382.00
- 答案依据：The metric cash from operations was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Net cash provided by operating activities.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Block, BLOCK_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：SQUARE, INC. CONSOLIDATED STATEMENTS OF CASH FLOWS (In thousands) Year Ended December 31, 2020 2019 2018 Cash flows from operating activities: Netincome(loss) $ 213,105 $ 375,446 $ (38,453) Adjustmentstoreconcilenetlosstonetcashprovidedbyoperatingactivities: Depreciationandamortization 84,212 75,598 60,961 Non-cashinterestandother 76,129 33,478 28,512 Lossonextinguishmentoflong-termdebt 6,651 5,047 Non-cashleaseexpense 70,253 29,696 Share-basedcompensation 397,800 297,863 216,881 Replacementstockawardsissuedinconnectionwithacquisition 899 Gainonsaleofassetgroup (373,445) Loss(gain)onrevaluationofequityinvestment (295,297) 12,326 (20,342) Transactionandloanlosses 177,670 126,959 88,077 Changeindeferredincometaxes (8,016) (1,376) (646) Changesinoperatingassetsandliabilities: Settlementsreceivable (473,871) (248,271) 245,795 Customerfunds (1,151,536) (204,208) (131,004) Purchaseofloansheldforsale (1,837,137) (2,266,738) (1,609,611) Salesandprincipalpaymentsofloansheldforsale 1,505,406 2,168,682 1,579,834 Customerspayable 1,733,138 523,795 15,597 Settlementspayable 143,528 41,697 (60,651) Charge-offstoaccruedtransactionlosses (73,613) (78,325) (58,192) Otherassetsandliabilities (186,819) (47,478) (27,624) Netcashprovidedbyoperatingactivities 381,603 465,699 295,080 Cash flows from investing activities: Purchaseofmarketabledebtsecurities (1,322,362) (992,583) (1,000,346) Proceedsfrommaturitiesofmarketabledebtsecurities 607,134 430,888 197,454 Proceedsfromsaleofmarketabledebtsecurities 585,427 548,619 171,992 Purchaseofmarketabledebtsecuritiesfromcustomerfunds (642,252) (311,499) (148,096) Proceedsfrommaturitiesofmarketabledebtsecuritiesfromcustomerfunds 382,887 158,055 Proceedsfromsaleofmarketabledebtsecuritiesfromcustomerfunds 51,430 17,493 48,334 Purchaseofpropertyandequipment (138,402) (62,498) (61,203) Purchaseofotherinvestments (51,277) (15,250) Proceedsfromsaleofequityinvestment 33,016 Purchaseofintangibleassets (1,584) Proceedsfromsaleofassetgroup 309,324 Businesscombinations,netofcashacquired (79,221) (20,372) (112,399) Netcashprovidedby(usedin)investingactivities: (606,636) 95,193 (905,848) Cash flows from financing activities: Proceedsfromissuanceofconvertibleseniornotes,net 2,116,544 855,663 Purchaseofconvertibleseniornotehedges (338,145) (172,586) Proceedsfromissuanceofwarrants 232,095 112,125 Principalpaymentonconversionofseniornotes (219,384) ProceedsfromPPPLiquidityFacilityadvances 464,094 Proceedsfromtheexerciseofstockoptionsandpurchasesundertheemployeestockpurchaseplan,net 161,985 118,514 133,850 Paymentsfortaxwithholdingrelatedtovestingofrestrictedstockunits (314,019) (212,264) (189,124) Otherfinancingactivities (7,359) (5,124) (4,789) Netcashprovidedby(usedin)financingactivities 2,315,195 (98,874) 515,755 Effectofforeignexchangerateoncashandcashequivalents 12,995 3,841 (7,221) Netincrease(decrease)incash,cashequivalentsandrestrictedcash 2,103,157 465,859 (102,234) Cash,cashequivalentsandrestrictedcash,beginningoftheyear 1,098,706 632,847 735,081 Cash,cashequivalentsandrestrictedcash,endoftheyear $ 3,201,863 $ 1,098,706 $ 632,847 Seeaccompanyingnotestoconsolidatedfinancialstatements. 89

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_10285

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2018_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：We need to calculate a financial metric by using information only provided within the balance sheet. Please answer the following question: what is Boeing's year end FY2018 net property, plant, and equipment (in USD millions)?
- 标准答案：$12645.00
- 答案依据：The metric ppne, net was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Property, plant and equipment, net.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents The Boeing Company and Subsidiaries Consolidated Statements of Financial Position (Dollarsinmillions,exceptpersharedata) December 31, 2018 2017 Assets Cash and cash equivalents $7,637 $8,813 Short-term and other investments 927 1,179 Accounts receivable, net 3,879 2,894 Unbilled receivables, net 10,025 8,194 Current portion of customer financing, net 460 309 Inventories 62,567 61,388 Other current assets 2,335 2,417 Total current assets 87,830 85,194 Customer financing, net 2,418 2,756 Property, plant and equipment, net 12,645 12,672 Goodwill 7,840 5,559 Acquired intangible assets, net 3,429 2,573 Deferred income taxes 284 321 Investments 1,087 1,260 Other assets, net of accumulated amortization of $503 and $482 1,826 2,027 Total assets $117,359 $112,362 Liabilities and equity Accounts payable $12,916 $12,202 Accrued liabilities 14,808 13,069 Advances and progress billings 50,676 48,042 Short-term debt and current portion of long-term debt 3,190 1,335 Total current liabilities 81,590 74,648 Deferred income taxes 1,736 2,188 Accrued retiree health care 4,584 5,545 Accrued pension plan liability, net 15,323 16,471 Other long-term liabilities 3,059 2,015 Long-term debt 10,657 9,782 Shareholders equity: Common stock, par value $5.00 1,200,000,000 shares authorized; 1,012,261,159 shares issued 5,061 5,061 Additional paid-in capital 6,768 6,804 Treasury stock, at cost (52,348) (43,454) Retained earnings 55,941 49,618 Accumulated other comprehensive loss (15,083) (16,373) Total shareholders equity 339 1,656 Noncontrolling interests 71 57 Total equity 410 1,713 Total liabilities and equity $117,359 $112,362 See Notes to the Consolidated Financial Statements on pages 54 113 . 50

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00517

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning)。
- 问题：Are there any product categories / service categories that represent more than 20% of Boeing's revenue for FY2022?
- 标准答案：Yes. Boeing has product and service categories that represent more than 20% of Boeing's revenue for FY2022. These categories are Commercial Airplanes which comprises 39% of total revenue, Defence which comprises 35% of total revenue and Services which comprises 26% of total revenue.
- 答案依据：Commercial Airplanes%=Revenues: Commercial Airplanes/Total revenues*100=25,867/66,608*100=39%. Defence%=Defense, Space & Security/Total revenues*100=23,162/66,608*100=35%. Services%=Global Services/Total revenues*100=17,611/66,608*100=26%.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The Boeing Company and Subsidiaries Notes to the Consolidated Financial Statements Summary of Business Segment Data (Dollars in millions) Years ended December 31, 2022 2021 2020 Revenues: Commercial Airplanes $25,867 $19,493 $16,162 Defense, Space & Security 23,162 26,540 26,257 Global Services 17,611 16,328 15,543 Boeing Capital 199 272 261 Unallocated items, eliminations and other (231) (347) (65) Total revenues $66,608 $62,286 $58,158

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01091

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Has Boeing reported any materially important ongoing legal battles from FY2022?
- 标准答案：Yes. Multiple lawsuits have been filed against Boeing resulting from a 2018 Lion Air crash and a 2019 Ethiopian Airlines crash.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Multiple legal actions have been filed against us as a result of the October 29, 2018 accident of Lion Air Flight 610 and the March 10, 2019 accident of Ethiopian Airlines Flight 302.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00678

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR information extraction。
- 问题：Does Boeing have an improving gross margin profile as of FY2022? If gross margin is not a useful metric for a company like this, then state that and explain why.
- 标准答案：Yes. Boeing has an improving gross margin profile as of FY2022. Gross profit improved from $3,017 million in FY2021 to $3,502 million in FY2022. Gross margin % improved from 4.8% in FY2021 to 5.3% in FY2022.
- 答案依据：Gross margin%=Gross margin/Total revenues*100=3,502/66,608*100=5.3% for 2022 and 3,017/62,286*100=4.8% for 2021.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The Boeing Company and Subsidiaries Consolidated Statements of Operations (Dollars in millions, except per share data) Years ended December 31, 2022 2021 2020 Sales of products $55,893 $51,386 $47,142 Sales of services 10,715 10,900 11,016 Total revenues 66,608 62,286 58,158 Cost of products (53,969) (49,954) (54,568) Cost of services (9,109) (9,283) (9,232) Boeing Capital interest expense (28) (32) (43) Total costs and expenses (63,106) (59,269) (63,843) 3,502 3,017 (5,685)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01290

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction OR Logical reasoning。
- 问题：Who are the primary customers of Boeing as of FY2022?
- 标准答案：Boeing's primary customers as of FY2022 are a limited number of commercial airlines and the US government. The US government accounted for 40% of Boeing's total revenues in FY2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We derive a significant portion of our revenues from a limited number of commercial airlines.

证据 2：We derive a substantial portion of our revenue from the U.S. government

证据 3：In 2022, 40% of our revenues were earned pursuant to U.S. government contracts

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00464

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Is Boeing's business subject to cyclicality?
- 标准答案：Yes, Boeing's business is subject to cyclicality due to its exposure to the airline industry which is a cyclical industry.
- 答案依据：A major portion of Boeing's revenue is derived from the sale of aircraft to commercial airlines. The commercial airlines business is cyclical, and subject to significant profit swings.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Historically, the airline industry has been cyclical and very competitive and has experienced significant profit swings and constant challenges to be more cost competitive.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00494

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What production rate changes is Boeing forecasting for FY2023?
- 标准答案：Boeing forecasts an increase in the production rates for the 737, 777X and 787 aircrafts in 2023.
- 答案依据：Boeing plans to gradually increase production rates for the 737 and 787 and to resume production of 777X.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We must minimize disruption caused by production changes, achieve operational stability and implement productivity improvements in order to meet customer demand and maintain our profitability. We have previously announced plans to adjust production rates on several of our commercial aircraft programs. The 787 program is currently producing at low rates and we expect to gradually increase to 5 per month in 2023. Production of the 777X is currently paused and is expected to resume in 2023. The 737 program has experienced operational and supply chain challenges stabilizing production at 31 per month. We plan to gradually increase 737 production rates based on market demand and supply chain capacity.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00585

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Boeing；文档：BOEING_2022_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：How does Boeing's effective tax rate in FY2022 compare to FY2021?
- 标准答案：Effective tax rate in FY2022 was 0.62%, compared to  -14.76% in FY2021.
- 答案依据：Effective tax rate=Income tax (expense) benefit/ Loss before income taxes*100=(31)/(5,022)*100=0.62% in 2022 and 743/(5,033)*100=-14.76%.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Boeing, BOEING_2022_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The Boeing Company and Subsidiaries Consolidated Statements of Operations (Dollars in millions, except per share data) Years ended December 31, 2022 2021 2020 Sales of products $55,893 $51,386 $47,142 Sales of services 10,715 10,900 11,016 Total revenues 66,608 62,286 58,158 Cost of products (53,969) (49,954) (54,568) Cost of services (9,109) (9,283) (9,232) Boeing Capital interest expense (28) (32) (43) Total costs and expenses (63,106) (59,269) (63,843) 3,502 3,017 (5,685) (Loss)/income from operating investments, net (16) 210 9 General and administrative expense (4,187) (4,157) (4,817) Research and development expense, net (2,852) (2,249) (2,476) Gain on dispositions, net 6 277 202 Loss from operations (3,547) (2,902) (12,767) Other income, net 1,058 551 447 Interest and debt expense (2,533) (2,682) (2,156) Loss before income taxes (5,022) (5,033) (14,476) Income tax (expense)/benefit (31) 743 2,535

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03473

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Coca-Cola；文档：COCACOLA_2017_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2017 return on assets (ROA) for Coca Cola? ROA is defined as: FY2017 net income / (average total assets between FY2016 and FY2017). Round your answer to two decimal places. Give a response to the question by relying on the details shown in the balance sheet and the P&L statement.
- 标准答案：0.01
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Net income. This metric was located in the 10K as a single line item named: NET INCOME ATTRIBUTABLE TO SHAREOWNERS OF THE COCA-COLA COMPANY.

Metric 2: Total assets. This metric was located in the 10K as a single line item named: TOTAL ASSETS.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Coca-Cola, COCACOLA_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：THE COCA-COLA COMPANY AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF INCOME Year Ended December 31, 2017 2016 2015 (In millions except per share data) NET OPERATING REVENUES $ 35,410 $ 41,863 $ 44,294 Cost of goods sold 13,256 16,465 17,482 GROSS PROFIT 22,154 25,398 26,812 Selling, general and administrative expenses 12,496 15,262 16,427 Other operating charges 2,157 1,510 1,657 OPERATING INCOME 7,501 8,626 8,728 Interest income 677 642 613 Interest expense 841 733 856 Equity income (loss) net 1,071 835 489 Other income (loss) net (1,666) (1,234) 631 INCOME FROM CONTINUING OPERATIONS BEFORE INCOME TAXES 6,742 8,136 9,605 Income taxes from continuing operations 5,560 1,586 2,239 NET INCOME FROM CONTINUING OPERATIONS 1,182 6,550 7,366 Income from discontinued operations (net of income taxes of $47, $0 and $0, respectively) 101 CONSOLIDATED NET INCOME 1,283 6,550 7,366 Less: Net income attributable to noncontrolling interests 35 23 15 NET INCOME ATTRIBUTABLE TO SHAREOWNERS OF THE COCA-COLA COMPANY $ 1,248 $ 6,527 $ 7,351 Basic net income per share from continuing operations1 $ 0.28 $ 1.51 $ 1.69 Basic net income per share from discontinued operations2 0.02 BASIC NET INCOME PER SHARE $ 0.29 3 $ 1.51 $ 1.69 Diluted net income per share from continuing operations1 $ 0.27 $ 1.49 $ 1.67 Diluted net income per share from discontinued operations2 0.02 DILUTED NET INCOME PER SHARE $ 0.29 $ 1.49 $ 1.67 AVERAGE SHARES OUTSTANDING BASIC 4,272 4,317 4,352 Effect of dilutive securities 52 50 53 AVERAGE SHARES OUTSTANDING DILUTED 4,324 4,367 4,405 1 Calculated based on net income from continuing operations less net income from continuing operations attributable to noncontrolling interests. 2 Calculated based on net income from discontinued operations less net income from discontinued operations attributable to noncontrolling interests. 3 Per share amounts do not add due to rounding. Refer to Notes to Consolidated Financial Statements. 72

证据 2：THE COCA-COLA COMPANY AND SUBSIDIARIES CONSOLIDATED BALANCE SHEETS December 31, 2017 2016 (In millions except par value) ASSETS CURRENT ASSETS Cash and cash equivalents $ 6,006 $ 8,555 Short-term investments 9,352 9,595 TOTAL CASH, CASH EQUIVALENTS AND SHORT-TERM INVESTMENTS 15,358 18,150 Marketable securities 5,317 4,051 Trade accounts receivable, less allowances of $477 and $466, respectively 3,667 3,856 Inventories 2,655 2,675 Prepaid expenses and other assets 2,000 2,481 Assets held for sale 219 2,797 Assets held for sale discontinued operations 7,329 TOTAL CURRENT ASSETS 36,545 34,010 EQUITY METHOD INVESTMENTS 20,856 16,260 OTHER INVESTMENTS 1,096 989 OTHER ASSETS 4,560 4,248 PROPERTY, PLANT AND EQUIPMENT net 8,203 10,635 TRADEMARKS WITH INDEFINITE LIVES 6,729 6,097 BOTTLERS' FRANCHISE RIGHTS WITH INDEFINITE LIVES 138 3,676 GOODWILL 9,401 10,629 OTHER INTANGIBLE ASSETS 368 726 TOTAL ASSETS $ 87,896 $ 87,270 LIABILITIES AND EQUITY CURRENT LIABILITIES Accounts payable and accrued expenses $ 8,748 $ 9,490 Loans and notes payable 13,205 12,498 Current maturities of long-term debt 3,298 3,527 Accrued income taxes 410 307 Liabilities held for sale 37 710 Liabilities held for sale discontinued operations 1,496 TOTAL CURRENT LIABILITIES 27,194 26,532 LONG-TERM DEBT 31,182 29,684 OTHER LIABILITIES 8,021 4,081 DEFERRED INCOME TAXES 2,522 3,753 THE COCA-COLA COMPANY SHAREOWNERS' EQUITY Common stock, $0.25 par value; Authorized 11,200 shares; Issued 7,040 and 7,040 shares, respectively 1,760 1,760 Capital surplus 15,864 14,993 Reinvested earnings 60,430 65,502 Accumulated other comprehensive income (loss) (10,305) (11,205) Treasury stock, at cost 2,781 and 2,752 shares, respectively (50,677) (47,988) EQUITY ATTRIBUTABLE TO SHAREOWNERS OF THE COCA-COLA COMPANY 17,072 23,062 EQUITY ATTRIBUTABLE TO NONCONTROLLING INTERESTS 1,905 158 TOTAL EQUITY 18,977 23,220 TOTAL LIABILITIES AND EQUITY $ 87,896 $ 87,270 Refer to Notes to Consolidated Financial Statements. 74

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_09724

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Coca-Cola；文档：COCACOLA_2021_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Coca Cola's FY2021 COGS % margin? Calculate what was asked by utilizing the line items clearly shown in the income statement.
- 标准答案：39.7%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of goods sold.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: Net Operating Revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Coca-Cola, COCACOLA_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：THE COCA-COLA COMPANY AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF INCOME (In millions except per share data) Year Ended December 31, 2021 2020 2019 Net Operating Revenues $ 38,655 $ 33,014 $ 37,266 Cost of goods sold 15,357 13,433 14,619 Gross Profit 23,298 19,581 22,647 Selling, general and administrative expenses 12,144 9,731 12,103 Other operating charges 846 853 458 Operating Income 10,308 8,997 10,086 Interest income 276 370 563 Interest expense 1,597 1,437 946 Equity income (loss) net 1,438 978 1,049 Other income (loss) net 2,000 841 34 Income Before Income Taxes 12,425 9,749 10,786 Income taxes 2,621 1,981 1,801 Consolidated Net Income 9,804 7,768 8,985 Less: Net income (loss) attributable to noncontrolling interests 33 21 65 Net Income Attributable to Shareowners of The Coca-Cola Company $ 9,771 $ 7,747 $ 8,920 Basic Net Income Per Share $ 2.26 $ 1.80 $ 2.09 Diluted Net Income Per Share $ 2.25 $ 1.79 $ 2.07 Average Shares Outstanding Basic 4,315 4,295 4,276 Effect of dilutive securities 25 28 38 Average Shares Outstanding Diluted 4,340 4,323 4,314 Calculated based on net income attributable to shareowners of The Coca-Cola Company. Refer to Notes to Consolidated Financial Statements. 1 1 1 60

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_06272

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Coca-Cola；文档：COCACOLA_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Coca Cola's FY2022 dividend payout ratio (using total cash dividends paid and net income attributable to shareholders)? Round answer to two decimal places. Answer the question asked by assuming you only have access to information clearly displayed in the cash flow statement and the income statement.
- 标准答案：0.8
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total cash dividends paid out. This metric was located in the 10K as a single line item named: Dividends.

Metric 2: Net income. This metric was located in the 10K as a single line item named: Net Income Attributable to Shareowners of The Coca-Cola Company.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Coca-Cola, COCACOLA_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：THE COCA-COLA COMPANY AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF INCOME (In millions except per share data) Year Ended December 31, 2022 2021 2020 Net Operating Revenues $ 43,004 $ 38,655 $ 33,014 Cost of goods sold 18,000 15,357 13,433 Gross Profit 25,004 23,298 19,581 Selling, general and administrative expenses 12,880 12,144 9,731 Other operating charges 1,215 846 853 Operating Income 10,909 10,308 8,997 Interest income 449 276 370 Interest expense 882 1,597 1,437 Equity income (loss) net 1,472 1,438 978 Other income (loss) net (262) 2,000 841 Income Before Income Taxes 11,686 12,425 9,749 Income taxes 2,115 2,621 1,981 Consolidated Net Income 9,571 9,804 7,768 Less: Net income (loss) attributable to noncontrolling interests 29 33 21 Net Income Attributable to Shareowners of The Coca-Cola Company $ 9,542 $ 9,771 $ 7,747 Basic Net Income Per Share $ 2.20 $ 2.26 $ 1.80 Diluted Net Income Per Share $ 2.19 $ 2.25 $ 1.79 Average Shares Outstanding Basic 4,328 4,315 4,295 Effect of dilutive securities 22 25 28 Average Shares Outstanding Diluted 4,350 4,340 4,323 Calculated based on net income attributable to shareowners of The Coca-Cola Company. Refer to Notes to Consolidated Financial Statements. 1 1 1 61

证据 2：THE COCA-COLA COMPANY AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF CASH FLOWS (In millions) Year Ended December 31, 2022 2021 2020 Operating Activities Consolidated net income $ 9,571 $ 9,804 $ 7,768 Depreciation and amortization 1,260 1,452 1,536 Stock-based compensation expense 356 337 126 Deferred income taxes (122) 894 (18) Equity (income) loss net of dividends (838) (615) (511) Foreign currency adjustments 203 86 (88) Significant (gains) losses net (129) (1,365) (914) Other operating charges 1,086 506 556 Other items 236 201 699 Net change in operating assets and liabilities (605) 1,325 690 Net Cash Provided by Operating Activities 11,018 12,625 9,844 Investing Activities Purchases of investments (3,751) (6,030) (13,583) Proceeds from disposals of investments 4,771 7,059 13,835 Acquisitions of businesses, equity method investments and nonmarketable securities (73) (4,766) (1,052) Proceeds from disposals of businesses, equity method investments and nonmarketable securities 458 2,180 189 Purchases of property, plant and equipment (1,484) (1,367) (1,177) Proceeds from disposals of property, plant and equipment 75 108 189 Collateral (paid) received associated with hedging activities net (1,465) Other investing activities 706 51 122 Net Cash Provided by (Used in) Investing Activities (763) (2,765) (1,477) Financing Activities Issuances of debt 3,972 13,094 26,934 Payments of debt (4,930) (12,866) (28,796) Issuances of stock 837 702 647 Purchases of stock for treasury (1,418) (111) (118) Dividends (7,616) (7,252) (7,047) Other financing activities (1,095) (353) 310 Net Cash Provided by (Used in) Financing Activities (10,250) (6,786) (8,070) Effect of Exchange Rate Changes on Cash, Cash Equivalents, Restricted Cash and Restricted Cash Equivalents (205) (159) 76 Cash, Cash Equivalents, Restricted Cash and Restricted Cash Equivalents Net increase (decrease) in cash, cash equivalents, restricted cash and restricted cash equivalents during the year (200) 2,915 373 Cash, cash equivalents, restricted cash and restricted cash equivalents at beginning of year 10,025 7,110 6,737 Cash, Cash Equivalents, Restricted Cash and Restricted Cash Equivalents at End of Year 9,825 10,025 7,110 Less: Restricted cash and restricted cash equivalents at end of year 306 341 315 Cash and Cash Equivalents at End of Year $ 9,519 $ 9,684 $ 6,795 Refer to Notes to Consolidated Financial Statements. 64

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_10130

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Corning；文档：CORNING_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Based on the information provided primarily in the balance sheet and the statement of income, what is FY2020 days payable outstanding (DPO) for Corning? DPO is defined as: 365 * (average accounts payable between FY2019 and FY2020) / (FY2020 COGS + change in inventory between FY2019 and FY2020). Round your answer to two decimal places.
- 标准答案：63.86
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Accounts payable. This metric was located in the 10K as a single line item named: AccountsÂ payable.

Metric 2: Inventories. This metric was located in the 10K as a single line item named: Inventories, net (Note 6).

Metric 3: Cost of goods sold. This metric was located in the 10K as a single line item named: CostÂ ofÂ sales.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Corning, CORNING_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Index Consolidated Statements of Income Corning Incorporated and Subsidiary Companies YearendedDecember31, (Inmillions,exceptpershareamounts) 2020 2019 2018 Netsales $ 11,303 $ 11,503 $ 11,290 Costofsales 7,772 7,468 6,829 Grossmargin 3,531 4,035 4,461 Operatingexpenses: Selling,generalandadministrativeexpenses 1,747 1,585 1,799 Research,developmentandengineeringexpenses 1,154 1,031 993 Amortizationofpurchasedintangibles 121 113 94 Operatingincome 509 1,306 1,575 Equityin(losses)earningsofaffiliatedcompanies(Note3) (25) 17 390 Interestincome 15 21 38 Interestexpense (276) (221) (191) Translatedearningscontract(loss)gain,net(Note15) (38) 248 (93) Transaction-relatedgain,net(Note4) 498 Otherexpense,net (60) (155) (216) Incomebeforeincometaxes 623 1,216 1,503 Provisionforincometaxes(Note8) (111) (256) (437) NetincomeattributabletoCorningIncorporated $ 512 $ 960 $ 1,066 Earningspercommonshareattributableto CorningIncorporated: Basic(Note18) $ 0.54 $ 1.11 $ 1.19 Diluted(Note18) $ 0.54 $ 1.07 $ 1.13 Theaccompanyingnotesareanintegralpartoftheseconsolidatedfinancialstatements. 70

证据 2：Index Consolidated Balance Sheets Corning Incorporated and Subsidiary Companies December31, (Inmillions,exceptshareandpershareamounts) 2020 2019 Assets Currentassets: Cashandcashequivalents $ 2,672 $ 2,434 Tradeaccountsreceivable,netofdoubtfulaccounts-$46and$41 2,133 1,836 Inventories,net(Note6) 2,438 2,320 Othercurrentassets(Note11and15) 761 873 Totalcurrentassets 8,004 7,463 Property,plantandequipment,netofaccumulateddepreciation- $13,663and$12,995(Note9) 15,742 15,337 Goodwill,net(Note10) 2,460 1,935 Otherintangibleassets,net(Note10) 1,308 1,185 Deferredincometaxes(Note8) 1,121 1,157 Otherassets(Note11and15) 2,140 1,821 Total Assets $ 30,775 $ 28,898 Liabilities and Equity Currentliabilities: Currentportionoflong-termdebtandshort-termborrowings(Note12) $ 156 $ 11 Accountspayable 1,174 1,587 Otheraccruedliabilities(Note11and14) 2,437 1,923 Totalcurrentliabilities 3,767 3,521 Long-termdebt(Note12) 7,816 7,729 Postretirementbenefitsotherthanpensions(Note13) 727 671 Otherliabilities(Note11and14) 5,017 3,980 Totalliabilities 17,327 15,901 Commitments,contingenciesandguarantees(Note14) Shareholdersequity(Note17): Convertiblepreferredstock,SeriesAParvalue$100pershare; Sharesauthorized3,100;Sharesissued:2,300 2,300 2,300 CommonstockParvalue$0.50pershare;Sharesauthorized:3.8billion; Sharesissued:1,726millionand1,718million 863 859 Additionalpaid-incapitalcommonstock 14,642 14,323 Retainedearnings 16,120 16,408 Treasurystock,atcost;sharesheld:961millionand956million (19,928) (19,812) Accumulatedothercomprehensiveloss (740) (1,171) TotalCorningIncorporatedshareholdersequity 13,257 12,907 Noncontrollinginterests 191 90 Totalequity 13,448 12,997 Total Liabilities and Equity $ 30,775 $ 28,898 Theaccompanyingnotesareanintegralpartoftheseconsolidatedfinancialstatements. 72

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02981

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Corning；文档：CORNING_2021_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Taking into account the information outlined in the income statement, what is the FY2019 - FY2021 3 year average unadjusted operating income % margin for Corning? Answer in units of percents and round to one decimal place.
- 标准答案：10.3%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Unadjusted operating income. This metric was located in the 10K as a single line item named: OperatingÂ income.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: NetÂ sales.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Corning, CORNING_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：TableofContents Consolidated Statements of Income Corning Incorporated and Subsidiary Companies YearendedDecember31, (Inmillions,exceptpershareamounts) 2021 2020 2019 Netsales $ 14,082 $ 11,303 $ 11,503 Costofsales 9,019 7,772 7,468 Grossmargin 5,063 3,531 4,035 Operatingexpenses: Selling,generalandadministrativeexpenses 1,827 1,747 1,585 Research,developmentandengineeringexpenses 995 1,154 1,031 Amortizationofpurchasedintangibles 129 121 113 Operatingincome 2,112 509 1,306 Equityinearnings(losses)ofaffiliatedcompanies(Note3) 35 (25) 17 Interestincome 11 15 21 Interestexpense (300) (276) (221) Translatedearningscontractgain(loss),net(Note15) 354 (38) 248 Transaction-relatedgain,net(Note4) 498 Otherincome(expense),net 185 (60) (155) Incomebeforeincometaxes 2,397 623 1,216 Provisionforincometaxes(Note8) (491) (111) (256) NetincomeattributabletoCorningIncorporated $ 1,906 $ 512 $ 960 EarningspercommonshareattributabletoCorningIncorporated: Basic(Note18) $ 1.30 $ 0.54 $ 1.11 Diluted(Note18) $ 1.28 $ 0.54 $ 1.07 ReconciliationofnetincomeattributabletoCorningIncorporatedversusnetincomeavailabletocommon shareholders: NetincomeattributabletoCorningIncorporated $ 1,906 $ 512 $ 960 SeriesAconvertiblepreferredstockdividend (24) (98) (98) Excessconsiderationpaidforredemptionofpreferredstock(1) (803) Netincomeavailabletocommonshareholders $ 1,079 $ 414 $ 862 (1) RefertoNote17(Shareholders'Equity)andNote18(EarningsperCommonShare)totheconsolidatedfinancialstatementsforadditionalinformation. Theaccompanyingnotesareanintegralpartoftheseconsolidatedfinancialstatements. 65

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01346

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Corning；文档：CORNING_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：How much has the effective tax rate of Corning changed between FY2021 and FY2022?
- 标准答案：The effective tax rate of Corning has changed from 20% in FY2021 to 23% in FY 2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Corning, CORNING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：RESULTS OF OPERATIONS The following table presents selected highlights from our operations (in millions): Year ended December 31, % change 2022 2021 22 vs. 21 Net sales $ 14,189 $ 14,082 1% Gross margin $ 4,506 $ 5,063 (11%) (gross margin %) 32% 36% Selling, general and administrative expenses $ 1,898 $ 1,827 4% (as a % of net sales) 13% 13% Research, development and engineering expenses $ 1,047 $ 995 5% (as a % of net sales) 7% 7% Translated earnings contract gain, net $ 351 $ 354 (1%) (as a % of net sales) 2% 3% Income before income taxes $ 1,797 $ 2,426 (26%) (as a % of net sales) 13% 17% Provision for income taxes $ (411) $ (491) 16% Effective tax rate 23% 20% Net income attributable to Corning Incorporated $ 1,316 $ 1,906 (31%) (as a % of net sales) 9% 14% Comprehensive income attributable to Corning Incorporated $ 661 $ 1,471 (55%)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00005

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Corning；文档：CORNING_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- 标准答案：Yes. Corning had a positive working capital amount of $831 million by FY 2022 close. This answer considers only operating current assets and current liabilities that were clearly shown in the balance sheet.
- 答案依据：Trade accounts receivable, net of doubtful accounts+Inventories+Other current assets-Accounts payable-Other accrued liabilities
1721+2904+1157-1804-3147

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Corning, CORNING_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Balance Sheets Corning Incorporated and Subsidiary Companies December 31, (in millions, except share and per share amounts) 2022 2021 Assets Current assets: Cash and cash equivalents $ 1,671 $ 2,148 Trade accounts receivable, net of doubtful accounts - $40 and $42 1,721 2,004 Inventories (Note 5) 2,904 2,481 Other current assets (Notes 10 and 14) 1,157 1,026 Total current assets 7,453 7,659 Property, plant and equipment, net of accumulated depreciation - $14,147 and $13,969 (Note 8) 15,371 15,804 Goodwill, net (Note 9) 2,394 2,421 Other intangible assets, net (Note 9) 1,029 1,148 Deferred income taxes (Note 7) 1,073 1,066 Other assets (Notes 10 and 14) 2,179 2,056 Total Assets $ 29,499 $ 30,154 Liabilities and Equity Current liabilities: Current portion of long-term debt and short-term borrowings (Note 11) $ 224 $ 55 Accounts payable 1,804 1,612 Other accrued liabilities (Notes 10 and 13) 3,147 3,139 Total current liabilities 5,175 4,806 Long-term debt (Note 11) 6,687 6,989 Postretirement benefits other than pensions (Note 12) 407 622 Other liabilities (Notes 10 and 13) 4,955 5,192 Total liabilities 17,224 17,609

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04209

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Costco；文档：COSTCO_2021_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：Using only the information within the balance sheet, how much total assets did Costco have at the end of FY2021? Answer in USD millions.
- 标准答案：$59268.00
- 答案依据：The metric total assets was directly extracted from the company 10K. The line item name, as seen in the 10K, was: TOTAL ASSETS.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Costco, COSTCO_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents COSTCO WHOLESALE CORPORATION CONSOLIDATED BALANCE SHEETS (amounts in millions, except par value and share data) August 29, 2021 August 30, 2020 ASSETS CURRENT ASSETS Cash and cash equivalents $ 11,258 $ 12,277 Short-term investments 917 1,028 Receivables, net 1,803 1,550 Merchandise inventories 14,215 12,242 Other current assets 1,312 1,023 Total current assets 29,505 28,120 OTHER ASSETS Property and equipment, net 23,492 21,807 Operating lease right-of-use assets 2,890 2,788 Other long-term assets 3,381 2,841 TOTAL ASSETS $ 59,268 $ 55,556 LIABILITIES AND EQUITY CURRENT LIABILITIES Accounts payable $ 16,278 $ 14,172 Accrued salaries and benefits 4,090 3,605 Accrued member rewards 1,671 1,393 Deferred membership fees 2,042 1,851 Current portion of long-term debt 799 95 Other current liabilities 4,561 3,728 Total current liabilities 29,441 24,844 OTHER LIABILITIES Long-term debt, excluding current portion 6,692 7,514 Long-term operating lease liabilities 2,642 2,558 Other long-term liabilities 2,415 1,935 TOTAL LIABILITIES 41,190 36,851 COMMITMENTS AND CONTINGENCIES EQUITY Preferred stock $0.01 par value; 100,000,000 shares authorized; no shares issued and outstanding Common stock $0.01 par value; 900,000,000 shares authorized; 441,825,000 and 441,255,000 shares issued and outstanding 4 4 Additional paid-in capital 7,031 6,698 Accumulated other comprehensive loss (1,137) (1,297) Retained earnings 11,666 12,879 Total Costco stockholders equity 17,564 18,284 Noncontrolling interests 514 421 TOTAL EQUITY 18,078 18,705 TOTAL LIABILITIES AND EQUITY $ 59,268 $ 55,556 The accompanying notes are an integral part of these consolidated financial statements. 38

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
