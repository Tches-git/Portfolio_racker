import Link from 'next/link'

import type { AnalysisRunListResponse } from '../lib/types'

const FAVORITES = [
  { name: '贵州茅台', code: '600519' },
  { name: '宁德时代', code: '300750' },
  { name: '招商银行', code: '600036' },
]

export function WorkspaceInsights({ stockCode, workspace }: { stockCode: string; workspace: AnalysisRunListResponse }) {
  return (
    <section className="panel span-12">
      <div className="sectionHead">
        <div>
          <div className="sectionEyebrow">Workspace</div>
          <h2>研究工作台能力</h2>
        </div>
      </div>
      <div className="detailGrid">
        <div className="card">
          <div className="itemTitle">快捷收藏</div>
          <div className="pillRow">
            {FAVORITES.map((item) => (
              <Link className="chip" key={item.code} href={`/stocks/${item.code}`}>
                {item.name}
              </Link>
            ))}
          </div>
        </div>
        <div className="card">
          <div className="itemTitle">最近访问</div>
          <p className="bodyText">当前正在查看 <strong>{stockCode}</strong>，可继续进入摘要、历史、导出或任务详情页。</p>
          <div className="actionList compactActions">
            <Link className="downloadLink" href={`/stocks/${stockCode}/summary`}>摘要详情</Link>
            <Link className="downloadLink" href={`/stocks/${stockCode}/history`}>历史脉络</Link>
            <Link className="downloadLink" href="/runs">任务中心</Link>
          </div>
        </div>
        <div className="card">
          <div className="itemTitle">任务中心习惯</div>
          <div className="metricStack">
            <div className="metricRow"><span>推荐入口</span><strong>全局运行中心</strong></div>
            <div className="metricRow"><span>查看顺序</span><strong>任务中心 → 任务详情</strong></div>
            <div className="metricRow"><span>回流路径</span><strong>股票页 / 导出中心</strong></div>
          </div>
        </div>
        <div className="card">
          <div className="itemTitle">组合工作区</div>
          <div className="metricStack">
            <div className="metricRow"><span>跟踪股票</span><strong>{workspace.workspace.tracked_stocks.length}</strong></div>
            <div className="metricRow"><span>最活跃标的</span><strong>{workspace.workspace.most_active_stock || '--'}</strong></div>
            <div className="metricRow"><span>失败标的数</span><strong>{workspace.workspace.failed_stock_count}</strong></div>
          </div>
        </div>
        <div className="card">
          <div className="itemTitle">研究模板</div>
          <p className="bodyText">下一步可继续扩成“快速跟踪 / 深度研判 / 结果复核”等预设模板，但当前先保持兼容层最小实现。</p>
        </div>
      </div>
    </section>
  )
}
