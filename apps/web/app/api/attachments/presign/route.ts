import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function POST(req: Request) {
  const body = await req.json()
  const api = apiBase()
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${api}/attachments/presign`, {
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

