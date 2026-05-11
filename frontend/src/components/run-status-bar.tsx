export function RunStatusBar({ stockCode, hasData, statusHint }: { stockCode: string; hasData: boolean; statusHint?: string }) {
  return (
    <section className="statusBar">
      <div>
        <div className="statusLabel">当前查看</div>
        <div className="statusValue">{stockCode}</div>
      </div>
      <div>
        <div className="statusLabel">数据状态</div>
        <div className={`statusPill ${hasData ? 'statusReady' : 'statusPending'}`}>
          {hasData ? 'API 已返回结果' : '等待分析产物 / API 数据'}
        </div>
      </div>
      <div>
        <div className="statusLabel">运行提示</div>
        <div className="statusHint">{statusHint || '当前已支持浏览器触发分析与轮询状态。'}</div>
      </div>
    </section>
  )
}
