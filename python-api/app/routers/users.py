from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db, require_admin
from ..models import User
from ..schemas import UsersResponse, UserOut


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=UsersResponse)
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {
        "users": [UserOut(id=u.id, name=u.name, email=u.email, role=u.role) for u in users]
    }

