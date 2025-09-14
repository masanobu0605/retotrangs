import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function POST(req: Request) {
  const body = await req.json()
  const api = apiBase()
  const res = await fetch(`${api}/auth/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'X-Tenant': 'default' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  const cookieStore = await cookies()
  if (res.ok && data.token) {
    cookieStore.set('session', data.token, {
      httpOnly: true,
      sameSite: 'lax',
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      maxAge: 60 * 60 * 24 * 7,
    })
  }
  return NextResponse.json({ role: data.role ?? null, ok: res.ok }, { status: res.status })
}
