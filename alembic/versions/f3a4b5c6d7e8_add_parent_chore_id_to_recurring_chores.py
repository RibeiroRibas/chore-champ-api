"""add parent_chore_id to recurring_chores

Revision ID: f3a4b5c6d7e8
Revises: e2f3a4b5c6d7
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f3a4b5c6d7e8"
down_revision: Union[str, Sequence[str], None] = "e2f3a4b5c6d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "recurring_chores",
        sa.Column("parent_chore_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_recurring_chores_parent_chore_id",
        "recurring_chores",
        "chores",
        ["parent_chore_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_recurring_chores_parent_chore_id",
        "recurring_chores",
        type_="foreignkey",
    )
    op.drop_column("recurring_chores", "parent_chore_id")
