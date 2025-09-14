from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..deps import get_db
from ..schemas import RegisterRequest
from ..routers.auth import register as register_impl


router = APIRouter(tags=["public"])


@router.post("/users/register")
def users_register(body: RegisterRequest, db: Session = Depends(get_db)):
    return register_impl(body, db)

