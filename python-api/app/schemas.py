from __future__ import annotations

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class MeResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    tenant: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str


class UsersResponse(BaseModel):
    users: list[UserOut]

