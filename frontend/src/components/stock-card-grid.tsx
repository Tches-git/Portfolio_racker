import Link from 'next/link'

import type { WorkspaceStocksResponse } from '../lib/types'

export function StockCardGrid({ stocks }: { stocks: WorkspaceStocksResponse['items'] }) {
  return (
    <section className="panel span-12">
      <div className="sectionHead">
        <div>
          <div className="sectionEyebrow">Portfolio</div>
          <h2>组合跟踪</h2>
        </div>
        <span className="inlineMeta">按最近沉淀的研究记录排序</span>
      </div>
      <div className="stockGrid">
        {stocks.length ? stocks.slice(0, 8).map((item) => (
          <Link className="stockCard" href={`/stocks/${item.code}`} key={item.code}>
            <div>
              <div className="itemTitle">{item.name || item.code}</div>
              <div className="itemMeta">{item.code}</div>
            </div>
            <div className="metricStack">
              <div className="metricRow"><span>分析次数</span><strong>{item.count}</strong></div>
              <div className="metricRow"><span>最近记录</span><strong>{item.latest || '--'}</strong></div>
            </div>
          </Link>
        )) : <div className="emptyState">暂无组合股票。先运行一次分析后，这里会自动形成跟踪列表。</div>}
      </div>
    </section>
  )
}
