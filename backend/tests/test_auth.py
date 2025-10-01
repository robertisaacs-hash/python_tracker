import pytest
from httpx import AsyncClient
from app.main import app
import os

@pytest.mark.asyncio
async def test_register_and_login(monkeypatch):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # register
        resp = await ac.post("/api/auth/register", json={"username":"testuser","password":"testpass"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "testuser"

        # obtain token
        form = {"username":"testuser","password":"testpass","grant_type":"password"}
        resp2 = await ac.post("/api/auth/token", data=form)
        assert resp2.status_code == 200
        token = resp2.json().get("access_token")
        assert token