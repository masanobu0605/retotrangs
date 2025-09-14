"use client"
import Link from 'next/link'
import { useState } from 'react'

export default function LoginPage() {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('admin123')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const data = await res.json().catch(() => ({}))
    setLoading(false)
    if (res.ok) {
      if (data.role === 'admin') window.location.href = '/admin'
      else window.location.href = '/me'
    } else setError(data?.detail ?? 'ログインに失敗しました')
  }

  return (
    <div className="mx-auto max-w-xl">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold">ログイン</h1>
        <p className="text-sm text-gray-500">管理者は管理画面へ、一般ユーザーはマイページへ移動します</p>
      </div>
      <form onSubmit={onSubmit} className="card grid gap-4">
        <label className="grid gap-1">
          <span className="text-sm text-gray-600">メール</span>
          <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label className="grid gap-1">
          <span className="text-sm text-gray-600">パスワード</span>
          <input className="input" value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
        </label>
        <button className="btn-primary" disabled={loading}>{loading ? '認証中…' : 'ログイン'}</button>
        <p className="text-sm text-gray-500">アカウント未作成ですか？<Link className="ml-2 underline" href="/">新規登録へ</Link></p>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </form>
    </div>
  )
}

