import { cookies } from 'next/headers'

async function getUsers() {
  const cookieStore = await cookies()
  const token = cookieStore.get('session')?.value
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/admin/users`, {
    headers: token ? { cookie: `session=${token}` } : {},
    cache: 'no-store',
  })
  if (!res.ok) return []
  const data = await res.json()
  return data.users ?? []
}

export default async function AdminPage() {
  const users = await getUsers()
  return (
    <div>
      <h1>管理画面: ユーザー一覧</h1>
      <p><a href="/api/logout">ログアウト</a></p>
      <table style={{ borderCollapse: 'collapse', minWidth: 480 }}>
        <thead>
          <tr>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>ID</th>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>名前</th>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>メール</th>
            <th style={{ borderBottom: '1px solid #ccc', textAlign: 'left', padding: 4 }}>役割</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u: any) => (
            <tr key={u.id}>
              <td style={{ borderBottom: '1px solid #eee', padding: 4 }}>{u.id}</td>
              <td style={{ borderBottom: '1px solid #eee', padding: 4 }}>{u.name}</td>
              <td style={{ borderBottom: '1px solid #eee', padding: 4 }}>{u.email}</td>
              <td style={{ borderBottom: '1px solid #eee', padding: 4 }}>{u.role}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

