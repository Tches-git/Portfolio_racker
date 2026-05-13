'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState } from 'react'
import type { FormEvent } from 'react'

import { isApiError, login, register } from '../lib/api'

export function LoginForm({ nextPath = '/' }: { nextPath?: string }) {
  const router = useRouter()
  const [identity, setIdentity] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await login({ email_or_username: identity.trim(), password })
      router.push(nextPath || '/')
      router.refresh()
    } catch (err) {
      setError(errorMessage(err, '登录失败，请检查账号和密码。'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="authCard">
      <div className="authBrand">
        <span className="brandMark">研</span>
        <div>
          <div className="authKicker">金融消息追踪平台</div>
          <h1>登录研究中枢</h1>
        </div>
      </div>
      <p className="authCopy">进入你的独立数据空间，继续跟踪组合事件、预警和研报交付。</p>
      <form className="authForm" onSubmit={handleSubmit}>
        <label>
          <span>邮箱或用户名</span>
          <input value={identity} onChange={(event) => setIdentity(event.target.value)} autoComplete="username" required />
        </label>
        <label>
          <span>密码</span>
          <input value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" minLength={1} required type="password" />
        </label>
        {error ? <div className="authError">{error}</div> : null}
        <button className="primaryButton" disabled={submitting} type="submit">{submitting ? '登录中...' : '登录'}</button>
      </form>
      <div className="authSwitch">还没有账号？<Link href="/register">创建账号</Link></div>
    </section>
  )
}

export function RegisterForm({ nextPath = '/' }: { nextPath?: string }) {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      await register({ email: email.trim(), username: username.trim(), password })
      router.push(nextPath || '/')
      router.refresh()
    } catch (err) {
      setError(errorMessage(err, '注册失败，请稍后再试。'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="authCard">
      <div className="authBrand">
        <span className="brandMark">研</span>
        <div>
          <div className="authKicker">多用户工作区</div>
          <h1>创建研究账号</h1>
        </div>
      </div>
      <p className="authCopy">注册后会自动登录。第一位注册用户会成为管理员，后续用户默认是普通用户。</p>
      <form className="authForm" onSubmit={handleSubmit}>
        <label>
          <span>邮箱</span>
          <input value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" required type="email" />
        </label>
        <label>
          <span>用户名</span>
          <input value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required />
        </label>
        <label>
          <span>密码</span>
          <input value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="new-password" minLength={8} required type="password" />
        </label>
        {error ? <div className="authError">{error}</div> : null}
        <button className="primaryButton" disabled={submitting} type="submit">{submitting ? '创建中...' : '创建账号'}</button>
      </form>
      <div className="authSwitch">已有账号？<Link href="/login">去登录</Link></div>
    </section>
  )
}

function errorMessage(error: unknown, fallback: string) {
  if (isApiError(error)) return error.message || fallback
  return error instanceof Error ? error.message : fallback
}
