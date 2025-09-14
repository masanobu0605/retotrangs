from __future__ import annotations

from dataclasses import dataclass
import uuid
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base, utcnow


def gen_uuid() -> str:
    return str(uuid.uuid4())


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)

    users: Mapped[list["User"]] = relationship(back_populates="tenant", cascade="all,delete-orphan")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="member")  # admin | member
    status: Mapped[str] = mapped_column(String(32), default="active")
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)

    tenant: Mapped[Tenant] = relationship(back_populates="users")


# 軽量MVPのため以下は定義のみ（エンドポイントは後続実装）
class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(255))
    website: Mapped[Optional[str]] = mapped_column(String(255))
    owner_user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("accounts.id"))
    first_name: Mapped[Optional[str]] = mapped_column(String(255))
    last_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class Deal(Base):
    __tablename__ = "deals"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("accounts.id"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[Optional[int]] = mapped_column(Integer)
    currency: Mapped[Optional[str]] = mapped_column(String(16))
    stage: Mapped[str] = mapped_column(String(32), default="New")
    probability: Mapped[Optional[int]] = mapped_column(Integer)
    owner_user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    expected_close_date: Mapped[Optional[str]] = mapped_column(String(32))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(32), nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    created_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    entity_type: Mapped[Optional[str]] = mapped_column(String(32))
    entity_id: Mapped[Optional[str]] = mapped_column(String)
    assignee_user_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("users.id"))
    due_date: Mapped[Optional[str]] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(16), default="open")
    priority: Mapped[Optional[str]] = mapped_column(String(16))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)

class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"
    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    response_body: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=utcnow)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
