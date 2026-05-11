import Link from 'next/link'

import { AnalysisLauncher } from '../../../components/analysis-launcher'
import { LoadingSkeleton } from '../../../components/loading-skeleton'
import { RecentRunsPanel } from '../../../components/recent-runs-panel'
import { ReportDashboard } from '../../../components/report-dashboard'
import { SearchShell } from '../../../components/search-shell'
import { StockNewsPanel } from '../../../components/stock-news-panel'
import { StockWorkspaceNav } from '../../../components/stock-workspace-nav'
import { fetchLatestReport, fetchRecentRuns, fetchStockEvents, fetchStockHistory, fetchStockNews, fetchWatchlists } from '../../../lib/api'

export default async function StockPage({ params }: { params: Promise<{ stockCode: string }> }) {
    const { stockCode } = await params
    const latest = await fetchLatestReport(stockCode).catch(() => null)
    const history = await fetchStockHistory(stockCode).catch(() => null)
    const recentRuns = await fetchRecentRuns(6).catch(() => ({ items: [] }))
    const news = await fetchStockNews(stockCode, 6).catch(() => ({ stock_code: stockCode, items: [], total: 0 }))
    const events = await fetchStockEvents(stockCode, 6).catch(() => ({ stock_code: stockCode, stock_name: '', items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode: 'realtime' }))
    const watchlists = await fetchWatchlists().catch(() => ({ items: [], total: 0 }))
    const stockRuns = recentRuns.items.filter((item) => item.stock_code === stockCode)
    const relatedWatchlists = watchlists.items.filter((item) => item.stock_codes.includes(stockCode))
    const hasData = Boolean(latest)

    return (
        <main>
            <section className="hero stockHero">
                <div className="heroTop">
                    <div>
                        <div className="eyebrow">Stock Workspace</div>
                        <h1>{latest?.stock.name || stockCode}</h1>
                        <p>{stockCode} · {latest?.stock.industry || '股票研究工作台'}。围绕新闻、事件、组合与研报任务建立单股情报中心。</p>
                    </div>
                    <div className="actionList compactActions">
                        <Link className="ghostLink" href="/">返回首页</Link>
                        <Link className="ghostLink" href={`/briefing?stock_codes=${stockCode}`}>今日简报</Link>
                        <Link className="ghostLink" href={`/events?stock=${stockCode}&mode=history`}>历史事件</Link>
                    </div>
                </div>
            </section>

            <StockWorkspaceNav stockCode={stockCode} current="overview" />
            <SearchShell initialCode={stockCode} />
            <div className="dashboardGrid">
                <div className="metricCard"><div className="statusLabel">数据状态</div><div className="metricCardValue">{hasData ? '已就绪' : '待分析'}</div><div className="inlineMeta">{hasData ? 'API 已返回最新报告' : '可先发起浏览器分析'}</div></div>
                <div className="metricCard"><div className="statusLabel">追踪事件</div><div className="metricCardValue">{events.total}</div><div className="inlineMeta">来源 {events.source_count} · 降级 {events.placeholder_count}</div></div>
                <div className="metricCard"><div className="statusLabel">高影响事件</div><div className="metricCardValue">{events.high_impact_count}</div><div className="inlineMeta">建议优先复核</div></div>
                <div className="metricCard"><div className="statusLabel">所属组合</div><div className="metricCardValue">{relatedWatchlists.length}</div><div className="inlineMeta">可进入组合级追踪</div></div>
                <div className="metricCard"><div className="statusLabel">相关任务</div><div className="metricCardValue">{stockRuns.length}</div><div className="inlineMeta">失败 {stockRuns.filter((item) => item.status === 'failed').length}</div></div>
                <div className="metricCard"><div className="statusLabel">最新新闻</div><div className="metricCardValue">{news.total}</div><div className="inlineMeta">东方财富 / 新浪回退</div></div>
            </div>
            <div className="grid">
                <StockNewsPanel news={news} />
                <section className="panel span-5">
                    <div className="sectionHead">
                        <div>
                            <div className="sectionEyebrow">Timeline</div>
                            <h2>事件追踪</h2>
                        </div>
                        <Link className="downloadLink" href={`/stocks/${stockCode}/timeline`}>打开时间线</Link>
                    </div>
                    <div className="timelineList">
                        {events.items.slice(0, 4).map((event) => (
                            <div className="timelineCard" key={event.event_id}>
                                <div className="timelineDot" />
                                <div className="card timelineBody">
                                    <div className="itemTitle">{event.title}</div>
                                    <div className="inlineMeta">{event.event_type} · {event.impact_level} · {event.provider || event.source}</div>
                                    <p className="bodyText">{event.reason}</p>
                                    <div className="chipRow">
                                        <Link className="downloadLink" href={`/events/${event.event_id}`}>事件详情</Link>
                                        <Link className="downloadLink" href={`/stocks/${stockCode}/timeline`}>完整时间线</Link>
                                    </div>
                                </div>
                            </div>
                        ))}
                        {!events.items.length ? <div className="emptyState">暂无可展示事件。</div> : null}
                    </div>
                </section>
                <section className="panel span-5">
                    <div className="sectionHead">
                        <div>
                            <div className="sectionEyebrow">Portfolio Context</div>
                            <h2>所属组合</h2>
                        </div>
                        <Link className="downloadLink" href="/watchlist">组合列表</Link>
                    </div>
                    <div className="metricStack">
                        {relatedWatchlists.map((watchlist) => (
                            <div className="card" key={watchlist.watchlist_id}>
                                <div className="itemTitle">{watchlist.name}</div>
                                <div className="inlineMeta">{watchlist.stock_codes.length} 只股票 · 最近刷新 {watchlist.last_refreshed_at || '尚未手动刷新'}</div>
                                <div className="chipRow">
                                    <Link className="downloadLink" href={`/watchlist/${watchlist.watchlist_id}`}>进入组合详情</Link>
                                    <Link className="downloadLink" href={`/events?stock_codes=${watchlist.stock_codes.join(',')}&mode=history`}>组合事件</Link>
                                </div>
                            </div>
                        ))}
                        {!relatedWatchlists.length ? <div className="emptyState">这只股票暂未加入任何组合，可到组合跟踪页创建股票池。</div> : null}
                    </div>
                </section>
                <AnalysisLauncher initialCode={stockCode} initialRuns={stockRuns} />
                <RecentRunsPanel runs={stockRuns} />
            </div>
            {!latest ? <div className="emptyState">当前股票暂无可展示结果，请先运行分析并确认 API 可访问。</div> : null}
            {!latest ? <LoadingSkeleton sections={2} /> : null}
            <ReportDashboard latest={latest} history={history} />
        </main>
    )
}
