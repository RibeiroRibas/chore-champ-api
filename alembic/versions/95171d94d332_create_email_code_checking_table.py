"""create email code checking table

Revision ID: 95171d94d332
Revises: b6d972c15d51
Create Date: 2026-03-01 16:14:36.328484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95171d94d332'
down_revision: Union[str, Sequence[str], None] = 'b6d972c15d51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'email_code_checking',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('code', sa.SMALLINT(), nullable=False),
        sa.Column('is_code_blocked', sa.Boolean(), nullable=False),
        sa.Column('validated', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('validation_attempts', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_code_checking_email'), 'email_code_checking', ['email'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_email_code_checking_email'), table_name='email_code_checking')
    op.drop_table('email_code_checking')
