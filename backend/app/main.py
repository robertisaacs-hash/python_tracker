from fastapi import FastAPI
from .routers import (
    auth_router, projects_router, tasks_router, profile_router, outlook_router,
    stores_router, resources_router, budgets_router, risks_router, analytics_router
)
from . import models
from .db import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Project Tracker API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(tasks_router.router)
app.include_router(profile_router.router)
app.include_router(outlook_router.router)
app.include_router(stores_router.router)
app.include_router(resources_router.router)
app.include_router(budgets_router.router)
app.include_router(risks_router.router)
app.include_router(analytics_router.router)

@app.get("/")
def root():
    return {"message": "Enterprise Project Tracker API v2.0.0", "status": "running"}