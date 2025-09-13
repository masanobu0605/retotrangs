import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

export async function GET(req: Request) {
  const cookieStore = await cookies()
  cookieStore.set('session', '', { path: '/', maxAge: 0 })
  const url = new URL(req.url)
  return NextResponse.redirect(new URL('/login', url))
}
