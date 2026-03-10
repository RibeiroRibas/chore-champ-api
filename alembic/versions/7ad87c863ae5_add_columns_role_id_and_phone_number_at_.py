"""add columns role_id and phone_number at users table

Revision ID: 7ad87c863ae5
Revises: f9ea9d185f6e
Create Date: 2026-03-08 10:21:54.736603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = '7ad87c863ae5'
down_revision: Union[str, Sequence[str], None] = 'f9ea9d185f6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role_id', sa.Integer(), ForeignKey('roles.id'), nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'role_id')
    op.drop_column('users', 'phone_number')
