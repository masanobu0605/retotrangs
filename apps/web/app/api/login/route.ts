import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const body = await req.json()
  const api = process.env.API_BASE_URL || 'http://localhost:8000'
  const res = await fetch(`${api}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  const cookieStore = await cookies()
  if (res.ok && data.token) {
    cookieStore.set('session', data.token, {
      httpOnly: true,
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24 * 7,
    })
  }
  return NextResponse.json({ role: data.role ?? null, ok: res.ok }, { status: res.status })
}

