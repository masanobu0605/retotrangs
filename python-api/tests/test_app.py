import pytest
import httpx
from main import app


@pytest.mark.asyncio
async def test_health_ok():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"ok": True, "service": "python-api"}


@pytest.mark.asyncio
async def test_hello_default_and_named():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        # default
        r1 = await client.get("/hello")
        assert r1.status_code == 200
        assert r1.json() == {"message": "Hello, world from python-api!"}

        # with query
        r2 = await client.get("/hello", params={"name": "masan"})
        assert r2.status_code == 200
        assert r2.json() == {"message": "Hello, masan from python-api!"}

