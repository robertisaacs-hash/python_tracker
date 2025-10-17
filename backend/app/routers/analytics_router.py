from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
import datetime
from .. import db, crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
def dashboard_analytics(
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Get dashboard analytics data"""
    # Get user's projects
    projects = crud.list_projects(db, current_user.id)
    
    # Calculate metrics
    total_projects = len(projects)
    active_projects = len([p for p in projects if p.status not in ["complete", "cancelled"]])
    completed_projects = len([p for p in projects if p.status == "complete"])
    
    # Budget analysis
    all_budgets = []
    for project in projects:
        budgets = crud.get_budgets(db, project.id)
        all_budgets.extend(budgets)
    
    total_budget = sum(b.planned_amount for b in all_budgets)
    total_spent = sum(b.actual_amount for b in all_budgets)
    budget_variance = total_budget - total_spent
    
    # Task analysis
    all_tasks = []
    for project in projects:
        tasks = crud.list_tasks(db, current_user.id, project.id)
        all_tasks.extend(tasks)
    
    total_tasks = len(all_tasks)
    completed_tasks = len([t for t in all_tasks if t.status == "complete"])
    overdue_tasks = len([t for t in all_tasks if t.deadline and t.deadline < datetime.datetime.now() and t.status != "complete"])
    
    # Risk analysis
    all_risks = []
    for project in projects:
        risks = crud.get_risks(db, project.id)
        all_risks.extend(risks)
    
    high_risks = len([r for r in all_risks if r.probability and r.impact and r.probability * r.impact >= 15])
    open_risks = len([r for r in all_risks if r.status == "open"])
    
    return {
        "projects": {
            "total": total_projects,
            "active": active_projects,
            "completed": completed_projects,
            "completion_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
        },
        "budget": {
            "total_planned": total_budget,
            "total_spent": total_spent,
            "variance": budget_variance,
            "variance_percentage": (budget_variance / total_budget * 100) if total_budget > 0 else 0
        },
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "overdue": overdue_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        },
        "risks": {
            "total": len(all_risks),
            "high_risk": high_risks,
            "open": open_risks
        }
    }

@router.get("/project-performance")
def project_performance(
    project_id: Optional[int] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Get project performance metrics"""
    if project_id:
        projects = [crud.get_project(db, project_id, current_user.id)]
        if not projects[0]:
            raise HTTPException(status_code=404, detail="Project not found")
    else:
        projects = crud.list_projects(db, current_user.id)
    
    performance_data = []
    for project in projects:
        tasks = crud.list_tasks(db, current_user.id, project.id)
        budgets = crud.get_budgets(db, project.id)
        risks = crud.get_risks(db, project.id)
        metrics = crud.get_metrics(db, project.id)
        
        # Calculate performance scores
        task_completion = (len([t for t in tasks if t.status == "complete"]) / len(tasks) * 100) if tasks else 0
        budget_performance = ((sum(b.planned_amount for b in budgets) - sum(b.actual_amount for b in budgets)) / sum(b.planned_amount for b in budgets) * 100) if budgets else 0
        risk_score = sum(r.probability * r.impact for r in risks if r.probability and r.impact) / len(risks) if risks else 0
        
        performance_data.append({
            "project_id": project.id,
            "project_name": project.name,
            "completion_percentage": project.completion_percentage,
            "task_completion_rate": task_completion,
            "budget_performance": budget_performance,
            "risk_score": risk_score,
            "overall_health": (task_completion + max(0, budget_performance) - (risk_score * 5)) / 2
        })
    
    return performance_data

@router.post("/metrics", response_model=schemas.MetricsOut)
def create_metric(
    metric_data: schemas.MetricsCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """Create a new project metric"""
    return crud.create_metric(db, metric_data)

@router.get("/metrics", response_model=List[schemas.MetricsOut])
def list_metrics(
    project_id: Optional[int] = None,
    current_user=Depends(get_current_user),
    db: Session = Depends(db.get_db)
):
    """List project metrics"""
    return crud.get_metrics(db, project_id=project_id)