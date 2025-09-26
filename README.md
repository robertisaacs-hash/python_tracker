# Python Project Tracker

A robust desktop project tracker with:
- User authentication
- Project and (sub)task management (mother-child relationships)
- Outlook profile integration (Microsoft Graph API)
- Modern Tkinter UI (ttkbootstrap)

## Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure Outlook Integration:**
   - Register an Azure App at https://portal.azure.com (for Microsoft Graph).
   - Set your `CLIENT_ID`, `TENANT_ID`, and `CLIENT_SECRET` in `outlook.py`.

3. **Run the app:**
   ```sh
   python main.py
   ```

## Features

- **Login/Register**: Secure authentication with password hashing.
- **Projects/Tasks**: Add/edit/delete projects. Tasks can have subtasks (mother-child).
- **Profile Tab**: View local and Outlook user profile.
- **Modern UI**: Polished interface with ttkbootstrap.

## Outlook Integration

- On the Profile tab, click "View Outlook Profile" to authenticate via Microsoft and fetch your profile.
- Requires your Outlook email to be set during registration or profile edit.

---

**Enjoy your advanced project tracker!**

```markdown
# React + FastAPI Project Tracker - Refactor Notes

This repo is a refactor of the original Tkinter desktop app into a client-server React app with FastAPI backend.

Key changes:
- Backend:
  - FastAPI app (app/main.py) exposes REST endpoints for auth, projects, tasks, profile.
  - SQLAlchemy models keep the original schema; Task.parent_id supports mother-child relationships.
  - JWT auth (auth.py) and password hashing (passlib).
  - Outlook integration moved to server-side (outlook_integration.py) to keep client secret safe.
  - CORS enabled for local dev; restrict in production.
- Frontend:
  - React + TypeScript
  - MUI for modern, responsive UI
  - Auth context stores token; React pages call backend API via axios.
  - TaskTree component supports nested subtasks.

How to run locally:
- Backend:
  - Create a virtualenv, install backend/requirements.txt
  - Set environment variables: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID (optional)
  - Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Frontend:
  - cd frontend
  - npm install
  - set VITE_API_BASE if backend not default
  - npm run dev

Next recommended steps (already planned for you):
- Add Alembic migrations for DB schema changes.
- Harden security: store SECRET_KEY and client secrets in env, restrict CORS, use HTTPS.
- Add refresh tokens / token rotation if longer sessions needed.
- Add unit/integration tests for backend endpoints and frontend components.
- Add file upload, CSV export, notification system, and optional real-time layer (WebSockets) for multi-user collaboration.

```