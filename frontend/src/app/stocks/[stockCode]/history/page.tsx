import Link from 'next/link'

import { RunStatusBar } from '../../../../components/run-status-bar'
import { SearchShell } from '../../../../components/search-shell'
import { StockWorkspaceNav } from '../../../../components/stock-workspace-nav'
import { fetchLatestReport, fetchRecentRuns, fetchReportDiff, fetchStockHistory } from '../../../../lib/api'
import type { AnalysisRunResponse, StockHistoryResponse } from '../../../../lib/types'

function recordTone(record: StockHistoryResponse['records'][number]) {
  if (record.dcf_upside >= 15) return 'tagPositive'
  if (record.dcf_upside <= -15) return 'tagNegative'
  return ''
}

function selectedRecord(records: StockHistoryResponse['records'], selectedTimestamp?: string) {
  if (selectedTimestamp) {
    const matched = records.find((item) => item.timestamp === selectedTimestamp)
    if (matched) return matched
  }
  return records[0] || null
}

function latestStockRun(runs: AnalysisRunResponse[], stockCode: string) {
  return runs.find((item) => item.stock_code === stockCode) || null
}

export default async function StockHistoryPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams?: Promise<{ selected?: string }>
}) {
  const { stockCode } = await params
  const resolvedSearchParams = searchParams ? await searchParams : undefined
  const latest = await fetchLatestReport(stockCode)
  const history = await fetchStockHistory(stockCode)
  const diff = await fetchReportDiff(stockCode)
  const recentRuns = await fetchRecentRuns(8)
  const currentRecord = selectedRecord(history?.records || [], resolvedSearchParams?.selected)
  const currentRun = latestStockRun(recentRuns.items, stockCode)
  const hasData = Boolean(latest)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Detail Route · History</div>
            <h1>{history?.stock.name || latest?.stock.name || stockCode} 历史脉络</h1>
            <p>继续把产品页拆成独立工作区，让历史观点、评级变化与研究记忆能在 sidebar 驱动的右侧工作区内持续深化。</p>
          </div>
          <Link className="ghostLink" href={`/stocks/${stockCode}`}>返回产品页</Link>
        </div>
      </section>

      <RunStatusBar stockCode={stockCode} hasData={hasData} statusHint="历史页已拆成独立工作区，可继续深化为 master-detail 与变化解释面板。" />
      <StockWorkspaceNav stockCode={stockCode} current="history" />
      <SearchShell initialCode={stockCode} />

      {!history ? <div className="emptyState">当前暂无历史脉络数据，请先完成至少一次分析并确认 API 可访问。</div> : null}

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Memory Timeline</div>
              <h2>研究记忆时间线</h2>
            </div>
          </div>
          {history?.insights.repeated_risk_patterns.length || history?.insights.repeated_catalyst_patterns.length ? (
            <div className="selectionHint">
              长期模式：
              {history.insights.repeated_risk_patterns.length ? ` 重复风险 ${history.insights.repeated_risk_patterns.join(' / ')}` : ''}
              {history.insights.repeated_catalyst_patterns.length ? `；重复催化 ${history.insights.repeated_catalyst_patterns.join(' / ')}` : ''}
            </div>
          ) : null}
          <div className="timelineList">
            {(history?.memory || []).length ? history!.memory.map((item) => (
              <div className="timelineCard" key={item.timestamp}>
                <div className="timelineDot" />
                <div className="card timelineBody">
                  <div className="itemTitle">{item.timestamp} · {item.rating || '未知评级'}</div>
                  <div className="itemMeta">{item.target_range || item.valuation_summary || '暂无估值锚'}</div>
                  <p>{item.thesis || '暂无 thesis'}</p>
                  {item.historical_delta ? <div className="pathText">{item.historical_delta}</div> : null}
                  {item.conflict_reason ? <div className="pathText">冲突原因：{item.conflict_reason}</div> : null}
                  {(item.key_risks.length || item.catalysts.length) ? (
                    <div className="pillRow">
                      {item.key_risks.map((risk) => <span className="tag" key={`${item.timestamp}-${risk}`}>风险：{risk}</span>)}
                      {item.catalysts.map((catalyst) => <span className="tag tagPositive" key={`${item.timestamp}-${catalyst}`}>催化：{catalyst}</span>)}
                    </div>
                  ) : null}
                </div>
              </div>
            )) : <div className="card">暂无历史记忆。</div>}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">History Snapshot</div>
              <h2>历史快照</h2>
            </div>
          </div>
          <div className="detailGrid detailGridSingle">
            <div className="card">
              <div className="itemTitle">记录规模</div>
              <div className="metricStack">
                <div className="metricRow"><span>历史记录数</span><strong>{history?.records.length ?? 0}</strong></div>
                <div className="metricRow"><span>研究记忆数</span><strong>{history?.memory.length ?? 0}</strong></div>
                <div className="metricRow"><span>最新状态</span><strong>{latest?.run_metrics.success ? '成功' : '待补数据'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">当前选中记录</div>
              {currentRecord ? (
                <div className="metricStack">
                  <div className="metricRow"><span>时间</span><strong>{currentRecord.timestamp}</strong></div>
                  <div className="metricRow"><span>评级</span><strong>{currentRecord.rating || '未知'}</strong></div>
                  <div className="metricRow"><span>评分</span><strong>{currentRecord.rating_score.toFixed(1)}</strong></div>
                  <div className="metricRow"><span>估值空间</span><strong>{currentRecord.dcf_upside.toFixed(1)}%</strong></div>
                </div>
              ) : <p className="bodyText">暂无可选历史记录。</p>}
            </div>
            <div className="card">
              <div className="itemTitle">任务联动</div>
              {currentRun ? (
                <div className="metricStack">
                  <div className="metricRow"><span>最近任务</span><strong>{currentRun.status}</strong></div>
                  <div className="metricRow"><span>最新阶段</span><strong>{currentRun.last_event || '--'}</strong></div>
                  <div className="metricRow"><span>时间线条数</span><strong>{currentRun.events.length}</strong></div>
                </div>
              ) : <p className="bodyText">当前股票暂无关联运行任务。</p>}
            </div>
            <div className="card">
              <div className="itemTitle">版本 Diff / 变化解释</div>
              <div className="metricStack">
                <div className="metricRow"><span>冲突次数</span><strong>{history?.insights.conflict_count ?? 0}</strong></div>
                <div className="metricRow"><span>评级漂移</span><strong>{history?.insights.rating_drift_summary || '--'}</strong></div>
                <div className="metricRow"><span>评级变化</span><strong>{diff?.rating_delta.toFixed(1) ?? '--'}</strong></div>
                <div className="metricRow"><span>估值空间变化</span><strong>{diff ? `${diff.upside_delta.toFixed(1)}%` : '--'}</strong></div>
                <div className="metricRow"><span>thesis 稳定度</span><strong>{history ? `${(history.insights.thesis_stability_score * 100).toFixed(0)}%` : '--'}</strong></div>
              </div>
              {diff?.summary ? <div className="pathText">版本 diff：{diff.summary}</div> : null}
              {history?.insights.latest_conflict_reason ? <div className="pathText">最近冲突：{history.insights.latest_conflict_reason}</div> : null}
            </div>
            <div className="card">
              <div className="itemTitle">冲突提示</div>
              <p className="bodyText">当前仍优先消费结构化 history payload；若后续继续收口 <code>AnalysisState.sections</code>，这里可直接承接更稳定的冲突/变化解释字段。</p>
            </div>
            <div className="card">
              <div className="itemTitle">后续动作</div>
              <div className="actionList">
                <Link className="downloadLink" href={`/stocks/${stockCode}/summary`}>查看摘要详情</Link>
                <Link className="downloadLink" href={`/stocks/${stockCode}/exports`}>查看导出中心</Link>
                {currentRun ? <Link className="downloadLink" href={`/runs/${currentRun.run_id}`}>进入任务详情</Link> : null}
              </div>
            </div>
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Records Table</div>
              <h2>历史记录明细</h2>
            </div>
          </div>
          <div className="selectionHint">点击任一历史记录即可更新右侧“当前选中记录”，形成更明确的 master-detail 工作方式。</div>
          <div className="tableWrap">
            <table className="table">
              <thead>
                <tr>
                  <th>时间</th>
                  <th>评级</th>
                  <th>评分</th>
                  <th>结论摘要</th>
                  <th>风险摘要</th>
                  <th>估值空间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {(history?.records || []).map((item) => {
                  const isSelected = currentRecord?.timestamp === item.timestamp
                  return (
                    <tr key={item.timestamp} className={isSelected ? 'tableRowActive' : ''}>
                      <td>{item.timestamp}</td>
                      <td>{item.rating || '未知'}</td>
                      <td>{item.rating_score.toFixed(1)}</td>
                      <td>
                        <div>{item.conclusion || '暂无摘要'}</div>
                        <div className="inlineMeta">来源引用 {item.source_reference_count} · 占位 {item.placeholder_source_count}</div>
                      </td>
                      <td>{item.risk_summary || '暂无风险'}</td>
                      <td><span className={`tag ${recordTone(item)}`}>{item.dcf_upside.toFixed(1)}%</span></td>
                      <td>
                        <Link className="downloadLink" href={`/stocks/${stockCode}/history?selected=${encodeURIComponent(item.timestamp)}`}>
                          {isSelected ? '当前已选' : '设为当前'}
                        </Link>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  )
}
