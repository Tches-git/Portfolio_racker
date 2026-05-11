import Link from 'next/link'

import { WatchlistCreateForm } from '../../components/watchlist-create-form'
import { fetchMarketEvents, fetchTrackingAlerts, fetchWatchlists } from '../../lib/api'

async function buildWatchlistSummary(stockCodes: string[]) {
  const [events, alerts] = await Promise.all([
    fetchMarketEvents(stockCodes, 3).catch(() => ({ items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode: 'realtime' })),
    fetchTrackingAlerts(stockCodes, 3).catch(() => ({ items: [], total: 0, high_severity_count: 0, risk_alert_count: 0, source_degraded_count: 0 })),
  ])
  return { events, alerts }
}

export default async function WatchlistPage() {
  const watchlists = await fetchWatchlists().catch(() => ({ items: [], total: 0 }))
  const summaries = await Promise.all(watchlists.items.map((item) => buildWatchlistSummary(item.stock_codes)))

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Watchlist</div>
            <h1>组合跟踪</h1>
            <p>以自选股票池为中心聚合事件、预警与简报，让金融消息追踪围绕真实关注范围运转。</p>
          </div>
          <Link className="ghostLink" href="/events">全局事件流</Link>
        </div>
      </section>

      <div className="dashboardGrid">
        <div className="metricCard"><div className="statusLabel">组合数量</div><div className="metricCardValue">{watchlists.total}</div><div className="inlineMeta">当前工作区</div></div>
        <div className="metricCard"><div className="statusLabel">追踪股票</div><div className="metricCardValue">{new Set(watchlists.items.flatMap((item) => item.stock_codes)).size}</div><div className="inlineMeta">去重统计</div></div>
        <div className="metricCard"><div className="statusLabel">组合事件</div><div className="metricCardValue">{summaries.reduce((sum, item) => sum + item.events.total, 0)}</div><div className="inlineMeta">实时采集</div></div>
        <div className="metricCard"><div className="statusLabel">组合预警</div><div className="metricCardValue">{summaries.reduce((sum, item) => sum + item.alerts.total, 0)}</div><div className="inlineMeta">待处理</div></div>
      </div>

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Tracked Portfolios</div>
              <h2>追踪组合</h2>
            </div>
          </div>
          <div className="metricStack">
            {watchlists.items.map((watchlist, index) => {
              const summary = summaries[index]
              const stockQuery = watchlist.stock_codes.join(',')
              return (
                <div className="card" key={watchlist.watchlist_id}>
                  <div className="heroTop">
                    <div>
                      <Link className="itemTitle" href={`/watchlist/${watchlist.watchlist_id}`}>{watchlist.name}</Link>
                      <div className="inlineMeta">{watchlist.description || '暂无说明'} · 最近刷新 {watchlist.last_refreshed_at || '尚未手动刷新'}</div>
                    </div>
                    <span className="tag">{watchlist.stock_codes.length} 只股票</span>
                  </div>
                  <div className="chipRow">
                    {watchlist.stock_codes.map((code) => <Link className="chip" href={`/stocks/${code}`} key={code}>{code}</Link>)}
                  </div>
                  <div className="dashboardGrid">
                    <div className="metricCard"><div className="statusLabel">事件</div><div className="metricCardValue">{summary.events.total}</div><div className="inlineMeta">高影响 {summary.events.high_impact_count}</div></div>
                    <div className="metricCard"><div className="statusLabel">预警</div><div className="metricCardValue">{summary.alerts.total}</div><div className="inlineMeta">高优先级 {summary.alerts.high_severity_count}</div></div>
                    <div className="metricCard"><div className="statusLabel">来源</div><div className="metricCardValue">{summary.events.source_count}</div><div className="inlineMeta">覆盖渠道</div></div>
                    <div className="metricCard"><div className="statusLabel">降级</div><div className="metricCardValue">{summary.events.placeholder_count}</div><div className="inlineMeta">需复核</div></div>
                  </div>
                  <div className="actionList compactActions">
                    <Link className="downloadLink" href={`/watchlist/${watchlist.watchlist_id}`}>打开组合详情</Link>
                    <Link className="downloadLink" href={`/events?stock_codes=${stockQuery}&mode=history`}>查看组合事件</Link>
                    <Link className="downloadLink" href={`/alerts?stock_codes=${stockQuery}`}>处理组合预警</Link>
                    <Link className="downloadLink" href={`/briefing?stock_codes=${stockQuery}`}>生成组合简报</Link>
                  </div>
                </div>
              )
            })}
            {!watchlists.items.length ? <div className="emptyState">暂无组合。可以先创建一个股票池，或运行一次股票分析沉淀默认追踪范围。</div> : null}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Create</div>
              <h2>新增组合</h2>
            </div>
          </div>
          <WatchlistCreateForm />
        </section>
      </div>
    </main>
  )
}
