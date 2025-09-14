from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from ..deps import get_db, get_current_user
from ..models import Task, User


router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskIn(BaseModel):
    title: str
    entity_type: str | None = None
    entity_id: str | None = None
    assignee_user_id: str | None = None
    due_date: str | None = None
    status: str | None = None
    priority: str | None = None


class TaskOut(BaseModel):
    id: str
    title: str
    status: str
    priority: str | None = None


@router.get("")
def list_tasks(
    status: str | None = Query(None),
    assignee: str | None = Query(None),
    entity_type: str | None = Query(None),
    entity_id: str | None = Query(None),
    db: Session = Depends(get_db),
):
    q = select(Task)
    rows = db.scalars(q).all()
    items = []
    for t in rows:
        if status and t.status != status:
            continue
        if assignee and t.assignee_user_id != assignee:
            continue
        if entity_type and t.entity_type != entity_type:
            continue
        if entity_id and t.entity_id != entity_id:
            continue
        items.append(TaskOut(id=t.id, title=t.title, status=t.status, priority=t.priority))
    return {"items": items}


@router.post("", response_model=TaskOut)
def create_task(
    body: TaskIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    t = Task(
        tenant_id=user.tenant_id,
        title=body.title,
        entity_type=body.entity_type, entity_id=body.entity_id,
        assignee_user_id=body.assignee_user_id,
        due_date=body.due_date,
        status=body.status or "open",
        priority=body.priority,
    )
    db.add(t)
    db.flush()
    return TaskOut(id=t.id, title=t.title, status=t.status, priority=t.priority)


@router.patch("/{id}", response_model=TaskOut)
def update_task(id: str, body: TaskIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    t = db.get(Task, id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(t, k, v)
    db.flush()
    return TaskOut(id=t.id, title=t.title, status=t.status, priority=t.priority)
