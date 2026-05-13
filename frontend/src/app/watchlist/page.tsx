import Link from 'next/link'

import { WatchlistCreateForm } from '../../components/watchlist-create-form'
import { WorkspaceShell } from '../../components/workbench/workspace-shell'
import { fetchDashboard } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'

function riskText(level: string) {
  if (level === 'high') return '高风险'
  if (level === 'medium') return '中风险'
  return '低风险'
}

export default async function WatchlistPage() {
  const apiOptions = await serverApiOptions()
  const dashboard = await fetchDashboard(apiOptions)
  const watchlists = dashboard.watchlists.items
  const summary = dashboard.portfolio_summary

  return (
    <WorkspaceShell
      eyebrow="组合管理"
      title="组合跟踪"
      description="组合是事件、预警和研报任务的追踪范围。新账号不会加载旧数据，只有你创建并刷新过的组合会沉淀事件。"
      actions={dashboard.actions}
    >
      <div className="wbStack">
        <section className="wbMetricGrid">
          <div className="wbMetric"><span>组合数量</span><strong>{dashboard.watchlists.total}</strong><em>当前账号</em></div>
          <div className="wbMetric"><span>追踪股票</span><strong>{summary.stock_count}</strong><em>组合去重</em></div>
          <div className="wbMetric"><span>开放预警</span><strong>{summary.alert_count}</strong><em>人工复核 {summary.manual_review_count}</em></div>
          <div className="wbMetric"><span>组合风险</span><strong>{summary.risk_score}</strong><em>{riskText(summary.risk_level)}</em></div>
        </section>

        <section className="wbTwoColumn">
          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">组合列表</div>
                <h2>当前追踪范围</h2>
              </div>
              <Link className="wbTextButton" href="/events">事件预警处理台</Link>
            </div>
            <div className="wbTableWrap">
              <table className="wbTable">
                <thead>
                  <tr>
                    <th>组合</th>
                    <th>股票池</th>
                    <th>最近刷新</th>
                    <th>动作</th>
                  </tr>
                </thead>
                <tbody>
                  {watchlists.map((watchlist) => (
                    <tr key={watchlist.watchlist_id}>
                      <td>
                        <Link className="wbPrimaryText" href={`/watchlist/${watchlist.watchlist_id}`}>{watchlist.name}</Link>
                        <div className="wbMuted">{watchlist.description || '暂无说明'}</div>
                      </td>
                      <td>
                        <div className="wbChipRow">
                          {watchlist.stock_codes.slice(0, 6).map((code) => <span className="wbChip" key={code}>{code}</span>)}
                          {watchlist.stock_codes.length > 6 ? <span className="wbChip">+{watchlist.stock_codes.length - 6}</span> : null}
                        </div>
                      </td>
                      <td>{watchlist.last_refreshed_at || '尚未刷新'}</td>
                      <td><Link className="wbTextButton" href={`/watchlist/${watchlist.watchlist_id}`}>打开</Link></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!watchlists.length ? <div className="wbEmpty">暂无组合。右侧创建第一个组合后，驾驶舱才会开始沉淀事件和预警。</div> : null}
            </div>
          </div>

          <div className="wbPanel">
            <div className="wbPanelHead">
              <div>
                <div className="wbEyebrow">创建范围</div>
                <h2>新建组合</h2>
              </div>
            </div>
            <WatchlistCreateForm />
          </div>
        </section>
      </div>
    </WorkspaceShell>
  )
}
