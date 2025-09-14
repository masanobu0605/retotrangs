from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..models_cf import Attachment
from ..models import User


router = APIRouter(prefix="/attachments", tags=["attachments"])


class PresignIn(BaseModel):
    entity_type: str
    entity_id: str
    filename: str
    content_type: str | None = None


class PresignOut(BaseModel):
    upload_url: str
    object_url: str


@router.post("/presign", response_model=PresignOut)
def presign(
    body: PresignIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # 実運用はS3プリサイン。MVPはローカルURLスタブを返す
    a = Attachment(
        tenant_id=user.tenant_id,
        entity_type=body.entity_type, entity_id=body.entity_id,
        filename=body.filename, content_type=body.content_type,
        url=f"/attachments/stub/{body.filename}",
    )
    db.add(a)
    db.flush()
    base = "http://localhost:8000"  # TODO: 設定化
    return PresignOut(
        upload_url=f"{base}/upload/stub",  # 未実装、将来差し替え
        object_url=f"{base}{a.url}",
    )

