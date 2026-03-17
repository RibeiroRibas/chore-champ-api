"""add is_recurring to chores, create days_of_week and recurring_chores

Revision ID: e2f3a4b5c6d7
Revises: a7b8c9d0e1f2
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e2f3a4b5c6d7"
down_revision: Union[str, Sequence[str], None] = "a7b8c9d0e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "chores",
        sa.Column(
            "is_recurring",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.create_table(
        "days_of_week",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        sa.text(
            """
            INSERT INTO days_of_week (id, name) VALUES
            (1, 'Segunda'), (2, 'Terça'), (3, 'Quarta'), (4, 'Quinta'),
            (5, 'Sexta'), (6, 'Sábado'), (7, 'Domingo')
            """
        )
    )

    op.create_table(
        "recurring_chores",
        sa.Column("chore_id", sa.Integer(), nullable=False),
        sa.Column("day_of_week_id", sa.Integer(), nullable=False),
        sa.Column("family_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chore_id"],
            ["chores.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["day_of_week_id"],
            ["days_of_week.id"],
        ),
        sa.ForeignKeyConstraint(
            ["family_id"],
            ["families.id"],
        ),
        sa.PrimaryKeyConstraint("chore_id", "day_of_week_id"),
    )


def downgrade() -> None:
    op.drop_table("recurring_chores")
    op.drop_table("days_of_week")
    op.drop_column("chores", "is_recurring")
