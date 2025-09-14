from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import get_settings


class Base(DeclarativeBase):
    pass


def _make_engine_url() -> str:
    settings = get_settings()
    return settings.effective_db_url()


url = _make_engine_url()
connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope() -> Generator:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def utcnow() -> datetime:
    return datetime.utcnow()
