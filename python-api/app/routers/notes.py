from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from ..deps import get_db, get_current_user
from ..models import Note, User


router = APIRouter(prefix="/notes", tags=["notes"])


class NoteIn(BaseModel):
    entity_type: str
    entity_id: str
    body: str


class NoteOut(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    body: str
    created_by: str


@router.get("")
def list_notes(
    entity_type: str = Query(...),
    entity_id: str = Query(...),
    db: Session = Depends(get_db),
):
    rows = db.scalars(select(Note).where(Note.entity_type == entity_type, Note.entity_id == entity_id)).all()
    return {"items": [
        NoteOut(id=n.id, entity_type=n.entity_type, entity_id=n.entity_id, body=n.body, created_by=n.created_by)
        for n in rows
    ]}


@router.post("", response_model=NoteOut)
def create_note(
    body: NoteIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    n = Note(
        tenant_id=user.tenant_id,
        entity_type=body.entity_type, entity_id=body.entity_id,
        body=body.body, created_by=user.id
    )
    db.add(n)
    db.flush()
    return NoteOut(id=n.id, entity_type=n.entity_type, entity_id=n.entity_id, body=n.body, created_by=n.created_by)

