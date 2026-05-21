import Link from 'next/link'

import { deleteWatchlistFromForm, updateWatchlistFromForm } from '../app/watchlist/actions'
import type { Watchlist } from '../lib/types'
import { EmptyState } from './workbench/primitives'

function formatTime(value: string) {
  return value ? value.replace('T', ' ').slice(0, 16) : '尚未刷新'
}

export function WatchlistManagementPanel({ watchlists }: { watchlists: Watchlist[] }) {
  return (
    <div className="watchlistManager">
      <div className="wbPanelHead">
        <div>
          <div className="wbEyebrow">组合列表</div>
          <h2>当前追踪范围</h2>
        </div>
        <Link className="wbTextButton" href="/events">事件预警处理台</Link>
      </div>

      <div className="wbTableWrap">
        <table className="wbTable">
          <thead>
            <tr>
              <th>组合</th>
              <th>股票池</th>
              <th>最近刷新</th>
              <th>动作</th>
            </tr>
          </thead>
          <tbody>
            {watchlists.map((watchlist) => (
              <tr key={watchlist.watchlist_id}>
                <td>
                  <Link className="wbPrimaryText" href={`/watchlist/${watchlist.watchlist_id}`}>{watchlist.name}</Link>
                  <div className="wbMuted">{watchlist.description || '暂无说明'}</div>
                </td>
                <td>
                  <div className="watchlistStockLine">
                    {watchlist.stock_codes.slice(0, 5).map((code) => <span className="wbChip" key={code}>{code}</span>)}
                    {watchlist.stock_codes.length > 5 ? <span className="wbChip">+{watchlist.stock_codes.length - 5}</span> : null}
                  </div>
                </td>
                <td>{formatTime(watchlist.last_refreshed_at)}</td>
                <td className="watchlistActionCell">
                  <Link className="wbTextButton" href={`/watchlist/${watchlist.watchlist_id}`}>打开</Link>
                  <details className="watchlistManageDetails">
                    <summary>管理</summary>
                    <div className="watchlistInlineEditor">
                      <form action={updateWatchlistFromForm} className="watchlistEditForm">
                        <input type="hidden" name="watchlist_id" value={watchlist.watchlist_id} />
                        <label>
                          <span>组合名称</span>
                          <input className="input" name="name" defaultValue={watchlist.name} required />
                        </label>
                        <label>
                          <span>组合说明</span>
                          <input className="input" name="description" defaultValue={watchlist.description} placeholder="可选" />
                        </label>
                        <label>
                          <span>调整股票池</span>
                          <textarea className="input watchlistStockTextarea" name="stock_codes" defaultValue={watchlist.stock_codes.join(' ')} required />
                          <em>用空格、逗号或顿号分隔，保存后自动去重。</em>
                        </label>
                        <div className="watchlistEditorActions">
                          <button className="button" type="submit">保存</button>
                        </div>
                      </form>
                      <form action={deleteWatchlistFromForm} className="watchlistDeleteForm">
                        <input type="hidden" name="watchlist_id" value={watchlist.watchlist_id} />
                        <label className="watchlistDeleteConfirm">
                          <input type="checkbox" required />
                          <span>确认删除</span>
                        </label>
                        <button className="wbTextButton tone-danger" type="submit">删除组合</button>
                      </form>
                    </div>
                  </details>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!watchlists.length ? <EmptyState title="暂无组合" description="创建第一个组合后，驾驶舱才会开始沉淀事件和预警。" /> : null}
      </div>
    </div>
  )
}
