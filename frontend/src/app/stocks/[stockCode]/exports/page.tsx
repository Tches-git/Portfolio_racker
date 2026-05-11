import Link from 'next/link'

import { RunStatusBar } from '../../../../components/run-status-bar'
import { SearchShell } from '../../../../components/search-shell'
import { StockWorkspaceNav } from '../../../../components/stock-workspace-nav'
import { API_BASE, fetchLatestReport, fetchRecentRuns } from '../../../../lib/api'
import type { AnalysisRunResponse, LatestReportResponse } from '../../../../lib/types'

type ExportArtifact = LatestReportResponse['exports'][number]

const EXPORT_CATEGORIES = [
  { key: 'all', label: '全部' },
  { key: 'report', label: '研报正文' },
  { key: 'commentary', label: '事件点评' },
  { key: 'presentation', label: '展示交付' },
  { key: 'sources', label: '来源数据' },
  { key: 'logs', label: '运行日志' },
  { key: 'other', label: '其他' },
]

function previewHint(item: LatestReportResponse['exports'][number]) {
  if (item.kind === 'html') return '浏览器预览'
  if (item.kind === 'markdown') return '文本查看'
  if (item.kind === 'event_commentary') return '事件点评'
  if (item.kind === 'json') return '结构化查看'
  return '下载交付物'
}

function previewMode(item: LatestReportResponse['exports'][number] | null) {
  if (!item) return '暂无预览'
  if (item.kind === 'html') return '内嵌 HTML 预览'
  if (item.kind === 'markdown') return 'Markdown 文本预览'
  if (item.kind === 'event_commentary') return '事件点评 Markdown 预览'
  if (item.kind === 'sources') return '来源 JSON 预览'
  return '下载后预览'
}

function selectedArtifact(items: ExportArtifact[], selectedFilename?: string) {
  if (selectedFilename) {
    const matched = items.find((item) => item.filename === selectedFilename)
    if (matched) return matched
  }
  return items[0] || null
}

function latestStockRun(runs: AnalysisRunResponse[], stockCode: string) {
  return runs.find((item) => item.stock_code === stockCode) || null
}

function mergeArtifacts(primary: ExportArtifact[], secondary: ExportArtifact[]) {
  const byFilename = new Map<string, ExportArtifact>()
  ;[...primary, ...secondary].forEach((item) => {
    if (!item.filename || byFilename.has(item.filename)) return
    byFilename.set(item.filename, item)
  })
  return Array.from(byFilename.values())
}

function artifactCategory(item: ExportArtifact) {
  if (item.kind === 'event_commentary' || item.filename.startsWith('event_commentary_')) return 'commentary'
  if (item.kind === 'markdown') return 'report'
  if (item.kind === 'html' || item.kind === 'pdf') return 'presentation'
  if (item.kind === 'sources' || item.kind === 'json' || item.filename.endsWith('.json')) return 'sources'
  if (item.kind === 'trace' || item.filename.endsWith('.log')) return 'logs'
  return 'other'
}

function categoryCounts(items: ExportArtifact[]) {
  const counts: Record<string, number> = { all: items.length }
  EXPORT_CATEGORIES.forEach((category) => {
    if (category.key !== 'all') counts[category.key] = 0
  })
  items.forEach((item) => {
    const category = artifactCategory(item)
    counts[category] = (counts[category] || 0) + 1
  })
  return counts
}

export default async function StockExportsPage({
  params,
  searchParams,
}: {
  params: Promise<{ stockCode: string }>
  searchParams?: Promise<{ selected?: string; category?: string }>
}) {
  const { stockCode } = await params
  const resolvedSearchParams = searchParams ? await searchParams : undefined
  const latest = await fetchLatestReport(stockCode)
  const recentRuns = await fetchRecentRuns(8)
  const currentRun = latestStockRun(recentRuns.items, stockCode)
  const allArtifacts = mergeArtifacts(latest?.exports || [], currentRun?.exports || [])
  const activeCategory = EXPORT_CATEGORIES.some((item) => item.key === resolvedSearchParams?.category) ? resolvedSearchParams?.category || 'all' : 'all'
  const visibleArtifacts = activeCategory === 'all' ? allArtifacts : allArtifacts.filter((item) => artifactCategory(item) === activeCategory)
  const counts = categoryCounts(allArtifacts)
  const currentArtifact = selectedArtifact(visibleArtifacts.length ? visibleArtifacts : allArtifacts, resolvedSearchParams?.selected)
  const hasData = Boolean(latest)

  return (
    <main>
      <section className="hero">
        <div className="heroTop">
          <div>
            <div className="eyebrow">Detail Route · Exports</div>
            <h1>{latest?.stock.name || stockCode} 导出中心</h1>
            <p>复用现有只读导出 contract 与下载接口，把研报正文、事件点评、展示交付、来源数据和运行日志组织成更接近产品后台的导出工作区。</p>
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
              <div className="sectionEyebrow">交付物</div>
              <h2>导出物清单</h2>
            </div>
          </div>
          <div className="filterBar">
            {EXPORT_CATEGORIES.map((category) => (
              <Link
                className={`filterChip${activeCategory === category.key ? ' filterChipActive' : ''}`}
                href={`/stocks/${stockCode}/exports${category.key === 'all' ? '' : `?category=${category.key}`}`}
                key={category.key}
              >
                {category.label} {counts[category.key] || 0}
              </Link>
            ))}
          </div>
          <div className="selectionHint">点击导出物的“设为当前”即可把右侧工作台切到该交付物，继续沿统一下载 contract 工作。</div>
          <div className="list">
            {visibleArtifacts.length ? visibleArtifacts.map((item) => {
              const isSelected = currentArtifact?.filename === item.filename
              const category = EXPORT_CATEGORIES.find((entry) => entry.key === artifactCategory(item))?.label || '其他'
              return (
                <div className={`card${isSelected ? ' selectedCard' : ''}`} key={item.filename}>
                  <div className="itemTitle">{item.kind}</div>
                  <div className="itemMeta">{category} · {item.filename}</div>
                  <div className="pathText">{item.path}</div>
                  <div className="exportActions">
                    <a className="downloadLink" href={`${API_BASE}${item.download_url}`} target="_blank" rel="noreferrer">下载 / 查看</a>
                    <Link className="ghostLink" href={`/stocks/${stockCode}/exports?category=${activeCategory}&selected=${encodeURIComponent(item.filename)}`}>{isSelected ? '当前已选' : '设为当前'}</Link>
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
              <div className="sectionEyebrow">控制台</div>
              <h2>导出工作台</h2>
            </div>
          </div>
          <div className="detailGrid detailGridSingle">
            <div className="card">
              <div className="itemTitle">最近生成</div>
              <div className="metricStack">
                <div className="metricRow"><span>生成时间</span><strong>{latest?.generated_at || '--'}</strong></div>
                <div className="metricRow"><span>导出数量</span><strong>{allArtifacts.length}</strong></div>
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
                <div className="metricRow"><span>研报正文</span><strong>{counts.report || 0}</strong></div>
                <div className="metricRow"><span>事件点评</span><strong>{counts.commentary || 0}</strong></div>
                <div className="metricRow"><span>可下载</span><strong>{allArtifacts.length}</strong></div>
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
              <div className="sectionEyebrow">交付说明</div>
              <h2>交付说明</h2>
            </div>
          </div>
          <div className="detailGrid">
            {allArtifacts.map((item) => (
              <div className="card" key={`${item.filename}-guide`}>
                <div className="itemTitle">{item.kind} 使用建议</div>
                <div className="itemMeta">{item.filename}</div>
                <p className="bodyText">
                  {item.kind === 'event_commentary' ? '适合围绕单条事件沉淀点评、复盘和后续跟踪动作。' : item.kind === 'markdown' ? '适合继续编辑、沉淀研究文本与版本对比。' : item.kind === 'html' ? '适合浏览器展示与分享预览。' : item.kind === 'pdf' ? '适合固定版式交付或归档。' : item.kind === 'json' || item.kind === 'sources' ? '适合后续自动化消费与结构化接入。' : '可作为运行产物进行下载与归档。'}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}
