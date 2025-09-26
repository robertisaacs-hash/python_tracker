from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.TaskOut)
def create_task(task_in: schemas.TaskCreate, current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    return crud.create_task(db, current_user.id, task_in.description, task_in.project_id, task_in.priority, task_in.deadline, task_in.parent_id)

@router.get("/", response_model=List[schemas.TaskOut])
def list_tasks(project_id: int = None, parent_id: int | None = None, current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    tasks = crud.list_tasks(db, current_user.id, project_id=project_id, parent_id=parent_id)
    # populate nested subtasks for parent-level requests
    out = []
    for t in tasks:
        def map_task(task):
            subt = crud.list_tasks(db, current_user.id, project_id=task.project_id, parent_id=task.id)
            mapped = schemas.TaskOut.from_orm(task)
            mapped.subtasks = [map_task(s) for s in subt]
            return mapped
        out.append(map_task(t))
    return out

@router.patch("/{task_id}")
def update_task(task_id: int, payload: dict, current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    task = crud.get_task(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = crud.update_task(db, task, **payload)
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(db.get_db)):
    task = crud.get_task(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return {"ok": True}