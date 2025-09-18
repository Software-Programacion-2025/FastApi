"""add state column to tasks

Revision ID: 20250915_add_state
Revises: 27d376d56b88
Create Date: 2025-09-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250915_add_state'
down_revision = '27d376d56b88'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'state' column with default 'pending'
    op.add_column('tasks', sa.Column('state', sa.String(length=20), nullable=False, server_default='pending'))


def downgrade() -> None:
    op.drop_column('tasks', 'state')
