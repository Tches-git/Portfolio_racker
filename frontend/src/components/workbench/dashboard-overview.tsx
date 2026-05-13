import Link from 'next/link'

import type { DashboardResponse, MarketEvent } from '../../lib/types'
import { WorkbenchIcon } from './icons'
import { RiskQueue } from './risk-queue'
import { SetupWizard } from './setup-wizard'

function riskText(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}

function eventTitle(event: MarketEvent) {
  return event.summary || event.reason || '暂无摘要'
}

export function DashboardOverview({ data }: { data: DashboardResponse }) {
  if (data.mode === 'setup') {
    return <SetupWizard setup={data.setup} />
  }

  const summary = data.portfolio_summary
  const primaryWatchlist = data.watchlists.items.find((item) => item.watchlist_id === summary.primary_watchlist_id) || data.watchlists.items[0]

  return (
    <div className="wbStack">
      <section className="wbMetricGrid">
        <div className="wbMetric">
          <span>风险分</span>
          <strong>{summary.risk_score}</strong>
          <em>{riskText(summary.risk_level)}</em>
        </div>
        <div className="wbMetric">
          <span>开放预警</span>
          <strong>{summary.alert_count}</strong>
          <em>人工复核 {summary.manual_review_count}</em>
        </div>
        <div className="wbMetric">
          <span>追踪事件</span>
          <strong>{summary.event_count}</strong>
          <em>高影响 {summary.high_impact_count}</em>
        </div>
        <div className="wbMetric">
          <span>股票池</span>
          <strong>{summary.stock_count}</strong>
          <em>{summary.watchlist_count} 个组合</em>
        </div>
      </section>

      <section className="wbTwoColumn">
        <div className="wbPanel">
          <div className="wbPanelHead">
            <div>
              <div className="wbEyebrow">组合风险</div>
              <h2>{primaryWatchlist?.name || '主组合'}</h2>
            </div>
            {primaryWatchlist ? <Link className="wbTextButton" href={`/watchlist/${primaryWatchlist.watchlist_id}`}>进入组合</Link> : null}
          </div>
          <p className="wbLead">{summary.risk_summary || '暂无风险摘要。'}</p>
          <div className="wbActionGrid">
            <Link className="wbActionTile" href={primaryWatchlist ? `/watchlist/${primaryWatchlist.watchlist_id}` : '/watchlist'}>
              <WorkbenchIcon name="portfolio" />
              <span>组合驾驶舱</span>
            </Link>
            <Link className="wbActionTile" href="/events?view=alerts">
              <WorkbenchIcon name="alerts" />
              <span>处理预警</span>
            </Link>
            <Link className="wbActionTile" href="/runs">
              <WorkbenchIcon name="runs" />
              <span>任务交付</span>
            </Link>
          </div>
        </div>
        <RiskQueue alerts={data.risk_queue} compact />
      </section>

      <section className="wbTwoColumn">
        <div className="wbPanel">
          <div className="wbPanelHead">
            <div>
              <div className="wbEyebrow">今日主题</div>
              <h2>组合简报</h2>
            </div>
            <Link className="wbTextButton" href="/events">查看事件</Link>
          </div>
          <p className="wbLead">{data.today_briefing.summary || '暂无简报。刷新组合后会在这里汇总今日主题。'}</p>
          <div className="wbChipRow">
            {data.today_briefing.themes.slice(0, 8).map((theme) => <span className="wbChip" key={theme}>{theme}</span>)}
            {!data.today_briefing.themes.length ? <span className="wbChip">暂无主题</span> : null}
          </div>
        </div>
        <div className="wbPanel">
          <div className="wbPanelHead">
            <div>
              <div className="wbEyebrow">任务</div>
              <h2>最近交付</h2>
            </div>
            <Link className="wbTextButton" href="/runs">全部任务</Link>
          </div>
          <div className="wbList">
            {data.recent_runs.items.slice(0, 5).map((run) => (
              <Link className="wbListItem" href={`/runs/${run.run_id}`} key={run.run_id}>
                <strong>{run.stock_code}</strong>
                <span>{run.status} · {run.updated_at || run.created_at || '暂无时间'}</span>
              </Link>
            ))}
            {!data.recent_runs.items.length ? <div className="wbEmpty">当前还没有研报任务。</div> : null}
          </div>
        </div>
      </section>

      <section className="wbPanel">
        <div className="wbPanelHead">
          <div>
            <div className="wbEyebrow">事件明细</div>
            <h2>最新关键事件</h2>
          </div>
          <Link className="wbTextButton" href="/events?view=events">打开事件台</Link>
        </div>
        <div className="wbTableWrap">
          <table className="wbTable">
            <thead>
              <tr>
                <th>事件</th>
                <th>股票</th>
                <th>类型</th>
                <th>影响</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              {data.latest_events.items.slice(0, 8).map((event) => (
                <tr key={event.event_id}>
                  <td>
                    <Link className="wbPrimaryText" href={`/events?view=events&selected_event_id=${event.event_id}`}>{event.title}</Link>
                    <div className="wbMuted">{eventTitle(event)}</div>
                  </td>
                  <td>{event.stock_code}</td>
                  <td>{event.event_type}</td>
                  <td><span className={`wbBadge ${event.impact_level === 'high' ? 'wbBadgeDanger' : ''}`}>{event.impact_level}</span></td>
                  <td>{event.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {!data.latest_events.items.length ? <div className="wbEmpty">暂无历史事件。进入组合详情后手动刷新即可沉淀事件。</div> : null}
        </div>
      </section>
    </div>
  )
}
