"use client"
import { useState, FormEvent } from 'react'

type Def = { id: string; entity_type: string; key: string; name: string; field_type: string; required: boolean }

export default function PutCustomFieldsForm({ entityId, defs, initialValues }: { entityId: string, defs: Def[], initialValues: Record<string, any> }) {
  const [values, setValues] = useState<Record<string, any>>(initialValues || {})
  const [loading, setLoading] = useState(false)
  const update = (k: string, v: any) => setValues((s) => ({ ...s, [k]: v }))

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setLoading(true)
    const res = await fetch('/api/custom_fields/values', {
      method: 'PUT', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ entity_type: 'account', entity_id: entityId, values })
    })
    setLoading(false)
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-3">
      {defs.map((d) => (
        <label key={d.id} className="grid gap-1">
          <span className="text-sm text-gray-600">{d.name}</span>
          <input className="input" value={values[d.key] ?? ''} onChange={(e) => update(d.key, e.target.value)} />
        </label>
      ))}
      <div>
        <button className="btn-primary" disabled={loading}>{loading ? '保存中…' : '保存'}</button>
      </div>
    </form>
  )
}

