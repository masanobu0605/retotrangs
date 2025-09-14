import os
import pytest
from fastapi.testclient import TestClient
from app.main import app, settings


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_register_and_login_and_me():
    email = "user1@example.com"
    password = "pass1234"
    # register
    r = client.post("/auth/register", json={"name": "User1", "email": email, "password": password})
    assert r.status_code in (200, 201)
    # login
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["token"]
    # me
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == email

