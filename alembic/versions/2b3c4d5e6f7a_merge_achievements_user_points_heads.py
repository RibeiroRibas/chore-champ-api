"""merge achievements and user_points heads

Revision ID: 2b3c4d5e6f7a
Revises: ('01a2b3c4d5e6', 'd8e9f0a1b2c3')
Create Date: 2026-03-07

"""

from typing import Sequence, Union

from alembic import op


revision: str = "2b3c4d5e6f7a"
down_revision: Union[str, Sequence[str], None] = ("01a2b3c4d5e6", "d8e9f0a1b2c3")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Merge migration: no schema changes required.
    pass


def downgrade() -> None:
    # Merge migration: no schema changes required.
    pass

