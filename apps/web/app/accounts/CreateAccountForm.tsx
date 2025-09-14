"use client"
import { useState, FormEvent } from 'react'
import { useRouter } from 'next/navigation'

export default function CreateAccountForm() {
  const [name, setName] = useState('')
  const [industry, setIndustry] = useState('')
  const [website, setWebsite] = useState('')
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)
  const router = useRouter()

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setMsg(null)
    setLoading(true)
    const res = await fetch('/api/accounts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name, industry: industry || null, website: website || null }),
    })
    setLoading(false)
    if (res.ok) {
      setName(''); setIndustry(''); setWebsite('')
      router.refresh()
    } else {
      const data = await res.json().catch(() => ({}))
      setMsg(data?.detail || '作成に失敗しました')
    }
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-2">
      <div className="font-semibold">アカウント作成</div>
      <div className="grid gap-1">
        <label className="text-sm text-gray-600">名前</label>
        <input className="input" value={name} onChange={(e) => setName(e.target.value)} required />
      </div>
      <div className="grid gap-1">
        <label className="text-sm text-gray-600">業種</label>
        <input className="input" value={industry} onChange={(e) => setIndustry(e.target.value)} />
      </div>
      <div className="grid gap-1">
        <label className="text-sm text-gray-600">Web</label>
        <input className="input" value={website} onChange={(e) => setWebsite(e.target.value)} />
      </div>
      <div className="flex items-center gap-2">
        <button className="btn-primary" disabled={loading}>{loading ? '作成中…' : '作成'}</button>
        {msg && <span className="text-sm text-red-600">{msg}</span>}
      </div>
    </form>
  )
}

