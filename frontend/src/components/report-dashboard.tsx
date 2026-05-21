import { sameOriginApiUrl } from '../lib/api'
import { formatExportKind } from '../lib/labels'
import type { LatestReportResponse, StockHistoryResponse } from '../lib/types'

export function ReportDashboard({ latest, history }: { latest: LatestReportResponse | null; history: StockHistoryResponse | null }) {
  if (!latest) {
    return <div className="card">暂无只读 API 数据，请先运行一次分析并启动 <code>python main.py api</code>。</div>
  }

  return (
    <div className="grid">
      <section className="panel span-7" id="summary">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">摘要</div>
            <h2>最新研究摘要</h2>
          </div>
          <a className="ghostLink" href={`/stocks/${latest.stock.code}/summary`}>进入详情页</a>
        </div>
        <div className="list">
          <div className="card">
            <div className="itemTitle">{latest.stock.name} ({latest.stock.code})</div>
            <div className="itemMeta">{latest.stock.industry} · 生成于 {latest.generated_at}</div>
            <p>{latest.summary.conclusion_brief || '暂无摘要'}</p>
          </div>
          <div className="kpis">
            <div className="card"><div className="kpi-label">评级</div><div className="kpi-value">{latest.summary.rating || '--'}</div></div>
            <div className="card"><div className="kpi-label">评分</div><div className="kpi-value">{latest.summary.rating_score.toFixed(1)}</div></div>
            <div className="card"><div className="kpi-label">DCF每股价值</div><div className="kpi-value">{latest.valuation.per_share_value.toFixed(2)}</div></div>
            <div className="card"><div className="kpi-label">当前价格</div><div className="kpi-value">{latest.valuation.current_price.toFixed(2)}</div></div>
            <div className="card"><div className="kpi-label">上涨空间</div><div className="kpi-value">{latest.valuation.upside.toFixed(1)}%</div></div>
            <div className="card"><div className="kpi-label">来源数</div><div className="kpi-value">{latest.quality.source_reference_count}</div></div>
            <div className="card"><div className="kpi-label">占位来源</div><div className="kpi-value">{latest.quality.placeholder_source_count}</div></div>
            <div className="card"><div className="kpi-label">运行状态</div><div className="kpi-value">{latest.run_metrics.success ? '成功' : '失败'}</div></div>
          </div>
        </div>
      </section>

      <section className="panel span-5" id="exports">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">导出物</div>
            <h2>导出物</h2>
          </div>
          <a className="ghostLink" href={`/stocks/${latest.stock.code}/exports`}>进入详情页</a>
        </div>
        <div className="list">
          {latest.exports.length ? latest.exports.map((item) => (
            <div className="card" key={item.filename}>
              <div className="itemTitle">{formatExportKind(item.kind)}</div>
              <div className="itemMeta">{item.filename}</div>
              <div className="pathText">{item.path}</div>
              <a className="downloadLink" href={sameOriginApiUrl(item.download_url)} target="_blank" rel="noreferrer">下载 / 查看</a>
            </div>
          )) : <div className="card">当前未发现导出物。</div>}
        </div>
      </section>

      <section className="panel span-12" id="history">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">历史</div>
            <h2>历史研究脉络</h2>
          </div>
          <a className="ghostLink" href={`/stocks/${latest.stock.code}/history`}>进入详情页</a>
        </div>
        <div className="list">
          {(history?.memory || []).slice(0, 4).map((item) => (
            <div className="card" key={item.timestamp}>
              <div className="itemTitle">{item.timestamp} · {item.rating || '未知评级'}</div>
              <div className="itemMeta">{item.target_range || item.valuation_summary || '暂无估值锚'}</div>
              <p>{item.thesis || '暂无 thesis'}</p>
              {item.historical_delta ? <div className="pathText">{item.historical_delta}</div> : null}
            </div>
          ))}
        </div>
      </section>

      <section className="panel span-12" id="records">
        <div className="sectionHead">
          <div>
            <div className="sectionEyebrow">记录</div>
            <h2>最近历史记录</h2>
          </div>
        </div>
        <div className="tableWrap">
          <table className="table">
            <thead>
              <tr>
                <th>时间</th>
                <th>评级</th>
                <th>结论摘要</th>
                <th>风险</th>
                <th>估值空间</th>
              </tr>
            </thead>
            <tbody>
              {(history?.records || []).slice(0, 6).map((item) => (
                <tr key={item.timestamp}>
                  <td>{item.timestamp}</td>
                  <td>{item.rating || '未知'}</td>
                  <td>{item.conclusion || '暂无摘要'}</td>
                  <td>{item.risk_summary || '暂无风险'}</td>
                  <td>{item.dcf_upside.toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}
