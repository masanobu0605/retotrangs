import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function GET(req: Request) {
  const api = apiBase()
  const url = new URL(req.url)
  const qs = url.search
  const res = await fetch(`${api}/notes${qs}`, {
    headers: { 'X-Tenant': 'default' },
    cache: 'no-store',
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}

export async function POST(req: Request) {
  const body = await req.json()
  const api = apiBase()
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${api}/notes`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'X-Tenant': 'default',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}

