"""create achievements and user_achievements

Revision ID: 01a2b3c4d5e6
Revises: c7d8e9f0a1b2
Create Date: 2026-03-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


revision: str = "01a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = "c7d8e9f0a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "achievements",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("emoji", sa.String(), nullable=False),
        sa.Column("required_points", sa.Integer(), nullable=False),
    )
    op.create_table(
        "user_achievements",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("achievement_id", sa.Integer(), nullable=False),
        sa.Column("acquired_at", sa.DateTime(), nullable=True, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["achievement_id"], ["achievements.id"], ondelete="CASCADE"),
    )

    achievements_t = table(
        "achievements",
        column("id", sa.Integer()),
        column("title", sa.String()),
        column("description", sa.String()),
        column("emoji", sa.String()),
        column("required_points", sa.Integer()),
    )

    op.bulk_insert(
        achievements_t,
        [
            {
                "id": 1,
                "title": "Primeiros passos",
                "description": "Conclua sua primeira tarefa",
                "emoji": "⭐",
                "required_points": 50,
            },
            {
                "id": 2,
                "title": "Mão amiga",
                "description": "Conquiste 50 pontos",
                "emoji": "🤝",
                "required_points": 100,
            },
            {
                "id": 3,
                "title": "Super ajudante",
                "description": "Conquiste 150 pontos",
                "emoji": "🦸",
                "required_points": 150,
            },
            {
                "id": 4,
                "title": "Herói da casa",
                "description": "Conquiste 300 pontos",
                "emoji": "🏆",
                "required_points": 300,
            },
            {
                "id": 5,
                "title": "Lenda",
                "description": "Conquiste 500 pontos",
                "emoji": "👑",
                "required_points": 500,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("user_achievements")
    op.drop_table("achievements")

