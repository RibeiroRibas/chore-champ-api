"""insert creator at table roles

Revision ID: 65975e388538
Revises: 9fca7da02cc6
Create Date: 2026-03-08 16:06:07.556548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65975e388538'
down_revision: Union[str, Sequence[str], None] = '9fca7da02cc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO roles (name) VALUES ('Criador')")


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('Criador')")
