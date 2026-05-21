import Link from 'next/link'

import { AnalysisLauncher } from '../analysis-launcher'
import { sameOriginApiUrl } from '../../lib/api'
import { formatEventStatus, formatEventType, formatExportKind, formatImpactLevel } from '../../lib/labels'
import type { StockWorkbenchResponse } from '../../lib/types'
import { EmptyState, RiskTicker, StatusBadge } from './primitives'

const TABS = [
  { key: 'summary', label: '概览' },
  { key: 'timeline', label: '事件' },
  { key: 'backtest', label: '回测' },
  { key: 'exports', label: '交付' },
] as const

export function StockWorkbench({ data }: { data: StockWorkbenchResponse }) {
  return (
    <div className="wbStack">
      <RiskTicker items={[
        { label: '研究状态', value: data.latest_report ? '完成' : '待分析', tone: data.latest_report ? 'success' : 'neutral' },
        { label: '事件数', value: data.timeline.total },
        { label: '高影响', value: data.timeline.high_impact_count, tone: data.timeline.high_impact_count ? 'warning' : 'neutral' },
        { label: '交付物', value: data.exports.length },
      ]} />

      <div className="wbTabs">
        {TABS.map((tab) => (
          <Link className={`wbTab ${data.active_tab === tab.key ? 'wbTabActive' : ''}`} href={`/stocks/${data.stock_code}?tab=${tab.key}`} key={tab.key}>
            {tab.label}
          </Link>
        ))}
        <Link className="wbTab" href={`/markets/${data.stock_code}`}>行情</Link>
        <Link className="wbTab" href="/watchlist">加入组合</Link>
      </div>

      {data.active_tab === 'summary' ? <SummaryTab data={data} /> : null}
      {data.active_tab === 'timeline' ? <TimelineTab data={data} /> : null}
      {data.active_tab === 'backtest' ? <BacktestTab data={data} /> : null}
      {data.active_tab === 'exports' ? <ExportsTab data={data} /> : null}
    </div>
  )
}

function SummaryTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbSplitPane">
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
        ) : <EmptyState title="暂无研报" description="可以从右侧发起一次多智能体研报任务，完成后会沉淀到当前账号的研究记忆。" />}
        <div className="wbList">
          {data.history?.records.slice(0, 3).map((record) => (
            <div className="wbListItem" key={record.timestamp}>
              <strong>{record.rating || '历史研报'} · {record.rating_score.toFixed(0)}</strong>
              <span>{record.timestamp} · 风险 {record.risk_count}</span>
            </div>
          ))}
        </div>
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
                <td>{formatEventType(event.event_type)}</td>
                <td><StatusBadge tone={event.impact_level === 'high' ? 'danger' : event.impact_level === 'medium' ? 'warning' : 'neutral'}>{formatImpactLevel(event.impact_level)}</StatusBadge></td>
                <td>{event.provider || event.source || '未知'}</td>
                <td>{formatEventStatus(event.status)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {!data.timeline.items.length ? <EmptyState title="暂无事件" description={data.is_tracked ? '暂无历史事件，请刷新所属组合。' : '这只股票尚未加入组合，加入后才会沉淀历史事件。'} action={data.is_tracked ? { label: '进入组合', href: '/watchlist' } : { label: '加入组合', href: '/watchlist' }} /> : null}
      </div>
    </section>
  )
}

function HistoryTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbSplitPane">
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

function BacktestTab({ data }: { data: StockWorkbenchResponse }) {
  return (
    <section className="wbTwoColumn">
      <div className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">事件影响回测</div>
            <h2>事件后收益分布</h2>
          </div>
        </div>
        <div className="wbFactGrid">
          <div><span>可匹配事件</span><strong>{data.event_backtest.matched_event_count}</strong></div>
          <div><span>事件总数</span><strong>{data.event_backtest.total_events}</strong></div>
          <div><span>窗口</span><strong>{data.event_backtest.windows.map((item) => `T+${item}`).join(' / ') || '--'}</strong></div>
          <div><span>分组</span><strong>{data.event_backtest.groups.length}</strong></div>
        </div>
        {data.event_backtest.fallback_message ? <EmptyState title="回测数据不足" description={data.event_backtest.fallback_message} /> : null}
        <div className="wbTableWrap">
          <table className="wbTable">
            <thead><tr><th>类型</th><th>事件</th><th>T+1</th><th>T+5</th><th>正收益</th><th>平均回撤</th></tr></thead>
            <tbody>
              {data.event_backtest.groups.map((group) => (
                <tr key={group.key}>
                  <td className="wbPrimaryText">{group.label}</td>
                  <td>{group.event_count}</td>
                  <td>{formatPct(group.average_returns.t1)}</td>
                  <td>{formatPct(group.average_returns.t5)}</td>
                  <td>{formatRate(group.positive_rate)}</td>
                  <td>{formatPct(group.average_max_drawdown)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {!data.event_backtest.groups.length ? <EmptyState title="暂无回测结果" description="刷新组合或扩大事件历史后，会自动出现事件类型分组收益表现。" /> : null}
        </div>
      </div>
      <div className="wbPanel">
        <div className="wbPanelHead"><div><div className="wbEyebrow">代表性事件</div><h2>回测样本</h2></div></div>
        <div className="wbList">
          {data.event_backtest.items.slice(0, 10).map((item) => (
            <Link className="wbListItem" href={`/events?selected_event_id=${item.event_id}`} key={item.event_id}>
              <strong>{item.title}</strong>
              <span>{item.base_date} · T+1 {formatPct(item.returns.t1)} · T+5 {formatPct(item.returns.t5)} · 最大回撤 {formatPct(item.max_drawdown)}</span>
            </Link>
          ))}
          {!data.event_backtest.items.length ? <EmptyState title="暂无事件样本" description="当前股票还没有可与行情匹配的事件样本。" /> : null}
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
                <td>{formatExportKind(item.kind)}</td>
                <td><span className="wbMuted">{item.download_url}</span></td>
                <td>
                  <div className="exportActionLinks">
                    <a className="wbTextButton" href={sameOriginApiUrl(previewExportUrl(item.download_url))} target="_blank" rel="noreferrer">预览</a>
                    <a className="wbTextButton" href={sameOriginApiUrl(item.download_url)} target="_blank" rel="noreferrer">下载</a>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!data.exports.length ? <EmptyState title="暂无导出物" description="完成研报或事件点评任务后，交付文件会出现在这里。" action={{ label: '创建任务', href: `/runs` }} /> : null}
      </div>
    </section>
  )
}

function previewExportUrl(downloadUrl: string) {
  const normalized = downloadUrl || ''
  return normalized.endsWith('/preview') ? normalized : `${normalized}/preview`
}

function formatPct(value: number | undefined) {
  const normalized = Number(value || 0)
  return `${normalized >= 0 ? '+' : ''}${normalized.toFixed(2)}%`
}

function formatRate(value: number | undefined) {
  return `${(Number(value || 0) * 100).toFixed(1)}%`
}
