import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function GET() {
  const api = apiBase()
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${api}/me`, {
    headers: token ? { Authorization: `Bearer ${token}`, 'X-Tenant': 'default' } : { 'X-Tenant': 'default' },
    cache: 'no-store',
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}
