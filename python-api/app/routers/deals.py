from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from ..deps import get_db, get_current_user
from ..models import Deal, User


router = APIRouter(prefix="/deals", tags=["deals"])


class DealIn(BaseModel):
    title: str
    amount: int | None = None
    currency: str | None = None
    stage: str | None = None
    probability: int | None = None
    account_id: str | None = None


class DealOut(BaseModel):
    id: str
    title: str
    amount: int | None = None
    currency: str | None = None
    stage: str | None = None
    probability: int | None = None


@router.get("")
def list_deals(db: Session = Depends(get_db)):
    rows = db.scalars(select(Deal).order_by(Deal.updated_at.desc())).all()
    return {"items": [DealOut(id=d.id, title=d.title, amount=d.amount, currency=d.currency, stage=d.stage, probability=d.probability) for d in rows]}


@router.post("", response_model=DealOut)
def create_deal(body: DealIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    d = Deal(tenant_id=user.tenant_id, title=body.title, amount=body.amount, currency=body.currency, stage=body.stage or "New", probability=body.probability, account_id=body.account_id, owner_user_id=user.id)
    db.add(d)
    db.flush()
    return DealOut(id=d.id, title=d.title, amount=d.amount, currency=d.currency, stage=d.stage, probability=d.probability)


@router.patch("/{id}", response_model=DealOut)
def update_deal(id: str, body: DealIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    d = db.get(Deal, id)
    if not d:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(d, k, v)
    db.flush()
    return DealOut(id=d.id, title=d.title, amount=d.amount, currency=d.currency, stage=d.stage, probability=d.probability)
