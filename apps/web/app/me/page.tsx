import Link from 'next/link'
import { headers } from 'next/headers'

async function getMe() {
  const h = await headers()
  const res = await fetch(`/api/me`, {
    headers: { cookie: h.get('cookie') ?? '' },
    cache: 'no-store',
  })
  if (!res.ok) return null
  return res.json()
}

export default async function MePage() {
  const me = await getMe()
  if (!me) return (
    <div className="mx-auto max-w-xl">
      <div className="card">
        <p>ログインが必要です。</p>
        <div className="mt-4">
          <Link className="btn-primary" href="/login">ログインへ</Link>
        </div>
      </div>
    </div>
  )
  return (
    <div className="mx-auto max-w-xl space-y-4">
      <h1 className="text-2xl font-bold">マイページ</h1>
      <div className="card grid gap-2">
        <div><span className="text-sm text-gray-500">名前</span><div className="font-medium">{me.name}</div></div>
        <div><span className="text-sm text-gray-500">メール</span><div className="font-medium">{me.email}</div></div>
        <div><span className="text-sm text-gray-500">役割</span><div className="font-medium">{me.role}</div></div>
        <div className="pt-2"><Link href="/api/logout" className="btn-primary">ログアウト</Link></div>
      </div>
    </div>
  )
}
