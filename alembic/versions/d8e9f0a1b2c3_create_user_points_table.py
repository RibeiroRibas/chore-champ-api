"""create user_points table

Revision ID: d8e9f0a1b2c3
Revises: c7d8e9f0a1b2
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d8e9f0a1b2c3"
down_revision: Union[str, Sequence[str], None] = "c7d8e9f0a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_points",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("total_points", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("points_redeemed", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("family_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["family_id"], ["families.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_user_points_user_id"),
    )


def downgrade() -> None:
    op.drop_table("user_points")
