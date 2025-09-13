import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const body = await req.json()
  const api = process.env.API_BASE_URL || 'http://localhost:8000'
  const res = await fetch(`${api}/users/register`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}
