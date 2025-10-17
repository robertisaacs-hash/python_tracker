from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/budgets", tags=["budgets"])

@router.post("/", response_model=schemas.BudgetOut)
def create_budget(
    budget_data: schemas.BudgetCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Create a new budget entry"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return crud.create_budget(db, budget_data)

@router.get("/", response_model=List[schemas.BudgetOut])
def list_budgets(
    project_id: Optional[int] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """List budgets with optional project filtering"""
    return crud.get_budgets(db, project_id=project_id)

@router.get("/summary")
def budget_summary(
    project_id: Optional[int] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Get budget summary with variance analysis"""
    budgets = crud.get_budgets(db, project_id=project_id)
    
    summary = {
        "total_planned": sum(b.planned_amount for b in budgets),
        "total_actual": sum(b.actual_amount for b in budgets),
        "variance": sum(b.planned_amount - b.actual_amount for b in budgets),
        "categories": {}
    }
    
    for budget in budgets:
        cat = budget.category.value
        if cat not in summary["categories"]:
            summary["categories"][cat] = {"planned": 0, "actual": 0, "variance": 0}
        summary["categories"][cat]["planned"] += budget.planned_amount
        summary["categories"][cat]["actual"] += budget.actual_amount
        summary["categories"][cat]["variance"] += budget.planned_amount - budget.actual_amount
    
    return summary