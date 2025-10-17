from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/resources", tags=["resources"])

@router.post("/", response_model=schemas.ResourceOut)
def create_resource(
    resource_data: schemas.ResourceCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Create a new resource (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return crud.create_resource(db, resource_data)

@router.get("/", response_model=List[schemas.ResourceOut])
def list_resources(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """List all resources with optional filtering"""
    return crud.get_resources(db, skip=skip, limit=limit, role=role)

@router.get("/{resource_id}", response_model=schemas.ResourceOut)
def get_resource(
    resource_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Get resource details by ID"""
    resource = crud.get_resource(db, resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.post("/{resource_id}/projects")
def assign_resource_to_project(
    resource_id: int,
    assignment_data: schemas.ProjectResourceCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Assign a resource to a project"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    assignment_data.resource_id = resource_id
    return crud.assign_resource_to_project(db, assignment_data)