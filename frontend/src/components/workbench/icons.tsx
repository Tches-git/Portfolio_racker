export type IconName = 'dashboard' | 'portfolio' | 'events' | 'alerts' | 'runs' | 'stock' | 'check' | 'arrow' | 'refresh' | 'export' | 'market' | 'trend' | 'list' | 'quality'

const LABELS: Record<IconName, string> = {
  dashboard: '驾驶舱',
  portfolio: '组合',
  events: '事件',
  alerts: '预警',
  runs: '任务',
  stock: '股票',
  check: '完成',
  arrow: '进入',
  refresh: '刷新',
  export: '导出',
  market: '行情',
  trend: '趋势',
  list: '列表',
  quality: '质量',
}

export function WorkbenchIcon({ name }: { name: IconName }) {
  return <span className={`wbIcon wbIcon-${name}`} aria-label={LABELS[name]} />
}
