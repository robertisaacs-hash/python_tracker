import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_project_and_task():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # register and login
        await ac.post("/api/auth/register", json={"username":"user1","password":"pass1"})
        token_resp = await ac.post("/api/auth/token", data={"username":"user1","password":"pass1","grant_type":"password"})
        token = token_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # create project
        p = await ac.post("/api/projects/", json={"name":"ProjA"}, headers=headers)
        assert p.status_code == 200
        proj_id = p.json()["id"]

        # create task
        t = await ac.post("/api/tasks/", json={"description":"Task1","project_id":proj_id}, headers=headers)
        assert t.status_code == 200
        assert t.json()["description"] == "Task1"