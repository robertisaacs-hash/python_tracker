from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/risks", tags=["risks"])

@router.post("/", response_model=schemas.RiskOut)
def create_risk(
    risk_data: schemas.RiskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Create a new risk entry"""
    return crud.create_risk(db, risk_data)

@router.get("/", response_model=List[schemas.RiskOut])
def list_risks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """List risks with optional filtering"""
    return crud.get_risks(db, project_id=project_id, status=status)

@router.get("/risk-matrix")
def risk_matrix(
    project_id: Optional[int] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Generate risk matrix data for visualization"""
    risks = crud.get_risks(db, project_id=project_id)
    
    matrix = {}
    for risk in risks:
        if risk.probability and risk.impact:
            score = risk.probability * risk.impact
            if score not in matrix:
                matrix[score] = []
            matrix[score].append({
                "id": risk.id,
                "title": risk.title,
                "category": risk.category.value,
                "probability": risk.probability,
                "impact": risk.impact,
                "score": score
            })
    
    return {
        "matrix": matrix,
        "high_risk": [item for score, items in matrix.items() for item in items if score >= 15],
        "medium_risk": [item for score, items in matrix.items() for item in items if 9 <= score < 15],
        "low_risk": [item for score, items in matrix.items() for item in items if score < 9]
    }