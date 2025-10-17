# Enterprise Project Tracker - Posit Connect Deployment Guide

## Deployment to Posit Connect

### Prerequisites
1. Posit Connect server with Python 3.9+ support
2. Access to deploy applications on the server
3. Database connection (PostgreSQL recommended for production)

### Environment Variables for Production

Set these environment variables in Posit Connect:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Azure AD Integration (Optional)
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
AZURE_TENANT_ID=your-azure-tenant-id
MSAL_REDIRECT_URI=https://your-connect-server.com/api/outlook/callback
```

### Deployment Steps

1. **Prepare the deployment package:**
   ```bash
   cd backend
   zip -r project-tracker.zip . -x "*.git*" "*__pycache__*" "*.pytest_cache*"
   ```

2. **Deploy to Posit Connect:**
   - Upload the zip file to Posit Connect
   - Set the entrypoint to `startup:app`
   - Configure environment variables
   - Set Python version to 3.9+

3. **Post-deployment configuration:**
   - Run database migrations if needed
   - Create admin users
   - Configure access permissions

### Database Migration

The startup script automatically handles database initialization. For manual migration:

```bash
# On the Posit Connect terminal
alembic upgrade head
```

### Security Considerations

1. **Change default credentials:**
   - Default admin: admin/admin123
   - Update in production immediately

2. **Environment Variables:**
   - Use strong SECRET_KEY
   - Secure database credentials
   - Limit token expiration time

3. **Network Security:**
   - Configure CORS origins properly
   - Use HTTPS in production
   - Implement rate limiting

### Monitoring and Maintenance

1. **Logs:** Check Posit Connect application logs
2. **Database:** Monitor database performance and size
3. **Backups:** Regular database backups recommended
4. **Updates:** Keep dependencies updated

### Troubleshooting

Common issues and solutions:

1. **Database Connection Errors:**
   - Verify DATABASE_URL format
   - Check network connectivity
   - Ensure database exists

2. **Migration Failures:**
   - Check Alembic configuration
   - Verify database permissions
   - Manual table creation fallback

3. **Authentication Issues:**
   - Verify SECRET_KEY configuration
   - Check token expiration settings
   - Validate user credentials