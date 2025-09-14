"use client"
import { useEffect, useState } from 'react'

export default function TasksPage() {
  const [items, setItems] = useState<any[]>([])
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(false)

  const load = async () => {
    const res = await fetch('/api/tasks')
    const data = await res.json().catch(() => ({}))
    setItems(data.items || [])
  }

  useEffect(() => { load() }, [])

  const onCreate = async () => {
    setLoading(true)
    const res = await fetch('/api/tasks', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ title })
    })
    setLoading(false)
    if (res.ok) { setTitle(''); load() }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">タスク</h1>
      <div className="card p-4 flex gap-2">
        <input className="input flex-1" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="タスク名" />
        <button className="btn-primary" onClick={onCreate} disabled={loading || !title}>{loading ? '作成中…' : '作成'}</button>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th className="th">タイトル</th>
              <th className="th">状態</th>
              <th className="th">優先度</th>
            </tr>
          </thead>
          <tbody>
            {items.map((t) => (
              <tr key={t.id}>
                <td className="td">{t.title}</td>
                <td className="td">{t.status}</td>
                <td className="td">{t.priority || '-'}</td>
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

