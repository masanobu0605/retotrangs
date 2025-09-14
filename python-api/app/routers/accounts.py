from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..deps import get_db, get_current_user
from ..models import Account, User
from pydantic import BaseModel


router = APIRouter(prefix="/accounts", tags=["accounts"])


class AccountIn(BaseModel):
    name: str
    industry: str | None = None
    website: str | None = None


class AccountOut(BaseModel):
    id: str
    name: str
    industry: str | None = None
    website: str | None = None


@router.get("")
def list_accounts(db: Session = Depends(get_db)):
    rows = db.scalars(select(Account)).all()
    return {"items": [AccountOut(id=a.id, name=a.name, industry=a.industry, website=a.website) for a in rows]}


@router.post("", response_model=AccountOut)
def create_account(body: AccountIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    acc = Account(tenant_id=user.tenant_id, name=body.name, industry=body.industry, website=body.website, owner_user_id=user.id)
    db.add(acc)
    db.flush()
    return AccountOut(id=acc.id, name=acc.name, industry=acc.industry, website=acc.website)


@router.get("/{id}", response_model=AccountOut)
def get_account(id: str, db: Session = Depends(get_db)):
    acc = db.get(Account, id)
    if not acc:
        raise HTTPException(status_code=404, detail="Not found")
    return AccountOut(id=acc.id, name=acc.name, industry=acc.industry, website=acc.website)


@router.patch("/{id}", response_model=AccountOut)
def update_account(id: str, body: AccountIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    acc = db.get(Account, id)
    if not acc:
        raise HTTPException(status_code=404, detail="Not found")
    acc.name = body.name
    acc.industry = body.industry
    acc.website = body.website
    db.flush()
    return AccountOut(id=acc.id, name=acc.name, industry=acc.industry, website=acc.website)


@router.delete("/{id}")
def delete_account(id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    acc = db.get(Account, id)
    if not acc:
        return {"ok": True}
    db.delete(acc)
    return {"ok": True}
