"""Add enterprise features - stores, resources, budgets, risks, metrics, audit logs

Revision ID: 0002
Revises: 0001
Create Date: 2025-10-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Create new enterprise tables
    
    # Stores table
    op.create_table('stores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('store_number', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('district', sa.String(), nullable=True),
        sa.Column('format', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_number')
    )
    op.create_index(op.f('ix_stores_id'), 'stores', ['id'], unique=False)

    # Resources table
    op.create_table('resources',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('store_number', sa.String(), nullable=True),
        sa.Column('availability', sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column('hourly_rate', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('skills', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_id'), 'resources', ['id'], unique=False)

    # Budgets table
    op.create_table('budgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.Enum('CAPITAL', 'OPERATING', 'TRAINING', 'TECHNOLOGY', 'MARKETING', name='budgetcategory'), nullable=False),
        sa.Column('planned_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('actual_amount', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('fiscal_year', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_budgets_id'), 'budgets', ['id'], unique=False)

    # Risks table
    op.create_table('risks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('REGULATORY', 'OPERATIONAL', 'FINANCIAL', 'TECHNOLOGY', 'MARKET', name='riskcategory'), nullable=False),
        sa.Column('probability', sa.Integer(), nullable=True),
        sa.Column('impact', sa.Integer(), nullable=True),
        sa.Column('mitigation_plan', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_risks_id'), 'risks', ['id'], unique=False)

    # Project metrics table
    op.create_table('project_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('target_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('actual_value', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('measurement_date', sa.Date(), nullable=True),
        sa.Column('units', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_metrics_id'), 'project_metrics', ['id'], unique=False)

    # Audit logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('old_values', sa.JSON(), nullable=True),
        sa.Column('new_values', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)

    # Association tables
    op.create_table('project_stores',
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('store_id', sa.Integer(), nullable=False),
        sa.Column('rollout_phase', sa.Integer(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('completion_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ),
        sa.PrimaryKeyConstraint('project_id', 'store_id')
    )

    op.create_table('project_resources',
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=False),
        sa.Column('allocation_percentage', sa.Numeric(precision=5, scale=2), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('role_in_project', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.PrimaryKeyConstraint('project_id', 'resource_id')
    )

    # Update existing tables
    
    # Add columns to users table
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    op.add_column('users', sa.Column('department', sa.String(), nullable=True))
    op.add_column('users', sa.Column('store_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))

    # Add columns to projects table
    op.add_column('projects', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('projects', sa.Column('project_type', sa.Enum('PORTFOLIO', 'PROGRAM', 'PROJECT', 'WORKSTREAM', name='projecttype'), nullable=True))
    op.add_column('projects', sa.Column('status', sa.Enum('BACKLOG', 'PLANNING', 'IN_PROGRESS', 'UAT', 'PILOT', 'ROLLOUT', 'COMPLETE', 'ON_HOLD', 'CANCELLED', name='taskstatus'), nullable=True))
    op.add_column('projects', sa.Column('priority', sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'BACKLOG', name='priority'), nullable=True))
    op.add_column('projects', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('projects', sa.Column('end_date', sa.Date(), nullable=True))
    op.add_column('projects', sa.Column('budget_total', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('projects', sa.Column('actual_cost', sa.Numeric(precision=12, scale=2), nullable=True))
    op.add_column('projects', sa.Column('completion_percentage', sa.Integer(), nullable=True))
    op.add_column('projects', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.add_column('projects', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('projects', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'projects', 'projects', ['parent_id'], ['id'])

    # Add columns to tasks table
    op.add_column('tasks', sa.Column('title', sa.String(), nullable=True))
    op.add_column('tasks', sa.Column('estimated_hours', sa.Numeric(precision=8, scale=2), nullable=True))
    op.add_column('tasks', sa.Column('actual_hours', sa.Numeric(precision=8, scale=2), nullable=True))
    op.add_column('tasks', sa.Column('completion_percentage', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('assigned_to', sa.Integer(), nullable=True))
    op.add_column('tasks', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'resources', ['assigned_to'], ['id'])
    
    # Update existing columns
    op.alter_column('tasks', 'priority',
               existing_type=sa.INTEGER(),
               type_=sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'BACKLOG', name='priority'),
               existing_nullable=True)
    op.alter_column('tasks', 'status',
               existing_type=sa.VARCHAR(),
               type_=sa.Enum('BACKLOG', 'PLANNING', 'IN_PROGRESS', 'UAT', 'PILOT', 'ROLLOUT', 'COMPLETE', 'ON_HOLD', 'CANCELLED', name='taskstatus'),
               existing_nullable=True)


def downgrade():
    # Drop new tables
    op.drop_table('project_resources')
    op.drop_table('project_stores')
    op.drop_index(op.f('ix_audit_logs_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_project_metrics_id'), table_name='project_metrics')
    op.drop_table('project_metrics')
    op.drop_index(op.f('ix_risks_id'), table_name='risks')
    op.drop_table('risks')
    op.drop_index(op.f('ix_budgets_id'), table_name='budgets')
    op.drop_table('budgets')
    op.drop_index(op.f('ix_resources_id'), table_name='resources')
    op.drop_table('resources')
    op.drop_index(op.f('ix_stores_id'), table_name='stores')
    op.drop_table('stores')
    
    # Remove added columns from existing tables
    op.drop_column('tasks', 'updated_at')
    op.drop_column('tasks', 'assigned_to')
    op.drop_column('tasks', 'completion_percentage')
    op.drop_column('tasks', 'actual_hours')
    op.drop_column('tasks', 'estimated_hours')
    op.drop_column('tasks', 'title')
    
    op.drop_column('projects', 'updated_at')
    op.drop_column('projects', 'created_at')
    op.drop_column('projects', 'parent_id')
    op.drop_column('projects', 'completion_percentage')
    op.drop_column('projects', 'actual_cost')
    op.drop_column('projects', 'budget_total')
    op.drop_column('projects', 'end_date')
    op.drop_column('projects', 'start_date')
    op.drop_column('projects', 'priority')
    op.drop_column('projects', 'status')
    op.drop_column('projects', 'project_type')
    op.drop_column('projects', 'description')
    
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'store_number')
    op.drop_column('users', 'department')
    op.drop_column('users', 'role')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    
    # Revert column types
    op.alter_column('tasks', 'status',
               existing_type=sa.Enum('BACKLOG', 'PLANNING', 'IN_PROGRESS', 'UAT', 'PILOT', 'ROLLOUT', 'COMPLETE', 'ON_HOLD', 'CANCELLED', name='taskstatus'),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.alter_column('tasks', 'priority',
               existing_type=sa.Enum('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'BACKLOG', name='priority'),
               type_=sa.INTEGER(),
               existing_nullable=True)