# Enterprise Project Tracker v2.0

A comprehensive enterprise-grade project portfolio management system designed for global retail operations, featuring advanced project hierarchy, resource management, budget tracking, risk assessment, and analytics.

## 🚀 Features

### 🏢 Enterprise Project Management
- **Multi-tier Project Hierarchy**: Portfolio → Programs → Projects → Workstreams
- **Advanced Status Workflow**: Backlog → Planning → In Progress → UAT → Pilot → Rollout → Complete
- **Priority Management**: Critical (P0) → High (P1) → Medium (P2) → Low (P3) → Backlog (P4)
- **Resource Assignment & Capacity Planning**
- **Budget Tracking & Variance Analysis**
- **Risk Management with Impact Assessment**
- **Performance Metrics & KPI Tracking**

### 🏪 Retail-Specific Features
- **Store Management**: Multi-store project rollouts with phased deployment
- **Geographic Hierarchy**: Region → District → Store structure
- **Store Format Support**: Supercenter, Neighborhood Market, Express, Sam's Club
- **Resource Allocation**: FTE availability, hourly rates, skills matrix
- **Compliance & Audit Trail**: Complete change history and user actions

### 📊 Analytics & Reporting
- **Executive Dashboard**: High-level portfolio overview
- **Project Performance**: Health scores, completion rates, budget variance
- **Risk Matrix**: Probability vs Impact visualization
- **Resource Utilization**: Capacity planning and allocation tracking
- **Budget Analysis**: Planned vs Actual with variance reporting

### 🔧 Technical Features
- **FastAPI Backend**: High-performance async API
- **React Frontend**: Modern, responsive user interface
- **PostgreSQL Database**: Enterprise-grade data persistence
- **JWT Authentication**: Secure user sessions
- **Role-based Access Control**: Admin, Manager, User permissions
- **Microsoft Graph Integration**: Outlook profile sync
- **Docker Support**: Containerized deployment
- **Posit Connect Ready**: Enterprise deployment platform

## 🏗️ Architecture

```
Frontend (React/TypeScript)
├── Executive Dashboard
├── Project Management
├── Store Management
├── Resource Management
├── Budget Tracking
├── Risk Management
└── Analytics & Reporting

Backend (FastAPI/Python)
├── Authentication & Authorization
├── Project Management API
├── Store Management API
├── Resource Management API
├── Budget Management API
├── Risk Management API
├── Analytics API
└── Outlook Integration API

Database (PostgreSQL)
├── Users & Authentication
├── Projects & Tasks (Hierarchical)
├── Stores & Geographic Data
├── Resources & Assignments
├── Budgets & Financial Tracking
├── Risks & Mitigation Plans
├── Metrics & KPIs
└── Audit Logs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+ (or SQLite for development)
- Docker (optional)

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/python-tracker.git
   cd python-tracker
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   
   # Configure environment
   cp .env.example .env
   # Edit .env with your database and Azure credentials
   
   # Run migrations
   alembic upgrade head
   
   # Start the API server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Default Admin: admin/admin123 (change immediately!)

### Docker Deployment

1. **Using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🌐 Posit Connect Deployment

### Prerequisites
- Posit Connect server with Python 3.9+ support
- PostgreSQL database
- Azure AD app registration (for Outlook integration)

### Deployment Steps

1. **Prepare deployment package:**
   ```bash
   cd backend
   zip -r enterprise-tracker.zip . -x "*.git*" "*__pycache__*" "*.pytest_cache*"
   ```

2. **Configure Posit Connect:**
   - Upload the deployment package
   - Set entrypoint: `startup:app`
   - Configure environment variables (see POSIT_DEPLOYMENT.md)

3. **Environment Variables:**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:port/db
   SECRET_KEY=your-super-secret-key
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   AZURE_CLIENT_ID=your-azure-client-id
   AZURE_CLIENT_SECRET=your-azure-secret
   AZURE_TENANT_ID=your-azure-tenant-id
   ```

For detailed deployment instructions, see [POSIT_DEPLOYMENT.md](backend/POSIT_DEPLOYMENT.md).

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Current user profile

### Project Management
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Store Management
- `GET /api/stores/` - List stores
- `POST /api/stores/` - Create store (admin/manager)
- `GET /api/stores/{id}` - Get store details

### Resource Management
- `GET /api/resources/` - List resources
- `POST /api/resources/` - Create resource (admin/manager)
- `POST /api/resources/{id}/projects` - Assign to project

### Budget Management
- `GET /api/budgets/` - List budgets
- `POST /api/budgets/` - Create budget entry
- `GET /api/budgets/summary` - Budget variance analysis

### Risk Management
- `GET /api/risks/` - List risks
- `POST /api/risks/` - Create risk entry
- `GET /api/risks/risk-matrix` - Risk matrix visualization

### Analytics
- `GET /api/analytics/dashboard` - Executive dashboard data
- `GET /api/analytics/project-performance` - Project health metrics

## 🔐 Security Features

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (Admin, Manager, User)
- Password hashing with bcrypt
- Session management with configurable expiration

### Data Security
- SQL injection prevention with SQLAlchemy ORM
- Input validation with Pydantic schemas
- CORS configuration for frontend integration
- Audit logging for all data changes

### Production Security Checklist
- [ ] Change default admin credentials
- [ ] Configure strong SECRET_KEY
- [ ] Set up HTTPS/TLS
- [ ] Configure CORS origins
- [ ] Enable rate limiting
- [ ] Set up database connection pooling
- [ ] Configure log retention policies

## 📊 Enterprise Reporting

### Executive Dashboard
- Portfolio completion rates
- Budget variance analysis
- High-risk items summary
- Resource utilization metrics

### Project Performance
- Project health scores
- Task completion rates
- Budget performance indicators
- Risk assessment summaries

### Financial Reports
- Budget vs Actual analysis
- Category-wise spending breakdown
- Fiscal year comparisons
- Variance trend analysis

## 🧪 Testing

### Running Tests
```bash
cd backend
pytest tests/ -v --cov=app
```

### Test Coverage
- Unit tests for all CRUD operations
- Integration tests for API endpoints
- Authentication and authorization tests
- Business logic validation tests

## 🔧 Configuration

### Environment Variables

#### Database Configuration
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Security Configuration
```bash
SECRET_KEY=your-256-bit-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 1 week
```

#### Azure AD Integration (Optional)
```bash
AZURE_CLIENT_ID=your-azure-app-id
AZURE_CLIENT_SECRET=your-azure-app-secret
AZURE_TENANT_ID=your-azure-tenant-id
MSAL_REDIRECT_URI=https://your-domain.com/api/outlook/callback
```

### Database Migration

#### Creating New Migrations
```bash
alembic revision --autogenerate -m "Description of changes"
```

#### Applying Migrations
```bash
alembic upgrade head
```

#### Rollback Migrations
```bash
alembic downgrade -1
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Quality Standards
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Maintain test coverage above 80%
- Document all API endpoints
- Use semantic commit messages

## 📝 Changelog

### Version 2.0.0 (Current)
- ✨ Enterprise-grade project hierarchy (Portfolio/Program/Project/Workstream)
- 🏪 Store management with geographic hierarchy
- 👥 Resource management with skills tracking
- 💰 Budget tracking and variance analysis
- ⚠️ Risk management with impact assessment
- 📊 Advanced analytics and reporting dashboard
- 🔒 Enhanced security with role-based access control
- 🌐 Posit Connect deployment support
- 🧪 Comprehensive test suite

### Version 1.0.0
- Basic project and task management
- User authentication
- Outlook integration
- Simple React frontend

## 📞 Support

### Documentation
- API Documentation: http://localhost:8000/docs
- Deployment Guide: [POSIT_DEPLOYMENT.md](backend/POSIT_DEPLOYMENT.md)
- Architecture Overview: See above

### Troubleshooting
1. **Database Connection Issues**: Verify DATABASE_URL format and network connectivity
2. **Authentication Problems**: Check SECRET_KEY configuration and token expiration
3. **Migration Failures**: Ensure database permissions and run manual table creation
4. **Frontend Build Issues**: Verify Node.js version and clear npm cache

### Getting Help
- Create an issue on GitHub
- Check the FAQ in the wiki
- Review the API documentation
- Contact the development team

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the frontend framework
- PostgreSQL for reliable data persistence
- Material-UI for the component library
- Posit for the enterprise deployment platform

---

**Built with ❤️ for Enterprise Project Management**
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

```markdown
# Project Tracker (React + FastAPI) — Full Refactor

This repository has a FastAPI backend and a React (Vite + TypeScript + MUI) frontend. It supports:
- Users, Projects, Tasks with parent-child (mother-child) relationships
- Server-side Microsoft Graph / Outlook authorization-code flow (per-user tokens)
- Docker + docker-compose for easy local development
- Alembic migrations for DB schema management
- Tests with pytest and httpx
- CI workflow for backend tests and frontend build

Quick start (with Docker Compose)
1. Copy the files into a repo with `backend/` and `frontend/`.
2. Edit `backend/.env` with your secrets (SECRET_KEY and Azure credentials).
3. Run:
   docker-compose build
   docker-compose up
4. Backend API: http://localhost:8000
   Frontend: http://localhost:3000

Notes
- For Outlook integration: register an Azure AD app, add redirect URI e.g. http://localhost:8000/api/outlook/callback, and set AZURE_* env vars.
- In production: secure SECRET_KEY, restrict CORS, add HTTPS and proper session/token management.
```