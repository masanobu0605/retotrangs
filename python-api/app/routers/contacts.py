from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from ..deps import get_db, get_current_user
from ..models import Contact, User


router = APIRouter(prefix="/contacts", tags=["contacts"])


class ContactIn(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    account_id: str | None = None


class ContactOut(BaseModel):
    id: str
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


@router.get("")
def list_contacts(db: Session = Depends(get_db)):
    rows = db.scalars(select(Contact)).all()
    return {"items": [
        ContactOut(id=c.id, first_name=c.first_name, last_name=c.last_name, email=c.email, phone=c.phone)
        for c in rows
    ]}


@router.post("", response_model=ContactOut)
def create_contact(body: ContactIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    c = Contact(
        tenant_id=user.tenant_id,
        account_id=body.account_id,
        first_name=body.first_name, last_name=body.last_name,
        email=body.email, phone=body.phone,
    )
    db.add(c)
    db.flush()
    return ContactOut(id=c.id, first_name=c.first_name, last_name=c.last_name, email=c.email, phone=c.phone)


@router.get("/{id}", response_model=ContactOut)
def get_contact(id: str, db: Session = Depends(get_db)):
    c = db.get(Contact, id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    return ContactOut(id=c.id, first_name=c.first_name, last_name=c.last_name, email=c.email, phone=c.phone)


@router.patch("/{id}", response_model=ContactOut)
def update_contact(id: str, body: ContactIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    c = db.get(Contact, id)
    if not c:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.flush()
    return ContactOut(id=c.id, first_name=c.first_name, last_name=c.last_name, email=c.email, phone=c.phone)


@router.delete("/{id}")
def delete_contact(id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    c = db.get(Contact, id)
    if c:
        db.delete(c)
    return {"ok": True}

