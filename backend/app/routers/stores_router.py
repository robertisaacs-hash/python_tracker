from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/stores", tags=["stores"])

@router.post("/", response_model=schemas.StoreOut)
def create_store(
    store_data: schemas.StoreCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Create a new store (admin only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return crud.create_store(db, store_data)

@router.get("/", response_model=List[schemas.StoreOut])
def list_stores(
    skip: int = 0,
    limit: int = 100,
    region: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """List all stores with optional filtering"""
    return crud.get_stores(db, skip=skip, limit=limit, region=region)

@router.get("/{store_id}", response_model=schemas.StoreOut)
def get_store(
    store_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Get store details by ID"""
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

@router.post("/{store_id}/projects")
def assign_project_to_store(
    store_id: int,
    assignment_data: schemas.ProjectStoreCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Assign a project to a store"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    assignment_data.store_id = store_id
    return crud.assign_project_to_store(db, assignment_data)