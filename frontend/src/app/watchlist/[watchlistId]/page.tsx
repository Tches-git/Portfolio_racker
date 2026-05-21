import { WatchlistMarketCenter } from '../../../components/workbench/watchlist-market-center'
import { WorkspaceShell } from '../../../components/workbench/workspace-shell'
import { fetchUiWatchlistDetail } from '../../../lib/api'
import { serverApiOptions } from '../../../lib/server-auth'

export default async function WatchlistDetailPage({ params }: { params: Promise<{ watchlistId: string }> }) {
  const { watchlistId } = await params
  const detail = await fetchUiWatchlistDetail(watchlistId, await serverApiOptions())

  if (!detail) {
    return (
      <WorkspaceShell
        eyebrow="组合行情数据中心"
        title="未找到组合"
        description="该组合可能不存在，或你当前账号没有访问权限。"
        actions={[{ label: '返回组合列表', href: '/watchlist', method: 'GET', action_type: 'navigate', target_id: 'watchlist', variant: 'secondary' }]}
      >
        <div className="wbEmpty">组合 ID：{watchlistId}</div>
      </WorkspaceShell>
    )
  }

  const stockQuery = detail.watchlist.stock_codes.join(',')

  return (
    <WorkspaceShell
      eyebrow="组合行情数据中心"
      title={detail.watchlist.name}
      description="股票行情、区间走势、事件预警和研究建议集中展示。"
      className="watchlistCommandPage watchlistMarketPage"
      compact
      actions={[
        { label: '事件预警', href: `/events?stock_codes=${stockQuery}`, method: 'GET', action_type: 'navigate', target_id: detail.watchlist.watchlist_id, variant: 'secondary' },
        { label: '任务交付', href: '/runs', method: 'GET', action_type: 'navigate', target_id: detail.watchlist.watchlist_id, variant: 'secondary' },
        { label: '返回列表', href: '/watchlist', method: 'GET', action_type: 'navigate', target_id: detail.watchlist.watchlist_id, variant: 'secondary' },
      ]}
    >
      <WatchlistMarketCenter detail={detail} />
    </WorkspaceShell>
  )
}
