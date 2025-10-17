from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from enum import Enum
import datetime

# Enum schemas matching models
class TaskStatusEnum(str, Enum):
    BACKLOG = "backlog"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    UAT = "uat"
    PILOT = "pilot"
    ROLLOUT = "rollout"
    COMPLETE = "complete"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class PriorityEnum(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKLOG = "backlog"

class ProjectTypeEnum(str, Enum):
    PORTFOLIO = "portfolio"
    PROGRAM = "program"
    PROJECT = "project"
    WORKSTREAM = "workstream"

class BudgetCategoryEnum(str, Enum):
    CAPITAL = "capital"
    OPERATING = "operating"
    TRAINING = "training"
    TECHNOLOGY = "technology"
    MARKETING = "marketing"

class RiskCategoryEnum(str, Enum):
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"
    FINANCIAL = "financial"
    TECHNOLOGY = "technology"
    MARKET = "market"

# User schemas
class UserCreate(BaseModel):
    username: str
    password: str
    outlook_email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = "user"
    department: Optional[str] = None
    store_number: Optional[str] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    outlook_email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    store_number: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    outlook_email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    department: Optional[str] = None
    store_number: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Project schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_type: ProjectTypeEnum = ProjectTypeEnum.PROJECT
    priority: PriorityEnum = PriorityEnum.MEDIUM
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    budget_total: Optional[Decimal] = None
    parent_id: Optional[int] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectTypeEnum] = None
    status: Optional[TaskStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    budget_total: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    completion_percentage: Optional[int] = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    project_type: ProjectTypeEnum
    status: TaskStatusEnum
    priority: PriorityEnum
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    budget_total: Optional[Decimal] = None
    actual_cost: Optional[Decimal] = None
    completion_percentage: int
    parent_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Task schemas
class TaskCreate(BaseModel):
    description: str
    title: Optional[str] = None
    project_id: int
    priority: PriorityEnum = PriorityEnum.MEDIUM
    deadline: Optional[datetime.datetime] = None
    estimated_hours: Optional[Decimal] = None
    assigned_to: Optional[int] = None
    parent_id: Optional[int] = None

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[TaskStatusEnum] = None
    deadline: Optional[datetime.datetime] = None
    estimated_hours: Optional[Decimal] = None
    actual_hours: Optional[Decimal] = None
    completion_percentage: Optional[int] = None
    assigned_to: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    description: str
    title: Optional[str] = None
    priority: PriorityEnum
    status: TaskStatusEnum
    deadline: Optional[datetime.datetime] = None
    estimated_hours: Optional[Decimal] = None
    actual_hours: Optional[Decimal] = None
    completion_percentage: int
    assigned_to: Optional[int] = None
    parent_id: Optional[int] = None
    created_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    subtasks: List["TaskOut"] = []
    
    class Config:
        orm_mode = True

# Store schemas
class StoreCreate(BaseModel):
    store_number: str
    name: str
    region: Optional[str] = None
    district: Optional[str] = None
    format: Optional[str] = None

class StoreOut(BaseModel):
    id: int
    store_number: str
    name: str
    region: Optional[str] = None
    district: Optional[str] = None
    format: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Resource schemas
class ResourceCreate(BaseModel):
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    store_number: Optional[str] = None
    availability: Optional[Decimal] = Decimal('1.0')
    hourly_rate: Optional[Decimal] = None
    skills: Optional[dict] = None

class ResourceOut(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    role: Optional[str] = None
    store_number: Optional[str] = None
    availability: Optional[Decimal] = None
    hourly_rate: Optional[Decimal] = None
    skills: Optional[dict] = None
    is_active: bool
    created_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Budget schemas
class BudgetCreate(BaseModel):
    project_id: int
    category: BudgetCategoryEnum
    planned_amount: Decimal
    currency: str = "USD"
    fiscal_year: Optional[str] = None
    description: Optional[str] = None

class BudgetOut(BaseModel):
    id: int
    project_id: int
    category: BudgetCategoryEnum
    planned_amount: Decimal
    actual_amount: Decimal
    currency: str
    fiscal_year: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Risk schemas
class RiskCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    category: RiskCategoryEnum
    probability: Optional[int] = None
    impact: Optional[int] = None
    mitigation_plan: Optional[str] = None
    owner_id: Optional[int] = None

class RiskOut(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str] = None
    category: RiskCategoryEnum
    probability: Optional[int] = None
    impact: Optional[int] = None
    mitigation_plan: Optional[str] = None
    owner_id: Optional[int] = None
    status: str
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Metrics schemas
class MetricsCreate(BaseModel):
    project_id: int
    metric_name: str
    target_value: Optional[Decimal] = None
    actual_value: Optional[Decimal] = None
    measurement_date: Optional[datetime.date] = None
    units: Optional[str] = None
    notes: Optional[str] = None

class MetricsOut(BaseModel):
    id: int
    project_id: int
    metric_name: str
    target_value: Optional[Decimal] = None
    actual_value: Optional[Decimal] = None
    measurement_date: Optional[datetime.date] = None
    units: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    
    class Config:
        orm_mode = True

# Association schemas
class ProjectStoreCreate(BaseModel):
    project_id: int
    store_id: int
    rollout_phase: int = 1
    start_date: Optional[datetime.date] = None
    completion_date: Optional[datetime.date] = None

class ProjectResourceCreate(BaseModel):
    project_id: int
    resource_id: int
    allocation_percentage: Decimal = Decimal('100.0')
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None
    role_in_project: Optional[str] = None

# Update forward references
TaskOut.update_forward_refs()

class Token(BaseModel):
    access_token: str
    token_type: str