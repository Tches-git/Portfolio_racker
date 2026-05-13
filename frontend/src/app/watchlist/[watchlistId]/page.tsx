import Link from 'next/link'

import { EventAnalyzeButton } from '../../../components/event-analyze-button'
import { WatchlistRefreshButton } from '../../../components/watchlist-refresh-button'
import { RiskQueue } from '../../../components/workbench/risk-queue'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchUiWatchlistDetail } from '../../../lib/api'
import { serverApiOptions } from '../../../lib/server-auth'

function riskText(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}

export default async function WatchlistDetailPage({ params }: { params: Promise<{ watchlistId: string }> }) {
  const { watchlistId } = await params
  const apiOptions = await serverApiOptions()
  const detail = await fetchUiWatchlistDetail(watchlistId, apiOptions)

  if (!detail) {
    return (
      <WorkspaceShell
        eyebrow="组合驾驶舱"
        title="未找到组合"
        description="该组合可能不存在，或你当前账号没有访问权限。"
        actions={[{ label: '返回组合列表', href: '/watchlist', method: 'GET', action_type: 'navigate', target_id: 'watchlist', variant: 'secondary' }]}
      >
        <div className="wbEmpty">组合 ID：{watchlistId}</div>
      </WorkspaceShell>
    )
  }

  const { watchlist, summary, events, alerts, briefing } = detail
  const stockQuery = watchlist.stock_codes.join(',')

  return (
    <WorkspaceShell
      eyebrow="组合驾驶舱"
      title={watchlist.name}
      description={`${watchlist.description || '组合级金融消息追踪范围'} · 最近刷新：${summary.last_refreshed_at || '尚未手动刷新'}`}
      actions={[
        { label: '事件预警', href: `/events?stock_codes=${stockQuery}`, method: 'GET', action_type: 'navigate', target_id: watchlist.watchlist_id, variant: 'secondary' },
        { label: '任务交付', href: '/runs', method: 'GET', action_type: 'navigate', target_id: watchlist.watchlist_id, variant: 'secondary' },
      ]}
    >
      <div className="wbStack">
        <section className="wbMetricGrid">
          <div className="wbMetric"><span>风险分</span><strong>{summary.risk_score}</strong><em>{riskText(summary.risk_level)}</em></div>
          <div className="wbMetric"><span>追踪股票</span><strong>{summary.stock_count}</strong><em>组合股票池</em></div>
          <div className="wbMetric"><span>历史事件</span><strong>{summary.event_count}</strong><em>高影响 {summary.high_impact_count}</em></div>
          <div className="wbMetric"><span>开放预警</span><strong>{summary.open_alert_count}</strong><em>人工复核 {summary.manual_review_count}</em></div>
        </section>

        <section className="wbTwoColumn">
          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">组合摘要</div>
                <h2>风险状态</h2>
              </div>
              <WatchlistRefreshButton watchlistId={watchlist.watchlist_id} />
            </div>
            <p className="wbLead">{summary.risk_summary || '暂无风险摘要。手动刷新组合事件后，这里会展示组合级影响判断。'}</p>
            <div className="wbChipRow">
              {summary.dominant_rules.map((rule) => <span className="wbChip" key={rule}>{rule}</span>)}
              {!summary.dominant_rules.length ? <span className="wbChip">暂无规则命中</span> : null}
            </div>
            <div className="wbList">
              {summary.priority_actions.map((action) => <div className="wbListItem" key={action}><strong>建议动作</strong><span>{action}</span></div>)}
              {!summary.priority_actions.length ? <div className="wbEmpty">暂无优先动作。</div> : null}
            </div>
          </div>

          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">今日主题</div>
                <h2>{briefing.title || '组合简报'}</h2>
              </div>
            </div>
            <p className="wbLead">{briefing.summary || '暂无组合简报。'}</p>
            <div className="wbChipRow">
              {briefing.themes.map((theme) => <span className="wbChip" key={theme}>{theme}</span>)}
              {!briefing.themes.length ? <span className="wbChip">暂无主题</span> : null}
            </div>
          </div>
        </section>

        <section className="wbPanel">
          <div className="wbPanelHead">
            <div>
              <div className="wbEyebrow">股票池</div>
              <h2>受影响股票</h2>
            </div>
            <Link className="wbTextButton" href={`/events?stock_codes=${stockQuery}`}>查看组合事件</Link>
          </div>
          <div className="wbTableWrap">
            <table className="wbTable">
              <thead><tr><th>股票</th><th>事件</th><th>高影响</th><th>预警</th><th>优先动作</th></tr></thead>
              <tbody>
                {(summary.impacted_stocks.length ? summary.impacted_stocks : watchlist.stock_codes.map((code) => ({ stock_code: code, stock_name: '', event_count: 0, high_impact_count: 0, alert_count: 0, risk_score: 0, risk_level: 'low', priority_action: '等待组合刷新', latest_event_at: '' }))).map((stock) => (
                  <tr key={stock.stock_code}>
                    <td><Link className="wbPrimaryText" href={`/stocks/${stock.stock_code}`}>{stock.stock_name || stock.stock_code}</Link><div className="wbMuted">{riskText(stock.risk_level)} · {stock.latest_event_at || '暂无事件'}</div></td>
                    <td>{stock.event_count}</td>
                    <td>{stock.high_impact_count}</td>
                    <td>{stock.alert_count}</td>
                    <td>{stock.priority_action || '保持观察'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="wbTwoColumn">
          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">关键事件</div>
                <h2>组合事件雷达</h2>
              </div>
              <Link className="wbTextButton" href={`/events?stock_codes=${stockQuery}&view=events`}>打开事件台</Link>
            </div>
            <div className="wbTableWrap">
              <table className="wbTable">
                <thead><tr><th>事件</th><th>股票</th><th>影响</th><th>动作</th></tr></thead>
                <tbody>
                  {events.items.slice(0, 8).map((event) => (
                    <tr key={event.event_id}>
                      <td><Link className="wbPrimaryText" href={`/events?view=events&selected_event_id=${event.event_id}`}>{event.title}</Link><div className="wbMuted">{event.summary || event.reason}</div></td>
                      <td>{event.stock_code}</td>
                      <td><span className={`wbBadge ${event.impact_level === 'high' ? 'wbBadgeDanger' : ''}`}>{event.impact_level}</span></td>
                      <td><EventAnalyzeButton eventId={event.event_id} label="点评" /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!events.items.length ? <div className="wbEmpty">暂无历史事件。点击“刷新组合事件”后会写入当前账号的事件历史。</div> : null}
            </div>
          </div>
          <RiskQueue alerts={alerts} compact />
        </section>
      </div>
    </WorkspaceShell>
  )
}
