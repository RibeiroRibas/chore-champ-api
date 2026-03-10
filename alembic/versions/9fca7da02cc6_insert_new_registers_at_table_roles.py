"""insert new registers at table roles

Revision ID: 9fca7da02cc6
Revises: 7ad87c863ae5
Create Date: 2026-03-08 10:25:56.653176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fca7da02cc6'
down_revision: Union[str, Sequence[str], None] = '7ad87c863ae5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO roles (name) VALUES ('Administrator'), ('Colaborador')")


def downgrade() -> None:
    op.execute("DELETE FROM roles WHERE name IN ('Administrator', 'Colaborador')")
