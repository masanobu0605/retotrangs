import { headers } from 'next/headers'
import CreateAccountForm from './CreateAccountForm'

async function getAccounts() {
  const h = await headers()
  const res = await fetch(`${process.env.API_BASE_URL || 'http://localhost:8000'}/accounts`, {
    headers: { 'X-Tenant': 'default', cookie: h.get('cookie') ?? '' },
    cache: 'no-store',
  })
  if (!res.ok) return []
  return (await res.json()).items as any[]
}

export default async function AccountsPage() {
  const items = await getAccounts()
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">アカウント一覧</h1>
      <div className="card p-4">
        {/* @ts-expect-error Server/Client boundary */}
        <CreateAccountForm />
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th className="th">名前</th>
              <th className="th">業種</th>
              <th className="th">Web</th>
            </tr>
          </thead>
          <tbody>
            {items.map((a) => (
              <tr key={a.id}>
                <td className="td"><a href={`/accounts/${a.id}`} className="underline">{a.name}</a></td>
                <td className="td">{a.industry || '-'}</td>
                <td className="td">{a.website || '-'}</td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td className="td" colSpan={3}>データがありません</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
