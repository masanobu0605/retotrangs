from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .config import get_settings


ph = PasswordHasher()


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False


def create_token(payload: dict, expires_in: int = 60 * 60 * 24 * 7) -> str:
    settings = get_settings()
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=expires_in)
    data = {"iat": int(now.timestamp()), "exp": int(exp.timestamp()), **payload}
    return jwt.encode(data, settings.session_secret, algorithm="HS256")


def decode_token(token: str) -> Optional[dict]:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.session_secret, algorithms=["HS256"])  # type: ignore
    except Exception:
        return None

