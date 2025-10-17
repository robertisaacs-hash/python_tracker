import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import get_db
from app import models, crud, schemas
import tempfile
import os

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user(db_session):
    user_data = schemas.UserCreate(
        username="testuser",
        password="testpass",
        first_name="Test",
        last_name="User",
        role="user"
    )
    user = crud.create_user(db_session, user_data)
    return user

@pytest.fixture
def admin_user(db_session):
    admin_data = schemas.UserCreate(
        username="admin",
        password="adminpass",
        first_name="Admin",
        last_name="User",
        role="admin"
    )
    admin = crud.create_user(db_session, admin_data)
    return admin

@pytest.fixture
def auth_headers(test_user):
    login_data = {"username": "testuser", "password": "testpass"}
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(admin_user):
    login_data = {"username": "admin", "password": "adminpass"}
    response = client.post("/api/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestStoreManagement:
    def test_create_store_as_admin(self, setup_database, admin_headers):
        store_data = {
            "store_number": "001",
            "name": "Test Store",
            "region": "North",
            "district": "District 1",
            "format": "Supercenter"
        }
        response = client.post("/api/stores/", json=store_data, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["store_number"] == "001"
        assert response.json()["name"] == "Test Store"

    def test_create_store_as_user_forbidden(self, setup_database, auth_headers):
        store_data = {
            "store_number": "002",
            "name": "Test Store 2",
            "region": "South"
        }
        response = client.post("/api/stores/", json=store_data, headers=auth_headers)
        assert response.status_code == 403

    def test_list_stores(self, setup_database, auth_headers):
        response = client.get("/api/stores/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestResourceManagement:
    def test_create_resource(self, setup_database, admin_headers):
        resource_data = {
            "name": "John Doe",
            "email": "john.doe@company.com",
            "role": "Project Manager",
            "availability": 1.0,
            "hourly_rate": 75.00,
            "skills": {"project_management": True, "agile": True}
        }
        response = client.post("/api/resources/", json=resource_data, headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"
        assert response.json()["hourly_rate"] == 75.00

    def test_list_resources(self, setup_database, auth_headers):
        response = client.get("/api/resources/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestProjectEnhancements:
    def test_create_enhanced_project(self, setup_database, auth_headers):
        project_data = {
            "name": "Enterprise Initiative",
            "description": "Large scale enterprise project",
            "project_type": "program",
            "priority": "high",
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "budget_total": 1000000.00
        }
        response = client.post("/api/projects/", json=project_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["project_type"] == "program"
        assert response.json()["priority"] == "high"

    def test_project_hierarchy(self, setup_database, auth_headers):
        # Create parent project
        parent_data = {
            "name": "Parent Program",
            "project_type": "program",
            "priority": "high"
        }
        parent_response = client.post("/api/projects/", json=parent_data, headers=auth_headers)
        parent_id = parent_response.json()["id"]

        # Create child project
        child_data = {
            "name": "Child Project",
            "project_type": "project",
            "priority": "medium",
            "parent_id": parent_id
        }
        child_response = client.post("/api/projects/", json=child_data, headers=auth_headers)
        assert child_response.status_code == 200
        assert child_response.json()["parent_id"] == parent_id

class TestBudgetManagement:
    def test_create_budget(self, setup_database, auth_headers, db_session, test_user):
        # First create a project
        project_data = schemas.ProjectCreate(name="Budget Test Project")
        project = crud.create_project(db_session, test_user.id, project_data)

        budget_data = {
            "project_id": project.id,
            "category": "capital",
            "planned_amount": 50000.00,
            "fiscal_year": "2024",
            "description": "Hardware purchases"
        }
        response = client.post("/api/budgets/", json=budget_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["planned_amount"] == 50000.00
        assert response.json()["category"] == "capital"

    def test_budget_summary(self, setup_database, auth_headers):
        response = client.get("/api/budgets/summary", headers=auth_headers)
        assert response.status_code == 200
        assert "total_planned" in response.json()
        assert "total_actual" in response.json()
        assert "variance" in response.json()

class TestRiskManagement:
    def test_create_risk(self, setup_database, auth_headers, db_session, test_user):
        # First create a project
        project_data = schemas.ProjectCreate(name="Risk Test Project")
        project = crud.create_project(db_session, test_user.id, project_data)

        risk_data = {
            "project_id": project.id,
            "title": "Budget Overrun Risk",
            "description": "Risk of exceeding allocated budget",
            "category": "financial",
            "probability": 3,
            "impact": 4,
            "mitigation_plan": "Regular budget reviews and controls"
        }
        response = client.post("/api/risks/", json=risk_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Budget Overrun Risk"
        assert response.json()["probability"] == 3
        assert response.json()["impact"] == 4

    def test_risk_matrix(self, setup_database, auth_headers):
        response = client.get("/api/risks/risk-matrix", headers=auth_headers)
        assert response.status_code == 200
        assert "matrix" in response.json()
        assert "high_risk" in response.json()
        assert "medium_risk" in response.json()
        assert "low_risk" in response.json()

class TestAnalytics:
    def test_dashboard_analytics(self, setup_database, auth_headers):
        response = client.get("/api/analytics/dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "projects" in data
        assert "budget" in data
        assert "tasks" in data
        assert "risks" in data

    def test_project_performance(self, setup_database, auth_headers):
        response = client.get("/api/analytics/project-performance", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestTaskEnhancements:
    def test_create_enhanced_task(self, setup_database, auth_headers, db_session, test_user):
        # First create a project
        project_data = schemas.ProjectCreate(name="Task Test Project")
        project = crud.create_project(db_session, test_user.id, project_data)

        task_data = {
            "description": "Enhanced task with all features",
            "title": "Test Task",
            "project_id": project.id,
            "priority": "high",
            "estimated_hours": 8.0,
            "deadline": "2024-12-31T23:59:59"
        }
        response = client.post("/api/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"
        assert response.json()["priority"] == "high"
        assert response.json()["estimated_hours"] == 8.0

class TestAuthentication:
    def test_user_registration_with_enterprise_fields(self, setup_database):
        user_data = {
            "username": "enterprise_user",
            "password": "password123",
            "first_name": "Enterprise",
            "last_name": "User",
            "department": "IT",
            "store_number": "001",
            "role": "manager"
        }
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json()["first_name"] == "Enterprise"
        assert response.json()["department"] == "IT"

    def test_login_updates_last_login(self, setup_database, test_user):
        login_data = {"username": "testuser", "password": "testpass"}
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

if __name__ == "__main__":
    pytest.main([__file__])