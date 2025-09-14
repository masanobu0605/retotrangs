import './globals.css'
import type { ReactNode } from 'react'
import { Inter } from 'next/font/google'
import Link from 'next/link'
import { cookies } from 'next/headers'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'CRMデモ',
  description: 'Next.js + FastAPI Demo',
}

async function Nav() {
  const cookieStore = await cookies()
  const hasSession = !!cookieStore.get('session')?.value
  return (
    <nav className="container flex items-center justify-between py-4">
      <div className="flex items-center gap-4">
        <Link href="/" className="font-semibold">CRM</Link>
        <Link href="/admin" className="btn-ghost">管理</Link>
        <Link href="/accounts" className="btn-ghost">アカウント</Link>
        <Link href="/contacts" className="btn-ghost">コンタクト</Link>
        <Link href="/tasks" className="btn-ghost">タスク</Link>
        <Link href="/me" className="btn-ghost">ユーザー</Link>
      </div>
      <div className="flex items-center gap-2">
        {hasSession ? (
          <Link href="/api/logout" className="btn-primary">ログアウト</Link>
        ) : (
          <Link href="/login" className="btn-primary">ログイン</Link>
        )}
      </div>
    </nav>
  )
}

export default async function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ja">
      <body className={inter.className}>
        <header className="border-b border-gray-200 dark:border-gray-800 bg-white/70 dark:bg-gray-900/70 backdrop-blur">
          <Nav />
        </header>
        <main className="container py-8">{children}</main>
        <footer className="container py-6 text-sm text-gray-500">© {new Date().getFullYear()} Demo</footer>
      </body>
    </html>
  )
}
