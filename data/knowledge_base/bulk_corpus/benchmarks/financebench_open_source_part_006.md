# FinanceBench 样本：financebench_id_01482

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2023_8K_dated-2023-05-05。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：At the Pepsico AGM held on May 3, 2023, what was the outcome of the shareholder vote on the shareholder proposal for a congruency report by Pepsico on net-zero emissions policies?
- 标准答案：The shareholder proposal for a congruency report by Pepsico on net-zero emissions policies was defeated.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2023_8K_dated-2023-05-05, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：(8) The shareholder proposal regarding a congruency report on net-zero emissions policies was defeated: For 19,718,780 Against 977,228,788

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00705

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2023_8K_dated-2023-05-30。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：By how much did Pepsico increase its unsecured five year revolving credit agreement on May 26, 2023?
- 标准答案：$400,000,000 increase.
- 答案依据：Increase in five year unsecured revolving credit agreement = May 26, 2023, five year unsecured revolving credit agreement amount of $4,200,000,000 - May 27, 2022, five year unsecured revolving credit agreement amount of $3,800,000,000 = $400,000,000

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2023_8K_dated-2023-05-30, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Effective May 26, 2023, PepsiCo terminated the $3,800,000,000 five year unsecured revolving credit agreement, dated as of May 27, 2022, among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent (the 2022 Five Year Credit Agreement). There were no outstanding borrowings under the 2022 Five Year Credit Agreement at the time of its termination. On May 26, 2023, PepsiCo entered into a new $4,200,000,000 five year unsecured revolving credit agreement (the 2023 Five Year Credit Agreement) among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent. The 2023 Five Year Credit Agreement enables PepsiCo and its borrowing subsidiaries to borrow up to $4,200,000,000 in U.S. Dollars and/or Euros, including a $750,000,000 swing line subfacility for Euro-denominated borrowings permitted to be borrowed on a same day basis, subject to customary terms and conditions, and expires on May 26, 2028. PepsiCo may also, upon the agreement of either the then existing lenders or of additional banks not currently party to the 2023 Five Year Credit Agreement, increase the commitments under the 2023 Five Year Credit Agreement to up to $4,950,000,000 in U.S. Dollars and/or Euros. PepsiCo may, once a year, request renewal of the 2023 Five Year Credit Agreement for an additional one year period. Subject to certain conditions stated in the 2023 Five Year Credit Agreement, PepsiCo and its borrowing subsidiaries may borrow, prepay and reborrow amounts under the 2023 Five Year Credit Agreement at any time during the term of the 2023 Five Year Credit Agreement. Funds borrowed under the 2023 Five Year Credit Agreement may be used for general corporate purposes of PepsiCo and its subsidiaries. The 2023 Five Year Credit Agreement contains customary representations and warranties and events of default. In the ordinary course of their respective businesses, the lenders under the 2023 Five Year Credit Agreement and their affiliates have engaged, and may in the future engage, in commercial banking and/or investment banking transactions with PepsiCo and its affiliates.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00882

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2023_8K_dated-2023-05-30。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：As of May 26, 2023, what is the total amount Pepsico may borrow under its unsecured revolving credit agreements?
- 标准答案：Total amount Pepsico may borrow under unsecured revolving credit agreements = $8,400,000,000.
- 答案依据：Total amount that may be borrowed under unsecured revolving credit agreements = 2023, 364 day unsecured revolving credit agreement amount of $4,200,000,000 + 2023, five year unsecured revolving credit agreement amount of $4,200,000,000 = $8,400,000,000.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2023_8K_dated-2023-05-30, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Item 8.01. Other Events. Effective May 26, 2023, PepsiCo, Inc. (PepsiCo) terminated the $3,800,000,000 364 day unsecured revolving credit agreement, dated as of May 27, 2022, among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent (the 2022 364 Day Credit Agreement). There were no outstanding borrowings under the 2022 364 Day Credit Agreement at the time of its termination. On May 26, 2023, PepsiCo entered into a new $4,200,000,000 364 day unsecured revolving credit agreement (the 2023 364 Day Credit Agreement) among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent. The 2023 364 Day Credit Agreement enables PepsiCo and its borrowing subsidiaries to borrow up to $4,200,000,000 in U.S. Dollars and/or Euros, subject to customary terms and conditions, and expires on May 24, 2024. PepsiCo may also, upon the agreement of either the then existing lenders or of additional banks not currently party to the 2023 364 Day Credit Agreement, increase the commitments under the 2023 364 Day Credit Agreement to up to $4,950,000,000 in U.S. Dollars and/or Euros. PepsiCo may request renewal of the 2023 364 Day Credit Agreement for an additional 364 day period or convert any amounts outstanding into a term loan for a period of up to one year, which term loan would mature no later than the anniversary of the then effective termination date. Subject to certain conditions stated in the 2023 364 Day Credit Agreement, PepsiCo and its borrowing subsidiaries may borrow, prepay and reborrow amounts under the 2023 364 Day Credit Agreement at any time during the term of the 2023 364 Day Credit Agreement. Funds borrowed under the 2023 364 Day Credit Agreement may be used for general corporate purposes of PepsiCo and its subsidiaries. The 2023 364 Day Credit Agreement contains customary representations and warranties and events of default. In the ordinary course of their respective businesses, the lenders under the 2023 364 Day Credit Agreement and their affiliates have engaged, and may in the future engage, in commercial banking and/or investment banking transactions with PepsiCo and its affiliates. Effective May 26, 2023, PepsiCo terminated the $3,800,000,000 five year unsecured revolving credit agreement, dated as of May 27, 2022, among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent (the 2022 Five Year Credit Agreement). There were no outstanding borrowings under the 2022 Five Year Credit Agreement at the time of its termination. On May 26, 2023, PepsiCo entered into a new $4,200,000,000 five year unsecured revolving credit agreement (the 2023 Five Year Credit Agreement) among PepsiCo, as borrower, the lenders party thereto, and Citibank, N.A., as administrative agent. The 2023 Five Year Credit Agreement enables PepsiCo and its borrowing subsidiaries to borrow up to $4,200,000,000 in U.S. Dollars and/or Euros, including a $750,000,000 swing line subfacility for Euro-denominated borrowings permitted to be borrowed on a same day basis, subject to customary terms and conditions, and expires on May 26, 2028. PepsiCo may also, upon the agreement of either the then existing lenders or of additional banks not currently party to the 2023 Five Year Credit Agreement, increase the commitments under the 2023 Five Year Credit Agreement to up to $4,950,000,000 in U.S. Dollars and/or Euros. PepsiCo may, once a year, request renewal of the 2023 Five Year Credit Agreement for an additional one year period. Subject to certain conditions stated in the 2023 Five Year Credit Agreement, PepsiCo and its borrowing subsidiaries may borrow, prepay and reborrow amounts under the 2023 Five Year Credit Agreement at any time during the term of the 2023 Five Year Credit Agreement. Funds borrowed under the 2023 Five Year Credit Agreement may be used for general corporate purposes of PepsiCo and its subsidiaries. The 2023 Five Year Credit Agreement contains customary representations and warranties and events of default. In the ordinary course of their respective businesses, the lenders under the 2023 Five Year Credit Agreement and their affiliates have engaged, and may in the future engage, in commercial banking and/or investment banking transactions with PepsiCo and its affiliates.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01474

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2023Q1_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：As of FY2023Q1, why did Pepsico raise full year guidance for FY2023?
- 标准答案：Pepsico experienced a strong start to FY2023.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2023Q1_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We are very pleased with our performance and business momentum as our categories and geographies remained resilient during the first quarter. Given our strong start to the year, we now expect our full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and core constant currency EPS to increase 9 percent (previously 8 percent), said Chairman and CEO Ramon Laguarta.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01476

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2023Q1_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：As of FY2023Q1, by how many percentage points did Pepsico raise full year guidance in respect of core constant currency EPS growth?
- 标准答案：Pepsico raised full year guidance in respect of core constant currency EPS growth by 1 percentage point.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2023Q1_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We are very pleased with our performance and business momentum as our categories and geographies remained resilient during the first quarter. Given our strong start to the year, we now expect our full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and core constant currency EPS to increase 9 percent (previously 8 percent), said Chairman and CEO Ramon Laguarta.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00302

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：PFIZER_2021_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Did Pfizer grow its PPNE between FY20 and FY21?
- 标准答案：Yes, change in PPNE was positive year over year
- 答案依据：14882 - 13745 > 0

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, PFIZER_2021_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：As of December 31, (MILLIONS, EXCEPT PER COMMON SHARE DATA) 2021 2020 Assets Cash and cash equivalents $ 1,944 $ 1,786 Short-term investments 29,125 10,437 Trade accounts receivable, less allowance for doubtful accounts: 2021$492; 2020$508 11,479 7,913 Inventories 9,059 8,020 Current tax assets 4,266 3,264 Other current assets 3,820 3,646 Total current assets 59,693 35,067 Equity-method investments 16,472 16,856 Long-term investments 5,054 3,406 Property, plant and equipment 14,882 13,745

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00702

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：PFIZER_2021_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Were there any potential events that are not in Pfizer's standard business operations that substantially increased net income in 2019?
- 标准答案：Yes, the gain on completion of Consumer Healthcare JV Transaction
- 答案依据：Income statement shows the gain on completion of Consumer Healthcare JV transaction occured in FY19. In FY21, this event did not affect the net income at all due to the seemingly one time nature of the line item

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, PFIZER_2021_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Year Ended December 31, (MILLIONS, EXCEPT PER COMMON SHARE DATA) 2021 2020 2019 Revenues $ 81,288 $ 41,651 $ 40,905 Costs and expenses: Cost of sales 30,821 8,484 8,054 Selling, informational and administrative expenses 12,703 11,597 12,726 Research and development expenses 13,829 9,393 8,385 Amortization of intangible assets 3,700 3,348 4,429 Restructuring charges and certain acquisition-related costs 802 579 601 (Gain) on completion of Consumer Healthcare JV transaction (6) (8,107) Other (income)/deductionsnet (4,878) 1,219 3,497 Income from continuing operations before provision/(benefit) for taxes on income 24,311 7,036 11,321 Provision/(benefit) for taxes on income 1,852 370 583 Income from continuing operations 22,459 6,666 10,738 Discontinued operationsnet of tax (434) 2,529 5,318 Net income before allocation to noncontrolling interests 22,025 9,195 16,056 Less: Net income attributable to noncontrolling interests 45 36 29 Net income attributable to Pfizer Inc. common shareholders $ 21,979 $ 9,159 $ 16,026

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02416

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：PFIZER_2021_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What are three main companies acquired by Pfizer mentioned in this 10K report?
- 标准答案：Trillium, Array, and Therachon
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, PFIZER_2021_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Note 2. Acquisitions, Divestitures, Equity-Method Investments, Licensing Arrangements and Collaborative Arrangements A. Acquisitions Trillium On November 17, 2021, we acquired all of the issued and outstanding common stock not already owned by Pfizer of Trillium, a clinical stage immuno-oncology company developing therapies targeting cancer immune evasion pathways and specific cell targeting approaches, for a price of $18.50 per share in cash, for total consideration of $2.0 billion, net of cash acquired. As a result, Trillium became our wholly owned subsidiary. We previously held a 2% ownership investment in Trillium. Trilliums lead program, TTI-622, is an investigational fusion protein that is designed to block the inhibitory activity of CD47, a molecule that is overexpressed by a wide variety of tumors. We accounted for the transaction as an asset acquisition since the lead asset, TTI-622, represented substantially all of the fair value of the gross assets acquired, which exclude cash acquired. At the acquisition date, we recorded a $2.1 billion charge representing an acquired IPR&D asset with no alternative future use in Research and development expenses, of which the $2.0 billion net cash consideration is presented as a cash outflow from operating activities. In connection with this acquisition, we recorded $256 million of assets acquired primarily consisting of cash and investments. Liabilities assumed were approximately $81 million. Array On July 30, 2019, we acquired Array, a commercial stage biopharmaceutical company focused on the discovery, development and commercialization of targeted small molecule medicines to treat cancer and other diseases of high unmet need, for $48 per share in cash. The total fair value of the consideration transferred was $11.2 billion ($10.9 billion, net of cash acquired). In addition, $157 million in payments to Array employees for the fair value of previously unvested stock options was recognized as post-closing compensation expense and recorded in Restructuring charges and certain acquisition-related costs (see Note 3). We financed the majority of the transaction with debt and the balance with existing cash.

证据 2：Therachon On July 1, 2019, we acquired all the remaining shares of Therachon, a privately-held clinical-stage biotechnology company focused on rare diseases, with assets in development for the treatment of achondroplasia, a genetic condition and the most common form of short-limb dwarfism, for $340 million upfront, plus potential milestone payments of up to $470 million contingent on the achievement of key milestones in the development and commercialization of the lead asset. We accounted for the transaction as an asset acquisition since the lead asset represented substantially all the fair value of the gross assets acquired. The total fair value of the consideration transferred for Therachon was $322 million, which consisted of $317 million of cash and our previous $5 million investment in Therachon. In connection with this asset acquisition, we recorded a charge of $337 million in Research and development expenses.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00283

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：Pfizer_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：How much does Pfizer expect to pay to spin off Upjohn in the future in USD million?
- 标准答案：77.78
- 答案依据：10% cost is remaining amount in the future. Calculation: 700/9 is 10% of the cost remaining

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, Pfizer_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We expect to incur costs of approximately $700 million in connection with separating Upjohn, of which approximately 90% has been incurred since inception and through the second quarter of 2023. These charges include costs and expenses related to separation of legal entities and transaction costs.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00724

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：Pfizer_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：For Pfizer, which geographic region had the biggest drop in Q22023 year over year revenues (on a percentage basis)?
- 标准答案：Developed Rest of the World
- 答案依据：It's plainly stated in table format the year over year revenue changes for each of the regions

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, Pfizer_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The following summarizes revenues by geographic area: Three Months Ended Six Months Ended (MILLIONS) July 2, 2023 July 3, 2022 % Change July 2, 2023 July 3, 2022 % Change United States $ 6,185 $ 11,222 (45) $ 14,692 $ 20,140 (27) Developed Europe 2,415 5,480 (56) 5,236 11,569 (55) Developed Rest of World 1,305 5,034 (74) 3,778 8,320 (55) Emerging Markets 2,828 6,006 (53) 7,308 13,373 (45) Revenues $ 12,734 $ 27,742 (54) $ 31,015 $ 53,402 (42)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02419

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Pfizer；文档：Pfizer_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：As of Q2'2023, is Pfizer spinning off any large business segments?
- 标准答案：Yes, it's spinning off Upjohn.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Pfizer, Pfizer_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：We expect to incur costs of approximately $700 million in connection with separating Upjohn, of which approximately 90% has been incurred since inception and through the second quarter of 2023. These charges include costs and expenses related to separation of legal entities and transaction costs.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00746

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Which debt securities are registered to trade on a national securities exchange under Ulta Beauty's name as of FY2023?
- 标准答案：There are none
- 答案依据：No debt securities listed under securities registered pursuant to Section 12(b) of the Act.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：UNITED STATES SECURITIES AND EXCHANGE COMMISSION Washington, DC 20549 FORM 10-K Annual Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934 For the fiscal year ended January 28, 2023 or Transition Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934 For the transition period from _____________ to _____________ Commission File Number: 001-33764 ULTA BEAUTY, INC. (Exact name of registrant as specified in its charter) Delaware (State or other jurisdiction of incorporation or organization) 38-4022268 (I.R.S. Employer Identification No.) 1000 Remington Blvd., Suite 120 Bolingbrook, Illinois (Address of principal executive offices) 60440 (Zip code) Registrants telephone number, including area code: (630) 410-4800 Securities registered pursuant to Section 12(b) of the Act: Title of each class Trading symbol Name of each exchange on which registered Common stock, par value $0.01 per share ULTA The NASDAQ Global Select Market Securities registered pursuant to Section 12(g) of the Act: None

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00521

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are major acquisitions that Ulta Beauty has done in FY2023 and FY2022?
- 标准答案：Ulta Beauty did not make any acquisitions in FY2023 and FY2022.
- 答案依据：Consolidated statement of cash flows reflects - for Acquisitions, net of cash acquired in FY2023 and FY2022.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Ulta Beauty, Inc. Consolidated Statements of Cash Flows Fiscal year ended January 28, January 29, January 30, (In thousands) 2023 2022 2021 Operating activities Net income $ 1,242,408 $ 985,837 $ 175,835 Adjustments to reconcile net income to net cash provided by operating activities: Depreciation and amortization 241,372 268,460 297,772 Non-cash lease expense 301,912 276,229 268,071 Long-lived asset impairment charge 72,533 Deferred income taxes 15,653 (25,666) (24,008) Stock-based compensation expense 43,044 47,259 27,583 Loss on disposal of property and equipment 6,688 5,358 6,827 Change in operating assets and liabilities: Receivables 34,260 (40,573) (53,772) Merchandise inventories (104,233) (331,003) 125,486 Prepaid expenses and other current assets (19,432) (3,412) (4,363) Income taxes (45,182) (35,652) 58,916 Accounts payable 8,309 66,156 62,324 Accrued liabilities 48,249 58,598 58,599 Deferred revenue 41,098 79,196 36,848 Operating lease liabilities (324,500) (303,914) (297,513) Other assets and liabilities (7,731) 12,392 (783) Net cash provided by operating activities 1,481,915 1,059,265 810,355 Investing activities Proceeds from short-term investments 110,000 Capital expenditures (312,126) (172,187) (151,866) Acquisitions, net of cash acquired (1,220)

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00601

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What drove the reduction in SG&A expense as a percent of net sales in FY2023?
- 标准答案：Lower marketing expenses and leverage of incentive compensation due to higher sales. The answer here assumes FY2023 refers to the 12 months ended on January 28, 2023 (although the company refers to this period as its fiscal 2022.
- 答案依据：Fiscal 2022 = FY2023. Fiscal 2021 = FY2022.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：For the Full Year of Fiscal 2022 Net sales increased 18.3% to $10.2 billion compared to $8.6 billion in fiscal 2021, primarily due to the favorable impact from the continued resilience of the beauty category, retail price increases, the impact of new brands and product innovation, increased social occasions, and fewer COVID-19 limitations compared to fiscal 2021. Comparable sales increased 15.6% compared to an increase of 37.9% in fiscal 2021, driven by a 10.8% increase in transactions and a 4.3% increase in average ticket. Gross profit increased 20.1% to $4.0 billion compared to $3.4 billion in fiscal 2021. As a percentage of net sales, gross profit increased to 39.6% compared to 39.0% in fiscal 2021, primarily due to leverage of fixed costs, strong growth in other revenue, and favorable channel mix shifts, partially offset by higher inventory shrink and lower merchandise margin. SG&A expenses increased 16.2% to $2.4 billion compared to $2.1 billion in fiscal 2021. As a percentage of net sales, SG&A expenses decreased to 23.5% compared to 23.9% in fiscal 2021, primarily due to lower marketing expenses and leverage of incentive compensation due to higher sales, partially offset by deleverage of corporate overhead due to strategic investments and deleverage of store payroll and benefits due to wage investments.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00603

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What drove the increase in Ulta Beauty's merchandise inventories balance at end of FY2023?
- 标准答案：Increase in Merchandise inventories balance was driven by the opening of 47 new stores. The answer here assumes FY2023 refers to the 12 months ended on January 28, 2023 (although the company refers to this period as its fiscal 2022.
- 答案依据：Fiscal 2022 = FY2023. Fiscal 2021 = FY2022.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Balance Sheet Cash and cash equivalents at the end of the fourth quarter of fiscal 2022 were $737.9 million. Merchandise inventories, net at the end of the fourth quarter of fiscal 2022 totaled $1.6 billion compared to $1.5 billion at the end of the fourth quarter of fiscal 2021. The $104.2 million increase was primarily due to the opening of 47 new stores since January 29, 2022, inventory to support new brand launches and brand expansions, and inventory cost increases.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00605

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What percent of Ulta Beauty's total spend on stock repurchases for FY 2023 occurred in Q4 of FY2023?
- 标准答案：36%. The answer here assumes FY2023 refers to the 12 months ended on January 28, 2023 (although the company refers to this period as its fiscal 2022.
- 答案依据：Fiscal 2022 = FY2023. Fiscal 2021 = FY2022. Percent spent in Q4 of FY2023 = Amount spent in Q4 of FY2023/Total amount spent in FY2023*100 =$328.1 million /$900 million * 100 = 36%

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Share Repurchase Program During the fourth quarter of fiscal 2022, the Company repurchased 722,457 shares of its common stock at a cost of $328.1 million. During fiscal 2022, the Company repurchased 2.2 million shares of its common stock at a cost of $900.0 million. As of January 28, 2023, $1.1 billion remained available under the $2.0 billion share repurchase program announced in March 2022.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00606

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Ulta Beauty；文档：ULTABEAUTY_2023Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Did Ulta Beauty's wages expense as a percent of net sales increase or decrease in FY2023?
- 标准答案：Wages expense as a percent of net sales increased in FY2023. The answer here assumes FY2023 refers to the 12 months ended on January 28, 2023 (although the company refers to this period as its fiscal 2022.
- 答案依据：Fiscal 2022 = FY2023. Fiscal 2021 = FY2022. Store payroll and benefits = wages. Store payroll and benefits offsets reduction in SG&A percent of net sales in FY2023.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Ulta Beauty, ULTABEAUTY_2023Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：For the Full Year of Fiscal 2022 Net sales increased 18.3% to $10.2 billion compared to $8.6 billion in fiscal 2021, primarily due to the favorable impact from the continued resilience of the beauty category, retail price increases, the impact of new brands and product innovation, increased social occasions, and fewer COVID-19 limitations compared to fiscal 2021. Comparable sales increased 15.6% compared to an increase of 37.9% in fiscal 2021, driven by a 10.8% increase in transactions and a 4.3% increase in average ticket. Gross profit increased 20.1% to $4.0 billion compared to $3.4 billion in fiscal 2021. As a percentage of net sales, gross profit increased to 39.6% compared to 39.0% in fiscal 2021, primarily due to leverage of fixed costs, strong growth in other revenue, and favorable channel mix shifts, partially offset by higher inventory shrink and lower merchandise margin. SG&A expenses increased 16.2% to $2.4 billion compared to $2.1 billion in fiscal 2021. As a percentage of net sales, SG&A expenses decreased to 23.5% compared to 23.9% in fiscal 2021, primarily due to lower marketing expenses and leverage of incentive compensation due to higher sales, partially offset by deleverage of corporate overhead due to strategic investments and deleverage of store payroll and benefits due to wage investments.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00859

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Verizon；文档：VERIZON_2021_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Among all of the derivative instruments that Verizon used to manage the exposure to fluctuations of foreign currencies exchange rates or interest rates, which one had the highest notional value in FY 2021?
- 标准答案：Cross currency swaps. Its notional value was $32,502 million.
- 答案依据：The derivative instruments used to mangae the exposure were interest rate swaps, cross currency swaps, forward starting interest rate swaps, and foreign exchange forwards. 32502 > 19779 > 1000 > 932

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Verizon, VERIZON_2021_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Derivative Instruments We enter into derivative transactions primarily to manage our exposure to fluctuations in foreign currency exchange rates and interest rates. We employ risk management strategies, which may include the use of a variety of derivatives including interest rate swaps, cross currency swaps, forward starting interest rate swaps, treasury rate locks, interest rate caps, swaptions and foreign exchange forwards. We do not hold derivatives for trading purposes. The following table sets forth the notional amounts of our outstanding derivative instruments: (dollars in millions) At December 31, 2021 2020 Interest rate swaps $ 19,779 $ 17,768 Cross currency swaps 32,502 26,288 Forward starting interest rate swaps 1,000 2,000 Foreign exchange forwards 932 1,405

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02024

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Verizon；文档：VERIZON_2021_10K。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：As of FY 2021, how much did Verizon expect to pay for its retirees in 2024?
- 标准答案：The estimated pension benefits were $1097 million, and the estimated health care and life insurance benefits were $862 million.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Verizon, VERIZON_2021_10K, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Pension and postretirement health care and life insurance benefits earned during the year, as well as interest on projected benefit obligations, are accrued.

证据 2：Estimated Future Benefit Payments The benefit payments to retirees are expected to be paid as follows: (dollars in millions) Year Pension Benefits Health Care and Life 2022 $ 2,049 $ 906 2023 1,648 883 2024 1,097 862 2025 1,066 850 2026 1,034 840 2027 to 2031 5,097 4,139

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00216

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Verizon；文档：VERIZON_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Logical reasoning。
- 问题：Does Verizon have a reasonably healthy liquidity profile based on its quick ratio for FY 2022? If the quick ratio is not relevant to measure liquidity, please state that and explain why.
- 标准答案：No. The quick ratio was approximately 0.54 for Verizon. It indicated that Verizon does not have a healthy liquidity profile.
- 答案依据：Quick ratio = (current assets - inventories - prepaid expenses) / current liabilities = (37857 - 2388 - 8358) / 50171 = 0.5403719

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Verizon, VERIZON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Balance Sheets Verizon Communications Inc. and Subsidiaries (dollars in millions, except per share amounts) At December 31, 2022 2021 Assets Current assets Cash and cash equivalents $ 2,605 $ 2,921 Accounts receivable 25,332 24,742 Less Allowance for credit losses 826 896 Accounts receivable, net 24,506 23,846 Inventories 2,388 3,055 Prepaid expenses and other 8,358 6,906 Total current assets 37,857 36,728 Property, plant and equipment 307,689 289,897 Less Accumulated depreciation 200,255 190,201 Property, plant and equipment, net 107,434 99,696 Investments in unconsolidated businesses 1,071 1,061 Wireless licenses 149,796 147,619 Goodwill 28,671 28,603 Other intangible assets, net 11,461 11,677 Operating lease right-of-use assets 26,130 27,883 Other assets 17,260 13,329 Total assets $ 379,680 $ 366,596 Liabilities and Equity Current liabilities Debt maturing within one year $ 9,963 $ 7,443 Accounts payable and accrued liabilities 23,977 24,833 Current operating lease liabilities 4,134 3,859 Other current liabilities 12,097 11,025 Total current liabilities 50,171 47,160

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00215

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Verizon；文档：VERIZON_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning)。
- 问题：Is Verizon a capital intensive business based on FY 2022 data?
- 标准答案：Yes. Verizon's capital intensity ratio was approximately 2.774729. This means that it took approximately $2.77 of assets to generate $1 of revenue and thus, Verizon can be considered capital intensive.
- 答案依据：capital intensity ratio = total asset / revenue = 379680/ 136835 = 2.774729, which is relatively high

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Verizon, VERIZON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Balance Sheets Verizon Communications Inc. and Subsidiaries (dollars in millions, except per share amounts) At December 31, 2022 2021 Assets Current assets Cash and cash equivalents $ 2,605 $ 2,921 Accounts receivable 25,332 24,742 Less Allowance for credit losses 826 896 Accounts receivable, net 24,506 23,846 Inventories 2,388 3,055 Prepaid expenses and other 8,358 6,906 Total current assets 37,857 36,728 Property, plant and equipment 307,689 289,897 Less Accumulated depreciation 200,255 190,201 Property, plant and equipment, net 107,434 99,696 Investments in unconsolidated businesses 1,071 1,061 Wireless licenses 149,796 147,619 Goodwill 28,671 28,603 Other intangible assets, net 11,461 11,677 Operating lease right-of-use assets 26,130 27,883 Other assets 17,260 13,329 Total assets $ 379,680 $ 366,596

证据 2：Consolidated Operating Revenues (dollars in millions) Increase/(Decrease) Years Ended December 31, 2022 2021 2022 vs. 2021 Consumer $ 103,506 $ 95,300 $ 8,206 8.6 % Business 31,072 31,042 30 0.1 Corporate and other 2,510 7,722 (5,212) (67.5) Eliminations (253) (451) 198 43.9 Consolidated Operating Revenues $ 136,835 $ 133,613 $ 3,222 2.4

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00566

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Verizon；文档：VERIZON_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：Has Verizon increased its debt on balance sheet between 2022 and the 2021 fiscal period?
- 标准答案：No. Verizon's debt decreased by $229 million.
- 答案依据：debt change = debt in 2022 - debt in 2021 = 150639 - 150868 = -229

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Verizon, VERIZON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：At December 31, Maturities Interest Rates % 2022 2021 Verizon Communications < 5 Years 0.75 - 5.82 $ 23,929 $ 18,406 5-10 Years 1.50 - 7.88 42,637 43,225 > 10 Years 1.13 - 8.95 60,134 73,520 < 5 Years Floating (1) 2,992 4,086 5-10 Years Floating (1) 3,029 824 Alltel Corporation 5-10 Years 6.80 - 7.88 94 38 > 10 Years N/A N/A 58 Operating telephone company subsidiariesdebentures < 5 Years N/A N/A 141 5-10 Years 6.00 - 8.75 475 375 > 10 Years 5.13 - 7.38 139 250 Other subsidiariesasset-backed debt < 5 Years 0.41 - 5.72 9,767 9,620 < 5 Years Floating (2) 10,271 4,610 Finance lease obligations (average rate of 2.5% and 2.2% in 2022 and 2021, respectively) 1,732 1,325 Unamortized discount, net of premium (4,039) (4,922) Unamortized debt issuance costs (671) (688) Total long-term debt, including current maturities 150,489 150,868 Less long-term debt maturing within one year 9,813 7,443 Total long-term debt $ 140,676 $ 143,425 Long-term debt maturing within one year $ 9,813 $ 7,443 Add commercial paper 150 Debt maturing within one year 9,963 7,443 Add long-term debt 140,676 143,425 Total debt $ 150,639 $ 150,868

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_06247

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Walmart；文档：WALMART_2018_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is FY2018 days payable outstanding (DPO) for Walmart? DPO is defined as: 365 * (average accounts payable between FY2017 and FY2018) / (FY2018 COGS + change in inventory between FY2017 and FY2018). Round your answer to two decimal places. Please base your judgments on the information provided primarily in the statement of financial position and the P&L statement.
- 标准答案：42.69
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Accounts payable. This metric was located in the 10K as a single line item named: Accounts payable.

Metric 2: Inventories. This metric was located in the 10K as a single line item named: Inventories.

Metric 3: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of sales.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Walmart, WALMART_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Walmart Inc. Consolidated Statements of Income Fiscal Years Ended January 31, (Amounts in millions, except per share data) 2018 2017 2016 Revenues: Net sales $ 495,761 $ 481,317 $ 478,614 Membership and other income 4,582 4,556 3,516 Total revenues 500,343 485,873 482,130 Costs and expenses: Cost of sales 373,396 361,256 360,984 Operating, selling, general and administrative expenses 106,510 101,853 97,041 Operating income 20,437 22,764 24,105 Interest: Debt 1,978 2,044 2,027 Capital lease and financing obligations 352 323 521 Interest income (152) (100) (81) Interest, net 2,178 2,267 2,467 Loss on extinguishment of debt 3,136 Income before income taxes 15,123 20,497 21,638 Provision for income taxes 4,600 6,204 6,558 Consolidated net income 10,523 14,293 15,080 Consolidated net income attributable to noncontrolling interest (661) (650) (386) Consolidated net income attributable to Walmart $ 9,862 $ 13,643 $ 14,694 Net income per common share: Basic net income per common share attributable to Walmart $ 3.29 $ 4.40 $ 4.58 Diluted net income per common share attributable to Walmart 3.28 4.38 4.57 Weighted-average common shares outstanding: Basic 2,995 3,101 3,207 Diluted 3,010 3,112 3,217 Dividends declared per common share $ 2.04 $ 2.00 $ 1.96 See accompanying notes. 55

证据 2：Walmart Inc. Consolidated Balance Sheets As of January 31, (Amounts in millions) 2018 2017 ASSETS Current assets: Cash and cash equivalents $ 6,756 $ 6,867 Receivables, net 5,614 5,835 Inventories 43,783 43,046 Prepaid expenses and other 3,511 1,941 Total current assets 59,664 57,689 Property and equipment: Property and equipment 185,154 179,492 Less accumulated depreciation (77,479) (71,782) Property and equipment, net 107,675 107,710 Property under capital lease and financing obligations: Property under capital lease and financing obligations 12,703 11,637 Less accumulated amortization (5,560) (5,169) Property under capital lease and financing obligations, net 7,143 6,468 Goodwill 18,242 17,037 Other assets and deferred charges 11,798 9,921 Total assets $ 204,522 $ 198,825 LIABILITIES AND EQUITY Current liabilities: Short-term borrowings $ 5,257 $ 1,099 Accounts payable 46,092 41,433 Accrued liabilities 22,122 20,654 Accrued income taxes 645 921 Long-term debt due within one year 3,738 2,256 Capital lease and financing obligations due within one year 667 565 Total current liabilities 78,521 66,928 Long-term debt 30,045 36,015 Long-term capital lease and financing obligations 6,780 6,003 Deferred income taxes and other 8,354 9,344 Commitments and contingencies Equity: Common stock 295 305 Capital in excess of par value 2,648 2,371 Retained earnings 85,107 89,354 Accumulated other comprehensive loss (10,181) (14,232) Total Walmart shareholders' equity 77,869 77,798 Noncontrolling interest 2,953 2,737 Total equity 80,822 80,535 Total liabilities and equity $ 204,522 $ 198,825 See accompanying notes. 57

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04784

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Walmart；文档：WALMART_2019_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：Based on the information provided primarily in the statement of income, what is the FY2018 - FY2019 change in unadjusted operating income % margin for Walmart? Answer in units of percents and round to one decimal place.
- 标准答案：0.2%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating income.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: Total revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Walmart, WALMART_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：WalmartInc. ConsolidatedStatementsofIncome FiscalYearsEndedJanuary31, (Amounts in millions, except per share data) 2019 2018 2017 Revenues: Net sales $ 510,329 $ 495,761 $ 481,317 Membership and other income 4,076 4,582 4,556 Total revenues 514,405 500,343 485,873 Costsandexpenses: Cost of sales 385,301 373,396 361,256 Operating, selling, general and administrative expenses 107,147 106,510 101,853 Operatingincome 21,957 20,437 22,764 Interest: Debt 1,975 1,978 2,044 Capital lease and financing obligations 371 352 323 Interest income (217) (152) (100) Interest, net 2,129 2,178 2,267 Loss on extinguishment of debt 3,136 Other (gains) and losses 8,368 Incomebeforeincometaxes 11,460 15,123 20,497 Provision for income taxes 4,281 4,600 6,204 Consolidatednetincome 7,179 10,523 14,293 Consolidatednetincomeattributabletononcontrollinginterest (509) (661) (650) ConsolidatednetincomeattributabletoWalmart $ 6,670 $ 9,862 $ 13,643 Netincomepercommonshare: BasicnetincomepercommonshareattributabletoWalmart $ 2.28 $ 3.29 $ 4.40 DilutednetincomepercommonshareattributabletoWalmart 2.26 3.28 4.38 Weighted-averagecommonsharesoutstanding: Basic 2,929 2,995 3,101 Diluted 2,945 3,010 3,112 Dividendsdeclaredpercommonshare $ 2.08 $ 2.04 $ 2.00 See accompanying notes. 48

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_06741

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Walmart；文档：WALMART_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2018 - FY2020 3 year average unadjusted EBITDA % margin for Walmart? Define unadjusted EBITDA as unadjusted operating income + depreciation and amortization from the cash flow statement. Answer in units of percents and round to one decimal place. Calculate what was asked by utilizing the line items clearly shown in the P&L statement and the cash flow statement.
- 标准答案：6.2%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization.

Metric 2: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating income.

Metric 3: Total revenue. This metric was located in the 10K as a single line item named: Total revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Walmart, WALMART_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Walmart Inc. Consolidated Statements of Income Fiscal Years Ended January 31, (Amounts in millions, except per share data) 2020 2019 2018 Revenues: Net sales $ 519,926 $ 510,329 $ 495,761 Membership and other income 4,038 4,076 4,582 Total revenues 523,964 514,405 500,343 Costs and expenses: Cost of sales 394,605 385,301 373,396 Operating, selling, general and administrative expenses 108,791 107,147 106,510 Operating income 20,568 21,957 20,437 Interest: Debt 2,262 1,975 1,978 Finance, capital lease and financing obligations 337 371 352 Interest income (189) (217) (152) Interest, net 2,410 2,129 2,178 Loss on extinguishment of debt 3,136 Other (gains) and losses (1,958) 8,368 Income before income taxes 20,116 11,460 15,123 Provision for income taxes 4,915 4,281 4,600 Consolidated net income 15,201 7,179 10,523 Consolidated net income attributable to noncontrolling interest (320) (509) (661) Consolidated net income attributable to Walmart $ 14,881 $ 6,670 $ 9,862 Net income per common share: Basic net income per common share attributable to Walmart $ 5.22 $ 2.28 $ 3.29 Diluted net income per common share attributable to Walmart 5.19 2.26 3.28 Weighted-average common shares outstanding: Basic 2,850 2,929 2,995 Diluted 2,868 2,945 3,010 Dividends declared per common share $ 2.12 $ 2.08 $ 2.04 See accompanying notes. 50

证据 2：Walmart Inc. Consolidated Statements of Cash Flows Fiscal Years Ended January 31, (Amounts in millions) 2020 2019 2018 Cash flows from operating activities: Consolidated net income $ 15,201 $ 7,179 $ 10,523 Adjustments to reconcile consolidated net income to net cash provided by operating activities: Depreciation and amortization 10,987 10,678 10,529 Unrealized (gains) and losses (1,886) 3,516 (Gains) and losses for disposal of business operations 15 4,850 Asda pension contribution (1,036) Deferred income taxes 320 (499) (304) Loss on extinguishment of debt 3,136 Other operating activities 1,981 1,734 1,210 Changes in certain assets and liabilities, net of effects of acquisitions: Receivables, net 154 (368) (1,074) Inventories (300) (1,311) (140) Accounts payable (274) 1,831 4,086 Accrued liabilities 186 183 928 Accrued income taxes (93) (40) (557) Net cash provided by operating activities 25,255 27,753 28,337 Cash flows from investing activities: Payments for property and equipment (10,705) (10,344) (10,051) Proceeds from the disposal of property and equipment 321 519 378 Proceeds from the disposal of certain operations 833 876 1,046 Payments for business acquisitions, net of cash acquired (56) (14,656) (375) Other investing activities 479 (431) (77) Net cash used in investing activities (9,128) (24,036) (9,079) Cash flows from financing activities: Net change in short-term borrowings (4,656) (53) 4,148 Proceeds from issuance of long-term debt 5,492 15,872 7,476 Repayments of long-term debt (1,907) (3,784) (13,061) Premiums paid to extinguish debt (3,059) Dividends paid (6,048) (6,102) (6,124) Purchase of Company stock (5,717) (7,410) (8,296) Dividends paid to noncontrolling interest (555) (431) (690) Purchase of noncontrolling interest (8) Other financing activities (908) (629) (261) Net cash used in financing activities (14,299) (2,537) (19,875) Effect of exchange rates on cash, cash equivalents and restricted cash (69) (438) 487 Net increase (decrease) in cash, cash equivalents and restricted cash 1,759 742 (130) Cash, cash equivalents and restricted cash at beginning of year 7,756 7,014 7,144 Cash, cash equivalents and restricted cash at end of year $ 9,515 $ 7,756 $ 7,014 Supplemental disclosure of cash flow information: Income taxes paid $ 3,616 $ 3,982 $ 6,179 Interest paid 2,464 2,348 2,450 See accompanying notes.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
