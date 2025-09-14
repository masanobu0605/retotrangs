import { headers } from 'next/headers'

function isAbsoluteUrl(u: string | undefined): u is string {
  return !!u && /^https?:\/\//i.test(u)
}

export async function siteBaseUrl(): Promise<string> {
  // 1) Prefer explicit env
  const fromEnv = process.env.NEXT_PUBLIC_SITE_URL
  if (isAbsoluteUrl(fromEnv)) return fromEnv!

  // 2) Derive from request headers (SSR/RSC)
  try {
    const h = await headers()
    const proto = h.get('x-forwarded-proto') ?? 'http'
    const host = h.get('x-forwarded-host') ?? h.get('host')
    if (host) return `${proto}://${host}`
  } catch {
    // noop
  }

  // 3) Fallback to localhost (dev)
  return 'http://localhost:3000'
}

export async function absolute(path: string): Promise<string> {
  const base = await siteBaseUrl()
  // Avoid accidental double slashes
  return `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}`
}

