"""Add made_at column

Revision ID: 002
Revises: 001
Create Date: 2022-03-30 19:01:34.958395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('expense', sa.Column('made_at', sa.DateTime, nullable=True))


def downgrade():
    op.drop_column('expense', 'made_at')
