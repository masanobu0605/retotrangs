"use client"
import { useState, FormEvent } from 'react'

export default function PresignAttachmentForm({ entityType, entityId }: { entityType: string, entityId: string }) {
  const [filename, setFilename] = useState('')
  const [contentType, setContentType] = useState('application/octet-stream')
  const [result, setResult] = useState<{ upload_url?: string; object_url?: string } | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const res = await fetch('/api/attachments/presign', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ entity_type: entityType, entity_id: entityId, filename, content_type: contentType })
    })
    const data = await res.json().catch(() => ({}))
    setLoading(false)
    setResult(data)
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-2 mt-3">
      <div className="grid gap-1">
        <label className="text-sm text-gray-600">ファイル名</label>
        <input className="input" value={filename} onChange={(e) => setFilename(e.target.value)} placeholder="example.pdf" />
      </div>
      <div className="grid gap-1">
        <label className="text-sm text-gray-600">Content-Type</label>
        <input className="input" value={contentType} onChange={(e) => setContentType(e.target.value)} />
      </div>
      <div>
        <button className="btn-primary" disabled={loading || !filename}>{loading ? '生成中…' : 'プリサイン生成'}</button>
      </div>
      {result && (
        <div className="text-sm text-gray-700">
          <div>upload_url: <code>{result.upload_url}</code></div>
          <div>object_url: <code>{result.object_url}</code></div>
        </div>
      )}
    </form>
  )
}

