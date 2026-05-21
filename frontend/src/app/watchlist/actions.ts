'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

import { apiFetch } from '../../lib/api'
import { serverApiOptions } from '../../lib/server-auth'
import type { Watchlist } from '../../lib/types'

function stockCodesFromForm(value: FormDataEntryValue | null) {
  return String(value || '')
    .split(/[,\s，、]+/)
    .map((item) => item.trim())
    .filter(Boolean)
}

export async function updateWatchlistFromForm(formData: FormData) {
  const watchlistId = String(formData.get('watchlist_id') || '')
  const stockCodes = stockCodesFromForm(formData.get('stock_codes'))
  if (!watchlistId || !stockCodes.length) {
    redirect('/watchlist?error=组合至少保留一只股票')
  }
  try {
    await apiFetch<Watchlist>(
      `/api/v1/watchlists/${encodeURIComponent(watchlistId)}`,
      {
        ...(await serverApiOptions()),
        method: 'PATCH',
        body: {
          name: String(formData.get('name') || ''),
          description: String(formData.get('description') || ''),
          stock_codes: stockCodes,
        },
      },
      '更新组合失败',
    )
    revalidatePath('/watchlist')
    revalidatePath(`/watchlist/${watchlistId}`)
    revalidatePath('/')
  } catch (error) {
    redirect(`/watchlist?error=${encodeURIComponent(error instanceof Error ? error.message : '更新组合失败')}`)
  }
  redirect('/watchlist?notice=组合已更新')
}

export async function deleteWatchlistFromForm(formData: FormData) {
  const watchlistId = String(formData.get('watchlist_id') || '')
  if (!watchlistId) {
    redirect('/watchlist?error=缺少组合 ID')
  }
  try {
    await apiFetch<void>(
      `/api/v1/watchlists/${encodeURIComponent(watchlistId)}`,
      {
        ...(await serverApiOptions()),
        method: 'DELETE',
      },
      '删除组合失败',
    )
    revalidatePath('/watchlist')
    revalidatePath('/')
  } catch (error) {
    redirect(`/watchlist?error=${encodeURIComponent(error instanceof Error ? error.message : '删除组合失败')}`)
  }
  redirect('/watchlist?notice=组合已删除')
}
