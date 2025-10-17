from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from . import models, schemas
from .auth import get_password_hash, verify_password, create_access_token
import datetime

# Users - Enhanced
def create_user(db: Session, user_data: schemas.UserCreate):
    hashed = get_password_hash(user_data.password)
    user = models.User(
        username=user_data.username, 
        password_hash=hashed, 
        outlook_email=user_data.outlook_email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        department=user_data.department,
        store_number=user_data.store_number,
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(
        and_(models.User.username == username, models.User.is_active == True)
    ).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    # Update last login
    user.last_login = datetime.datetime.utcnow()
    db.commit()
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()

# Projects - Enhanced with hierarchy and enterprise features
def create_project(db: Session, user_id: int, project_data: schemas.ProjectCreate):
    project = models.Project(
        name=project_data.name,
        description=project_data.description,
        project_type=project_data.project_type,
        priority=project_data.priority,
        start_date=project_data.start_date,
        end_date=project_data.end_date,
        budget_total=project_data.budget_total,
        parent_id=project_data.parent_id,
        user_id=user_id,
        status=models.TaskStatus.PLANNING,
        completion_percentage=0,
        actual_cost=0,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def update_project(db: Session, project_id: int, user_id: int, project_data: schemas.ProjectUpdate):
    project = db.query(models.Project).filter(
        and_(models.Project.id == project_id, models.Project.user_id == user_id)
    ).first()
    if project:
        for key, value in project_data.dict(exclude_unset=True).items():
            setattr(project, key, value)
        project.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(project)
    return project

def list_projects(db: Session, user_id: int, project_type: str = None):
    query = db.query(models.Project).filter(models.Project.user_id == user_id)
    if project_type:
        query = query.filter(models.Project.project_type == project_type)
    return query.all()

def get_project(db: Session, project_id: int, user_id: int):
    return db.query(models.Project).filter(
        and_(models.Project.id == project_id, models.Project.user_id == user_id)
    ).first()

def delete_project(db: Session, project_id: int, user_id: int):
    project = get_project(db, project_id, user_id)
    if project:
        db.delete(project)
        db.commit()
        return True
    return False

# Tasks - Enhanced with enterprise features
def create_task(db: Session, user_id: int, task_data: schemas.TaskCreate):
    task = models.Task(
        description=task_data.description,
        title=task_data.title,
        project_id=task_data.project_id,
        user_id=user_id,
        priority=task_data.priority,
        deadline=task_data.deadline,
        estimated_hours=task_data.estimated_hours,
        assigned_to=task_data.assigned_to,
        parent_id=task_data.parent_id,
        status=models.TaskStatus.BACKLOG,
        completion_percentage=0,
        actual_hours=0,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: int, user_id: int, task_data: schemas.TaskUpdate):
    task = db.query(models.Task).filter(
        and_(models.Task.id == task_id, models.Task.user_id == user_id)
    ).first()
    if task:
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        task.updated_at = datetime.datetime.utcnow()
        if task.status == models.TaskStatus.COMPLETE:
            task.completed_at = datetime.datetime.utcnow()
            task.completion_percentage = 100
        db.commit()
        db.refresh(task)
    return task

def get_task(db: Session, user_id: int, task_id: int):
    return db.query(models.Task).filter(
        and_(models.Task.user_id == user_id, models.Task.id == task_id)
    ).first()

def list_tasks(db: Session, user_id: int, project_id: int = None, parent_id=None, status: str = None):
    query = db.query(models.Task).filter(models.Task.user_id == user_id)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    if parent_id is None:
        query = query.filter(models.Task.parent_id.is_(None))
    else:
        query = query.filter(models.Task.parent_id == parent_id)
    if status:
        query = query.filter(models.Task.status == status)
    return query.order_by(models.Task.priority.asc(), models.Task.deadline.asc()).all()

def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()

# Stores
def create_store(db: Session, store_data: schemas.StoreCreate):
    store = models.Store(
        store_number=store_data.store_number,
        name=store_data.name,
        region=store_data.region,
        district=store_data.district,
        format=store_data.format,
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    return store

def get_stores(db: Session, skip: int = 0, limit: int = 100, region: str = None):
    query = db.query(models.Store).filter(models.Store.is_active == True)
    if region:
        query = query.filter(models.Store.region == region)
    return query.offset(skip).limit(limit).all()

def get_store(db: Session, store_id: int):
    return db.query(models.Store).filter(
        and_(models.Store.id == store_id, models.Store.is_active == True)
    ).first()

# Resources
def create_resource(db: Session, resource_data: schemas.ResourceCreate):
    resource = models.Resource(
        name=resource_data.name,
        email=resource_data.email,
        role=resource_data.role,
        store_number=resource_data.store_number,
        availability=resource_data.availability,
        hourly_rate=resource_data.hourly_rate,
        skills=resource_data.skills,
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

def get_resources(db: Session, skip: int = 0, limit: int = 100, role: str = None):
    query = db.query(models.Resource).filter(models.Resource.is_active == True)
    if role:
        query = query.filter(models.Resource.role == role)
    return query.offset(skip).limit(limit).all()

def get_resource(db: Session, resource_id: int):
    return db.query(models.Resource).filter(
        and_(models.Resource.id == resource_id, models.Resource.is_active == True)
    ).first()

# Budgets
def create_budget(db: Session, budget_data: schemas.BudgetCreate):
    budget = models.Budget(
        project_id=budget_data.project_id,
        category=budget_data.category,
        planned_amount=budget_data.planned_amount,
        currency=budget_data.currency,
        fiscal_year=budget_data.fiscal_year,
        description=budget_data.description,
        actual_amount=0,
        created_at=datetime.datetime.utcnow()
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

def get_budgets(db: Session, project_id: int = None):
    query = db.query(models.Budget)
    if project_id:
        query = query.filter(models.Budget.project_id == project_id)
    return query.all()

# Risks
def create_risk(db: Session, risk_data: schemas.RiskCreate):
    risk = models.Risk(
        project_id=risk_data.project_id,
        title=risk_data.title,
        description=risk_data.description,
        category=risk_data.category,
        probability=risk_data.probability,
        impact=risk_data.impact,
        mitigation_plan=risk_data.mitigation_plan,
        owner_id=risk_data.owner_id,
        status="open",
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk

def get_risks(db: Session, project_id: int = None, status: str = None):
    query = db.query(models.Risk)
    if project_id:
        query = query.filter(models.Risk.project_id == project_id)
    if status:
        query = query.filter(models.Risk.status == status)
    return query.all()

# Metrics
def create_metric(db: Session, metric_data: schemas.MetricsCreate):
    metric = models.ProjectMetrics(
        project_id=metric_data.project_id,
        metric_name=metric_data.metric_name,
        target_value=metric_data.target_value,
        actual_value=metric_data.actual_value,
        measurement_date=metric_data.measurement_date,
        units=metric_data.units,
        notes=metric_data.notes,
        created_at=datetime.datetime.utcnow()
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric

def get_metrics(db: Session, project_id: int = None):
    query = db.query(models.ProjectMetrics)
    if project_id:
        query = query.filter(models.ProjectMetrics.project_id == project_id)
    return query.all()

# Audit logging
def log_action(db: Session, user_id: int, action: str, entity_type: str, entity_id: int = None, 
               old_values: dict = None, new_values: dict = None, ip_address: str = None):
    log = models.AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log

# Project-Store associations
def assign_project_to_store(db: Session, assignment_data: schemas.ProjectStoreCreate):
    assignment = models.ProjectStore(
        project_id=assignment_data.project_id,
        store_id=assignment_data.store_id,
        rollout_phase=assignment_data.rollout_phase,
        start_date=assignment_data.start_date,
        completion_date=assignment_data.completion_date,
        status="planned"
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

# Project-Resource assignments
def assign_resource_to_project(db: Session, assignment_data: schemas.ProjectResourceCreate):
    assignment = models.ProjectResource(
        project_id=assignment_data.project_id,
        resource_id=assignment_data.resource_id,
        allocation_percentage=assignment_data.allocation_percentage,
        start_date=assignment_data.start_date,
        end_date=assignment_data.end_date,
        role_in_project=assignment_data.role_in_project
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment