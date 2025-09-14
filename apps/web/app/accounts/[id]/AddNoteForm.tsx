"use client"
import { useState, FormEvent } from 'react'

export default function AddNoteForm({ entityType, entityId }: { entityType: string, entityId: string }) {
  const [body, setBody] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const res = await fetch('/api/notes', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ entity_type: entityType, entity_id: entityId, body })
    })
    setLoading(false)
    if (res.ok) setBody('')
  }

  return (
    <form onSubmit={onSubmit} className="mt-3 grid gap-2">
      <textarea className="input" value={body} onChange={(e) => setBody(e.target.value)} placeholder="ノートを追加" />
      <div>
        <button className="btn-primary" disabled={loading || !body.trim()}>{loading ? '追加中…' : '追加'}</button>
      </div>
    </form>
  )
}

