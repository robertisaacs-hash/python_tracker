from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    outlook_email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    outlook_email: Optional[str] = None
    class Config:
        orm_mode = True

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    description: str
    project_id: int
    priority: Optional[int] = 3
    deadline: Optional[datetime.date] = None
    parent_id: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    description: str
    priority: int
    deadline: Optional[datetime.datetime]
    status: str
    parent_id: Optional[int]
    subtasks: List["TaskOut"] = []
    class Config:
        orm_mode = True

TaskOut.update_forward_refs()

class Token(BaseModel):
    access_token: str
    token_type: str