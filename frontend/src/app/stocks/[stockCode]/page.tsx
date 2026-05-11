import Link from 'next/link'

import { AnalysisLauncher } from '../../../components/analysis-launcher'
import { LoadingSkeleton } from '../../../components/loading-skeleton'
import { RecentRunsPanel } from '../../../components/recent-runs-panel'
import { ReportDashboard } from '../../../components/report-dashboard'
import { SearchShell } from '../../../components/search-shell'
import { StockNewsPanel } from '../../../components/stock-news-panel'
import { StockWorkspaceNav } from '../../../components/stock-workspace-nav'
import { fetchLatestReport, fetchRecentRuns, fetchStockEvents, fetchStockHistory, fetchStockNews } from '../../../lib/api'

export default async function StockPage({ params }: { params: Promise<{ stockCode: string }> }) {
    const { stockCode } = await params
    const latest = await fetchLatestReport(stockCode)
    const history = await fetchStockHistory(stockCode)
    const recentRuns = await fetchRecentRuns(6)
    const news = await fetchStockNews(stockCode, 6).catch(() => ({ stock_code: stockCode, items: [], total: 0 }))
    const events = await fetchStockEvents(stockCode, 6).catch(() => ({ stock_code: stockCode, stock_name: '', items: [], total: 0, high_impact_count: 0, placeholder_count: 0, duplicate_count: 0, source_count: 0, mode: 'realtime' }))
    const stockRuns = recentRuns.items.filter((item) => item.stock_code === stockCode)
    const hasData = Boolean(latest)

    return (
        <main>
            <section className="hero stockHero">
                <div className="heroTop">
                    <div>
                        <div className="eyebrow">Stock Workspace</div>
                        <h1>{latest?.stock.name || stockCode}</h1>
                        <p>{stockCode} · {latest?.stock.industry || '股票研究工作台'}。先看新闻与状态，再按需发起分析、查看历史或导出。</p>
                    </div>
                    <Link className="ghostLink" href="/">返回首页</Link>
                </div>
            </section>

            <StockWorkspaceNav stockCode={stockCode} current="overview" />
            <SearchShell initialCode={stockCode} />
            <div className="dashboardGrid">
                <div className="metricCard"><div className="statusLabel">数据状态</div><div className="metricCardValue">{hasData ? '已就绪' : '待分析'}</div><div className="inlineMeta">{hasData ? 'API 已返回最新报告' : '可先发起浏览器分析'}</div></div>
                <div className="metricCard"><div className="statusLabel">相关任务</div><div className="metricCardValue">{stockRuns.length}</div><div className="inlineMeta">当前股票最近任务</div></div>
                <div className="metricCard"><div className="statusLabel">失败任务</div><div className="metricCardValue">{stockRuns.filter((item) => item.status === 'failed').length}</div><div className="inlineMeta">需要优先处理</div></div>
                <div className="metricCard"><div className="statusLabel">最新新闻</div><div className="metricCardValue">{news.total}</div><div className="inlineMeta">东方财富 / 新浪回退</div></div>
                <div className="metricCard"><div className="statusLabel">追踪事件</div><div className="metricCardValue">{events.total}</div><div className="inlineMeta">高影响 {events.high_impact_count} · 来源 {events.source_count}</div></div>
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
                                </div>
                            </div>
                        ))}
                        {!events.items.length ? <div className="emptyState">暂无可展示事件。</div> : null}
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
