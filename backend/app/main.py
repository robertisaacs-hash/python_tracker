from fastapi import FastAPI
from .routers import auth_router, projects_router, tasks_router, profile_router, outlook_router
from . import models
from .db import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Project Tracker API (FastAPI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(projects_router.router)
app.include_router(tasks_router.router)
app.include_router(profile_router.router)
app.include_router(outlook_router.router)