from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=schemas.ProjectOut)
def create_project(project_in: schemas.ProjectCreate, current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    return crud.create_project(db, current_user.id, project_in.name)

@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    return crud.list_projects(db, current_user.id)