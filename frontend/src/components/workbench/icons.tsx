type IconName = 'dashboard' | 'portfolio' | 'events' | 'alerts' | 'runs' | 'stock' | 'check' | 'arrow' | 'refresh' | 'export'

const ICONS: Record<IconName, string> = {
  dashboard: '▦',
  portfolio: '◫',
  events: '◇',
  alerts: '!',
  runs: '▣',
  stock: '◉',
  check: '✓',
  arrow: '→',
  refresh: '↻',
  export: '⇩',
}

export function WorkbenchIcon({ name }: { name: IconName }) {
  return <span className="wbIcon" aria-hidden>{ICONS[name]}</span>
}
