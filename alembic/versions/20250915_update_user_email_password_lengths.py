"""update users email uniqueness and password length

Revision ID: 20250915_update_user
Revises: 20250915_add_state
Create Date: 2025-09-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250915_update_user'
down_revision = '20250915_add_state'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Expand password length and email length, and add unique + index to email
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('password', type_=sa.String(length=100))
        batch_op.alter_column('emails', type_=sa.String(length=100))
        batch_op.create_index('ix_users_emails', ['emails'], unique=True)


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('ix_users_emails')
        batch_op.alter_column('emails', type_=sa.String(length=30))
        batch_op.alter_column('password', type_=sa.String(length=30))
