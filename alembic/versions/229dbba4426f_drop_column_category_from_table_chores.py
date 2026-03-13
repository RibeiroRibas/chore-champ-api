"""drop column category from table chores

Revision ID: 229dbba4426f
Revises: d4e5f6a7b8c9
Create Date: 2026-03-12 19:22:21.867483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '229dbba4426f'
down_revision: Union[str, Sequence[str], None] = 'd4e5f6a7b8c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('chores','category')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'chores',
        sa.Column('category', sa.String(), nullable=True),
    )
