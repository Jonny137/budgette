"""First migration

Revision ID: 001
Revises: 
Create Date: 2022-03-19 15:37:35.046097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expensetype',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_expensetype_name'), 'expensetype', ['name'], unique=True)
    op.create_table('expense',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('person', sa.String(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expense_type_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['expense_type_id'], ['expensetype.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_expense_amount'), 'expense', ['amount'], unique=False)
    op.create_index(op.f('ix_expense_name'), 'expense', ['name'], unique=False)
    op.create_index(op.f('ix_expense_person'), 'expense', ['person'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_expense_person'), table_name='expense')
    op.drop_index(op.f('ix_expense_name'), table_name='expense')
    op.drop_index(op.f('ix_expense_amount'), table_name='expense')
    op.drop_table('expense')
    op.drop_index(op.f('ix_expensetype_name'), table_name='expensetype')
    op.drop_table('expensetype')
    # ### end Alembic commands ###
