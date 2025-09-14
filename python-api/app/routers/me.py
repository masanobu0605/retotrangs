from __future__ import annotations

from fastapi import APIRouter, Depends
from ..deps import get_current_user
from ..schemas import MeResponse
from ..models import User, Tenant


router = APIRouter(tags=["me"])


@router.get("/me", response_model=MeResponse)
def me(user: User = Depends(get_current_user)):
    return MeResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        tenant=user.tenant_id,
    )

