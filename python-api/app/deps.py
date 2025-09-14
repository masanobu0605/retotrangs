from __future__ import annotations

from fastapi import Header, HTTPException, Depends, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .db import session_scope, SessionLocal
from .security import decode_token
from .models import User, Tenant


def get_db(
    x_tenant: str | None = Header(default=None, alias="X-Tenant"),
    authorization: str | None = Header(default=None, alias="Authorization"),
    session_cookie: str | None = Cookie(default=None, alias="session"),
):
    # Resolve tenant and set GUC per request (Postgres) via SET LOCAL
    with session_scope() as session:
        tenant_id = None
        if x_tenant:
            # allow slug or uuid
            t = (
                session.query(Tenant)
                .filter((Tenant.slug == x_tenant) | (Tenant.id == x_tenant))
                .first()
            )
            if t:
                tenant_id = t.id
        if tenant_id is None:
            # fallback default tenant
            t = session.query(Tenant).filter(Tenant.slug == "default").first()
            if t:
                tenant_id = t.id
        if tenant_id:
            try:
                session.execute("SET LOCAL app.current_tenant = :tid", {"tid": tenant_id})
            except Exception:
                # In SQLite or non-PG, ignore
                pass
        token = None
        if authorization and authorization.lower().startswith("bearer "):
            token = authorization.split(" ", 1)[1]
        elif session_cookie:
            token = session_cookie
        if token:
            payload = decode_token(token) or {}
            uid = payload.get("sub")
            if uid:
                try:
                    session.execute("SET LOCAL app.current_user = :uid", {"uid": uid})
                except Exception:
                    pass
        yield session


bearer = HTTPBearer(auto_error=False)


def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    session_cookie: str | None = Cookie(default=None, alias="session"),
    db: Session = Depends(get_db),
):
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    elif session_cookie:
        token = session_cookie
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return user
