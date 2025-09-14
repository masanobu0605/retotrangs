from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..deps import get_db
from ..schemas import LoginRequest, RegisterRequest
from ..security import verify_password, hash_password, create_token
from ..models import User, Tenant
from ..deps import bearer


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    # Find user within current tenant (enforced by RLS if enabled)
    q = select(User).where(User.email == body.email)
    user = db.scalars(q).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"sub": user.id, "role": user.role})
    return {"token": token, "role": user.role}


@router.post("/check")
def check_token(creds = Depends(bearer)):
    return {"has_creds": bool(creds), "scheme": getattr(creds, 'scheme', None)}


@router.post("/register")
@router.post("/users/register", include_in_schema=False)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    # create default tenant if not exists
    tenant = db.query(Tenant).filter(Tenant.slug == "default").first()
    if not tenant:
        tenant = Tenant(name="Default", slug="default")
        db.add(tenant)
        db.flush()

    # Idempotent behavior: if the same email already exists in the tenant,
    # return 200 with the existing user's id instead of 400.
    exists = db.query(User).filter(
        User.tenant_id == tenant.id, User.email == body.email
    ).first()
    if exists:
        return {"id": exists.id}

    user = User(
        tenant_id=tenant.id,
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        role="member",
    )
    db.add(user)
    db.flush()
    return {"id": user.id}
