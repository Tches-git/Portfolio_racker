import Link from 'next/link'

import type { AnalysisRunResponse } from '../lib/types'

export function RecentRunsPanel({ runs }: { runs: AnalysisRunResponse[] }) {
  const activeRuns = runs.filter((run) => run.status === 'queued' || run.status === 'running')
  const failedRuns = runs.filter((run) => run.status === 'failed')
  const stockGroups = Array.from(new Set(runs.map((run) => run.stock_code)))

  return (
    <section className="panel span-12">
      <div className="sectionHead">
        <div>
          <div className="sectionEyebrow">最近任务</div>
          <h2>最近运行任务</h2>
        </div>
        <Link className="ghostLink" href="/runs">进入任务中心</Link>
      </div>
      <div className="runListLayout">
        <div className="runSummaryCard">
          <div className="itemTitle">任务概况</div>
          <div className="metricStack">
            <div className="metricRow"><span>最近任务数</span><strong>{runs.length}</strong></div>
            <div className="metricRow"><span>活跃任务</span><strong>{activeRuns.length}</strong></div>
            <div className="metricRow"><span>失败任务</span><strong>{failedRuns.length}</strong></div>
            <div className="metricRow"><span>涉及股票</span><strong>{stockGroups.length}</strong></div>
          </div>
        </div>
        <div className="runList">
          {runs.length ? runs.slice(0, 6).map((run) => (
            <Link className="runListItem" href={`/runs/${run.run_id}`} key={run.run_id}>
              <div>
                <div className="itemTitle">{run.stock_code}</div>
                <div className="itemMeta">{run.updated_at || run.created_at || '暂无时间'}</div>
              </div>
              <span className={`tag${run.status === 'completed' ? ' tagPositive' : run.status === 'failed' ? ' tagNegative' : ''}`}>{run.status}</span>
              <div className="inlineMeta">{run.observability.latest_signal || run.last_event || run.detail || '--'}</div>
            </Link>
          )) : <div className="emptyState">当前还没有可展示的运行任务。</div>}
        </div>
      </div>
    </section>
  )
}
