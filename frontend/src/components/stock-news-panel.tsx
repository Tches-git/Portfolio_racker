import type { StockNewsResponse } from '../lib/types'

export function StockNewsPanel({ news }: { news: StockNewsResponse }) {
  return (
    <section className="panel span-12">
      <div className="sectionHead">
        <div>
          <div className="sectionEyebrow">实时新闻</div>
          <h2>最新新闻</h2>
        </div>
        <span className="inlineMeta">{news.total} 条 · 东方财富优先，新浪搜索回退</span>
      </div>
      <div className="detailGrid">
        {news.items.length ? news.items.map((item, index) => (
          <div className="card" key={`${item.title}-${index}`}>
            <div className="itemTitle">{item.title || '未命名新闻'}</div>
            <div className="itemMeta">{item.time || '--'} · {item.source || item.channel || 'news'}</div>
            <p className="bodyText">{item.content || '暂无摘要'}</p>
            {item.url ? <a className="downloadLink" href={item.url} target="_blank" rel="noreferrer">打开来源</a> : null}
          </div>
        )) : <div className="emptyState">当前未获取到新闻，可稍后重试或运行完整分析。</div>}
      </div>
    </section>
  )
}
