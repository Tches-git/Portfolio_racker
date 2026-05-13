import Link from 'next/link'

import { AnalysisLauncher } from '../analysis-launcher'
import { sameOriginApiUrl } from '../../lib/api'
import type { StockWorkbenchResponse } from '../../lib/types'

const TABS = [
  { key: 'summary', label: '摘要' },
  { key: 'timeline', label: '事件' },
  { key: 'history', label: '复盘' },
  { key: 'exports', label: '交付' },
] as const

export function StockWorkbench({ data }: { data: StockWorkbenchResponse }) {
  return (
    <div className="wbStack">
      <div className="wbTabs">
        {TABS.map((tab) => (
          <Link className={`wbTab ${data.active_tab === tab.key ? 'wbTabActive' : ''}`} href={`/stocks/${data.stock_code}?tab=${tab.key}`} key={tab.key}>
            {tab.label}
          </Link>
        ))}
        <Link className="wbTab" href={`/markets/${data.stock_code}`}>行情</Link>
        <Link className="wbTab" href="/watchlist">加入组合</Link>
      </div>

      <section className="wbMetricGrid">
        <div className="wbMetric"><span>研究状态</span><strong>{data.latest_report ? '已生成' : '待分析'}</strong><em>{data.latest_report?.generated_at || '暂无研报'}</em></div>
        <div className="wbMetric"><span>事件</span><strong>{data.timeline.total}</strong><em>高影响 {data.timeline.high_impact_count}</em></div>
        <div className="wbMetric"><span>所属组合</span><strong>{data.related_watchlists.length}</strong><em>{data.is_tracked ? '已追踪' : '未追踪'}</em></div>
        <div className="wbMetric"><span>导出物</span><strong>{data.exports.length}</strong><em>研报 / 点评 / 日志</em></div>
      </section>

      {data.active_tab === 'summary' ? <SummaryTab data={data} /> : null}
      {data.active_tab === 'timeline' ? <TimelineTab data={data} /> : null}
      {data.active_tab === 'history' ? <HistoryTab data={data} /> : null}
      {data.active_tab === 'exports' ? <ExportsTab data={data} /> : null}
    </div>
  )
}

function SummaryTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbTwoColumn">
      <div className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">研究摘要</div>
            <h2>{data.stock_name || data.stock_code}</h2>
          </div>
        </div>
        {data.latest_report ? (
          <>
            <p className="wbLead">{data.latest_report.summary.conclusion_brief || '暂无结论摘要。'}</p>
            <div className="wbFactGrid">
              <div><span>评级</span><strong>{data.latest_report.summary.rating || '--'}</strong></div>
              <div><span>评分</span><strong>{data.latest_report.summary.rating_score.toFixed(0)}</strong></div>
              <div><span>估值空间</span><strong>{data.latest_report.valuation.upside.toFixed(1)}%</strong></div>
              <div><span>来源</span><strong>{data.latest_report.quality.source_reference_count}</strong></div>
            </div>
          </>
        ) : <div className="wbEmpty">还没有研报结果，可以从右侧发起一次分析任务。</div>}
      </div>
      <div className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">动作</div>
            <h2>生成研报</h2>
          </div>
        </div>
        <AnalysisLauncher initialCode={data.stock_code} initialRuns={data.related_runs.items} />
      </div>
    </section>
  )
}

function TimelineTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbPanel">
      <div className="wbPanelHead">
        <div>
          <div className="wbEyebrow">事件时间线</div>
          <h2>{data.stock_code} 历史事件</h2>
        </div>
        <Link className="wbTextButton" href={`/events?stock_codes=${data.stock_code}`}>事件台</Link>
      </div>
      <div className="wbTableWrap">
        <table className="wbTable">
          <thead><tr><th>事件</th><th>类型</th><th>影响</th><th>来源</th><th>状态</th></tr></thead>
          <tbody>
            {data.timeline.items.map((event) => (
              <tr key={event.event_id}>
                <td><Link className="wbPrimaryText" href={`/events?selected_event_id=${event.event_id}`}>{event.title}</Link><div className="wbMuted">{event.summary || event.reason}</div></td>
                <td>{event.event_type}</td>
                <td><span className={`wbBadge ${event.impact_level === 'high' ? 'wbBadgeDanger' : ''}`}>{event.impact_level}</span></td>
                <td>{event.provider || event.source || '未知'}</td>
                <td>{event.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!data.timeline.items.length ? <div className="wbEmpty">{data.is_tracked ? '暂无历史事件，请刷新所属组合。' : '这只股票尚未加入组合，加入后才会沉淀历史事件。'}</div> : null}
      </div>
    </section>
  )
}

function HistoryTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbTwoColumn">
      <div className="wbPanel">
        <div className="wbPanelHead"><div><div className="wbEyebrow">历史影响</div><h2>事件复盘</h2></div></div>
        <p className="wbLead">{data.impact_review.summary}</p>
        <div className="wbList">
          {data.impact_review.replay_items.slice(0, 8).map((item) => (
            <Link className="wbListItem" href={`/events?selected_event_id=${item.event_id}`} key={item.event_id}>
              <strong>{item.title}</strong>
              <span>{item.review_line}</span>
            </Link>
          ))}
          {!data.impact_review.replay_items.length ? <div className="wbEmpty">暂无可复盘事件。</div> : null}
        </div>
      </div>
      <div className="wbPanel">
        <div className="wbPanelHead"><div><div className="wbEyebrow">研报历史</div><h2>研究记忆</h2></div></div>
        <div className="wbList">
          {data.history?.records.slice(0, 8).map((record) => (
            <div className="wbListItem" key={record.timestamp}>
              <strong>{record.rating || '未评级'} · {record.rating_score.toFixed(0)}</strong>
              <span>{record.timestamp} · 风险 {record.risk_count}</span>
            </div>
          ))}
          {!data.history?.records.length ? <div className="wbEmpty">暂无历史研报。</div> : null}
        </div>
      </div>
    </section>
  )
}

function ExportsTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbPanel">
      <div className="wbPanelHead"><div><div className="wbEyebrow">交付中心</div><h2>导出物</h2></div></div>
      <div className="wbTableWrap">
        <table className="wbTable">
          <thead><tr><th>文件</th><th>类型</th><th>路径</th><th>动作</th></tr></thead>
          <tbody>
            {data.exports.map((item) => (
              <tr key={item.filename}>
                <td className="wbPrimaryText">{item.filename}</td>
                <td>{item.kind}</td>
                <td><span className="wbMuted">{item.download_url}</span></td>
                <td><a className="wbTextButton" href={sameOriginApiUrl(item.download_url)} target="_blank" rel="noreferrer">打开</a></td>
              </tr>
            ))}
          </tbody>
        </table>
        {!data.exports.length ? <div className="wbEmpty">暂无导出物。完成研报任务后会出现在这里。</div> : null}
      </div>
    </section>
  )
}
