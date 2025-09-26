from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash, verify_password, create_access_token
import datetime

# Users
def create_user(db: Session, username: str, password: str, outlook_email: str = None):
    hashed = get_password_hash(password)
    user = models.User(username=username, password_hash=hashed, outlook_email=outlook_email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

# Projects
def create_project(db: Session, user_id: int, name: str):
    project = models.Project(name=name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def list_projects(db: Session, user_id: int):
    return db.query(models.Project).filter(models.Project.user_id == user_id).all()

# Tasks (supports parent-child)
def create_task(db: Session, user_id: int, description: str, project_id: int, priority: int = 3, deadline=None, parent_id=None):
    task = models.Task(
        description=description, project_id=project_id, user_id=user_id,
        priority=priority, deadline=deadline, parent_id=parent_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, user_id: int, task_id: int):
    return db.query(models.Task).filter(models.Task.user_id==user_id, models.Task.id==task_id).first()

def list_tasks(db: Session, user_id: int, project_id: int = None, parent_id = None):
    q = db.query(models.Task).filter(models.Task.user_id==user_id)
    if project_id:
        q = q.filter(models.Task.project_id==project_id)
    if parent_id is None:
        q = q.filter(models.Task.parent_id.is_(None))
    else:
        q = q.filter(models.Task.parent_id==parent_id)
    return q.order_by(models.Task.priority.asc(), models.Task.deadline.asc()).all()

def update_task(db: Session, task: models.Task, **fields):
    for k, v in fields.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task):
    db.delete(task)
    db.commit()