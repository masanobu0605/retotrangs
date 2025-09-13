import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET() {
  const api = process.env.API_BASE_URL || 'http://localhost:8000'
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${api}/me`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: 'no-store',
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}

