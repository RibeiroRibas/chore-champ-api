"""create refresh_token table

Revision ID: a7b8c9d0e1f2
Revises: 229dbba4426f
Create Date: 2026-03-13 09:42:24.954933

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b8c9d0e1f2'
down_revision: Union[str, Sequence[str], None] = '229dbba4426f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("auth_id", sa.Integer(), nullable=False),
        sa.Column("refresh_token", sa.String(36), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["auth_id"], ["auth.id"]),
    )


def downgrade() -> None:
    op.drop_table("refresh_tokens")
