function isAbsoluteUrl(u: string | undefined): u is string {
  return !!u && /^https?:\/\//i.test(u)
}

export function apiBase(): string {
  const fromEnv = process.env.API_BASE_URL
  if (isAbsoluteUrl(fromEnv)) return fromEnv!
  // Fallback for dev/local
  return 'http://localhost:8000'
}

