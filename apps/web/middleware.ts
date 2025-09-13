import { NextResponse, type NextRequest } from 'next/server'
import { jwtVerify } from 'jose'

const ADMIN_PATHS = ['/admin']
const USER_PATHS = ['/me']

async function verify(req: NextRequest) {
  const token = req.cookies.get('session')?.value
  if (!token) return null
  const secret = process.env.SESSION_SECRET || 'devsupersecret'
  try {
    const { payload } = await jwtVerify(token, new TextEncoder().encode(secret))
    return payload as any
  } catch {
    return null
  }
}

export async function middleware(req: NextRequest) {
  const url = new URL(req.url)
  const pathname = url.pathname
  const needsAuth = ADMIN_PATHS.some((p) => pathname.startsWith(p)) || USER_PATHS.some((p) => pathname.startsWith(p))
  if (!needsAuth) return NextResponse.next()

  const payload = await verify(req)
  if (!payload) return NextResponse.redirect(new URL('/login', url))

  if (pathname.startsWith('/admin') && payload.role !== 'admin') {
    return NextResponse.redirect(new URL('/login', url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ['/admin/:path*', '/me/:path*'],
}

