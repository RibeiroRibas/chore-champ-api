"""create roles table

Revision ID: f9ea9d185f6e
Revises: 9ab6a0893a7f
Create Date: 2026-03-08 10:21:32.800462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9ea9d185f6e'
down_revision: Union[str, Sequence[str], None] = '9ab6a0893a7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('roles')
