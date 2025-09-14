from __future__ import annotations

import json
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from ..deps import get_db, get_current_user
from ..models_cf import CustomFieldDefinition, CustomFieldValue
from ..models import User


router = APIRouter(prefix="/custom_fields", tags=["custom_fields"])


class CFDefIn(BaseModel):
    entity_type: str
    key: str
    name: str
    field_type: str | None = "text"
    required: bool = False


class CFDefOut(BaseModel):
    id: str
    entity_type: str
    key: str
    name: str
    field_type: str
    required: bool


@router.get("/definitions")
def list_definitions(entity_type: str | None = Query(None), db: Session = Depends(get_db)):
    rows = db.scalars(select(CustomFieldDefinition)).all()
    items = []
    for d in rows:
        if entity_type and d.entity_type != entity_type:
            continue
        items.append(CFDefOut(
            id=d.id, entity_type=d.entity_type, key=d.key, name=d.name, field_type=d.field_type, required=d.required
        ))
    return {"items": items}


@router.post("/definitions", response_model=CFDefOut)
def create_definition(
    body: CFDefIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exists = db.query(CustomFieldDefinition).filter(
        CustomFieldDefinition.tenant_id == user.tenant_id,
        CustomFieldDefinition.entity_type == body.entity_type,
        CustomFieldDefinition.key == body.key,
    ).first()
    if exists:
        return CFDefOut(
            id=exists.id, entity_type=exists.entity_type, key=exists.key, name=exists.name,
            field_type=exists.field_type, required=exists.required
        )
    d = CustomFieldDefinition(
        tenant_id=user.tenant_id,
        entity_type=body.entity_type, key=body.key, name=body.name,
        field_type=(body.field_type or "text"), required=body.required,
    )
    db.add(d)
    db.flush()
    return CFDefOut(
        id=d.id, entity_type=d.entity_type, key=d.key, name=d.name, field_type=d.field_type, required=d.required
    )


class CFValuesPut(BaseModel):
    entity_type: str
    entity_id: str
    values: dict[str, object]


@router.get("/values")
def get_values(
    entity_type: str = Query(...),
    entity_id: str = Query(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = db.scalars(select(CustomFieldValue).where(
        CustomFieldValue.entity_type == entity_type,
        CustomFieldValue.entity_id == entity_id,
    )).all()
    result: dict[str, object] = {}
    for v in rows:
        try:
            result[v.key] = json.loads(v.value) if v.value is not None else None
        except Exception:
            result[v.key] = v.value
    return {"values": result}


@router.put("/values")
def put_values(
    body: CFValuesPut,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = {
        (v.key): v for v in db.scalars(select(CustomFieldValue).where(
            CustomFieldValue.tenant_id == user.tenant_id,
            CustomFieldValue.entity_type == body.entity_type,
            CustomFieldValue.entity_id == body.entity_id,
        )).all()
    }
    for k, v in (body.values or {}).items():
        as_text = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
        if k in existing:
            existing[k].value = as_text
        else:
            db.add(CustomFieldValue(
                tenant_id=user.tenant_id,
                entity_type=body.entity_type, entity_id=body.entity_id,
                key=k, value=as_text,
            ))
    return {"ok": True}

