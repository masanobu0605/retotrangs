from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import models, schemas, crud


def get_secret() -> str:
    return os.environ.get("SESSION_SECRET", "devsupersecret")


def create_access_token(sub: int, role: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(days=7))
    payload = {"sub": str(sub), "role": role, "exp": expire}
    token = jwt.encode(payload, get_secret(), algorithm="HS256")
    return token


bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    db: Session = Depends(get_db),
) -> models.User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
        user_id = int(payload.get("sub"))
        role = payload.get("role")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Optionally verify role from DB
    return user


def require_admin(user: models.User = Depends(get_current_user)) -> models.User:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user


app = FastAPI(title="Membership API")

origins = [o.strip() for o in os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"]
    ,
    allow_headers=["*"]
    ,
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    # seed admin
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    with next_db() as db:
        user = crud.get_user_by_email(db, admin_email)
        if not user:
            crud.create_user(db, name="Admin", email=admin_email, password=admin_password, role="admin")


from contextlib import contextmanager


@contextmanager
def next_db():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


@app.post("/users/register")
def register(payload: schemas.RegisterIn, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, payload.name, payload.email, payload.password)
    return {"id": user.id, "email": user.email}


@app.post("/auth/login")
def login(payload: schemas.LoginIn, db: Session = Depends(get_db)):
    user = crud.verify_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return {"token": token, "role": user.role, "user": schemas.UserOut.model_validate(user).model_dump()}


@app.get("/me")
def me(current: models.User = Depends(get_current_user)):
    return schemas.UserOut.model_validate(current).model_dump()


@app.get("/admin/users")
def admin_users(_: models.User = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {"users": [schemas.UserOut.model_validate(u).model_dump() for u in users]}

