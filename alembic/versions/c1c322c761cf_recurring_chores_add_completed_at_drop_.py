"""recurring_chores: add completed_at, drop parent_chore_id

Revision ID: c1c322c761cf
Revises: 3c4d5e6f7a8b
Create Date: 2026-03-27 20:20:06.854375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1c322c761cf'
down_revision: Union[str, Sequence[str], None] = '3c4d5e6f7a8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "c_recurring_chores",
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )
    op.drop_constraint(
        "fk_recurring_chores_parent_chore_id",
        "c_recurring_chores",
        type_="foreignkey",
    )
    op.drop_column("c_recurring_chores", "parent_chore_id")
def downgrade() -> None:
    op.add_column(
        "c_recurring_chores",
        sa.Column("parent_chore_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_recurring_chores_parent_chore_id",
        "c_recurring_chores",
        "c_chores",
        ["parent_chore_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("c_recurring_chores", "completed_at")
