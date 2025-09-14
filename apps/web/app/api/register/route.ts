import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function POST(req: Request) {
  const body = await req.json()
  const api = apiBase()
  const res = await fetch(`${api}/users/register`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'X-Tenant': 'default' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}
