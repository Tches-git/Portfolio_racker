'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useMemo, useState } from 'react'

import { createWatchlist, fetchStockSearch } from '../lib/api'
import type { StockSearchItem } from '../lib/types'

function extractStockCodes(value: string) {
  return value
    .split(/[,\s，、]+/)
    .map((item) => item.trim())
    .filter((item) => /^\d{6}$/.test(item))
}

function uniqueStocks(items: StockSearchItem[]) {
  const seen = new Set<string>()
  return items.filter((item) => {
    if (seen.has(item.code)) return false
    seen.add(item.code)
    return true
  })
}

export function WatchlistCreateForm() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [query, setQuery] = useState('')
  const [selectedStocks, setSelectedStocks] = useState<StockSearchItem[]>([])
  const [suggestions, setSuggestions] = useState<StockSearchItem[]>([])
  const [searching, setSearching] = useState(false)
  const [searchHint, setSearchHint] = useState('')
  const [description, setDescription] = useState('')
  const [pending, setPending] = useState(false)
  const [error, setError] = useState('')
  const manualCodes = useMemo(() => extractStockCodes(query), [query])

  useEffect(() => {
    const normalized = query.trim()
    if (!normalized) {
      setSuggestions([])
      setSearchHint('')
      return
    }
    let active = true
    const timer = setTimeout(async () => {
      setSearching(true)
      setSearchHint('')
      try {
        const payload = await fetchStockSearch(normalized, 8)
        if (!active) return
        const selected = new Set(selectedStocks.map((item) => item.code))
        setSuggestions(payload.items.filter((item) => !selected.has(item.code)))
        setSearchHint(payload.items.length ? '点击候选即可加入股票池' : '没有匹配结果，也可以直接输入 6 位股票代码')
      } catch (err) {
        if (!active) return
        setSuggestions([])
        setSearchHint(err instanceof Error ? err.message : '股票搜索暂不可用，可直接输入 6 位代码')
      } finally {
        if (active) setSearching(false)
      }
    }, 220)
    return () => {
      active = false
      clearTimeout(timer)
    }
  }, [query, selectedStocks])

  function addStock(item: StockSearchItem) {
    setSelectedStocks((current) => uniqueStocks([...current, item]))
    setQuery('')
    setSuggestions([])
    setSearchHint('')
    setError('')
  }

  function addManualCodes() {
    if (!manualCodes.length) return
    setSelectedStocks((current) => uniqueStocks([
      ...current,
      ...manualCodes.map((code) => ({ code, name: '', match_text: code })),
    ]))
    setQuery('')
    setSuggestions([])
    setSearchHint('')
    setError('')
  }

  function removeStock(code: string) {
    setSelectedStocks((current) => current.filter((item) => item.code !== code))
  }

  async function submit() {
    const stockCodes = Array.from(new Set([...selectedStocks.map((item) => item.code), ...manualCodes]))
    if (!name.trim() || !stockCodes.length) {
      setError('请填写组合名称，并通过搜索或代码至少加入一只股票')
      return
    }
    setPending(true)
    setError('')
    try {
      const created = await createWatchlist({ name, stock_codes: stockCodes, description })
      setName('')
      setQuery('')
      setSelectedStocks([])
      setDescription('')
      router.push(`/watchlist/${created.watchlist_id}`)
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '创建组合失败')
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="terminalForm">
      <div className="itemTitle">新建追踪组合</div>
      <div className="terminalFormStack">
        <input className="input" value={name} onChange={(event) => setName(event.target.value)} placeholder="组合名称" />
        <div className="stockSearchBox">
          <input
            className="input"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key !== 'Enter') return
              event.preventDefault()
              if (suggestions[0]) {
                addStock(suggestions[0])
              } else {
                addManualCodes()
              }
            }}
            placeholder="搜索股票名称 / 代码，例如输入公司简称"
          />
          <div className="stockSearchActions">
            <button className="ghostButton" type="button" onClick={addManualCodes} disabled={!manualCodes.length}>加入代码</button>
          </div>
          {selectedStocks.length ? (
            <div className="selectedStockChips" aria-label="已选股票">
              {selectedStocks.map((stock) => (
                <button key={stock.code} type="button" onClick={() => removeStock(stock.code)} title="点击移除">
                  <strong>{stock.name || stock.code}</strong>
                  <span>{stock.name ? stock.code : '手动代码'}</span>
                </button>
              ))}
            </div>
          ) : null}
          {suggestions.length ? (
            <div className="stockSearchResults">
              {suggestions.map((item) => (
                <button key={item.code} type="button" onClick={() => addStock(item)} className="stockSearchResult">
                  <span>
                    <strong>{item.name}</strong>
                    <em>{item.code}</em>
                  </span>
                  <small>加入</small>
                </button>
              ))}
            </div>
          ) : null}
          <div className="stockSearchHint">{searching ? '正在搜索股票...' : searchHint || '支持按股票名称模糊搜索；也可以粘贴多个 6 位代码后点“加入代码”。'}</div>
        </div>
        <input className="input" value={description} onChange={(event) => setDescription(event.target.value)} placeholder="组合说明，可选" />
        <button className="button" onClick={submit} disabled={pending}>{pending ? '创建中...' : '创建组合'}</button>
        {error ? <div className="inlineError">{error}</div> : null}
      </div>
    </div>
  )
}
