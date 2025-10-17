#!/usr/bin/env python3
"""
Startup script for Posit Connect deployment.
This script initializes the database and starts the FastAPI application.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def setup_database():
    """Initialize the database with Alembic migrations."""
    try:
        # Run Alembic migrations
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Database migrations completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Database migration failed: {e}")
        # If migrations fail, create tables directly
        try:
            from app import models
            from app.db import engine
            models.Base.metadata.create_all(bind=engine)
            print("Database tables created directly.")
        except Exception as db_error:
            print(f"Failed to create database tables: {db_error}")

def create_default_admin():
    """Create a default admin user if none exists."""
    try:
        from app.db import get_db
        from app import crud, schemas, models
        
        db = next(get_db())
        
        # Check if any admin users exist
        admin_exists = db.query(models.User).filter(models.User.role == "admin").first()
        
        if not admin_exists:
            admin_data = schemas.UserCreate(
                username="admin",
                password="admin123",  # Change in production
                role="admin",
                first_name="System",
                last_name="Administrator"
            )
            crud.create_user(db, admin_data)
            print("Default admin user created: admin/admin123")
        
        db.close()
    except Exception as e:
        print(f"Failed to create default admin: {e}")

def main():
    """Main startup function."""
    print("Starting Enterprise Project Tracker...")
    
    # Set up database
    setup_database()
    
    # Create default admin if needed
    create_default_admin()
    
    print("Startup completed successfully.")
    
    # Import the FastAPI app
    from app.main import app
    return app

# For Posit Connect
app = main()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)