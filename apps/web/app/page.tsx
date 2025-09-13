"use client"
import { useState } from 'react'

export default function Page() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMsg(null)
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    })
    if (res.ok) setMsg('登録しました。ログインしてください。')
    else setMsg('登録に失敗しました。')
  }

  return (
    <div>
      <h1>会員登録</h1>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, maxWidth: 360 }}>
        <label>
          氏名
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          メール
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label>
          パスワード
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
        </label>
        <button>登録</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  )
}

