import { cookies } from 'next/headers'

async function getMe() {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/me`, {
    headers: token ? { cookie: `session=${token}` } : {},
    cache: 'no-store',
  })
  if (!res.ok) return null
  return res.json()
}

export default async function MePage() {
  const me = await getMe()
  if (!me) return <p>ログインしてください。</p>
  return (
    <div>
      <h1>あなたの情報</h1>
      <p>名前: {me.name}</p>
      <p>メール: {me.email}</p>
      <p>役割: {me.role}</p>
      <p><a href="/api/logout">ログアウト</a></p>
    </div>
  )
}

