import pytest
from app import crud, schemas, models
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crud.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(setup_test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

class TestEnterpriseModels:
    def test_create_user_with_enterprise_fields(self, db_session):
        user_data = schemas.UserCreate(
            username="testuser",
            password="testpass",
            first_name="John",
            last_name="Doe",
            role="manager",
            department="IT",
            store_number="001"
        )
        user = crud.create_user(db_session, user_data)
        
        assert user.username == "testuser"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.role == "manager"
        assert user.department == "IT"
        assert user.store_number == "001"
        assert user.is_active == True

    def test_create_store(self, db_session):
        store_data = schemas.StoreCreate(
            store_number="001",
            name="Test Store",
            region="North",
            district="District 1",
            format="Supercenter"
        )
        store = crud.create_store(db_session, store_data)
        
        assert store.store_number == "001"
        assert store.name == "Test Store"
        assert store.region == "North"
        assert store.is_active == True

    def test_create_resource(self, db_session):
        from decimal import Decimal
        resource_data = schemas.ResourceCreate(
            name="John Smith",
            email="john@company.com",
            role="Developer",
            availability=Decimal("0.8"),
            hourly_rate=Decimal("65.00"),
            skills={"python": True, "react": True}
        )
        resource = crud.create_resource(db_session, resource_data)
        
        assert resource.name == "John Smith"
        assert resource.email == "john@company.com"
        assert resource.availability == Decimal("0.8")
        assert resource.skills == {"python": True, "react": True}

    def test_project_hierarchy(self, db_session):
        # Create user first
        user_data = schemas.UserCreate(username="projuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        # Create parent project
        parent_data = schemas.ProjectCreate(
            name="Parent Program",
            project_type=schemas.ProjectTypeEnum.PROGRAM,
            priority=schemas.PriorityEnum.HIGH
        )
        parent = crud.create_project(db_session, user.id, parent_data)
        
        # Create child project
        child_data = schemas.ProjectCreate(
            name="Child Project",
            project_type=schemas.ProjectTypeEnum.PROJECT,
            priority=schemas.PriorityEnum.MEDIUM,
            parent_id=parent.id
        )
        child = crud.create_project(db_session, user.id, child_data)
        
        assert child.parent_id == parent.id
        assert parent.project_type.value == "program"
        assert child.project_type.value == "project"

    def test_create_budget(self, db_session):
        from decimal import Decimal
        
        # Create user and project first
        user_data = schemas.UserCreate(username="budgetuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        project_data = schemas.ProjectCreate(name="Budget Test Project")
        project = crud.create_project(db_session, user.id, project_data)
        
        # Create budget
        budget_data = schemas.BudgetCreate(
            project_id=project.id,
            category=schemas.BudgetCategoryEnum.CAPITAL,
            planned_amount=Decimal("100000.00"),
            fiscal_year="2024"
        )
        budget = crud.create_budget(db_session, budget_data)
        
        assert budget.project_id == project.id
        assert budget.category.value == "capital"
        assert budget.planned_amount == Decimal("100000.00")

    def test_create_risk(self, db_session):
        # Create user and project first
        user_data = schemas.UserCreate(username="riskuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        project_data = schemas.ProjectCreate(name="Risk Test Project")
        project = crud.create_project(db_session, user.id, project_data)
        
        # Create risk
        risk_data = schemas.RiskCreate(
            project_id=project.id,
            title="Test Risk",
            category=schemas.RiskCategoryEnum.FINANCIAL,
            probability=3,
            impact=4,
            owner_id=user.id
        )
        risk = crud.create_risk(db_session, risk_data)
        
        assert risk.project_id == project.id
        assert risk.title == "Test Risk"
        assert risk.probability == 3
        assert risk.impact == 4
        assert risk.status == "open"

    def test_enhanced_task_creation(self, db_session):
        from decimal import Decimal
        
        # Setup prerequisites
        user_data = schemas.UserCreate(username="taskuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        project_data = schemas.ProjectCreate(name="Task Test Project")
        project = crud.create_project(db_session, user.id, project_data)
        
        resource_data = schemas.ResourceCreate(name="Task Resource")
        resource = crud.create_resource(db_session, resource_data)
        
        # Create enhanced task
        task_data = schemas.TaskCreate(
            description="Enhanced task",
            title="Test Task",
            project_id=project.id,
            priority=schemas.PriorityEnum.HIGH,
            estimated_hours=Decimal("8.0"),
            assigned_to=resource.id
        )
        task = crud.create_task(db_session, user.id, task_data)
        
        assert task.title == "Test Task"
        assert task.priority.value == "high"
        assert task.estimated_hours == Decimal("8.0")
        assert task.assigned_to == resource.id
        assert task.status.value == "backlog"

class TestCRUDOperations:
    def test_update_project(self, db_session):
        # Create user and project
        user_data = schemas.UserCreate(username="updateuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        project_data = schemas.ProjectCreate(name="Original Project")
        project = crud.create_project(db_session, user.id, project_data)
        
        # Update project
        update_data = schemas.ProjectUpdate(
            name="Updated Project",
            status=schemas.TaskStatusEnum.IN_PROGRESS,
            completion_percentage=50
        )
        updated_project = crud.update_project(db_session, project.id, user.id, update_data)
        
        assert updated_project.name == "Updated Project"
        assert updated_project.status.value == "in_progress"
        assert updated_project.completion_percentage == 50

    def test_task_status_workflow(self, db_session):
        # Setup
        user_data = schemas.UserCreate(username="workflowuser", password="pass")
        user = crud.create_user(db_session, user_data)
        
        project_data = schemas.ProjectCreate(name="Workflow Test")
        project = crud.create_project(db_session, user.id, project_data)
        
        task_data = schemas.TaskCreate(
            description="Workflow task",
            project_id=project.id
        )
        task = crud.create_task(db_session, user.id, task_data)
        
        # Test status progression
        assert task.status.value == "backlog"
        
        # Move to in progress
        update_data = schemas.TaskUpdate(status=schemas.TaskStatusEnum.IN_PROGRESS)
        updated_task = crud.update_task(db_session, task.id, user.id, update_data)
        assert updated_task.status.value == "in_progress"
        
        # Complete task
        complete_data = schemas.TaskUpdate(status=schemas.TaskStatusEnum.COMPLETE)
        completed_task = crud.update_task(db_session, task.id, user.id, complete_data)
        assert completed_task.status.value == "complete"
        assert completed_task.completion_percentage == 100
        assert completed_task.completed_at is not None

if __name__ == "__main__":
    pytest.main([__file__])