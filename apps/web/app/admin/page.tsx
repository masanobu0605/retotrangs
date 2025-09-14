import Link from 'next/link'
import { headers } from 'next/headers'
import { redirect } from 'next/navigation'
import { absolute } from '@/lib/url'

async function getUsers() {
  const h = await headers()
  const url = await absolute('/api/admin/users')
  const res = await fetch(url, {
    headers: { cookie: h.get('cookie') ?? '' },
    cache: 'no-store',
  })
  if (!res.ok) return []
  const data = await res.json().catch(() => ({}))
  return data.users ?? []
}

async function assertAdmin() {
  const h = await headers()
  const url = await absolute('/api/me')
  const res = await fetch(url, { headers: { cookie: h.get('cookie') ?? '' }, cache: 'no-store' })
  if (!res.ok) redirect('/login')
  const me = await res.json().catch(() => null)
  if (!me || me.role !== 'admin') redirect('/login')
}

export default async function AdminPage() {
  await assertAdmin()
  const users = await getUsers()
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">管理画面</h1>
        <Link href="/api/logout" className="btn-primary">ログアウト</Link>
      </div>
      <div className="card">
        <h2 className="mb-3 text-lg font-semibold">ユーザー一覧</h2>
        <table className="table">
          <thead>
            <tr>
              <th className="th">ID</th>
              <th className="th">名前</th>
              <th className="th">メール</th>
              <th className="th">役割</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u: any) => (
              <tr key={u.id}>
                <td className="td">{u.id}</td>
                <td className="td">{u.name}</td>
                <td className="td">{u.email}</td>
                <td className="td">{u.role}</td>
              </tr>
            ))}
            {users.length === 0 && (
              <tr>
                <td className="td" colSpan={4}>ユーザーがいません</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export const dynamic = 'force-dynamic'
