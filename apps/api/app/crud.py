from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models
from .security import hash_password, verify_password


def get_user_by_email(db: Session, email: str) -> models.User | None:
    stmt = select(models.User).where(models.User.email == email)
    return db.scalar(stmt)


def create_user(db: Session, name: str, email: str, password: str, role: str = "user") -> models.User:
    salt, hashed = hash_password(password)
    user = models.User(name=name, email=email, role=role, password_salt=salt, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_user(db: Session, email: str, password: str) -> models.User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_salt, user.password_hash):
        return None
    return user

