# FinanceBench 样本：financebench_id_05915

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：CVS Health；文档：CVSHEALTH_2018_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2018 fixed asset turnover ratio for CVS Health? Fixed asset turnover ratio is defined as: FY2018 revenue / (average PP&E between FY2017 and FY2018). Round your answer to two decimal places. Calculate what was asked by utilizing the line items clearly shown in the P&L statement and the balance sheet.
- 标准答案：17.98
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total revenue. This metric was located in the 10K as a single line item named: Total revenues.

Metric 2: Ppne, net. This metric was located in the 10K as a single line item named: Property and equipment, net.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, CVS Health, CVSHEALTH_2018_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：ConsolidatedStatementsofOperations FortheYearsEndedDecember31, In millions, except per share amounts 2018 2017 2016 Revenues: Products $ 183,910 $ 180,063 $ 173,377 Premiums 8,184 3,558 3,069 Services 1,825 1,144 1,080 Netinvestmentincome 660 21 20 Totalrevenues 194,579 184,786 177,546 Operatingcosts: Costofproductssold 156,447 153,448 146,533 Benefitcosts 6,594 2,810 2,179 Goodwillimpairments 6,149 181 Operatingexpenses 21,368 18,809 18,448 Totaloperatingcosts 190,558 175,248 167,160 Operatingincome 4,021 9,538 10,386 Interestexpense 2,619 1,062 1,078 Lossonearlyextinguishmentofdebt 643 Otherexpense(income) (4) 208 28 Incomebeforeincometaxprovision 1,406 8,268 8,637 Incometaxprovision 2,002 1,637 3,317 Income(loss)fromcontinuingoperations (596) 6,631 5,320 Lossfromdiscontinuedoperations,netoftax (8) (1) Netincome(loss) (596) 6,623 5,319 Net(income)lossattributabletononcontrollinginterests 2 (1) (2) Netincome(loss)attributabletoCVSHealth $ (594) $ 6,622 $ 5,317 Basicearnings(loss)pershare: Income(loss)fromcontinuingoperationsattributabletoCVSHealth $ (0.57) $ 6.48 $ 4.93 LossfromdiscontinuedoperationsattributabletoCVSHealth $ $ (0.01) $ Netincome(loss)attributabletoCVSHealth $ (0.57) $ 6.47 $ 4.93 Weightedaveragebasicsharesoutstanding 1,044 1,020 1,073 Dilutedearnings(loss)pershare: Income(loss)fromcontinuingoperationsattributabletoCVSHealth $ (0.57) $ 6.45 $ 4.91 LossfromdiscontinuedoperationsattributabletoCVSHealth $ $ (0.01) $ Netincome(loss)attributabletoCVSHealth $ (0.57) $ 6.44 $ 4.90 Weightedaveragedilutedsharesoutstanding 1,044 1,024 1,079 Dividendsdeclaredpershare $ 2.00 $ 2.00 $ 1.70 Seeaccompanyingnotestoconsolidatedfinancialstatements. Page38

证据 2：ConsolidatedBalanceSheets AtDecember31, In millions, except per share amounts 2018 2017 Assets: Cashandcashequivalents $ 4,059 $ 1,696 Investments 2,522 111 Accountsreceivable,net 17,631 13,181 Inventories 16,450 15,296 Othercurrentassets 4,581 945 Totalcurrentassets 45,243 31,229 Long-terminvestments 15,732 112 Propertyandequipment,net 11,349 10,292 Goodwill 78,678 38,451 Intangibleassets,net 36,524 13,630 Separateaccountsassets 3,884 Otherassets 5,046 1,417 Totalassets $ 196,456 $ 95,131 Liabilities: Accountspayable $ 8,925 $ 8,863 Pharmacyclaimsanddiscountspayable 12,302 10,355 Healthcarecostspayable 5,210 5 Policyholdersfunds 2,939 Accruedexpenses 10,711 6,581 Otherinsuranceliabilities 1,937 23 Short-termdebt 720 1,276 Currentportionoflong-termdebt 1,265 3,545 Totalcurrentliabilities 44,009 30,648 Long-termdebt 71,444 22,181 Deferredincometaxes 7,677 2,996 Separateaccountsliabilities 3,884 Otherlong-terminsuranceliabilities 8,119 334 Otherlong-termliabilities 2,780 1,277 Totalliabilities 137,913 57,436 Commitmentsandcontingencies(Note16) Shareholdersequity: CVSHealthshareholdersequity: Preferredstock,parvalue$0.01:0.1sharesauthorized;noneissuedoroutstanding Commonstock,parvalue$0.01:3,200sharesauthorized;1,720sharesissuedand1,295sharesoutstandingat December31,2018and1,712sharesissuedand1,014sharesoutstandingatDecember31,2017andcapital surplus 45,440 32,096 Treasurystock,atcost:425sharesatDecember31,2018and698sharesatDecember31,2017 (28,228) (37,796) Retainedearnings 40,911 43,556 Accumulatedothercomprehensiveincome(loss) 102 (165) TotalCVSHealthshareholdersequity 58,225 37,691 Noncontrollinginterests 318 4 Totalshareholdersequity 58,543 37,695 Totalliabilitiesandshareholdersequity $ 196,456 $ 95,131 Seeaccompanyingnotestoconsolidatedfinancialstatements. Page40

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00790

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：CVS Health；文档：CVSHEALTH_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning)。
- 问题：Is CVS Health a capital-intensive business based on FY2022 data?
- 标准答案：Yes, CVS Health requires an extensive asset base to operate, which is evident from its ROA of only 1.82% in 2022 and 3.39% in 2021, though it should be noted that a significant portion of this asset base is goodwill, and CVS's fixed assets/total assets ratio is on the lower side of 5.6%.
- 答案依据：Property and equipment, net/Total Assets
12873/228275

ROA=Net Income/Total Assets
4165/228275
7898/232999

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, CVS Health, CVSHEALTH_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Consolidated Statements of Operations For the Years Ended December 31, In millions, except per share amounts 2022 2021 2020 Revenues: Products $ 226,616 $ 203,738 $ 190,688 Premiums 85,330 76,132 69,364 Services 9,683 11,042 7,856 Net investment income 838 1,199 798 Total revenues 322,467 292,111 268,706 Operating costs: Cost of products sold 196,892 175,803 163,981 Benefit costs 71,281 64,260 55,679 Opioid litigation charges 5,803 Loss on assets held for sale 2,533 Store impairments 1,358 Goodwill impairment 431 Operating expenses 38,212 37,066 35,135 Total operating costs 314,721 278,918 254,795 Operating income 7,746 13,193 13,911 Interest expense 2,287 2,503 2,907 Loss on early extinguishment of debt 452 1,440 Other income (169) (182) (206) Income before income tax provision 5,628 10,420 9,770 Income tax provision 1,463 2,522 2,569 Income from continuing operations 4,165 7,898 7,201 Loss from discontinued operations, net of tax (9) Net income 4,165 7,898 7,192

证据 2：Consolidated Balance Sheets At December 31, In millions, except per share amounts 2022 2021 Assets: Cash and cash equivalents $ 12,945 $ 9,408 Investments 2,778 3,117 Accounts receivable, net 27,276 24,431 Inventories 19,090 17,760 Assets held for sale 908 Other current assets 2,685 5,292 Total current assets 65,682 60,008 Long-term investments 21,096 23,025 Property and equipment, net 12,873 12,896 Operating lease right-of-use assets 17,872 19,122 Goodwill 78,150 79,121 Intangible assets, net 24,754 29,026 Separate accounts assets 3,228 5,087 Other assets 4,620 4,714 Total assets $ 228,275 $ 232,999

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01107

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：CVS Health；文档：CVSHEALTH_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020?
- 标准答案：Yes, CVS Health has been involved in multiple ongoing legal battles. Some notable legal dispute areas for CVS are: (1) usual and customary pricing litigation: where it's claimed that CVSâs retail pharmacies overcharged for prescription drugs; (2) PBM litigation and investigations: where it's claimed that that rebate agreements between the drug manufacturers and PBMs caused inflated prices for certain drug products; and (3) controlled substances litigation: legal matters around opioids for which CVS has agreed to pay up to $4.3 billion to claimants in remediation and $625 million to attorneys and fees
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, CVS Health, CVSHEALTH_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Usual and Customary Pricing Litigation The Company and certain current and former directors and officers are named as a defendant in a number of lawsuits that allege that the Companys retail pharmacies overcharged for prescription drugs by not submitting the correct usual and customary price during the claims adjudication process.

证据 2：The Company is facing multiple lawsuits, including by state Attorneys General, governmental subdivisions and several putative class actions, regarding drug pricing and its rebate arrangements with drug manufacturers. These complaints, brought by a number of different types of plaintiffs under a variety of legal theories, generally allege that rebate agreements between the drug manufacturers and PBMs caused inflated prices for certain drug products.

证据 3：In December 2022, the Company agreed to a formal settlement agreement, the financial amounts of which were agreed to in principle in October 2022, with a leadership group of a number of state Attorneys General and the Plaintiffs Executive Committee (PEC). The agreement would resolve substantially all opioid claims against Company entities by states and political subdivisions, but not private plaintiffs. The maximum amount payable by the Company under the settlement would be approximately $4.3 billion in opioid remediation and $625 million in attorneys fees and costs and additional remediation. The amounts would be payable over 10 years, beginning in 2023.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01244

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：CVS Health；文档：CVSHEALTH_2022_10K。
- 问题类型：domain-relevant；推理类型：Information extraction。
- 问题：Has CVS Health paid dividends to common shareholders in Q2 of FY2022?
- 标准答案：Yes, CVS paid a $ 0.55 dividend per share every quarter in FY2022
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, CVS Health, CVSHEALTH_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Dividends During 2022, 2021 and 2020, the quarterly cash dividend was $0.55, $0.50 and $0.50 per share, respectively.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00839

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Foot Locker；文档：FOOTLOCKER_2022_8K_dated_2022-08-19。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Does Foot Locker's new CEO have previous CEO experience in a similar company to Footlocker?
- 标准答案：Yes. She was previous CEO of Ulta Beauty which means she had to manage a large retail company that has brick and mortar + online business. So yes she was a CEO in a similar company to Foot Locker before this.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Foot Locker, FOOTLOCKER_2022_8K_dated_2022-08-19, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：On August 19, 2022, Foot Locker, Inc. (the Company), issued a press release announcing that, as part of a planned succession process, Richard A. Johnson will step down as President and Chief Executive Officer of the Company, effective September 1, 2022. Mary N. Dillon, 61, former Executive Chair and Chief Executive Officer of Ulta Beauty, Inc., has been appointed President and Chief Executive Officer and a member of the Companys Board of Directors (the Board) and the Executive Committee of the Board, each effective September 1, 2022. A copy of the press release is furnished as Exhibit 99.1, which is incorporated herein by reference.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00822

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Foot Locker；文档：FOOTLOCKER_2022_8K_dated-2022-05-20。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Were there any board member nominees who had substantially more votes against joining than the other nominees?
- 标准答案：Yes, his name is Richard A. Johnson
- 答案依据：Richard A. Johnson had roughly 16.1 million votes against him joining whereas the maximum votes against joining among all other candidates was roughly 6.1 million.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Foot Locker, FOOTLOCKER_2022_8K_dated-2022-05-20, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Proposal 1. With respect to the proposal to elect ten nominees to the Board of Directors (the Board), each for a one-year term expiring at the annual meeting of shareholders to be held in 2023, the votes were cast for the proposal as set forth below: Name Votes For Votes Against Abstentions Broker Non-Votes Virginia C. Drosos 59,657,810 294,935 10,714,238 6,884,223 Alan D. Feldman 54,760,830 5,184,437 10,721,716 6,884,223 Richard A. Johnson 54,484,293 16,105,005 77,685 6,884,223 Guillermo G. Marmol 54,193,921 5,753,395 10,719,667 6,884,223 Darlene Nicosia 55,123,930 4,827,808 10,715,245 6,884,223 Steven Oakland 55,421,657 4,524,393 10,720,933 6,884,223 Ulice Payne, Jr. 54,993,396 4,950,917 10,722,670 6,884,223 Kimberly Underhill 55,046,260 4,906,500 10,714,223 6,884,223 Tristan Walker 55,528,794 4,419,340 10,718,849 6,884,223 Dona D. Young 53,876,257 6,074,467 10,716,259 6,884,223 Based on the votes set forth above, each of the ten nominees to the Board was duly elected.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04103

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：General Mills；文档：GENERALMILLS_2019_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is the FY2019 cash conversion cycle (CCC) for General Mills? CCC is defined as: DIO + DSO - DPO. DIO is defined as: 365 * (average inventory between FY2018 and FY2019) / (FY2019 COGS). DSO is defined as: 365 * (average accounts receivable between FY2018 and FY2019) / (FY2019 Revenue). DPO is defined as: 365 * (average accounts payable between FY2018 and FY2019) / (FY2019 COGS + change in inventory between FY2018 and FY2019). Round your answer to two decimal places. Address the question by using the line items and information shown within the income statement and the balance sheet.
- 标准答案：-3.7
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Accounts payable. This metric was located in the 10K as a single line item named: Accounts payable.

Metric 2: Accounts receivable, net. This metric was located in the 10K as a single line item named: Receivables.

Metric 3: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of sales.

Metric 4: Total revenue. This metric was located in the 10K as a single line item named: Net sales.

Metric 5: Inventories. This metric was located in the 10K as a single line item named: Inventories.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, General Mills, GENERALMILLS_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Table of Contents Consolidated Statements of Earnings GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions, Except per Share Data) Fiscal Year 2019 2018 2017 Net sales $ 16,865.2 $ 15,740.4 $ 15,619.8 Cost of sales 11,108.4 10,304.8 10,052.0 Selling, general, and administrative expenses 2,935.8 2,850.1 2,888.8 Divestitures loss 30.0 - 6.5 Restructuring, impairment, and other exit costs 275.1 165.6 180.4 Operating profit 2,515.9 2,419.9 2,492.1 Benefit plan non-service income (87.9) (89.4) (74.3) Interest, net 521.8 373.7 295.1 Earnings before income taxes and after-tax earnings from joint ventures 2,082.0 2,135.6 2,271.3 Income taxes 367.8 57.3 655.2 After-tax earnings from joint ventures 72.0 84.7 85.0 Net earnings, including earnings attributable to redeemable and noncontrolling interests 1,786.2 2,163.0 1,701.1 Net earnings attributable to redeemable and noncontrolling interests 33.5 32.0 43.6 Net earnings attributable to General Mills $ 1,752.7 $ 2,131.0 $ 1,657.5 Earnings per share - basic $ 2.92 $ 3.69 $ 2.82 Earnings per share - diluted $ 2.90 $ 3.64 $ 2.77 Dividends per share $ 1.96 $ 1.96 $ 1.92 See accompanying notes to consolidated financial statements. 53

证据 2：Table of Contents Consolidated Balance Sheets GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions, Except Par Value) May 26, 2019 May 27, 2018 ASSETS Current assets: Cash and cash equivalents $ 450.0 $ 399.0 Receivables 1,679.7 1,684.2 Inventories 1,559.3 1,642.2 Prepaid expenses and other current assets 497.5 398.3 Total current assets 4,186.5 4,123.7 Land, buildings, and equipment 3,787.2 4,047.2 Goodwill 13,995.8 14,065.0 Other intangible assets 7,166.8 7,445.1 Other assets 974.9 943.0 Total assets $ 30,111.2 $ 30,624.0 LIABILITIES AND EQUITY Current liabilities: Accounts payable $ 2,854.1 $ 2,746.2 Current portion of long-term debt 1,396.5 1,600.1 Notes payable 1,468.7 1,549.8 Other current liabilities 1,367.8 1,445.8 Total current liabilities 7,087.1 7,341.9 Long-term debt 11,624.8 12,668.7 Deferred income taxes 2,031.0 2,003.8 Other liabilities 1,448.9 1,341.0 Total liabilities 22,191.8 23,355.4 Redeemable interest 551.7 776.2 Stockholders equity: Common stock, 754.6 shares issued, $0.10 par value 75.5 75.5 Additional paid-in capital 1,386.7 1,202.5 Retained earnings 14,996.7 14,459.6 Common stock in treasury, at cost, shares of 152.7 and 161.5 (6,779.0) (7,167.5) Accumulated other comprehensive loss (2,625.4) (2,429.0) Total stockholders equity 7,054.5 6,141.1 Noncontrolling interests 313.2 351.3 Total equity 7,367.7 6,492.4 Total liabilities and equity $ 30,111.2 $ 30,624.0 See accompanying notes to consolidated financial statements. 55

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_03471

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：General Mills；文档：GENERALMILLS_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：By drawing conclusions from the information stated only in the statement of financial position, what is General Mills's FY2020 working capital ratio? Define working capital ratio as total current assets divided by total current liabilities. Round your answer to two decimal places.
- 标准答案：0.68
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total current liabilities. This metric was located in the 10K as a single line item named: Total current liabilities.

Metric 2: Total current assets. This metric was located in the 10K as a single line item named: Total current assets.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, General Mills, GENERALMILLS_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：50 Consolidated Balance Sheets GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions, Except Par Value) May 31, 2020 May 26, 2019 ASSETS Current assets: Cash and cash equivalents $ 1,677.8 $ 450.0 Receivables 1,615.1 1,679.7 Inventories 1,426.3 1,559.3 Prepaid expenses and other current assets 402.1 497.5 Total current assets 5,121.3 4,186.5 Land, buildings, and equipment 3,580.6 3,787.2 Goodwill 13,923.2 13,995.8 Other intangible assets 7,095.8 7,166.8 Other assets 1,085.8 974.9 Total assets $ 30,806.7 $ 30,111.2 LIABILITIES AND EQUITY Current liabilities: Accounts payable $ 3,247.7 $ 2,854.1 Current portion of long-term debt 2,331.5 1,396.5 Notes payable 279.0 1,468.7 Other current liabilities 1,633.3 1,367.8 Total current liabilities 7,491.5 7,087.1 Long-term debt 10,929.0 11,624.8 Deferred income taxes 1,947.1 2,031.0 Other liabilities 1,545.0 1,448.9 Total liabilities 21,912.6 22,191.8 Redeemable interest 544.6 551.7 Stockholders' equity: Common stock, 754.6 shares issued, $0.10 par value 75.5 75.5 Additional paid-in capital 1,348.6 1,386.7 Retained earnings 15,982.1 14,996.7 Common stock in treasury, at cost, shares of 144.8 and 152.7 (6,433.3) (6,779.0) Accumulated other comprehensive loss (2,914.4) (2,625.4) Total stockholders' equity 8,058.5 7,054.5 Noncontrolling interests 291.0 313.2 Total equity 8,349.5 7,367.7 Total liabilities and equity $ 30,806.7 $ 30,111.2 See accompanying notes to consolidated financial statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_04854

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：General Mills；文档：GENERALMILLS_2020_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：According to the information provided in the statement of cash flows, what is the FY2020 free cash flow (FCF) for General Mills? FCF here is defined as: (cash from operations - capex). Answer in USD millions.
- 标准答案：$3215.00
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cash from operations. This metric was located in the 10K as a single line item named: Net cash provided by operating activities.

Metric 2: Capital expenditures. This metric was located in the 10K as a single line item named: Purchases of land, buildings, and equipment.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, General Mills, GENERALMILLS_2020_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：52 Consolidated Statements of Cash Flows GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions) Fiscal Year 2020 2019 2018 Cash Flows - Operating Activities Net earnings, including earnings attributable to redeemable and noncontrolling interests $ 2,210.8 $ 1,786.2 $ 2,163.0 Adjustments to reconcile net earnings to net cash provided by operating activities: Depreciation and amortization 594.7 620.1 618.8 After-tax earnings from joint ventures (91.1) (72.0) (84.7) Distributions of earnings from joint ventures 76.5 86.7 113.2 Stock-based compensation 94.9 84.9 77.0 Deferred income taxes (29.6) 93.5 (504.3) Pension and other postretirement benefit plan contributions (31.1) (28.8) (31.8) Pension and other postretirement benefit plan costs (32.3) 6.1 4.6 Divestitures loss - 30.0 - Restructuring, impairment, and other exit costs 43.6 235.7 126.0 Changes in current assets and liabilities, excluding the effects of acquisitions and divestitures 793.9 (7.5) 542.1 Other, net 45.9 (27.9) (182.9) Net cash provided by operating activities 3,676.2 2,807.0 2,841.0 Cash Flows - Investing Activities Purchases of land, buildings, and equipment (460.8) (537.6) (622.7) Acquisition, net of cash acquired - - (8,035.8) Investments in affiliates, net (48.0) 0.1 (17.3) Proceeds from disposal of land, buildings, and equipment 1.7 14.3 1.4 Proceeds from divestitures - 26.4 - Other, net 20.9 (59.7) (11.0) Net cash used by investing activities (486.2) (556.5) (8,685.4) Cash Flows - Financing Activities Change in notes payable (1,158.6) (66.3) 327.5 Issuance of long-term debt 1,638.1 339.1 6,550.0 Payment of long-term debt (1,396.7) (1,493.8) (600.1) Proceeds from common stock issued on exercised options 263.4 241.4 99.3 Proceeds from common stock issued - - 969.9 Purchases of common stock for treasury (3.4) (1.1) (601.6) Dividends paid (1,195.8) (1,181.7) (1,139.7) Investments in redeemable interest - 55.7 - Distributions to noncontrolling and redeemable interest holders (72.5) (38.5) (51.8) Other, net (16.0) (31.2) (108.0) Net cash (used) provided by financing activities (1,941.5) (2,176.4) 5,445.5 Effect of exchange rate changes on cash and cash equivalents (20.7) (23.1) 31.8 Increase (decrease) in cash and cash equivalents 1,227.8 51.0 (367.1) Cash and cash equivalents - beginning of year 450.0 399.0 766.1 Cash and cash equivalents - end of year $ 1,677.8 $ 450.0 $ 399.0 Cash flow from changes in current assets and liabilities, excluding the effects of acquisitions and divestitures: Receivables $ 37.9 $ (42.7) $ (122.7) Inventories 103.1 53.7 15.6 Prepaid expenses and other current assets 94.2 (114.3) (10.7) Accounts payable 392.5 162.4 575.3 Other current liabilities 166.2 (66.6) 84.6 Changes in current assets and liabilities $ 793.9 $ (7.5) $ 542.1 See accompanying notes to consolidated financial statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_10136

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：General Mills；文档：GENERALMILLS_2022_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：We want to calculate a financial metric. Please help us compute it by basing your answers off of the cash flow statement and the income statement. Here's the question: what is the FY2022 retention ratio (using total cash dividends paid and net income attributable to shareholders) for General Mills? Round answer to two decimal places.
- 标准答案：0.54
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Total cash dividends paid out. This metric was located in the 10K as a single line item named: Dividends paid.

Metric 2: Net income. This metric was located in the 10K as a single line item named: Net earnings attributable to General Mills.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, General Mills, GENERALMILLS_2022_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：45 Consolidated Statements of Earnings GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions, Except per Share Data) Fiscal Year 2022 2021 2020 Net sales $ 18,992.8 $ 18,127.0 $ 17,626.6 Cost of sales 12,590.6 11,678.7 11,496.7 Selling, general, and administrative expenses 3,147.0 3,079.6 3,151.6 Divestitures (gain) loss (194.1) 53.5 - Restructuring, impairment, and other exit (recoveries) costs (26.5) 170.4 24.4 Operating profit 3,475.8 3,144.8 2,953.9 Benefit plan non-service income (113.4) (132.9) (112.8) Interest, net 379.6 420.3 466.5 Earnings before income taxes and after-tax earnings from joint ventures 3,209.6 2,857.4 2,600.2 Income taxes 586.3 629.1 480.5 After-tax earnings from joint ventures 111.7 117.7 91.1 Net earnings, including earnings attributable to redeemable and noncontrolling interests 2,735.0 2,346.0 2,210.8 Net earnings attributable to redeemable and noncontrolling interests 27.7 6.2 29.6 Net earnings attributable to General Mills $ 2,707.3 $ 2,339.8 $ 2,181.2 Earnings per share basic $ 4.46 $ 3.81 $ 3.59 Earnings per share diluted $ 4.42 $ 3.78 $ 3.56 Dividends per share $ 2.04 $ 2.02 $ 1.96 See accompanying notes to consolidated financial statements.

证据 2：49 Consolidated Statements of Cash Flows GENERAL MILLS, INC. AND SUBSIDIARIES (In Millions) Fiscal Year 2022 2021 2020 Cash Flows - Operating Activities Net earnings, including earnings attributable to redeemable and noncontrolling interests $ 2,735.0 $ 2,346.0 $ 2,210.8 Adjustments to reconcile net earnings to net cash provided by operating activities: Depreciation and amortization 570.3 601.3 594.7 After-tax earnings from joint ventures (111.7) (117.7) (91.1) Distributions of earnings from joint ventures 107.5 95.2 76.5 Stock-based compensation 98.7 89.9 94.9 Deferred income taxes 62.2 118.8 (29.6) Pension and other postretirement benefit plan contributions (31.3) (33.4) (31.1) Pension and other postretirement benefit plan costs (30.1) (33.6) (32.3) Divestitures (gain) loss (194.1) 53.5 - Restructuring, impairment, and other exit (recoveries) costs (117.1) 150.9 43.6 Changes in current assets and liabilities, excluding the effects of acquisition and divestitures 277.4 (155.9) 793.9 Other, net (50.7) (131.8) 45.9 Net cash provided by operating activities 3,316.1 2,983.2 3,676.2 Cash Flows - Investing Activities Purchases of land, buildings, and equipment (568.7) (530.8) (460.8) Acquisition (1,201.3) - - Investments in affiliates, net 15.4 15.5 (48.0) Proceeds from disposal of land, buildings, and equipment 3.3 2.7 1.7 Proceeds from divestitures, net of cash divested 74.1 2.9 - Other, net (13.5) (3.1) 20.9 Net cash used by investing activities (1,690.7) (512.8) (486.2) Cash Flows - Financing Activities Change in notes payable 551.4 71.7 (1,158.6) Issuance of long-term debt 2,203.7 1,576.5 1,638.1 Payment of long-term debt (3,140.9) (2,609.0) (1,396.7) Debt exchange participation incentive cash payment - (201.4) - Proceeds from common stock issued on exercised options 161.7 74.3 263.4 Purchases of common stock for treasury (876.8) (301.4) (3.4) Dividends paid (1,244.5) (1,246.4) (1,195.8) Distributions to noncontrolling and redeemable interest holders (129.8) (48.9) (72.5) Other, net (28.0) (30.9) (16.0) Net cash used by financing activities (2,503.2) (2,715.5) (1,941.5) Effect of exchange rate changes on cash and cash equivalents (58.0) 72.5 (20.7) (Decrease) increase in cash and cash equivalents (935.8) (172.6) 1,227.8 Cash and cash equivalents - beginning of year 1,505.2 1,677.8 450.0 Cash and cash equivalents - end of year $ 569.4 $ 1,505.2 $ 1,677.8 Cash flow from changes in current assets and liabilities, excluding the effects of acquisition and divestitures: Receivables $ (166.3) $ 27.9 $ 37.9 Inventories (85.8) (354.7) 103.1 Prepaid expenses and other current assets (35.3) (42.7) 94.2 Accounts payable 456.7 343.1 392.5 Other current liabilities 108.1 (129.5) 166.2 Changes in current assets and liabilities $ 277.4 $ (155.9) $ 793.9 See accompanying notes to consolidated financial statements.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00956

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning)。
- 问题：Are JnJ's FY2022 financials that of a high growth company?
- 标准答案：No, JnJ's FY2022 financials are not of a high growth company as sales grew by 1.3% in FY2022.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Results of Operations Analysis of Consolidated Sales For discussion on results of operations and financial condition pertaining to the fiscal years 2021 and 2020 see the Companys Annual Report on Form 10- K for the fiscal year ended January 2, 2022, Item 7. Management's Discussion and Analysis of Results of Operations and Financial Condition. In 2022, worldwide sales increased 1.3% to $94.9 billion as compared to an increase of 13.6% in 2021. These sales changes consisted of the following: Sales increase/(decrease) due to: 2022 2021 Volume 6.9 % 12.9 % Price (0.8) (0.7) Currency (4.8) 1.4 Total 1.3 % 13.6 %

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00669

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Numerical reasoning OR Logical reasoning。
- 问题：What drove gross margin change as of FY2022 for JnJ? If gross margin is not a useful metric for a company like this, then please state that and explain why.
- 标准答案：For FY22, JnJ had changes in gross margin due to: One-time COVID-19 vaccine manufacturing exit related costs, Currency impacts in the Pharmaceutical segment, Commodity inflation in the MedTech and Consumer Health segments, partially offset by Supply chain benefits in the Consumer Health segment.
- 答案依据：Gross margin change is equivalent to the increase in cost of products sold as a percent to sales.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Analysis of Consolidated Earnings Before Provision for Taxes on Income Consolidated earnings before provision for taxes on income was $21.7 billion and $22.8 billion for the years 2022 and 2021, respectively. As a percent to sales, consolidated earnings before provision for taxes on income was 22.9% and 24.3%, in 2022 and 2021, respectively. (Dollars in billions. Percentages in chart are as a percent to total sales) Cost of Products Sold and Selling, Marketing and Administrative Expenses: (Dollars in billions. Percentages in chart are as a percent to total sales) Cost of products sold increased as a percent to sales driven by: One-time COVID-19 vaccine manufacturing exit related costs Currency impacts in the Pharmaceutical segment Commodity inflation in the MedTech and Consumer Health segments partially offset by Supply chain benefits in the Consumer Health segment The intangible asset amortization expense included in cost of products sold was $4.3 billion and $4.7 billion for the fiscal years 2022 and 2021, respectively.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00711

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2022_10K。
- 问题类型：domain-relevant；推理类型：Numerical reasoning OR Logical reasoning。
- 问题：Roughly how many times has JnJ sold its inventory in FY2022? Calculate inventory turnover ratio for FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- 标准答案：JnJ sold its inventory 2.7 times in FY2022.
- 答案依据：Inventory turnover ratio = Cost of products sold/average inventories = 31,089/((12,483+10,387)/2) = 2.7

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：JOHNSON & JOHNSON AND SUBSIDIARIES CONSOLIDATED BALANCE SHEETS At January 1, 2023 and January 2, 2022 (Dollars in Millions Except Share and Per Share Amounts) (Note 1) 2022 2021 Assets Current assets Cash and cash equivalents (Notes 1 and 2) $ 14,127 14,487 Marketable securities (Notes 1 and 2) 9,392 17,121 Accounts receivable trade, less allowances for doubtful accounts $203 (2021, $230) 16,160 15,283 Inventories (Notes 1 and 3) 12,483 10,387

证据 2：JOHNSON & JOHNSON AND SUBSIDIARIES CONSOLIDATED STATEMENTS OF EARNINGS (Dollars and Shares in Millions Except Per Share Amounts) (Note 1) 2022 2021 2020 Sales to customers $ 94,943 93,775 82,584 Cost of products sold 31,089 29,855 28,427

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00651

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2022Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Is growth in JnJ's adjusted EPS expected to accelerate in FY2023?
- 标准答案：No, rate of growth in adjusted EPS is expected to decelerate slightly from 3.6% in FY2022 to 3.5% in FY2023.
- 答案依据：FY2023 adjusted EPS growth of 3.5% is slightly lower than FY2022 adjusted EPS growth of 3.6%.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2022Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：2022 Fourth-Quarter reported sales decline of 4.4% to $23.7 Billion primarily driven by unfavorable foreign exchange and reduced COVID-19 Vaccine sales vs. prior year. Operational growth excluding COVID-19 Vaccine of 4.6%* 2022 Fourth-Quarter earnings per share (EPS) of $1.33 decreasing 24.9% and adjusted EPS of $2.35 increasing by 10.3%* __________________________________________________________________________________________ 2022 Full-Year reported sales growth of 1.3% to $94.9 Billion primarily driven by strong commercial execution partially offset by unfavorable foreign exchange. Operational growth of 6.1%* 2022 Full-Year earnings per share (EPS) of $6.73 decreasing 13.8% and adjusted EPS of $10.15 increasing by 3.6%* __________________________________________________________________________________________ Company guides 2023 adjusted operational sales growth excluding COVID-19 Vaccine of 4.0%* and adjusted operational EPS of $10.50, reflecting growth of 3.5%*

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01484

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2022Q4_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：How did JnJ's US sales growth compare to international sales growth in FY2022?
- 标准答案：US sales increased 3.0% vs international sales decline of 0.6%.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2022Q4_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：REGIONAL SALES RESULTS Q4 % Change ($ in Millions) 2022 2021 Reported Operational1,2 Currency Adjusted Operational1,3 U.S. $12,516 $12,163 2.9% 2.9 - 2.7 International 11,190 12,641 (11.5) (1.1) (10.4) (1.0) Worldwide $23,706 $24,804 (4.4)% 0.9 (5.3) 0.8 Full Year % Change ($ in Millions) 2022 2021 Reported Operational1,2 Currency Adjusted Operational1,3 U.S. $48,580 $47,156 3.0% 3.0 - 3.0 International 46,363 46,619 (0.6)% 9.1 (9.7) 9.3 Worldwide $94,943 $93,775 1.3% 6.1 (4.8) 6.2

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01488

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2023_8K_dated-2023-08-30。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which business segment of JnJ will be treated as a discontinued operation from August 30, 2023 onward?
- 标准答案：The Consumer Health business segment will be treated as a discontinued operation from August 30, 2023 onward.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2023_8K_dated-2023-08-30, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Exhibit 99.1 Johnson & Johnson Announces Updated Financials and 2023 Guidance Following Completion of the Kenvue Separation Company expects increased 2023 Reported Sales Growth of 7.0% - 8.0%, Operational Sales Growth of 7.5% - 8.5%, and Adjusted Operational Sales Growth of 6.2% - 7.2%; Figures exclude the COVID-19 Vaccine Company expects 2023 Adjusted Reported Earnings Per Share (EPS) of $10.00 - $10.10, reflecting increased growth of 12.5% at the mid-point and Adjusted Operational EPS of $9.90 - $10.00, reflecting increased growth of 11.5% at the mid- point Company reduced outstanding share count by approximately 191 million; 2023 guidance reflects only a partial-year benefit of approximately 73.5 million shares or $0.28 benefit to EPS Company secured $13.2 billion in cash proceeds from the Kenvue debt offering and initial public offering and maintains 9.5% of equity stake in Kenvue Company maintains its quarterly dividend of $1.19 per share New Brunswick, N.J. (August 30, 2023) Johnson & Johnson (NYSE: JNJ) (the Company) today announced updates to its financials and 2023 guidance which reflect its operations as a company focused on transformational innovation in Pharmaceutical and MedTech. The Company has published a recorded webinar for investors to provide additional context behind the updated financials and 2023 guidance found in this release, which may be accessed by visiting the Investors section of the Company's website at webcasts & presentations. The completion of this transaction uniquely positions Johnson & Johnson as a Pharmaceutical and MedTech company focused on delivering transformative healthcare solutions to patients, said Joaquin Duato, Chairman of the Board and Chief Executive Officer. We are incredibly proud of the focus and dedication of our employees worldwide to achieve this milestone, which we are confident will unlock near- and long- term value for all of our stakeholders. As previously announced, the Company recently completed an exchange offer to finalize the separation of Kenvue Inc., formerly Johnson & Johnsons Consumer Health business. As a result of the completion of the exchange offer, Johnson & Johnson will now present its Consumer Health business financial results as discontinued operations, including a gain of approximately $20 billion in the third quarter of 2023

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01490

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2023_8K_dated-2023-08-30。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What is the amount of the gain accruing to JnJ as a result of the separation of its Consumer Health business segment, as of August 30, 2023?
- 标准答案：JnJ will make a gain of approximately $20 billion from the separation of its Consumer Health business segment.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2023_8K_dated-2023-08-30, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Exhibit 99.1 Johnson & Johnson Announces Updated Financials and 2023 Guidance Following Completion of the Kenvue Separation Company expects increased 2023 Reported Sales Growth of 7.0% - 8.0%, Operational Sales Growth of 7.5% - 8.5%, and Adjusted Operational Sales Growth of 6.2% - 7.2%; Figures exclude the COVID-19 Vaccine Company expects 2023 Adjusted Reported Earnings Per Share (EPS) of $10.00 - $10.10, reflecting increased growth of 12.5% at the mid-point and Adjusted Operational EPS of $9.90 - $10.00, reflecting increased growth of 11.5% at the mid- point Company reduced outstanding share count by approximately 191 million; 2023 guidance reflects only a partial-year benefit of approximately 73.5 million shares or $0.28 benefit to EPS Company secured $13.2 billion in cash proceeds from the Kenvue debt offering and initial public offering and maintains 9.5% of equity stake in Kenvue Company maintains its quarterly dividend of $1.19 per share New Brunswick, N.J. (August 30, 2023) Johnson & Johnson (NYSE: JNJ) (the Company) today announced updates to its financials and 2023 guidance which reflect its operations as a company focused on transformational innovation in Pharmaceutical and MedTech. The Company has published a recorded webinar for investors to provide additional context behind the updated financials and 2023 guidance found in this release, which may be accessed by visiting the Investors section of the Company's website at webcasts & presentations. The completion of this transaction uniquely positions Johnson & Johnson as a Pharmaceutical and MedTech company focused on delivering transformative healthcare solutions to patients, said Joaquin Duato, Chairman of the Board and Chief Executive Officer. We are incredibly proud of the focus and dedication of our employees worldwide to achieve this milestone, which we are confident will unlock near- and long- term value for all of our stakeholders. As previously announced, the Company recently completed an exchange offer to finalize the separation of Kenvue Inc., formerly Johnson & Johnsons Consumer Health business. As a result of the completion of the exchange offer, Johnson & Johnson will now present its Consumer Health business financial results as discontinued operations, including a gain of approximately $20 billion in the third quarter of 2023.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01491

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2023_8K_dated-2023-08-30。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：What is the amount of the cash proceeds that JnJ realised from the separation of Kenvue (formerly Consumer Health business segment), as of August 30, 2023?
- 标准答案：JnJ realised $13.2 billion in cash proceeds from the separation of Kenvue.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2023_8K_dated-2023-08-30, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Exhibit 99.1 Johnson & Johnson Announces Updated Financials and 2023 Guidance Following Completion of the Kenvue Separation Company expects increased 2023 Reported Sales Growth of 7.0% - 8.0%, Operational Sales Growth of 7.5% - 8.5%, and Adjusted Operational Sales Growth of 6.2% - 7.2%; Figures exclude the COVID-19 Vaccine Company expects 2023 Adjusted Reported Earnings Per Share (EPS) of $10.00 - $10.10, reflecting increased growth of 12.5% at the mid-point and Adjusted Operational EPS of $9.90 - $10.00, reflecting increased growth of 11.5% at the mid- point Company reduced outstanding share count by approximately 191 million; 2023 guidance reflects only a partial-year benefit of approximately 73.5 million shares or $0.28 benefit to EPS Company secured $13.2 billion in cash proceeds from the Kenvue debt offering and initial public offering and maintains 9.5% of equity stake in Kenvue Company maintains its quarterly dividend of $1.19 per share New Brunswick, N.J. (August 30, 2023) Johnson & Johnson (NYSE: JNJ) (the Company) today announced updates to its financials and 2023 guidance which reflect its operations as a company focused on transformational innovation in Pharmaceutical and MedTech. The Company has published a recorded webinar for investors to provide additional context behind the updated financials and 2023 guidance found in this release, which may be accessed by visiting the Investors section of the Company's website at webcasts & presentations. The completion of this transaction uniquely positions Johnson & Johnson as a Pharmaceutical and MedTech company focused on delivering transformative healthcare solutions to patients, said Joaquin Duato, Chairman of the Board and Chief Executive Officer. We are incredibly proud of the focus and dedication of our employees worldwide to achieve this milestone, which we are confident will unlock near- and long- term value for all of our stakeholders. As previously announced, the Company recently completed an exchange offer to finalize the separation of Kenvue Inc., formerly Johnson & Johnsons Consumer Health business. As a result of the completion of the exchange offer, Johnson & Johnson will now present its Consumer Health business financial results as discontinued operations, including a gain of approximately $20 billion in the third quarter of 2023.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_01487

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Johnson & Johnson；文档：JOHNSON_JOHNSON_2023Q2_EARNINGS。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Did JnJ's net earnings as a percent of sales increase in Q2 of FY2023 compared to Q2 of FY2022?
- 标准答案：Yes, net earnings as a percent of sales increased from 20% in Q2 of FY2022 to 20.1% in Q2 of FY2023.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Johnson & Johnson, JOHNSON_JOHNSON_2023Q2_EARNINGS, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Johnson & Johnson and Subsidiaries Condensed Consolidated Statement of Earnings (Unaudited; in Millions Except Per Share Figures) Percent Percent Percent Increase Amount to Sales Amount to Sales (Decrease) Sales to customers 25,530 $ 100.0 24,020 $ 100.0 6.3 Cost of products sold 8,212 32.2 7,919 33.0 3.7 Gross Profit 17,318 67.8 16,101 67.0 7.6 Selling, marketing and administrative expenses 6,665 26.1 6,226 25.9 7.1 Research and development expense 3,829 15.0 3,703 15.4 3.4 Interest (income) expense, net (23) (0.1) (26) (0.1) Other (income) expense, net* (60) (0.2) 273 1.1 Restructuring 145 0.5 85 0.4 Earnings before provision for taxes on income 6,762 26.5 5,840 24.3 15.8 Provision for taxes on income 1,618 6.4 1,026 4.3 57.7 Net earnings 5,144 $ 20.1 4,814 $ 20.0 6.9

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00299

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：JPMorgan；文档：JPMORGAN_2021Q1_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Which of JPM's business segments had the lowest net revenue in 2021 Q1?
- 标准答案：Corporate. Its net revenue was -$473 million.
- 答案依据：14,605 > 12,517 > 4,077 > 2,393 > -473

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, JPMorgan, JPMORGAN_2021Q1_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Segment results managed basis The following tables summarize the Firms results by segment for the periods indicated. Three months ended March 31, Consumer & Community Banking Corporate & Investment Bank Commercial Banking (in millions, except ratios) 2021 2020 Change 2021 2020 Change 2021 2020 Change Total net revenue $ 12,517 $ 13,287 (6) % $ 14,605 $ 10,003 46 % $ 2,393 $ 2,165 11 % Total noninterest expense 7,202 7,269 (1) 7,104 5,955 19 969 986 (2) Pre-provision profit/(loss) 5,315 6,018 (12) 7,501 4,048 85 1,424 1,179 21 Provision for credit losses (3,602) 5,772 NM (331) 1,401 NM (118) 1,010 NM Net income/(loss) 6,728 197 NM 5,740 1,985 189 1,168 139 NM Return on equity (ROE) 54 % 1 % 27 % 9 % 19 % 2 % Three months ended March 31, Asset & Wealth Management Corporate Total (in millions, except ratios) 2021 2020 Change 2021 2020 Change 2021 2020 Change Total net revenue $ 4,077 $ 3,389 20 % $ (473) $ 166 NM $ 33,119 $ 29,010 14 % Total noninterest expense 2,574 2,435 6 876 146 500 18,725 16,791 12 Pre-provision profit/(loss) 1,503 954 58 (1,349) 20 NM 14,394 12,219 18 Provision for credit losses (121) 94 NM 16 8 100 (4,156) 8,285 NM Net income/(loss) 1,244 669 86 (580) (125) (364) 14,300 2,865 399 ROE 35 % 25 % NM NM 23 % 4 %

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02119

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：JPMorgan；文档：JPMORGAN_2021Q1_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：If JPM went bankrupted by the end by 2021 Q1 and liquidated all of its assets to pay its shareholders, how much could each shareholder get?
- 标准答案：They could receive $66.56 per share.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, JPMorgan, JPMORGAN_2021Q1_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The Firm grew TBVPS, ending the first quarter of 2021 at $66.56, up 10% versus the prior year.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00206

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：JPMorgan；文档：JPMORGAN_2022_10K。
- 问题类型：domain-relevant；推理类型：Logical reasoning (based on numerical reasoning) OR Logical reasoning。
- 问题：Are JPM's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why.
- 标准答案：Since JPM is a financial institution, gross margin is not a relevant metric.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, JPMorgan, JPMORGAN_2022_10K, domain-relevant, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Overview JPMorgan Chase & Co. (JPMorgan Chase or the Firm, NYSE: JPM), a financial holding company incorporated under Delaware law in 1968, is a leading financial services firm based in the United States of America (U.S.), with operations worldwide. JPMorgan Chase had $3.7 trillion in assets and $292.3 billion in stockholders equity as of December 31, 2022. The Firm is a leader in investment banking, financial services for consumers and small businesses, commercial banking, financial transaction processing and asset management. Under the J.P. Morgan and Chase brands, the Firm serves millions of customers, predominantly in the U.S., and many of the worlds most prominent corporate, institutional and government clients globally.

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_00394

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：JPMorgan；文档：JPMORGAN_2022Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：In 2022 Q2, which of JPM's business segments had the highest net income?
- 标准答案：Corporate & Investment Bank. Its net income was $3725 million.
- 答案依据：3725 > 3100 > 1004 > 994 > -174

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, JPMorgan, JPMORGAN_2022Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Segment results managed basis The following tables summarize the Firms results by segment for the periods indicated. Three months ended June 30, Consumer & Community Banking Corporate & Investment Bank Commercial Banking (in millions, except ratios) 2022 2021 Change 2022 2021 Change 2022 2021 Change Total net revenue $ 12,614 $ 12,760 (1) % $ 11,947 $ 13,214 (10) % $ 2,683 $ 2,483 8 % Total noninterest expense 7,723 7,062 9 6,745 6,523 3 1,156 981 18 Pre-provision profit/(loss) 4,891 5,698 (14) 5,202 6,691 (22) 1,527 1,502 2 Provision for credit losses 761 (1,868) NM 59 (79) NM 209 (377) NM Net income/(loss) 3,100 5,645 (a) (45) 3,725 5,020 (a) (26) 994 1,422 (a) (30) Return on equity (ROE) 24 % 44 % 14 % 23 % 15 % 23 % Three months ended June 30, Asset & Wealth Management Corporate Total (in millions, except ratios) 2022 2021 Change 2022 2021 Change 2022 2021 Change Total net revenue $ 4,306 $ 4,107 5 % $ 80 $ (1,169) NM $ 31,630 $ 31,395 1 % Total noninterest expense 2,919 2,586 13 206 515 (60) 18,749 17,667 6 Pre-provision profit/(loss) 1,387 1,521 (9) (126) (1,684) 93 12,881 13,728 (6) Provision for credit losses 44 (10) NM 28 49 (43) 1,101 (2,285) NM Net income/(loss) 1,004 1,156 (a) (13) (174) (1,295) (a) 87 8,649 11,948 (28) ROE 23 % 32 % NM NM 13 % 18 %

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_02049

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：JPMorgan；文档：JPMORGAN_2023Q2_10Q。
- 问题类型：novel-generated；推理类型：未标注。
- 问题：Looking at VaR, did the risk that JPM faced in the second fiscal quarter of 2023 decrease compared to the same period in the prior year?
- 标准答案：Yes. It decreased.
- 答案依据：未提供

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, JPMorgan, JPMORGAN_2023Q2_10Q, novel-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：Average total VaR decreased by $7 million for the three months ended June 30, 2023, compared with the same period in the prior year predominantly driven by risk reductions impacting Credit Portfolio VaR as well as fixed income

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。


---

# FinanceBench 样本：financebench_id_10499

## 来源
- 数据集：FinanceBench open-source 本地子集
- 本地文件：`data/benchmarks/public/financebench_open_source_full.jsonl`
- 论文：https://arxiv.org/abs/2311.11944

## 关键事实
- 公司：Kraft Heinz；文档：KRAFTHEINZ_2019_10K。
- 问题类型：metrics-generated；推理类型：Numerical reasoning。
- 问题：What is Kraft Heinz's FY2019 inventory turnover ratio? Inventory turnover ratio is defined as: (FY2019 COGS) / (average inventory between FY2018 and FY2019). Round your answer to two decimal places. Please base your judgments on the information provided primarily in the balance sheet and the P&L statement.
- 标准答案：6.25
- 答案依据：The metric in question was calculated using other simpler metrics. The various simpler metrics (from the current and, if relevant, previous fiscal year(s)) used were:

Metric 1: Cost of goods sold. This metric was located in the 10K as a single line item named: Cost of products sold.

Metric 2: Inventories. This metric was located in the 10K as a single line item named: Inventories.

## 投研关注点
- 该样本用于评估金融 RAG 的证据定位、财报指标抽取、表格/文本理解和答案可追溯性。
- 适合测试多 Agent 中 FundamentalValuationAgent、CitationAuditAgent 对财报证据和数值答案的处理能力。

## RAG 检索关键词
FinanceBench, Kraft Heinz, KRAFTHEINZ_2019_10K, metrics-generated, financial QA, SEC filing, open-book QA, citation coverage

## 证据文本
证据 1：The Kraft Heinz Company Consolidated Statements of Income (in millions, except per share data) December 28, 2019 December 29, 2018 December 30, 2017 Net sales $ 24,977 $ 26,268 $ 26,076 Cost of products sold 16,830 17,347 17,043 Gross profit 8,147 8,921 9,033 Selling, general and administrative expenses, excluding impairment losses 3,178 3,190 2,927 Goodwill impairment losses 1,197 7,008 Intangible asset impairment losses 702 8,928 49 Selling, general and administrative expenses 5,077 19,126 2,976 Operating income/(loss) 3,070 (10,205) 6,057 Interest expense 1,361 1,284 1,234 Other expense/(income) (952) (168) (627) Income/(loss) before income taxes 2,661 (11,321) 5,450 Provision for/(benefit from) income taxes 728 (1,067) (5,482) Net income/(loss) 1,933 (10,254) 10,932 Net income/(loss) attributable to noncontrolling interest (2) (62) (9) Net income/(loss) attributable to common shareholders $ 1,935 $ (10,192) $ 10,941 Per share data applicable to common shareholders: Basic earnings/(loss) $ 1.59 $ (8.36) $ 8.98 Diluted earnings/(loss) 1.58 (8.36) 8.91 See accompanying notes to the consolidated financial statements. 45

证据 2：The Kraft Heinz Company Consolidated Balance Sheets (in millions, except per share data) December 28, 2019 December 29, 2018 ASSETS Cash and cash equivalents $ 2,279 $ 1,130 Trade receivables (net of allowances of $33 at December 28, 2019 and $24 at December 29, 2018) 1,973 2,129 Income taxes receivable 173 152 Inventories 2,721 2,667 Prepaid expenses 384 400 Other current assets 445 1,221 Assets held for sale 122 1,376 Total current assets 8,097 9,075 Property, plant and equipment, net 7,055 7,078 Goodwill 35,546 36,503 Intangible assets, net 48,652 49,468 Other non-current assets 2,100 1,337 TOTAL ASSETS $ 101,450 $ 103,461 LIABILITIES AND EQUITY Commercial paper and other short-term debt $ 6 $ 21 Current portion of long-term debt 1,022 377 Trade payables 4,003 4,153 Accrued marketing 647 722 Interest payable 384 408 Other current liabilities 1,804 1,767 Liabilities held for sale 9 55 Total current liabilities 7,875 7,503 Long-term debt 28,216 30,770 Deferred income taxes 11,878 12,202 Accrued postemployment costs 273 306 Other non-current liabilities 1,459 902 TOTAL LIABILITIES 49,701 51,683 Commitments and Contingencies (Note 17) Redeemable noncontrolling interest 3 Equity: Common stock, $0.01 par value (5,000 shares authorized; 1,224 shares issued and 1,221 shares outstanding at December 28, 2019; 1,224 shares issued and 1,220 shares outstanding at December 29, 2018) 12 12 Additional paid-in capital 56,828 58,723 Retained earnings/(deficit) (3,060) (4,853) Accumulated other comprehensive income/(losses) (1,886) (1,943) Treasury stock, at cost (3 shares at December 28, 2019 and 4 shares at December 29, 2018) (271) (282) Total shareholders' equity 51,623 51,657 Noncontrolling interest 126 118 TOTAL EQUITY 51,749 51,775 TOTAL LIABILITIES AND EQUITY $ 101,450 $ 103,461 See accompanying notes to the consolidated financial statements. 47

## 使用边界
- 该条目来自公共金融 QA benchmark，用于评测和证据召回，不代表实时投资事实。
- 生成 A 股研报时可以借鉴其财务问答和证据定位方式，但不能把英文 SEC 样本直接当作 A 股公司事实。
