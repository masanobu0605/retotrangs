import { jwtVerify } from 'jose'

export async function verifyToken(token: string, secret: string) {
  try {
    const { payload } = await jwtVerify(token, new TextEncoder().encode(secret))
    return payload as any
  } catch {
    return null
  }
}

