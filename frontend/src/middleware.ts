import { NextResponse, type NextRequest } from 'next/server'

const AUTH_COOKIE_NAME = 'portfolio_session'
const AUTH_ROUTES = new Set(['/login', '/register'])
const PUBLIC_FILE = /\.(?:css|js|map|png|jpg|jpeg|gif|svg|ico|txt|xml|webmanifest)$/i

export function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl
  if (isPublicPath(pathname)) {
    return NextResponse.next()
  }

  const hasSession = Boolean(request.cookies.get(AUTH_COOKIE_NAME)?.value)
  const isAuthRoute = AUTH_ROUTES.has(pathname)

  if (isAuthRoute && hasSession) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  if (!isAuthRoute && !hasSession) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('next', `${pathname}${search}`)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

function isPublicPath(pathname: string) {
  return pathname.startsWith('/api/v1') ||
    pathname.startsWith('/_next') ||
    pathname === '/favicon.ico' ||
    PUBLIC_FILE.test(pathname)
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
