import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'
import { apiBase } from '@/lib/api'

export async function GET() {
  const api = apiBase()
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${api}/admin/users`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: 'no-store',
  })
  const data = await res.json().catch(() => ({}))
  return NextResponse.json(data, { status: res.status })
}
