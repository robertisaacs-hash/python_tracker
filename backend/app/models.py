from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Date, JSON, Enum as SQLEnum, Numeric
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
import datetime

Base = declarative_base()

# Enterprise Enums
class TaskStatus(Enum):
    BACKLOG = "backlog"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    UAT = "uat"
    PILOT = "pilot"
    ROLLOUT = "rollout"
    COMPLETE = "complete"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class Priority(Enum):
    CRITICAL = 1    # Business critical/P0
    HIGH = 2        # Revenue impacting/P1
    MEDIUM = 3      # Standard business/P2
    LOW = 4         # Nice to have/P3
    BACKLOG = 5     # Future consideration

class ProjectType(Enum):
    PORTFOLIO = "portfolio"
    PROGRAM = "program"
    PROJECT = "project"
    WORKSTREAM = "workstream"

class BudgetCategory(Enum):
    CAPITAL = "capital"
    OPERATING = "operating"
    TRAINING = "training"
    TECHNOLOGY = "technology"
    MARKETING = "marketing"

class RiskCategory(Enum):
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    TECHNOLOGY = "technology"
    MARKET = "market"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    outlook_email = Column(String, unique=True, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, default="user")  # admin, manager, user
    department = Column(String)
    store_number = Column(String)  # For store-level users
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    outlook_tokens = relationship("OutlookToken", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    project_type = Column(SQLEnum(ProjectType), default=ProjectType.PROJECT)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PLANNING)
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    start_date = Column(Date)
    end_date = Column(Date)
    budget_total = Column(Numeric(12,2), default=0)
    actual_cost = Column(Numeric(12,2), default=0)
    completion_percentage = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("projects.id"), nullable=True)  # For portfolio hierarchy
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    budgets = relationship("Budget", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    metrics = relationship("ProjectMetrics", back_populates="project", cascade="all, delete-orphan")
    project_stores = relationship("ProjectStore", back_populates="project", cascade="all, delete-orphan")
    project_resources = relationship("ProjectResource", back_populates="project", cascade="all, delete-orphan")
    subprojects = relationship("Project", cascade="all, delete-orphan", backref="parent", remote_side=[id])

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    title = Column(String)  # Short title for task
    priority = Column(SQLEnum(Priority), default=Priority.MEDIUM)
    deadline = Column(DateTime, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.BACKLOG)
    estimated_hours = Column(Numeric(8,2))
    actual_hours = Column(Numeric(8,2), default=0)
    completion_percentage = Column(Integer, default=0)
    assigned_to = Column(Integer, ForeignKey("resources.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    project = relationship("Project", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    assigned_resource = relationship("Resource")
    subtasks = relationship("Task", cascade="all, delete-orphan", backref="parent", remote_side=[id])

class OutlookToken(Base):
    __tablename__ = "outlook_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="outlook_tokens")

# Enterprise Models
class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, index=True)
    store_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    region = Column(String)
    district = Column(String)
    format = Column(String)  # Supercenter, Neighborhood Market, etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project_stores = relationship("ProjectStore", back_populates="store")

class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    role = Column(String)  # Store Manager, IT Tech, Regional Manager
    store_number = Column(String)  # For store-specific resources
    availability = Column(Numeric(3,2), default=1.0)  # FTE availability
    hourly_rate = Column(Numeric(10,2))  # For budget tracking
    skills = Column(JSON)  # Skills matrix
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project_assignments = relationship("ProjectResource", back_populates="resource")

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(SQLEnum(BudgetCategory), nullable=False)
    planned_amount = Column(Numeric(12,2), nullable=False)
    actual_amount = Column(Numeric(12,2), default=0)
    currency = Column(String, default="USD")
    fiscal_year = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="budgets")

class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(SQLEnum(RiskCategory), nullable=False)
    probability = Column(Integer)  # 1-5 scale
    impact = Column(Integer)  # 1-5 scale
    mitigation_plan = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="open")  # open, mitigated, closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="risks")
    owner = relationship("User")

class ProjectMetrics(Base):
    __tablename__ = "project_metrics"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    metric_name = Column(String, nullable=False)  # Sales_Impact, Customer_Satisfaction, etc.
    target_value = Column(Numeric(12,2))
    actual_value = Column(Numeric(12,2))
    measurement_date = Column(Date)
    units = Column(String)  # %, $, count, etc.
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="metrics")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE, VIEW
    entity_type = Column(String, nullable=False)  # Project, Task, etc.
    entity_id = Column(Integer)
    old_values = Column(JSON)
    new_values = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String)

    # Relationships
    user = relationship("User")

# Association Tables
class ProjectStore(Base):
    __tablename__ = "project_stores"
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.id"), primary_key=True)
    rollout_phase = Column(Integer, default=1)  # 1, 2, 3 for phased rollouts
    start_date = Column(Date)
    completion_date = Column(Date)
    status = Column(String, default="planned")

    # Relationships
    project = relationship("Project", back_populates="project_stores")
    store = relationship("Store", back_populates="project_stores")

class ProjectResource(Base):
    __tablename__ = "project_resources"
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), primary_key=True)
    allocation_percentage = Column(Numeric(5,2), default=100.0)  # % of resource time
    start_date = Column(Date)
    end_date = Column(Date)
    role_in_project = Column(String)

    # Relationships
    project = relationship("Project", back_populates="project_resources")
    resource = relationship("Resource", back_populates="project_assignments")