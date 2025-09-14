from __future__ import annotations

import uuid
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from .db import Base, utcnow


def gen_uuid() -> str:
    return str(uuid.uuid4())


class CustomFieldDefinition(Base):
    __tablename__ = "custom_field_definitions"
    __table_args__ = (
        UniqueConstraint("tenant_id", "entity_type", "key", name="uq_cfdef_t_e_k"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)  # account | contact | deal | ...
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[str] = mapped_column(String(16), default="text")   # text/number/date/select/bool/json
    required: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class CustomFieldValue(Base):
    __tablename__ = "custom_field_values"
    __table_args__ = (
        UniqueConstraint("tenant_id", "entity_type", "entity_id", "key", name="uq_cfval_t_e_e_k"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # JSON文字列やプレーン文字列を格納
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(127))
    url: Mapped[Optional[str]] = mapped_column(String)  # 実運用は短期署名URL/S3キー
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)
