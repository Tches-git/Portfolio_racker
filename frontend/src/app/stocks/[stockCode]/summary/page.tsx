import Link from 'next/link'

import { SearchShell } from '../../../../components/search-shell'
import { StockWorkspaceNav } from '../../../../components/stock-workspace-nav'
import { fetchLatestReport } from '../../../../lib/api'

export default async function StockSummaryPage({ params }: { params: Promise<{ stockCode: string }> }) {
  const { stockCode } = await params
  const latest = await fetchLatestReport(stockCode)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Detail Route · Summary</div>
            <h1>{latest?.stock.name || stockCode} 摘要详情</h1>
            <p>把产品页继续拆成更细粒度详情路由，后续可以分别承接摘要、导出、历史等独立视图。</p>
          </div>
          <Link className="ghostLink" href={`/stocks/${stockCode}`}>返回产品页</Link>
        </div>
      </section>

      <StockWorkspaceNav stockCode={stockCode} current="summary" />
      <SearchShell initialCode={stockCode} />

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">摘要详情</div>
              <h2>研究摘要详情</h2>
            </div>
          </div>
          <div className="card">
            <div className="itemTitle">{latest?.stock.name || stockCode}</div>
            <div className="itemMeta">{latest?.stock.industry || '未知行业'} · {latest?.generated_at || '暂无生成时间'}</div>
            <p>{latest?.summary.conclusion_brief || '暂无摘要内容，请先运行分析并启动 API。'}</p>
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">关键指标</div>
              <h2>摘要信号卡</h2>
            </div>
          </div>
          <div className="kpis kpisCompact">
            <div className="card"><div className="kpi-label">评级</div><div className="kpi-value">{latest?.summary.rating || '--'}</div></div>
            <div className="card"><div className="kpi-label">评分</div><div className="kpi-value">{latest ? latest.summary.rating_score.toFixed(1) : '--'}</div></div>
            <div className="card"><div className="kpi-label">每股价值</div><div className="kpi-value">{latest ? latest.valuation.per_share_value.toFixed(2) : '--'}</div></div>
            <div className="card"><div className="kpi-label">上涨空间</div><div className="kpi-value">{latest ? `${latest.valuation.upside.toFixed(1)}%` : '--'}</div></div>
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">研究上下文</div>
              <h2>研究上下文</h2>
            </div>
          </div>
          <div className="detailGrid">
            <div className="card">
              <div className="itemTitle">估值锚</div>
              <div className="metricStack">
                <div className="metricRow"><span>DCF 每股价值</span><strong>{latest ? latest.valuation.per_share_value.toFixed(2) : '--'}</strong></div>
                <div className="metricRow"><span>当前价格</span><strong>{latest ? latest.valuation.current_price.toFixed(2) : '--'}</strong></div>
                <div className="metricRow"><span>上涨空间</span><strong>{latest ? `${latest.valuation.upside.toFixed(1)}%` : '--'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">质量快照</div>
              <div className="metricStack">
                <div className="metricRow"><span>来源引用数</span><strong>{latest?.quality.source_reference_count ?? 0}</strong></div>
                <div className="metricRow"><span>占位来源数</span><strong>{latest?.quality.placeholder_source_count ?? 0}</strong></div>
                <div className="metricRow"><span>运行结果</span><strong>{latest?.run_metrics.success ? '成功' : '待补数据'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">后续动作</div>
              <div className="actionList">
                <Link className="downloadLink" href={`/stocks/${stockCode}/exports`}>查看导出中心</Link>
                <Link className="downloadLink" href={`/stocks/${stockCode}/history`}>查看历史脉络</Link>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
