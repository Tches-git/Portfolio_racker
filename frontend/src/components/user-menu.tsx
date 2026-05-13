'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

import { logout } from '../lib/api'
import type { AuthUser } from '../lib/types'

export function UserMenu({ user }: { user: AuthUser }) {
  const router = useRouter()
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const displayName = user.username || user.email

  async function handleLogout() {
    setError('')
    try {
      await logout()
      router.push('/login')
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : '退出登录失败')
    }
  }

  return (
    <div className="userMenu">
      <button className="userMenuButton" type="button" onClick={() => setOpen((value) => !value)} aria-expanded={open}>
        <span className="userAvatar">{displayName.slice(0, 1).toUpperCase()}</span>
        <span className="userMenuName">{displayName}</span>
      </button>
      {open ? (
        <div className="userMenuPanel">
          <div className="userMenuIdentity">
            <strong>{displayName}</strong>
            <span>{user.email}</span>
          </div>
          <div className="userMenuRole">{user.role === 'admin' ? '管理员' : '普通用户'} · 独立数据空间</div>
          {error ? <div className="authError">{error}</div> : null}
          <button className="logoutButton" type="button" onClick={handleLogout}>退出登录</button>
        </div>
      ) : null}
    </div>
  )
}
