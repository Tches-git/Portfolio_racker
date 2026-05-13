import { cookies } from 'next/headers'

import { fetchCurrentUser, type ApiRequestInit } from './api'
import type { AuthUser } from './types'

export async function serverApiOptions(): Promise<ApiRequestInit> {
  const cookieStore = await cookies()
  const cookieHeader = cookieStore.toString()
  return cookieHeader ? { headers: { cookie: cookieHeader } } : {}
}

export async function getCurrentUserFromServer(): Promise<AuthUser | null> {
  try {
    return await fetchCurrentUser(await serverApiOptions())
  } catch {
    return null
  }
}
