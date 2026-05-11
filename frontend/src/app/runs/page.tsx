import Link from 'next/link'

import { BatchRunLauncher } from '../../components/batch-run-launcher'
import { RunStatusBar } from '../../components/run-status-bar'
import { fetchRecentRuns } from '../../lib/api'

function runTone(status: string) {
  if (status === 'completed') return 'tagPositive'
  if (status === 'failed') return 'tagNegative'
  return ''
}

export default async function RunsIndexPage({ searchParams }: { searchParams?: Promise<{ status?: string; stock?: string; archived?: string; selected?: string }> }) {
  const params = await searchParams
  const runs = await fetchRecentRuns(24)
  const selectedStatus = params?.status || 'all'
  const selectedStock = params?.stock || 'all'
  const archivedMode = params?.archived || 'all'
  const activeRuns = runs.items.filter((item) => item.status === 'queued' || item.status === 'running')
  const failedRuns = runs.items.filter((item) => item.status === 'failed')
  const filteredRuns = runs.items.filter((item) => (selectedStatus === 'all' || item.status === selectedStatus) && (selectedStock === 'all' || item.stock_code === selectedStock) && (archivedMode === 'all' || String(item.archived) === archivedMode))
  const selectedRun = filteredRuns.find((item) => item.run_id === params?.selected) || filteredRuns[0] || runs.items[0] || null
  const latestRun = runs.items[0] || null

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Run Center · Index</div>
            <h1>全局任务中心</h1>
            <p>把浏览器触发分析、最近任务、失败状态与导出跳转统一收拢到一个更接近成熟后台产品的任务面板。</p>
          </div>
          <Link className="ghostLink" href="/">返回首页</Link>
        </div>
      </section>

      <RunStatusBar stockCode={latestRun?.stock_code || '全局'} hasData={Boolean(activeRuns.length || latestRun?.status === 'completed')} statusHint="全局任务中心会汇总最近任务，并作为跨路由任务入口。" />

      <div className="grid">
        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">运行队列</div>
              <h2>运行队列</h2>
            </div>
          </div>
          <div className="detailGrid">
            <div className="card">
              <div className="itemTitle">活跃任务</div>
              <div className="metricStack">
                <div className="metricRow"><span>运行中 / 排队中</span><strong>{activeRuns.length}</strong></div>
                <div className="metricRow"><span>最近任务数</span><strong>{runs.total}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">运行分布</div>
              <div className="metricStack">
                <div className="metricRow"><span>已完成</span><strong>{runs.completed_count}</strong></div>
                <div className="metricRow"><span>失败</span><strong>{runs.failed_count}</strong></div>
                <div className="metricRow"><span>排队</span><strong>{runs.queued_count}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">最近完成</div>
              <p className="bodyText">{latestRun ? `${latestRun.stock_code} · ${latestRun.detail}` : '暂无最近任务。'}</p>
            </div>
            <div className="card">
              <div className="itemTitle">组合视角</div>
              <div className="metricStack">
                <div className="metricRow"><span>跟踪股票</span><strong>{runs.workspace.tracked_stocks.length}</strong></div>
                <div className="metricRow"><span>最活跃标的</span><strong>{runs.workspace.most_active_stock || '--'}</strong></div>
                <div className="metricRow"><span>最近完成标的</span><strong>{runs.workspace.latest_completed_stock || '--'}</strong></div>
                <div className="metricRow"><span>已归档任务</span><strong>{runs.workspace.archived_run_count}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">关注事项</div>
              <p className="bodyText">{failedRuns.length ? `当前有 ${failedRuns.length} 个失败任务，建议优先进入任务详情查看时间线。` : '当前未发现失败任务，可直接跟进活跃任务或回到产品页。'}</p>
            </div>
            <div className="card">
              <div className="itemTitle">任务入口</div>
              <div className="actionList compactActions">
                {latestRun ? <Link className="downloadLink" href={`/runs/${latestRun.run_id}`}>进入最近任务</Link> : null}
                {latestRun ? <Link className="downloadLink" href={`/stocks/${latestRun.stock_code}`}>进入对应产品页</Link> : <Link className="downloadLink" href="/stocks/600519">进入研究结果</Link>}
              </div>
            </div>
            <BatchRunLauncher initialStocks={runs.workspace.tracked_stocks.slice(0, 4)} />
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">股票聚合</div>
              <h2>按股票聚合</h2>
            </div>
          </div>
          <div className="detailGrid">
            {runs.stock_groups.map((group) => (
              <div className="card" key={group.stock_code}>
                <div className="itemTitle">{group.stock_code}</div>
                <div className="metricStack">
                  <div className="metricRow"><span>任务总数</span><strong>{group.total}</strong></div>
                  <div className="metricRow"><span>活跃任务</span><strong>{group.active_count}</strong></div>
                  <div className="metricRow"><span>失败任务</span><strong>{group.failed_count}</strong></div>
                  <div className="metricRow"><span>已归档</span><strong>{group.archived_count}</strong></div>
                </div>
                <div className="actionList compactActions">
                  <Link className="downloadLink" href={`/stocks/${group.stock_code}`}>产品页</Link>
                  {group.latest_run_id ? <Link className="downloadLink" href={`/runs/${group.latest_run_id}`}>最近任务</Link> : null}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">全部任务</div>
              <h2>最近任务列表</h2>
            </div>
          </div>
          <div className="filterBar">
            {['all', 'queued', 'running', 'completed', 'failed'].map((status) => <Link key={status} className={`filterChip ${selectedStatus === status ? 'filterChipActive' : ''}`} href={`/runs?status=${status}&stock=${selectedStock}&archived=${archivedMode}`}>{status === 'all' ? '全部状态' : status}</Link>)}
            <Link className={`filterChip ${selectedStock === 'all' ? 'filterChipActive' : ''}`} href={`/runs?status=${selectedStatus}&stock=all&archived=${archivedMode}`}>全部股票</Link>
            {runs.stock_groups.map((group) => <Link key={group.stock_code} className={`filterChip ${selectedStock === group.stock_code ? 'filterChipActive' : ''}`} href={`/runs?status=${selectedStatus}&stock=${group.stock_code}&archived=${archivedMode}`}>{group.stock_code}</Link>)}
            {['all', 'false', 'true'].map((archived) => <Link key={archived} className={`filterChip ${archivedMode === archived ? 'filterChipActive' : ''}`} href={`/runs?status=${selectedStatus}&stock=${selectedStock}&archived=${archived}`}>{archived === 'all' ? '全部归档' : archived === 'true' ? '仅归档' : '仅活跃'}</Link>)}
          </div>
          <div className="selectionHint">任务中心优先作为全局 master list：从这里进入任务详情，再回流到股票页、历史页或导出中心；动作可用性与观测摘要来自后端结构化 contract。</div>
          <div className="statusBar compactStatusBar">
            <div>
              <div className="statusLabel">失败任务专项视图</div>
              <div className="statusValue">{failedRuns.length}</div>
            </div>
            <div>
              <div className="statusLabel">推荐并发</div>
              <div className="statusValue">{runs.workspace.recommended_concurrency}</div>
            </div>
            <div>
              <div className="statusLabel">运行治理</div>
              <div className="statusHint">{runs.workspace.active_limit_reached ? '当前活跃任务达到建议上限，请优先消化队列。' : '当前活跃任务未超过建议并发。'} · 队列 {runs.workspace.queue_mode} · Worker {runs.workspace.worker_count} · 运维 {runs.workspace.ops_status} · 告警 {runs.workspace.alert_count} · 失败率 {(runs.workspace.failure_rate * 100).toFixed(1)}% · P95 {runs.workspace.p95_duration_s.toFixed(1)}s · 存储 {runs.workspace.store_backend} v{runs.workspace.schema_version} · WAL {runs.workspace.wal_enabled ? 'on' : 'off'} · 协作者 {runs.workspace.collaborator_count} · 审计动作 {runs.workspace.audited_action_count} · 自动重试 {runs.workspace.retry_scheduled_count} · 中断任务 {runs.workspace.stale_run_count}</div>
            </div>
          </div>
          {selectedRun ? (
            <div className="masterDetailPreview">
              <div className="card selectedCard">
                <div className="itemTitle">当前选中任务 · {selectedRun.stock_code}</div>
                <div className="inlineMeta">{selectedRun.run_id} · {selectedRun.observability.latest_signal || selectedRun.last_event || '--'}</div>
                <p className="bodyText">{selectedRun.detail || '暂无说明'}</p>
              </div>
              <div className="card">
                <div className="itemTitle">恢复/观测</div>
                <div className="metricStack">
                  <div className="metricRow"><span>恢复状态</span><strong>{selectedRun.observability.recovery_status}</strong></div>
                  <div className="metricRow"><span>重启中断</span><strong>{selectedRun.observability.stale_after_restart ? '是' : '否'}</strong></div>
                  <div className="metricRow"><span>负责人</span><strong>{selectedRun.observability.owner_label}</strong></div>
                  <div className="metricRow"><span>尝试次数</span><strong>{selectedRun.observability.attempts}/{selectedRun.observability.max_attempts}</strong></div>
                  <div className="metricRow"><span>执行器</span><strong>{selectedRun.observability.worker_id || '--'}</strong></div>
                </div>
              </div>
              <div className="card">
                <div className="itemTitle">下一步</div>
                <p className="bodyText">{selectedRun.actions.suggested_next_action}</p>
                <div className="actionList compactActions"><Link className="downloadLink" href={`/runs/${selectedRun.run_id}`}>打开任务详情</Link></div>
              </div>
            </div>
          ) : null}
          <div className="tableWrap">
            <table className="table">
              <thead>
                <tr>
                  <th>任务</th>
                  <th>股票</th>
                  <th>状态</th>
                  <th>最近事件</th>
                  <th>时间线</th>
                  <th>说明</th>
                  <th>建议</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredRuns.length ? filteredRuns.map((run) => (
                  <tr className={selectedRun?.run_id === run.run_id ? 'tableRowActive' : ''} key={run.run_id}>
                    <td>{run.run_id}</td>
                    <td>{run.stock_code}</td>
                    <td><span className={`tag ${runTone(run.status)}`}>{run.status}</span></td>
                    <td>{run.last_event || '--'}</td>
                    <td>{run.observability.event_count} 条</td>
                    <td>{run.detail || '--'}</td>
                    <td>{run.actions.suggested_next_action || '--'}</td>
                    <td>
                      <div className="tableActions">
                        <Link className="downloadLink" href={`/runs?status=${selectedStatus}&stock=${selectedStock}&archived=${archivedMode}&selected=${run.run_id}`}>预览</Link>
                        <Link className="downloadLink" href={`/runs/${run.run_id}`}>任务详情</Link>
                        <Link className="downloadLink" href={`/stocks/${run.stock_code}`}>产品页</Link>
                        <Link className="downloadLink" href={`/stocks/${run.stock_code}/exports`}>导出中心</Link>
                      </div>
                    </td>
                  </tr>
                )) : <tr><td colSpan={8}>当前筛选条件下没有任务。</td></tr>}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  )
}
