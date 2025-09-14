"use client"
import Link from 'next/link'
import { useState } from 'react'

export default function Page() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMsg(null)
    setLoading(true)
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    })
    const data = await res.json().catch(() => ({}))
    setLoading(false)
    if (res.ok) setMsg('登録しました。ログインしてください')
    else setMsg(data?.detail ?? '登録に失敗しました')
  }

  return (
    <div className="mx-auto max-w-xl">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold">会員登録</h1>
        <p className="text-sm text-gray-500">必要事項を入力してアカウントを作成します</p>
      </div>
      <form onSubmit={onSubmit} className="card grid gap-4">
        <label className="grid gap-1">
          <span className="text-sm text-gray-600">氏名</span>
          <input className="input" value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label className="grid gap-1">
          <span className="text-sm text-gray-600">メール</span>
          <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label className="grid gap-1">
          <span className="text-sm text-gray-600">パスワード</span>
          <input className="input" value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
        </label>
        <button className="btn-primary" disabled={loading}>{loading ? '送信中…' : '登録'}</button>
        <p className="text-sm text-gray-500">すでにアカウントをお持ちですか？<Link className="ml-2 underline" href="/login">ログインへ</Link></p>
        {msg && <p className="text-sm text-blue-700">{msg}</p>}
      </form>
    </div>
  )
}

