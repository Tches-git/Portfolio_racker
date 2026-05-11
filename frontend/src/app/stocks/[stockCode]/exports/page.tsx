import Link from 'next/link'

import { RunStatusBar } from '../../../../components/run-status-bar'
import { SearchShell } from '../../../../components/search-shell'
import { StockWorkspaceNav } from '../../../../components/stock-workspace-nav'
import { API_BASE, fetchLatestReport, fetchRecentRuns } from '../../../../lib/api'
import type { AnalysisRunResponse, LatestReportResponse } from '../../../../lib/types'

function previewHint(item: LatestReportResponse['exports'][number]) {
  if (item.kind === 'html') return '浏览器预览'
  if (item.kind === 'markdown') return '文本查看'
  if (item.kind === 'json') return '结构化查看'
  return '下载交付物'
}

function previewMode(item: LatestReportResponse['exports'][number] | null) {
  if (!item) return '暂无预览'
  if (item.kind === 'html') return '内嵌 HTML 预览'
  if (item.kind === 'markdown') return 'Markdown 文本预览'
  if (item.kind === 'sources') return '来源 JSON 预览'
  return '下载后预览'
}

function selectedArtifact(items: LatestReportResponse['exports'], selectedFilename?: string) {
  if (selectedFilename) {
    const matched = items.find((item) => item.filename === selectedFilename)
    if (matched) return matched
  }
  return items[0] || null
}

function latestStockRun(runs: AnalysisRunResponse[], stockCode: string) {
  return runs.find((item) => item.stock_code === stockCode) || null
}

export default async function StockExportsPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams?: Promise<{ selected?: string }>
}) {
  const { stockCode } = await params
  const resolvedSearchParams = searchParams ? await searchParams : undefined
  const latest = await fetchLatestReport(stockCode)
  const recentRuns = await fetchRecentRuns(8)
  const currentArtifact = selectedArtifact(latest?.exports || [], resolvedSearchParams?.selected)
  const currentRun = latestStockRun(recentRuns.items, stockCode)
  const hasData = Boolean(latest)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Detail Route · Exports</div>
            <h1>{latest?.stock.name || stockCode} 导出中心</h1>
            <p>复用现有只读导出 contract 与下载接口，把 Markdown / HTML / PDF / JSON 等交付物组织成更接近产品后台的导出工作区。</p>
          </div>
          <Link className="ghostLink" href={`/stocks/${stockCode}`}>返回产品页</Link>
        </div>
      </section>

      <RunStatusBar stockCode={stockCode} hasData={hasData} statusHint="导出中心继续复用统一下载链路，后续可在这里扩成更完整交付中心。" />
      <StockWorkspaceNav stockCode={stockCode} current="exports" />
      <SearchShell initialCode={stockCode} />

      {!latest ? <div className="emptyState">当前暂无可展示导出物，请先运行分析并确认 <code>python main.py api</code> 已启动。</div> : null}

      <div className="grid">
        <section className="panel span-7">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Artifacts</div>
              <h2>导出物清单</h2>
            </div>
          </div>
          <div className="selectionHint">点击导出物的“设为当前”即可把右侧工作台切到该交付物，继续沿统一下载 contract 工作。</div>
          <div className="list">
            {(latest?.exports || []).length ? latest!.exports.map((item) => {
              const isSelected = currentArtifact?.filename === item.filename
              return (
                <div className={`card${isSelected ? ' selectedCard' : ''}`} key={item.filename}>
                  <div className="itemTitle">{item.kind}</div>
                  <div className="itemMeta">{item.filename}</div>
                  <div className="pathText">{item.path}</div>
                  <div className="exportActions">
                    <a className="downloadLink" href={`${API_BASE}${item.download_url}`} target="_blank" rel="noreferrer">下载 / 查看</a>
                    <Link className="ghostLink" href={`/stocks/${stockCode}/exports?selected=${encodeURIComponent(item.filename)}`}>{isSelected ? '当前已选' : '设为当前'}</Link>
                    <span className="inlineMeta">{previewHint(item)}</span>
                  </div>
                </div>
              )
            }) : <div className="card">当前未发现导出物。</div>}
          </div>
        </section>

        <section className="panel span-5">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Control</div>
              <h2>导出工作台</h2>
            </div>
          </div>
          <div className="detailGrid detailGridSingle">
            <div className="card">
              <div className="itemTitle">最近生成</div>
              <div className="metricStack">
                <div className="metricRow"><span>生成时间</span><strong>{latest?.generated_at || '--'}</strong></div>
                <div className="metricRow"><span>导出数量</span><strong>{latest?.exports.length ?? 0}</strong></div>
                <div className="metricRow"><span>运行状态</span><strong>{latest?.run_metrics.success ? '成功' : '待补数据'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">当前选中导出物</div>
              {currentArtifact ? (
                <div className="metricStack">
                  <div className="metricRow"><span>类型</span><strong>{currentArtifact.kind}</strong></div>
                  <div className="metricRow"><span>文件名</span><strong>{currentArtifact.filename}</strong></div>
                  <div className="metricRow"><span>预览方式</span><strong>{previewMode(currentArtifact)}</strong></div>
                </div>
              ) : <p className="bodyText">暂无可选导出物。</p>}
            </div>
            <div className="card">
              <div className="itemTitle">导出预览</div>
              {currentArtifact ? (
                <div className="metricStack">
                  <div className="pathText">统一下载路径：{currentArtifact.download_url}</div>
                  <a className="downloadLink" href={`${API_BASE}${currentArtifact.download_url}`} target="_blank" rel="noreferrer">打开预览 / 下载</a>
                </div>
              ) : <p className="bodyText">请选择交付物后预览。</p>}
            </div>
            <div className="card">
              <div className="itemTitle">关联任务</div>
              {currentRun ? (
                <div className="metricStack">
                  <div className="metricRow"><span>任务状态</span><strong>{currentRun.status}</strong></div>
                  <div className="metricRow"><span>最近事件</span><strong>{currentRun.last_event || '--'}</strong></div>
                  <div className="metricRow"><span>导出物</span><strong>{currentRun.exports.length}</strong></div>
                </div>
              ) : <p className="bodyText">当前股票暂无关联运行任务。</p>}
            </div>
            <div className="card">
              <div className="itemTitle">交付概览</div>
              <div className="metricStack">
                <div className="metricRow"><span>可预览</span><strong>{latest?.delivery.previewable_count ?? 0}</strong></div>
                <div className="metricRow"><span>可下载</span><strong>{latest?.delivery.downloadable_count ?? 0}</strong></div>
                <div className="metricRow"><span>最新交付</span><strong>{latest?.delivery.latest_export_filename || '--'}</strong></div>
              </div>
            </div>
            <div className="card">
              <div className="itemTitle">接口约定</div>
              <p className="bodyText">当前页面复用 <code>{latest?.delivery.contract_path || '/api/v1/exports/{filename}'}</code> 作为统一下载链路，后续扩展导出中心时无需另起下载机制。</p>
            </div>
            <div className="card">
              <div className="itemTitle">后续产品化方向</div>
              <div className="actionList">
                <Link className="downloadLink" href={`/stocks/${stockCode}/summary`}>回到摘要详情</Link>
                <Link className="downloadLink" href={`/stocks/${stockCode}/history`}>查看历史脉络</Link>
                {currentRun ? <Link className="downloadLink" href={`/runs/${currentRun.run_id}`}>进入任务详情</Link> : null}
              </div>
            </div>
          </div>
        </section>

        <section className="panel span-12">
          <div className="sectionHead">
            <div>
              <div className="sectionEyebrow">Delivery</div>
              <h2>交付说明</h2>
            </div>
          </div>
          <div className="detailGrid">
            {(latest?.exports || []).map((item) => (
              <div className="card" key={`${item.filename}-guide`}>
                <div className="itemTitle">{item.kind} 使用建议</div>
                <div className="itemMeta">{item.filename}</div>
                <p className="bodyText">
                  {item.kind === 'markdown' ? '适合继续编辑、沉淀研究文本与版本对比。' : item.kind === 'html' ? '适合浏览器展示与分享预览。' : item.kind === 'pdf' ? '适合固定版式交付或归档。' : item.kind === 'json' ? '适合后续自动化消费与结构化接入。' : '可作为运行产物进行下载与归档。'}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
