from __future__ import annotations

import hashlib
import hmac
import os
from base64 import urlsafe_b64encode
from typing import Tuple


def hash_password(password: str, salt: bytes | None = None) -> Tuple[str, str]:
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt.hex(), dk.hex()


def verify_password(password: str, salt_hex: str, hash_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return hmac.compare_digest(dk.hex(), hash_hex)


def make_csrf_token() -> str:
    return urlsafe_b64encode(os.urandom(18)).decode().rstrip("=")

