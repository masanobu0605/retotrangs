import Link from 'next/link'
import { absolute } from '@/lib/url'

async function getContacts() {
  const url = await absolute('/api/contacts')
  const res = await fetch(url, { cache: 'no-store' })
  const data = await res.json().catch(() => ({}))
  return (data.items ?? []) as any[]
}

export default async function ContactsPage() {
  const items = await getContacts()
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">コンタクト一覧</h1>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th className="th">氏名</th>
              <th className="th">メール</th>
              <th className="th">電話</th>
            </tr>
          </thead>
          <tbody>
            {items.map((c) => (
              <tr key={c.id}>
                <td className="td">{[c.first_name, c.last_name].filter(Boolean).join(' ')}</td>
                <td className="td">{c.email || '-'}</td>
                <td className="td">{c.phone || '-'}</td>
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
