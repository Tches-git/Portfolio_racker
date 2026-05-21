# FinanceBench 样本：financebench_id_04412

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Lockheed Martin；文档：LOCKHEEDMARTIN_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：We need to calculate a reasonable approximation (or exact number if possible) of a financial metric. Basing your judgment by information plainly provided in the balance sheet and the P&L statement, what is Lockheed Martin's FY2020 asset turnover ratio? Asset turnover ratio is defined as: FY2020 revenue / (average total assets between FY2019 and FY2020). Round your answer to two decimal places.
- 标准答案：1.33
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total revenue. This metric was located in the 10K as a single line item named: Total net sales.

Metric 2: Total assets. This metric was located in the 10K as a single line item named: Total assets.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Lockheed Martin, LOCKHEEDMARTIN_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Lockheed Martin Corporation Consolidated Statements of Earnings (in millions, except per share data) Years Ended December 31, 2020 2019 2018 Net sales Products $ 54,928 $ 50,053 $ 45,005 Services 10,470 9,759 8,757 Total net sales 65,398 59,812 53,762 Cost of sales Products (48,996) (44,589) (40,293) Services (9,371) (8,731) (7,738) Severance charges (27) (96) Other unallocated, net 1,650 1,875 1,639 Total cost of sales (56,744) (51,445) (46,488) Gross profit 8,654 8,367 7,274 Other (expense) income, net (10) 178 60 Operating profit 8,644 8,545 7,334 Interest expense (591) (653) (668) Other non-operating income (expense), net 182 (651) (828) Earnings from continuing operations before income taxes 8,235 7,241 5,838 Income tax expense (1,347) (1,011) (792) Net earnings from continuing operations 6,888 6,230 5,046 Net loss from discontinued operations (55) Net earnings $ 6,833 $ 6,230 $ 5,046 Earnings (loss) per common share Basic Continuing operations $ 24.60 $ 22.09 $ 17.74 Discontinued operations (0.20) Basic earnings per common share $ 24.40 $ 22.09 $ 17.74 Diluted Continuing operations $ 24.50 $ 21.95 $ 17.59 Discontinued operations (0.20) Diluted earnings per common share $ 24.30 $ 21.95 $ 17.59 The accompanying notes are an integral part of these consolidated financial statements. 67

证据 2：Table of Contents Lockheed Martin Corporation Consolidated Balance Sheets (in millions, except par value) December 31, 2020 2019 Assets Current assets Cash and cash equivalents $ 3,160 $ 1,514 Receivables, net 1,978 2,337 Contract assets 9,545 9,094 Inventories 3,545 3,619 Other current assets 1,150 531 Total current assets 19,378 17,095 Property, plant and equipment, net 7,213 6,591 Goodwill 10,806 10,604 Intangible assets, net 3,012 3,213 Deferred income taxes 3,475 3,319 Other noncurrent assets 6,826 6,706 Total assets $ 50,710 $ 47,528 Liabilities and equity Current liabilities Accounts payable $ 880 $ 1,281 Contract liabilities 7,545 7,054 Salaries, benefits and payroll taxes 3,163 2,466 Current maturities of long-term debt 500 1,250 Other current liabilities 1,845 1,921 Total current liabilities 13,933 13,972 Long-term debt, net 11,669 11,404 Accrued pension liabilities 12,874 13,234 Other noncurrent liabilities 6,196 5,747 Total liabilities 44,672 44,357 Stockholders equity Common stock, $1 par value per share 279 280 Additional paid-in capital 221 Retained earnings 21,636 18,401 Accumulated other comprehensive loss (16,121) (15,554) Total stockholders equity 6,015 3,127 Noncontrolling interests in subsidiary 23 44 Total equity 6,038 3,171 Total liabilities and equity $ 50,710 $ 47,528 The accompanying notes are an integral part of these consolidated financial statements. 69

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03031

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Lockheed Martin；文档：LOCKHEEDMARTIN_2021_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Lockheed Martin's FY2021 net working capital? Define net working capital as total current assets less total current liabilities. Answer in USD millions. Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the balance sheet.
- 标准答案：$5818.00
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total current liabilities. This metric was located in the 10K as a single line item named: Total current liabilities.

Metric 2: Total current assets. This metric was located in the 10K as a single line item named: Total current assets.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Lockheed Martin, LOCKHEEDMARTIN_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Lockheed Martin Corporation Consolidated Balance Sheets (in millions, except par value) December 31, 2021 2020 Assets Current assets Cash and cash equivalents $ 3,604 $ 3,160 Receivables, net 1,963 1,978 Contract assets 10,579 9,545 Inventories 2,981 3,545 Other current assets 688 1,150 Total current assets 19,815 19,378 Property, plant and equipment, net 7,597 7,213 Goodwill 10,813 10,806 Intangible assets, net 2,706 3,012 Deferred income taxes 2,290 3,475 Other noncurrent assets 7,652 6,826 Total assets $ 50,873 $ 50,710 Liabilities and equity Current liabilities Accounts payable $ 780 $ 880 Salaries, benefits and payroll taxes 3,108 3,163 Contract liabilities 8,107 7,545 Current maturities of long-term debt 6 500 Other current liabilities 1,996 1,845 Total current liabilities 13,997 13,933 Long-term debt, net 11,670 11,669 Accrued pension liabilities 8,319 12,874 Other noncurrent liabilities 5,928 6,196 Total liabilities 39,914 44,672 Stockholders equity Common stock, $1 par value per share 271 279 Additional paid-in capital 94 221 Retained earnings 21,600 21,636 Accumulated other comprehensive loss (11,006) (16,121) Total stockholders equity 10,959 6,015 Noncontrolling interests in subsidiary 23 Total equity 10,959 6,038 Total liabilities and equity $ 50,873 $ 50,710 The accompanying notes are an integral part of these consolidated financial statements. 68

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03718

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Lockheed Martin；文档：LOCKHEEDMARTIN_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Lockheed Martin's 2 year total revenue CAGR from FY2020 to FY2022 (in units of percents and round to one decimal place)? Provide a response to the question by primarily using the statement of income.
- 标准答案：0.4%
- 答案依据：The metric total revenue was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total net sales. The final step was to execute the desired CAGR calculation on total revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Lockheed Martin, LOCKHEEDMARTIN_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Lockheed Martin Corporation Consolidated Statements of Earnings (in millions, except per share data) Years Ended December 31, 2022 2021 2020 Net sales Products $ 55,466 $ 56,435 $ 54,928 Services 10,518 10,609 10,470 Total net sales 65,984 67,044 65,398 Cost of sales Products (49,577) (50,273) (48,996) Services (9,280) (9,463) (9,371) Severance and other charges (100) (36) (27) Other unallocated, net 1,260 1,789 1,650 Total cost of sales (57,697) (57,983) (56,744) Gross profit 8,287 9,061 8,654 Other income (expense), net 61 62 (10) Operating profit 8,348 9,123 8,644 Interest expense (623) (569) (591) Non-service FAS pension (expense) income (971) (1,292) 219 Other non-operating (expense) income, net (74) 288 (37) Earnings from continuing operations before income taxes 6,680 7,550 8,235 Income tax expense (948) (1,235) (1,347) Net earnings from continuing operations 5,732 6,315 6,888 Net loss from discontinued operations (55) Net earnings $ 5,732 $ 6,315 $ 6,833 Earnings (loss) per common share Basic Continuing operations $ 21.74 $ 22.85 $ 24.60 Discontinued operations (0.20) Basic earnings per common share $ 21.74 $ 22.85 $ 24.40 Diluted Continuing operations $ 21.66 $ 22.76 $ 24.50 Discontinued operations (0.20) Diluted earnings per common share $ 21.66 $ 22.76 $ 24.30 The accompanying notes are an integral part of these consolidated financial statements. Table of Contents 63

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04171

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2018_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：Basing your judgments off of the balance sheet, what is the year end FY2018 amount of accounts payable for MGM Resorts? Answer in USD millions.
- 标准答案：$303.00
- 答案依据：The metric accounts payable was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Accounts payable.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：MGMRESORTSINTERNATIONALANDSUBSIDIARIES CONSOLIDATEDBALANCESHEETS (Inthousands,exceptsharedata) December31, 2018 2017 ASSETS Currentassets Cash and cash equivalents $ 1,526,762 $ 1,499,995 Accounts receivable, net 657,206 542,273 Inventories 110,831 102,292 Income tax receivable 28,431 42,551 Prepaid expenses and other 203,548 189,244 Total current assets 2,526,778 2,376,355 Propertyandequipment,net 20,729,888 19,635,459 Otherassets Investments in and advances to unconsolidated affiliates 732,867 1,033,297 Goodwill 1,821,392 1,806,531 Other intangible assets, net 3,944,463 3,877,960 Other long-term assets, net 455,318 430,440 Total other assets 6,954,040 7,148,228 $ 30,210,706 $ 29,160,042 LIABILITIESANDSTOCKHOLDERS'EQUITY Currentliabilities Accounts payable $ 302,578 $ 255,028 Construction payable 311,793 474,807 Current portion of long-term debt 43,411 158,042 Accrued interest on long-term debt 140,046 135,785 Other accrued liabilities 2,151,054 2,114,635 Total current liabilities 2,948,882 3,138,297 Deferredincometaxes,net 1,342,538 1,295,375 Long-termdebt,net 15,088,005 12,751,052 Otherlong-termobligations 259,240 284,416 Commitmentsandcontingencies(Note11) Redeemablenoncontrollinginterests 102,250 79,778 Stockholders'equity Common stock, $.01 par value: authorized 1,000,000,000 shares, issued and outstanding 527,479,528 and 566,275,789 shares 5,275 5,663 Capital in excess of par value 4,092,085 5,357,709 Retained earnings 2,423,479 2,217,299 Accumulated other comprehensive loss (8,556) (3,610) Total MGM Resorts International stockholders' equity 6,512,283 7,577,061 Noncontrolling interests 3,957,508 4,034,063 Total stockholders' equity 10,469,791 11,611,124 $ 30,210,706 $ 29,160,042 Theaccompanyingnotesareanintegralpartoftheseconsolidatedfinancialstatements. 55

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03849

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2018 - FY2020 3 year average of capex as a % of revenue for MGM Resorts? Answer in units of percents and round to one decimal place. Please utilize information provided primarily within the statement of cash flows and the statement of income.
- 标准答案：7.9%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Capital expenditures. This metric was located in the 10K as a single line item named: Capital expenditures, net of construction payable.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: [blank line item referring to total revenue].

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：MGM RESORTS INTERNATIONAL AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF OPERATIONS (In thousands, except per share data) Year Ended December 31, 2020 2019 2018 Revenues Casino $ 2,871,720 $ 6,517,759 $ 5,753,150 Rooms 830,382 2,322,579 2,212,573 Foodandbeverage 696,040 2,145,247 1,959,021 Entertainment,retailandother 518,991 1,477,200 1,412,860 Reimbursedcosts 244,949 436,887 425,492 5,162,082 12,899,672 11,763,096 Expenses Casino 1,701,783 3,623,899 3,199,775 Rooms 419,156 829,677 791,761 Foodandbeverage 674,118 1,661,626 1,501,868 Entertainment,retailandother 412,705 1,051,400 999,979 Reimbursedcosts 244,949 436,887 425,492 Generalandadministrative 2,122,333 2,101,217 1,764,638 Corporateexpense 460,148 464,642 419,204 Preopeningandstart-upexpenses 84 7,175 151,392 Propertytransactions,net 93,567 275,802 9,147 GainonREITtransactions,net (1,491,945) (2,677,996) Depreciationandamortization 1,210,556 1,304,649 1,178,044 5,847,454 9,078,978 10,441,300 Income from unconsolidated affiliates 42,938 119,521 147,690 Operating income (loss) (642,434) 3,940,215 1,469,486 Non-operating income (expense) Interestexpense,netofamountscapitalized (676,380) (847,932) (769,513) Non-operatingitemsfromunconsolidatedaffiliates (103,304) (62,296) (47,827) Other,net (89,361) (183,262) (18,140) (869,045) (1,093,490) (835,480) Income (loss) before income taxes (1,511,479) 2,846,725 634,006 Benefit(provision)forincometaxes 191,572 (632,345) (50,112) Net income (loss) (1,319,907) 2,214,380 583,894 Less:Net(income)lossattributabletononcontrollinginterests 287,183 (165,234) (117,122) Net income (loss) attributable to MGM Resorts International $ (1,032,724) $ 2,049,146 $ 466,772 Earnings (loss) per share Basic $ (2.02) $ 3.90 $ 0.82 Diluted $ (2.02) $ 3.88 $ 0.81 Weighted average common shares outstanding Basic 494,152 524,173 544,253 Diluted 494,152 527,645 549,536 The accompanying notes are an integral part of these consolidated financial statements. 63

证据 2：MGM RESORTS INTERNATIONAL AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF CASH FLOWS (In thousands) Year Ended December 31, 2020 2019 2018 Cash flows from operating activities Netincome(loss) $ (1,319,907) $ 2,214,380 $ 583,894 Adjustmentstoreconcilenetincome(loss)tonetcashprovidedby(usedin) operatingactivities: Depreciationandamortization 1,210,556 1,304,649 1,178,044 Amortizationofdebtdiscounts,premiumsandissuancecosts 34,363 38,972 41,102 Lossonearlyretirementofdebt 126,462 198,151 3,619 Provisionforcreditlosses 71,422 39,270 39,762 Stock-basedcompensation 106,956 88,838 70,177 Propertytransactions,net 93,567 275,802 9,147 GainonREITtransactions,net (1,491,945) (2,677,996) Noncashleaseexpense 183,399 71,784 Loss(income)fromunconsolidatedaffiliates 60,366 (57,225) (96,542) Distributionsfromunconsolidatedaffiliates 86,584 299 11,563 Deferredincometaxes 18,347 595,046 46,720 Changeinoperatingassetsandliabilities: Accountsreceivable 960,099 (726,610) (149,554) Inventories 14,705 6,522 (7,860) Incometaxesreceivableandpayable,net (216,250) 1,259 14,120 Prepaidexpensesandother (37) 7,567 (8,656) Accountspayableandaccruedliabilities (1,382,980) 465,602 21,508 Other (48,750) (35,909) (34,505) Netcashprovidedby(usedin)operatingactivities (1,493,043) 1,810,401 1,722,539 Cash flows from investing activities Capitalexpenditures,netofconstructionpayable (270,579) (739,006) (1,486,843) Dispositionsofpropertyandequipment 6,136 2,578 25,612 ProceedsfromMandalayBayandMGMGrandLasVegastransaction 2,455,839 ProceedsfromBellagiotransaction 4,151,499 ProceedsfromsaleofCircusCircusLasVegasandadjacentland 652,333 Proceedsfromsaleofbusinessunitsandinvestmentinunconsolidatedaffiliate 163,616 AcquisitionofNorthfield,netofcashacquired (1,034,534) AcquisitionofEmpireCityCasino,netofcashacquired (535,681) Investmentsinunconsolidatedaffiliates (96,925) (81,877) (56,295) Distributionsfromunconsolidatedaffiliates 63,960 100,700 322,631 Other 873 (31,112) (17,208) Netcashprovidedby(usedin)investingactivities 2,159,304 3,519,434 (2,083,021) Cash flows from financing activities Netborrowings(repayments)underbankcreditfacilitiesmaturitiesof 90daysorless (1,595,089) (3,634,049) 1,242,259 Issuanceoflong-termdebt 3,550,000 3,250,000 1,000,000 Retirementofseniornotes (846,815) (3,764,167) (2,265) Debtissuancecosts (62,348) (63,391) (76,519) Proceedsfromissuanceofbridgeloanfacility 1,304,625 IssuanceofMGMGrowthPropertiesClassAshares,net 524,704 1,250,006 Dividendspaidtocommonshareholders (77,606) (271,288) (260,592) Distributionstononcontrollinginterestowners (286,385) (223,303) (184,932) Purchasesofcommonstock (353,720) (1,031,534) (1,283,333) Other (53,939) (41,868) (45,384) Netcashprovidedby(usedin)financingactivities 2,103,427 (4,529,594) 389,234 Effect of exchange rate on cash 2,345 2,601 (1,985) Cash and cash equivalents Netincreasefortheperiod 2,772,033 802,842 26,767 Balance,beginningofperiod 2,329,604 1,526,762 1,499,995 Balance,endofperiod $ 5,101,637 $ 2,329,604 $ 1,526,762 Supplemental cash flow disclosures Interestpaid,netofamountscapitalized $ 639,718 $ 826,970 $ 723,609 Federal,stateandforeignincometaxespaid(refundsreceived),net 8,543 28,493 (10,100) Non-cash investing and financing activities NotereceivablerelatedtosaleofCircusCircusLasVegasandadjacentland $ $ 133,689 $ InvestmentinBellagioBREITVenture 62,133 InvestmentinMGPBREITVenture 802,000 MGPBREITVentureassumptionofbridgeloanfacility 1,304,625 The accompanying notes are an integral part of these consolidated financial statements. 65

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01254

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Has MGM Resorts paid dividends to common shareholders in FY2022?
- 标准答案：Yes. MGM maintained 0.01$ per share annual dividend through out FY 2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：. We maintained an annual dividend of $0.01 per share throughout 2022.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00382

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2022Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which region had the Highest EBITDAR Contribution for MGM during FY2022?
- 标准答案：Las Vegas resorts contributed ~90% of company level EBITDAR during FY2022.
- 答案依据：3142308/3497254

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2022Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：dited) Three months ended Twelve months ended December 31, 2022 December 31, 2021 December 31, 2022 December 31, 2021 Las Vegas Strip Resorts $ 877,052 $ 698,739 $ 3,142,308 $ 1,738,211 Regional Operations 319,517 309,250 1,294,630 1,217,814 MGM China (54,979) 5,015 (203,136) 25,367 Unconsolidated affiliates(1) (43,029) (49,698) (222,079) (131,590) Management and other operations (3,037) 2,087 (11,934) 15,766 Stock compensation (25,159) (26,494) (71,297) (63,984) Corporate(2) (113,058) (117,491) (431,238) (380,501) $ 957,307 $ 3,497,254

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01911

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2022Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What was MGM's interest coverage ratio using FY2022 Adjusted EBIT as the numerator and annual Interest Expense as the denominator?
- 标准答案：As adjusted EBIT is negative, coverage ratio is zero
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2022Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：dited) Three months ended Twelve months ended December 31, 2022 December 31, 2021 December 31, 2022 December 31, 2021 Net income attributable to MGM Resorts International $ 284,002 $ 131,013 $ 1,473,093 $ 1,254,370 Plus: Net loss attributable to noncontrolling interests (604,016) (14,926) (1,266,362) (45,981) Net income (loss) (320,014) 116,087 206,731 1,208,389 Provision for income taxes 285,937 31,152 697,068 253,415 Income (loss) before income taxes (34,077) 147,239 903,799 1,461,804 Non-operating (income) expense Interest expense, net of amounts capitalized 137,132 201,477 594,954 799,593 Other, net (104,951) 20,131 (59,381) 17,302 32,181 221,608 535,573 816,895 Operating income (loss) (1,896) 368,847 1,439,372 2,278,699 Preopening and start-up expenses 504 3,452 1,876 5,094 Property transactions, net (1,060,701) (68,578) (1,036,997) (67,736) Depreciation and amortization 1,421,637 297,031 3,482,050 1,150,610 Gain on REIT transactions, net (2,277,747) Gain on consolidation of CityCenter, net (1,562,329) Triple-net operating lease and ground lease rent expense 600,467 262,307 1,950,566 833,158 Gain related to sale of Harmon land - unconsolidated affiliate (49,755) Income from unconsolidated affiliates related to real estate ventures (2,704) (41,651) (61,866) (166,658) Adjusted EBITDAR $ 957,307 $ 3,497,254

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01912

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2022Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which region had the worst topline performance for MGM during FY2022?
- 标准答案：MGM China experienced the worst topline performance amongst the other regions presented. Its revenue declined 44% in FY2022 whereas the other regions presented increased their revenues.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2022Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Las Vegas Strip Resorts Net revenues of $8.4 billion in the current year compared to $4.7 billion in the prior year, an increase of 77%;

证据 2：Regional Operations Net revenues of $3.8 billion in the current year compared to $3.4 billion in the prior year, an increase of 12%;

证据 3：MGM China Net revenues of $674 million in the current year compared to $1.2 billion in the prior year, a decrease of 44%;

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00407

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：MGM Resorts；文档：MGMRESORTS_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which type of debt received the largest investment among the short term investments for MGM in H1 FY2023?
- 标准答案：the biggest short term investment is in corporate bonds (almost 82% of the total investment)
- 答案依据：416420/509921

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, MGM Resorts, MGMRESORTS_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Fair value level June 30, 2023 December 31, 2022 (In thousands) Cash and cash equivalents: Money market funds Level 1 $ 2,195 $ 12,009 Commercial paper and certificates of deposit Level 2 5,992 Cash and cash equivalents 2,195 18,001 Short-term investments: U.S. government securities Level 1 57,696 56,835 U.S. agency securities Level 2 29,049 9,530 Commercial paper and certificates of deposit Level 2 4,561 4,466 Corporate bonds Level 2 416,420 213,875 Short-term investments 507,726 284,706 Total debt investments $ 509,921 $ 302,707

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04700

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Microsoft；文档：MICROSOFT_2016_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is the FY2016 COGS for Microsoft? Please state answer in USD millions. Provide a response to the question by primarily using the statement of income.
- 标准答案：$32780.00
- 答案依据：The metric cost of goods sold was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total cost of revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Microsoft, MICROSOFT_2016_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents PART II Item 8 ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA INCOME STATEMENTS (In millions, except per share amounts) Year Ended June 30, 2016 2015 2014 Revenue: Product $ 61,502 $ 75,956 $ 72,948 Service and other 23,818 17,624 13,885 Total revenue 85,320 93,580 86,833 Cost of revenue: Product 17,880 21,410 16,681 Service and other 14,900 11,628 10,397 Total cost of revenue 32,780 33,038 27,078 Gross margin 52,540 60,542 59,755 Research and development 11,988 12,046 11,381 Sales and marketing 14,697 15,713 15,811 General and administrative 4,563 4,611 4,677 Impairment, integration, and restructuring 1,110 10,011 127 Operating income 20,182 18,161 27,759 Other income (expense), net (431) 346 61 Income before income taxes 19,751 18,507 27,820 Provision for income taxes 2,953 6,314 5,746 Net income $ 16,798 $ 12,193 $ 22,074 Earnings per share: Basic $ 2.12 $ 1.49 $ 2.66 Diluted $ 2.10 $ 1.48 $ 2.63 Weighted average shares outstanding: Basic 7,925 8,177 8,299 Diluted 8,013 8,254 8,399 Cash dividends declared per common share $ 1.44 $ 1.24 $ 1.12 See accompanying notes. 52

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00552

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Microsoft；文档：MICROSOFT_2023_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：Has Microsoft increased its debt on balance sheet between FY2023 and the FY2022 period?
- 标准答案：No. Microsoft decreased its debt by $2.5bn in FY 2023 vs FY 2022.
- 答案依据：Current portion of long-term debt+Long-term debt
5247+41990
2749+47032

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Microsoft, MICROSOFT_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：BALANCE SHEETS (In millions) June 30, 2023 2022 Assets Current assets: Cash and cash equivalents $ 34,704 $ 13,931 Short-term investments 76,558 90,826 Total cash, cash equivalents, and short-term investments 111,262 104,757 Accounts receivable, net of allowance for doubtful accounts of $650 and $633 48,688 44,261 Inventories 2,500 3,742 Other current assets 21,807 16,924 Total current assets 184,257 169,684 Property and equipment, net of accumulated depreciation of $68,251 and $59,660 95,641 74,398 Operating lease right-of-use assets 14,346 13,148 Equity investments 9,879 6,891 Goodwill 67,886 67,524 Intangible assets, net 9,366 11,298 Other long-term assets 30,601 21,897 Total assets $ 411,976 $ 364,840 Liabilities and stockholders equity Current liabilities: Accounts payable $ 18,095 $ 19,000 Current portion of long-term debt 5,247 2,749 Accrued compensation 11,009 10,661 Short-term income taxes 4,152 4,067 Short-term unearned revenue 50,901 45,538 Other current liabilities 14,745 13,067 Total current liabilities 104,149 95,082 Long-term debt 41,990 47,032 Long-term income taxes 25,560 26,069 Long-term unearned revenue 2,912 2,870 Deferred income taxes 433 230 Operating lease liabilities 12,728 11,489 Other long-term liabilities 17,981 15,526 Total liabilities 205,753 198,298 Commitments and contingencies Stockholders equity: Common stock and paid-in capital shares authorized 24,000; outstanding 7,432 and 7,464 93,718 86,939 Retained earnings 118,848 84,281 Accumulated other comprehensive loss (6,343) (4,678) Total stockholders equity 206,223 166,542 Total liabilities and stockholders equity $ 411,976 $ 364,8

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04458

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Netflix；文档：NETFLIX_2015_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：We want to calculate a financial metric. Please help us compute it by basing your answers off of the statement of income and the statement of cash flows. Here's the question: what is the FY2015 unadjusted EBITDA % margin for Netflix? Calculate unadjusted EBITDA using unadjusted operating income and D&A (from cash flow statement).
- 标准答案：5.4%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization of property, equipment and intangibles.

Metric 2: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating income.

Metric 3: Total revenue. This metric was located in the 10K as a single line item named: Revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Netflix, NETFLIX_2015_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents NETFLIX, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (in thousands, except per share data) Year ended December 31, 2015 2014 2013 Revenues $ 6,779,511 $ 5,504,656 $ 4,374,562 Cost of revenues 4,591,476 3,752,760 3,117,203 Marketing 824,092 607,186 469,942 Technology and development 650,788 472,321 378,769 General and administrative 407,329 269,741 180,301 Operating income 305,826 402,648 228,347 Other income (expense): Interest expense (132,716) (50,219) (29,142) Interest and other income (expense) (31,225) (3,060) (3,002) Loss on extinguishment of debt (25,129) Income before income taxes 141,885 349,369 171,074 Provision for income taxes 19,244 82,570 58,671 Net income $ 122,641 $ 266,799 $ 112,403 Earnings per share: Basic $ 0.29 $ 0.63 $ 0.28 Diluted $ 0.28 $ 0.62 $ 0.26 Weighted-average common shares outstanding: Basic 425,889 420,544 407,385 Diluted 436,456 431,894 425,327 See accompanying notes to consolidated financial statements. 38

证据 2：Table of Contents NETFLIX, INC. CONSOLIDATED STATEMENTS OF CASH FLOWS (in thousands) Year Ended December 31, 2015 2014 2013 Cash flows from operating activities: Net income $ 122,641 $ 266,799 $ 112,403 Adjustments to reconcile net income to net cash (used in) provided by operating activities: Additions to streaming content assets (5,771,652) (3,773,019) (3,030,701) Change in streaming content liabilities 1,162,413 593,125 673,785 Amortization of streaming content assets 3,405,382 2,656,279 2,121,981 Amortization of DVD content assets 79,380 71,491 71,325 Depreciation and amortization of property, equipment and intangibles 62,283 54,028 48,374 Stock-based compensation expense 124,725 115,239 73,100 Excess tax benefits from stock-based compensation (80,471) (89,341) (81,663) Other non-cash items 31,628 15,282 5,332 Loss on extinguishment of debt 25,129 Deferred taxes (58,655) (30,063) (22,044) Changes in operating assets and liabilities: Other current assets 18,693 (9,198) 43,177 Accounts payable 51,615 83,812 18,374 Accrued expenses 48,810 55,636 1,941 Deferred revenue 72,135 58,819 46,295 Other non-current assets and liabilities (18,366) (52,406) (8,977) Net cash (used in) provided by operating activities (749,439) 16,483 97,831 Cash flows from investing activities: Acquisition of DVD content assets (77,958) (74,790) (65,927) Purchases of property and equipment (91,248) (69,726) (54,143) Other assets (1,912) 1,334 5,939 Purchases of short-term investments (371,915) (426,934) (550,264) Proceeds from sale of short-term investments 259,079 385,300 347,502 Proceeds from maturities of short-term investments 104,762 141,950 60,925 Net cash used in investing activities (179,192) (42,866) (255,968) Cash flows from financing activities: Proceeds from issuance of common stock 77,980 60,544 124,557 Proceeds from issuance of debt 1,500,000 400,000 500,000 Issuance costs (17,629) (7,080) (9,414) Redemption of debt (219,362) Excess tax benefits from stock-based compensation 80,471 89,341 81,663 Principal payments of lease financing obligations (545) (1,093) (1,180) Net cash provided by financing activities 1,640,277 541,712 476,264 Effect of exchange rate changes on cash and cash equivalents (15,924) (6,686) (3,453) Net increase in cash and cash equivalents 695,722 508,643 314,674 Cash and cash equivalents, beginning of year 1,113,608 604,965 290,291 Cash and cash equivalents, end of year $ 1,809,330 $ 1,113,608 $ 604,965 Supplemental disclosure: Income taxes paid $ 27,658 $ 50,573 $ 7,465 Interest paid 111,761 41,085 19,114 Investing activities included in liabilities 18,824 23,802 11,508 See accompanying notes to consolidated financial statements. 40

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03282

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Netflix；文档：NETFLIX_2017_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is Netflix's year end FY2017 total current liabilities (in USD millions)? Base your judgments on the information provided primarily in the balance sheet.
- 标准答案：$5466.00
- 答案依据：The metric total current liabilities was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total current liabilities.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Netflix, NETFLIX_2017_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents NETFLIX, INC. CONSOLIDATED BALANCE SHEETS (in thousands, except share and per share data) As of December 31, 2017 2016 Assets Current assets: Cash and cash equivalents $ 2,822,795 $ 1,467,576 Short-term investments 266,206 Current content assets, net 4,310,934 3,726,307 Other current assets 536,245 260,202 Total current assets 7,669,974 5,720,291 Non-current content assets, net 10,371,055 7,274,501 Property and equipment, net 319,404 250,395 Other non-current assets 652,309 341,423 Total assets $ 19,012,742 $ 13,586,610 Liabilities and Stockholders Equity Current liabilities: Current content liabilities $ 4,173,041 $ 3,632,711 Accounts payable 359,555 312,842 Accrued expenses 315,094 197,632 Deferred revenue 618,622 443,472 Total current liabilities 5,466,312 4,586,657 Non-current content liabilities 3,329,796 2,894,654 Long-term debt 6,499,432 3,364,311 Other non-current liabilities 135,246 61,188 Total liabilities 15,430,786 10,906,810 Commitments and contingencies (Note 5) Stockholders equity: Preferred stock, $0.001 par value; 10,000,000 shares authorized at December 31, 2017 and 2016; no shares issued and outstanding at December 31, 2017 and 2016 Common stock, $0.001 par value; 4,990,000,000 shares authorized at December 31, 2017 and December 31, 2016, respectively; 433,392,686 and 430,054,212 issued and outstanding at December 31, 2017 and December 31, 2016, respectively 1,871,396 1,599,762 Accumulated other comprehensive loss (20,557) (48,565) Retained earnings 1,731,117 1,128,603 Total stockholders equity 3,581,956 2,679,800 Total liabilities and stockholders equity $ 19,012,742 $ 13,586,610 See accompanying notes to consolidated financial statements. 43

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04302

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Nike；文档：NIKE_2018_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：We need to calculate a reasonable approximation (or exact number if possible) of a financial metric. Basing your judgment by information plainly provided in the statement of income, what is Nike's three year average of cost of goods sold as a % of revenue from FY2016 to FY2018? Answer in units of percents and round to one decimal place.
- 标准答案：55.1%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of sales.

Metric 2: Total revenue. This metric was located in the 10K as a single line item named: Revenues.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Nike, NIKE_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents NIKE, Inc. Consolidated Statements of Income Year Ended May 31, (In millions, except per share data) 2018 2017 2016 Revenues $ 36,397 $ 34,350 $ 32,376 Cost of sales 20,441 19,038 17,405 Gross profit 15,956 15,312 14,971 Demand creation expense 3,577 3,341 3,278 Operating overhead expense 7,934 7,222 7,191 Total selling and administrative expense 11,511 10,563 10,469 Interest expense (income), net 54 59 19 Other expense (income), net 66 (196) (140) Income before income taxes 4,325 4,886 4,623 Income tax expense 2,392 646 863 NET INCOME $ 1,933 $ 4,240 $ 3,760 Earnings per common share: Basic $ 1.19 $ 2.56 $ 2.21 Diluted $ 1.17 $ 2.51 $ 2.16 Dividends declared per common share $ 0.78 $ 0.70 $ 0.62 The accompanying Notes to the Consolidated Financial Statements are an integral part of this statement. 44

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03531

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Nike；文档：NIKE_2019_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：According to the details clearly outlined within the balance sheet, how much total current assets did Nike have at the end of FY2019? Answer in USD millions.
- 标准答案：$16525.00
- 答案依据：The metric total current assets was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Total current assets.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Nike, NIKE_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents NIKE, INC. CONSOLIDATED BALANCE SHEETS MAY 31, (Dollars in millions) 2019 2018 ASSETS Current assets: Cash and equivalents $ 4,466 $ 4,249 Short-term investments 197 996 Accounts receivable, net 4,272 3,498 Inventories 5,622 5,261 Prepaid expenses and other current assets 1,968 1,130 Total current assets 16,525 15,134 Property, plant and equipment, net 4,744 4,454 Identifiable intangible assets, net 283 285 Goodwill 154 154 Deferred income taxes and other assets 2,011 2,509 TOTAL ASSETS $ 23,717 $ 22,536 LIABILITIES AND SHAREHOLDERS' EQUITY Current liabilities: Current portion of long-term debt $ 6 $ 6 Notes payable 9 336 Accounts payable 2,612 2,279 Accrued liabilities 5,010 3,269 Income taxes payable 229 150 Total current liabilities 7,866 6,040 Long-term debt 3,464 3,468 Deferred income taxes and other liabilities 3,347 3,216 Commitments and contingencies (Note 18) Redeemable preferred stock Shareholders' equity: Common stock at stated value: Class A convertible 315 and 329 shares outstanding Class B 1,253 and 1,272 shares outstanding 3 3 Capital in excess of stated value 7,163 6,384 Accumulated other comprehensive income (loss) 231 (92) Retained earnings 1,643 3,517 Total shareholders' equity 9,040 9,812 TOTAL LIABILITIES AND SHAREHOLDERS' EQUITY $ 23,717 $ 22,536 The accompanying Notes to the Consolidated Financial Statements are an integral part of this statement. 52 NIKE, INC.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04080

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Nike；文档：NIKE_2021_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：When primarily referencing the income statement and the statement of financial position, what is the FY2021 inventory turnover ratio for Nike? Inventory turnover ratio is defined as: (FY2021 COGS) / (average inventory between FY2020 and FY2021). Round your answer to two decimal places.
- 标准答案：3.46
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of sales.

Metric 2: Inventories. This metric was located in the 10K as a single line item named: Inventories.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Nike, NIKE_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents NIKE, INC. CONSOLIDATED STATEMENTS OF INCOME YEAR ENDED MAY 31, (In millions, except per share data) 2021 2020 2019 Revenues $ 44,538 $ 37,403 $ 39,117 Cost of sales 24,576 21,162 21,643 Gross profit 19,962 16,241 17,474 Demand creation expense 3,114 3,592 3,753 Operating overhead expense 9,911 9,534 8,949 Total selling and administrative expense 13,025 13,126 12,702 Interest expense (income), net 262 89 49 Other (income) expense, net 14 139 (78) Income before income taxes 6,661 2,887 4,801 Income tax expense 934 348 772 NET INCOME $ 5,727 $ 2,539 $ 4,029 Earnings per common share: Basic $ 3.64 $ 1.63 $ 2.55 Diluted $ 3.56 $ 1.60 $ 2.49 Weighted average common shares outstanding: Basic 1,573.0 1,558.8 1,579.7 Diluted 1,609.4 1,591.6 1,618.4 The accompanying Notes to the Consolidated Financial Statements are an integral part of this statement. 2021 FORM 10-K 57

证据 2：Table of Contents NIKE, INC. CONSOLIDATED BALANCE SHEETS MAY 31, (In millions) 2021 2020 ASSETS Current assets: Cash and equivalents $ 9,889 $ 8,348 Short-term investments 3,587 439 Accounts receivable, net 4,463 2,749 Inventories 6,854 7,367 Prepaid expenses and other current assets 1,498 1,653 Total current assets 26,291 20,556 Property, plant and equipment, net 4,904 4,866 Operating lease right-of-use assets, net 3,113 3,097 Identifiable intangible assets, net 269 274 Goodwill 242 223 Deferred income taxes and other assets 2,921 2,326 TOTAL ASSETS $ 37,740 $ 31,342 LIABILITIES AND SHAREHOLDERS' EQUITY Current liabilities: Current portion of long-term debt $ $ 3 Notes payable 2 248 Accounts payable 2,836 2,248 Current portion of operating lease liabilities 467 445 Accrued liabilities 6,063 5,184 Income taxes payable 306 156 Total current liabilities 9,674 8,284 Long-term debt 9,413 9,406 Operating lease liabilities 2,931 2,913 Deferred income taxes and other liabilities 2,955 2,684 Commitments and contingencies (Note 18) Redeemable preferred stock Shareholders' equity: Common stock at stated value: Class A convertible 305 and 315 shares outstanding Class B 1,273 and 1,243 shares outstanding 3 3 Capital in excess of stated value 9,965 8,299 Accumulated other comprehensive income (loss) (380) (56) Retained earnings (deficit) 3,179 (191) Total shareholders' equity 12,767 8,055 TOTAL LIABILITIES AND SHAREHOLDERS' EQUITY $ 37,740 $ 31,342 The accompanying Notes to the Consolidated Financial Statements are an integral part of this statement. 2021 FORM 10-K 59

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01163

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Nike；文档：NIKE_2023_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning。
- 问题：Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Nike in FY2023?
- 标准答案：Among the three, cash flow from operations was the highest for Nike in FY2023.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Nike, NIKE_2023_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：NIKE, INC. CONSOLIDATED STATEMENTS OF CASH FLOWS YEAR ENDED MAY 31, (Dollars in millions) 2023 2022 2021 Cash provided (used) by operations: Net income $ 5,070 $ 6,046 $ 5,727 Adjustments to reconcile net income to net cash provided (used) by operations: Depreciation 703 717 744 Deferred income taxes (117) (650) (385) Stock-based compensation 755 638 611 Amortization, impairment and other 156 123 53 Net foreign currency adjustments (213) (26) (138) Changes in certain working capital components and other assets and liabilities: (Increase) decrease in accounts receivable 489 (504) (1,606) (Increase) decrease in inventories (133) (1,676) 507 (Increase) decrease in prepaid expenses, operating lease right-of-use assets and other current and non-current assets (644) (845) (182) Increase (decrease) in accounts payable, accrued liabilities, operating lease liabilities and other current and non-current liabilities (225) 1,365 1,326 Cash provided (used) by operations 5,841 5,188 6,657 Cash provided (used) by investing activities: Purchases of short-term investments (6,059) (12,913) (9,961) Maturities of short-term investments 3,356 8,199 4,236 Sales of short-term investments 4,184 3,967 2,449 Additions to property, plant and equipment (969) (758) (695) Other investing activities 52 (19) 171 Cash provided (used) by investing activities 564 (1,524) (3,800) Cash provided (used) by financing activities: Increase (decrease) in notes payable, net (4) 15 (52) Repayment of borrowings (500) (197) Proceeds from exercise of stock options and other stock issuances 651 1,151 1,172 Repurchase of common stock (5,480) (4,014) (608) Dividends common and preferred (2,012) (1,837) (1,638) Other financing activities (102) (151) (136) Cash provided (used) by financing activities (7,447) (4,836) (1,459) Effect of exchange rate changes on cash and equivalents (91) (143) 143 Net increase (decrease) in cash and equivalents (1,133) (1,315) 1,541 Cash and equivalents, beginning of year 8,574 9,889 8,348 CASH AND EQUIVALENTS, END OF YEAR $ 7,441 $ 8,574 $ 9,889

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00080

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Paypal；文档：PAYPAL_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Does Paypal have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- 标准答案：Yes. Paypal has a positive working capital of $ 1.6Bn as of FY2022 end.
- 答案依据：Accounts receivable, net+Loans and interest receivable, net of allowances +Funds receivable and customer accounts+Prepaid expenses and other current assets-Accounts payable-Funds payable and amounts due to customers-Accrued expenses and other current liabilities -Income taxes payable
963+7431+36357+1898-126-40107-4055-813

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Paypal, PAYPAL_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：PayPal Holdings, Inc. CONSOLIDATED BALANCE SHEETS As of December 31, 2022 2021 (In millions, except par value) ASSETS Current assets: Cash and cash equivalents $ 7,776 $ 5,197 Short-term investments 3,092 4,303 Accounts receivable, net 963 800 Loans and interest receivable, net of allowances of $598 and $491 as of December 31, 2022 and 2021, respectively 7,431 4,846 Funds receivable and customer accounts 36,357 36,141 Prepaid expenses and other current assets 1,898 1,287 Total current assets 57,517 52,574 Long-term investments 5,018 6,797 Property and equipment, net 1,730 1,909 Goodwill 11,209 11,454 Intangible assets, net 788 1,332 Other assets 2,455 1,737 Total assets $ 78,717 $ 75,803 LIABILITIES AND EQUITY Current liabilities: Accounts payable $ 126 $ 197 Funds payable and amounts due to customers 40,107 38,841 Accrued expenses and other current liabilities 4,055 3,755 Income taxes payable 813 236 Total current liabilities 45,101 43,029 Deferred tax liability and other long-term liabilities 2,925 2,998 Long-term debt 10,417 8,049 Total liabilities 58,443 54,076 Commitments and contingencies (Note 13) Equity: Common stock, $0.0001 par value; 4,000 shares authorized; 1,136 and 1,168 shares outstanding as of December 31, 2022 and 2021, respectively Preferred stock, $0.0001 par value; 100 shares authorized, unissued Treasury stock at cost, 173 and 132 shares as of December 31, 2022 and 2021, respectively (16,079) (11,880) Additional paid-in-capital 18,327 17,208 Retained earnings 18,954 16,535 Accumulated other comprehensive income (loss) (928) (136) Total equity 20,274 21,727 Total liabilities and equity $ 78,717 $ 75,803 The accompanying notes are an integral part of these consolidated financial statements. 6

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04980

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2021_10K。
- 问题类型：metrics-generated；推理类型：Information extraction。
- 问题：What is the FY2021 capital expenditure amount (in USD billions) for PepsiCo? Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the statement of cash flows.
- 标准答案：$4.60
- 答案依据：The metric capital expenditures was directly extracted from the company 10K. The line item name, as seen in the 10K, was: Capital spending.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2021_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Statement of Cash Flows PepsiCo, Inc. and Subsidiaries Fiscal years ended December 25, 2021, December 26, 2020 and December 28, 2019 (in millions) 2021 2020 2019 Operating Activities Net income $ 7,679 $ 7,175 $ 7,353 Depreciation and amortization 2,710 2,548 2,432 Operating lease right-of-use asset amortization 505 478 412 Share-based compensation expense 301 264 237 Restructuring and impairment charges 247 289 370 Cash payments for restructuring charges (256) (255) (350) Acquisition and divestiture-related charges (4) 255 55 Cash payments for acquisition and divestiture-related charges (176) (131) (10) Pension and retiree medical plan expenses 123 408 519 Pension and retiree medical plan contributions (785) (562) (716) Deferred income taxes and other tax charges and credits 298 361 453 Tax expense/(benefit) related to the TCJ Act 190 (8) Tax payments related to the TCJ Act (309) (78) (423) Change in assets and liabilities: Accounts and notes receivable (651) (420) (650) Inventories (582) (516) (190) Prepaid expenses and other current assets 159 26 (87) Accounts payable and other current liabilities 1,762 766 735 Income taxes payable 30 (159) (287) Other, net 375 164 (196) Net Cash Provided by Operating Activities 11,616 10,613 9,649 Investing Activities Capital spending (4,625) (4,240) (4,232) Sales of property, plant and equipment 166 55 170 Acquisitions, net of cash acquired, and investments in noncontrolled affiliates (61) (6,372) (2,717) Divestitures and sales of investments in noncontrolled affiliates 169 6 253 Short-term investments, by original maturity: More than three months - purchases (1,135) More than three months - maturities 1,135 16 More than three months - sales 62 Three months or less, net (58) 27 19 Other investing, net 5 40 (8) Net Cash Used for Investing Activities (3,269) (11,619) (6,437) (Continued on following page) 61

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01009

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What are the geographies that Pepsico primarily operates in as of FY2022?
- 标准答案：As of FY2022, Pepsico primarily operates in the following geographies: North America, Latin America, Europe, Africa, Middle East, South Asia, Asia Pacific, Australia, New Zealand and China.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Forward-Looking Statements This Annual Report on Form 10-K contains statements reflecting our views about our future performance that constitute forward-looking statements within the meaning of the Private Securities Litigation Reform Act of 1995 (Reform Act). Statements that constitute forward-looking statements within the meaning of the Reform Act are generally identified through the inclusion of words such as aim, anticipate, believe, drive, estimate, expect, expressed confidence, forecast, future, goal, guidance, intend, may, objective, outlook, plan, position, potential, project, seek, should, strategy, target, will or similar statements or variations of such words and other similar expressions. All statements addressing our future operating performance, and statements addressing events and developments that we expect or anticipate will occur in the future, are forward-looking statements within the meaning of the Reform Act. These forward-looking statements are based on currently available information, operating plans and projections about future events and trends. They inherently involve risks and uncertainties that could cause actual results to differ materially from those predicted in any such forward-looking statement. These risks and uncertainties include, but are not limited to, those described in Item 1A. Risk Factors and Item 7. Managements Discussion and Analysis of Financial Condition and Results of Operations Our Business Our Business Risks. Investors are cautioned not to place undue reliance on any such forward-looking statements, which speak only as of the date they are made. We undertake no obligation to update any forward-looking statement, whether as a result of new information, future events or otherwise. The discussion of risks in this report is by no means all-inclusive but is designed to highlight what we believe are important factors to consider when evaluating our future performance. PART I Item 1. Business. When used in this report, the terms we, us, our, PepsiCo and the Company mean PepsiCo, Inc. and its consolidated subsidiaries, collectively. Certain terms used in this Annual Report on Form 10-K are defined in the Glossary included in Item 7. of this report. Company Overview We were incorporated in Delaware in 1919 and reincorporated in North Carolina in 1986. We are a leading global beverage and convenient food company with a complementary portfolio of brands, including Lays, Doritos, Cheetos, Gatorade, Pepsi-Cola, Mountain Dew, Quaker and SodaStream. Through our operations, authorized bottlers, contract manufacturers and other third parties, we make, market, distribute and sell a wide variety of beverages and convenient foods, serving customers and consumers in more than 200 countries and territories. Our Operations We are organized into seven reportable segments (also referred to as divisions), as follows: 1) Frito-Lay North America (FLNA), which includes our branded convenient food businesses in the United States and Canada; 2) Quaker Foods North America (QFNA), which includes our branded convenient food businesses, such as cereal, rice, pasta and other branded food, in the United States and Canada; 3) PepsiCo Beverages North America (PBNA), which includes our beverage businesses in the United States and Canada; 4) Latin America (LatAm), which includes all of our beverage and convenient food businesses in Latin America; 5) Europe, which includes all of our beverage and convenient food businesses in Europe;

证据 2：6) Africa, Middle East and South Asia (AMESA), which includes all of our beverage and convenient food businesses in Africa, the Middle East and South Asia; and 7) Asia Pacific, Australia and New Zealand and China Region (APAC), which includes all of our beverage and convenient food businesses in Asia Pacific, Australia and New Zealand, and China region.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00735

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Has Pepsico reported any materially important ongoing legal battles from FY2022 and FY2021?
- 标准答案：No, Pepsico is not involved in material legal battles.
- 答案依据：Management believes the final outcome of legal proceedings will not have a material adverse outcome.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Item 3. Legal Proceedings. We and our subsidiaries are party to a variety of litigation, claims, legal or regulatory proceedings, inquiries and investigations. While the results of such litigation, claims, legal or regulatory proceedings, inquiries and investigations cannot be predicted with certainty, management believes that the final outcome of the foregoing will not have a material adverse effect on our financial condition, results of operations or cash flows. See also Item 1. Business Regulatory Matters and Item 1A. Risk Factors.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01328

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：What is the quantity of restructuring costs directly outlined in Pepsico's income statements for FY2022? If restructuring costs are not explicitly outlined then state 0.
- 标准答案：Pepsico's restructuring costs in FY2022 amounted to $411 million .
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Note 3 Restructuring and Impairment Charges 2019 Multi-Year Productivity Plan We publicly announced a multi-year productivity plan on February 15, 2019 (2019 Productivity Plan) that will leverage new technology and business models to further simplify, harmonize and automate processes; re-engineer our go-to-market and information systems, including deploying the right automation for each market; and simplify our organization and optimize our manufacturing and supply chain footprint. To build on the successful implementation of the 2019 Productivity Plan, in the fourth quarter of 2022, we expanded and extended the plan through the end of 2028 to take advantage of additional opportunities within the initiatives described above. As a result, we expect to incur pre-tax charges of approximately $3.65 billion, including cash expenditures of approximately $2.9 billion. These pre-tax charges are expected to consist of approximately 55% of severance and other employee-related costs, 10% for asset impairments (all non-cash) resulting from plant closures and related actions and 35% for other costs associated with the implementation of our initiatives. The total plan pre-tax charges are expected to be incurred by division approximately as follows: FLNA QFNA PBNA LatAm Europe AMESA APAC Corporate Expected pre-tax charges 15 % 1 % 25 % 10 % 25 % 5 % 4 % 15 % A summary of our 2019 Productivity Plan charges is as follows: 2022 2021 2020 Cost of sales $ 33 $ 29 $ 30 Selling, general and administrative expenses 347 208 239 Other pension and retiree medical benefits expense 31 10 20 Total restructuring and impairment charges $ 411 $ 247 $ 289

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03620

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2022 unadjusted EBITDA less capex for PepsiCo? Define unadjusted EBITDA as unadjusted operating income + depreciation and amortization [from cash flow statement]. Answer in USD millions. Respond to the question by assuming the perspective of an investment analyst who can only use the details shown within the statement of cash flows and the income statement.
- 标准答案：$9068.00
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization.

Metric 2: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating Profit.

Metric 3: Capital expenditures. This metric was located in the 10K as a single line item named: Capital spending.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Statement of Income PepsiCo, Inc. and Subsidiaries Fiscal years ended December 31, 2022, December 25, 2021 and December 26, 2020 (in millions except per share amounts) 2022 2021 2020 Net Revenue $ 86,392 $ 79,474 $ 70,372 Cost of sales 40,576 37,075 31,797 Gross profit 45,816 42,399 38,575 Selling, general and administrative expenses 34,459 31,237 28,453 Gain associated with the Juice Transaction (see Note 13) (3,321) Impairment of intangible assets (see Notes 1 and 4) 3,166 42 Operating Profit 11,512 11,162 10,080 Other pension and retiree medical benefits income 132 522 117 Net interest expense and other (939) (1,863) (1,128) Income before income taxes 10,705 9,821 9,069 Provision for income taxes 1,727 2,142 1,894 Net income 8,978 7,679 7,175 Less: Net income attributable to noncontrolling interests 68 61 55 Net Income Attributable to PepsiCo $ 8,910 $ 7,618 $ 7,120 Net Income Attributable to PepsiCo per Common Share Basic $ 6.45 $ 5.51 $ 5.14 Diluted $ 6.42 $ 5.49 $ 5.12 Weighted-average common shares outstanding Basic 1,380 1,382 1,385 Diluted 1,387 1,389 1,392 See accompanying notes to the consolidated financial statements. 60

证据 2：Table of Contents Consolidated Statement of Cash Flows PepsiCo, Inc. and Subsidiaries Fiscal years ended December 31, 2022, December 25, 2021 and December 26, 2020 (in millions) 2022 2021 2020 Operating Activities Net income $ 8,978 $ 7,679 $ 7,175 Depreciation and amortization 2,763 2,710 2,548 Gain associated with the Juice Transaction (3,321) Impairment and other charges 3,618 Operating lease right-of-use asset amortization 517 505 478 Share-based compensation expense 343 301 264 Restructuring and impairment charges 411 247 289 Cash payments for restructuring charges (224) (256) (255) Acquisition and divestiture-related charges 80 (4) 255 Cash payments for acquisition and divestiture-related charges (46) (176) (131) Pension and retiree medical plan expenses 419 123 408 Pension and retiree medical plan contributions (384) (785) (562) Deferred income taxes and other tax charges and credits (873) 298 361 Tax expense related to the TCJ Act 86 190 Tax payments related to the TCJ Act (309) (309) (78) Change in assets and liabilities: Accounts and notes receivable (1,763) (651) (420) Inventories (1,142) (582) (516) Prepaid expenses and other current assets 118 159 26 Accounts payable and other current liabilities 1,842 1,762 766 Income taxes payable 57 30 (159) Other, net (359) 375 164 Net Cash Provided by Operating Activities 10,811 11,616 10,613 Investing Activities Capital spending (5,207) (4,625) (4,240) Sales of property, plant and equipment 251 166 55 Acquisitions, net of cash acquired, investments in noncontrolled affiliates and purchases of intangible and other assets (873) (61) (6,372) Proceeds associated with the Juice Transaction 3,456 Other divestitures, sales of investments in noncontrolled affiliates and other assets 49 169 6 Short-term investments, by original maturity: More than three months - purchases (291) (1,135) More than three months - maturities 150 1,135 Three months or less, net 24 (58) 27 Other investing, net 11 5 40 Net Cash Used for Investing Activities (2,430) (3,269) (11,619) (Continued on following page) 62

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04481

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：PepsiCo；文档：PEPSICO_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2022 unadjusted EBITDA % margin for PepsiCo? Calculate unadjusted EBITDA using unadjusted operating income and D&A (from cash flow statement). Give a response to the question by relying on the details shown in the statement of cash flows and the P&L statement.
- 标准答案：16.5%
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Depreciation and amortization. This metric was located in the 10K as a single line item named: Depreciation and amortization.

Metric 2: Unadjusted operating income. This metric was located in the 10K as a single line item named: Operating Profit.

Metric 3: Total revenue. This metric was located in the 10K as a single line item named: Net Revenue.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, PepsiCo, PEPSICO_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Statement of Income PepsiCo, Inc. and Subsidiaries Fiscal years ended December 31, 2022, December 25, 2021 and December 26, 2020 (in millions except per share amounts) 2022 2021 2020 Net Revenue $ 86,392 $ 79,474 $ 70,372 Cost of sales 40,576 37,075 31,797 Gross profit 45,816 42,399 38,575 Selling, general and administrative expenses 34,459 31,237 28,453 Gain associated with the Juice Transaction (see Note 13) (3,321) Impairment of intangible assets (see Notes 1 and 4) 3,166 42 Operating Profit 11,512 11,162 10,080 Other pension and retiree medical benefits income 132 522 117 Net interest expense and other (939) (1,863) (1,128) Income before income taxes 10,705 9,821 9,069 Provision for income taxes 1,727 2,142 1,894 Net income 8,978 7,679 7,175 Less: Net income attributable to noncontrolling interests 68 61 55 Net Income Attributable to PepsiCo $ 8,910 $ 7,618 $ 7,120 Net Income Attributable to PepsiCo per Common Share Basic $ 6.45 $ 5.51 $ 5.14 Diluted $ 6.42 $ 5.49 $ 5.12 Weighted-average common shares outstanding Basic 1,380 1,382 1,385 Diluted 1,387 1,389 1,392 See accompanying notes to the consolidated financial statements. 60

证据 2：Table of Contents Consolidated Statement of Cash Flows PepsiCo, Inc. and Subsidiaries Fiscal years ended December 31, 2022, December 25, 2021 and December 26, 2020 (in millions) 2022 2021 2020 Operating Activities Net income $ 8,978 $ 7,679 $ 7,175 Depreciation and amortization 2,763 2,710 2,548 Gain associated with the Juice Transaction (3,321) Impairment and other charges 3,618 Operating lease right-of-use asset amortization 517 505 478 Share-based compensation expense 343 301 264 Restructuring and impairment charges 411 247 289 Cash payments for restructuring charges (224) (256) (255) Acquisition and divestiture-related charges 80 (4) 255 Cash payments for acquisition and divestiture-related charges (46) (176) (131) Pension and retiree medical plan expenses 419 123 408 Pension and retiree medical plan contributions (384) (785) (562) Deferred income taxes and other tax charges and credits (873) 298 361 Tax expense related to the TCJ Act 86 190 Tax payments related to the TCJ Act (309) (309) (78) Change in assets and liabilities: Accounts and notes receivable (1,763) (651) (420) Inventories (1,142) (582) (516) Prepaid expenses and other current assets 118 159 26 Accounts payable and other current liabilities 1,842 1,762 766 Income taxes payable 57 30 (159) Other, net (359) 375 164 Net Cash Provided by Operating Activities 10,811 11,616 10,613 Investing Activities Capital spending (5,207) (4,625) (4,240) Sales of property, plant and equipment 251 166 55 Acquisitions, net of cash acquired, investments in noncontrolled affiliates and purchases of intangible and other assets (873) (61) (6,372) Proceeds associated with the Juice Transaction 3,456 Other divestitures, sales of investments in noncontrolled affiliates and other assets 49 169 6 Short-term investments, by original maturity: More than three months - purchases (291) (1,135) More than three months - maturities 150 1,135 Three months or less, net 24 (58) 27 Other investing, net 11 5 40 Net Cash Used for Investing Activities (2,430) (3,269) (11,619) (Continued on following page) 62

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
