import Link from 'next/link'

import { BatchRunLauncher } from '../batch-run-launcher'
import { RunActionControls } from '../run-action-controls'
import type { RunWorkbenchResponse } from '../../lib/types'

function statusText(status: string) {
  if (status === 'queued') return '排队'
  if (status === 'running') return '运行中'
  if (status === 'completed') return '已完成'
  if (status === 'failed') return '失败'
  return status
}

export function TaskDeliveryCenter({ data }: { data: RunWorkbenchResponse }) {
  const selected = data.selected_run || data.runs.items[0] || null

  return (
    <div className="wbStack">
      <section className="wbMetricGrid">
        <div className="wbMetric"><span>任务总数</span><strong>{data.runs.total}</strong><em>当前账号</em></div>
        <div className="wbMetric"><span>运行中</span><strong>{data.runs.running_count + data.runs.queued_count}</strong><em>排队 + 执行</em></div>
        <div className="wbMetric"><span>完成</span><strong>{data.runs.completed_count}</strong><em>可查看交付</em></div>
        <div className="wbMetric"><span>失败</span><strong>{data.runs.failed_count}</strong><em>可重试</em></div>
      </section>

      <section className="wbTwoColumn">
        <div className="wbPanel">
          <div className="wbPanelHead"><div><div className="wbEyebrow">任务列表</div><h2>研报与事件点评</h2></div></div>
          <div className="wbTableWrap">
            <table className="wbTable">
              <thead><tr><th>股票</th><th>状态</th><th>最近事件</th><th>导出</th><th>动作</th></tr></thead>
              <tbody>
                {data.runs.items.map((run) => (
                  <tr key={run.run_id}>
                    <td><Link className="wbPrimaryText" href={`/runs/${run.run_id}`}>{run.stock_code}</Link></td>
                    <td><span className={`wbBadge ${run.status === 'failed' ? 'wbBadgeDanger' : ''}`}>{statusText(run.status)}</span></td>
                    <td>{run.last_event || run.detail || '--'}</td>
                    <td>{run.exports.length}</td>
                    <td><Link className="wbTextButton" href={`/stocks/${run.stock_code}`}>股票</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!data.runs.items.length ? <div className="wbEmpty">当前还没有任务。可以在右侧批量创建研报任务。</div> : null}
          </div>
        </div>
        <div className="wbPanel">
          <div className="wbPanelHead"><div><div className="wbEyebrow">创建任务</div><h2>批量运行</h2></div></div>
          <BatchRunLauncher initialStocks={data.runs.workspace.tracked_stocks} />
        </div>
      </section>

      <section className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">当前任务</div>
            <h2>{selected ? `${selected.stock_code} · ${statusText(selected.status)}` : '未选择任务'}</h2>
          </div>
          {selected ? <Link className="wbTextButton" href={`/runs/${selected.run_id}`}>详情页</Link> : null}
        </div>
        {selected ? (
          <div className="wbDetailGrid">
            <div>
              <p className="wbLead">{selected.detail || selected.error || '任务状态同步中。'}</p>
              <div className="wbChipRow">
                <span className="wbChip">导出 {selected.exports.length}</span>
                <span className="wbChip">事件 {selected.events.length}</span>
                <span className="wbChip">{selected.actions.suggested_next_action}</span>
                <span className="wbChip">{selected.updated_at || selected.created_at || '暂无时间'}</span>
              </div>
            </div>
            <RunActionControls run={selected} />
          </div>
        ) : <div className="wbEmpty">选择或创建任务后，可以在这里处理重试、取消和归档。</div>}
      </section>
    </div>
  )
}
