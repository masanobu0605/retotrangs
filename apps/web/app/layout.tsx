import './globals.css'
import type { ReactNode } from 'react'

export const metadata = {
  title: 'Membership Demo',
  description: 'Next.js + FastAPI demo',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <header style={{ padding: 12, borderBottom: '1px solid #eee' }}>
          <nav style={{ display: 'flex', gap: 12 }}>
            <a href="/">トップ</a>
            <a href="/login">ログイン</a>
            <a href="/admin">管理</a>
            <a href="/me">ユーザー</a>
          </nav>
        </header>
        <main style={{ padding: 16 }}>{children}</main>
      </body>
    </html>
  )
}

