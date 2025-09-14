"use client"
import { useState } from 'react'

export default function CreateTaskInline({ entityType, entityId }: { entityType?: string, entityId?: string }) {
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(false)

  const onCreate = async () => {
    setLoading(true)
    const res = await fetch('/api/tasks', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ title, entity_type: entityType, entity_id: entityId })
    })
    setLoading(false)
    if (res.ok) setTitle('')
  }

  return (
    <div className="mt-3 flex gap-2">
      <input className="input flex-1" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="タスク名" />
      <button className="btn-primary" onClick={onCreate} disabled={loading || !title}>{loading ? '作成中…' : '追加'}</button>
    </div>
  )
}

