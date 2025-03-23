"""empty message

Revision ID: 85d20c3060ae
Revises: a9d664f14f75
Create Date: 2025-03-21 08:55:40.541697

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "85d20c3060ae"
down_revision: Union[str, None] = "a9d664f14f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lesson_results",
        sa.Column("percentage", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lesson_steps",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("lesson_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_id"],
            ["lessons.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lesson_step_results",
        sa.Column("percentage", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lesson_step_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_step_id"],
            ["lesson_steps.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lesson_step_texts",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("lesson_step_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_step_id"],
            ["lesson_steps.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "lesson_step_timings",
        sa.Column("time", sa.String(), nullable=False),
        sa.Column("date", sa.String(), nullable=True),
        sa.Column("level", sa.String(), nullable=True),
        sa.Column("lesson_step_result_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["lesson_step_result_id"],
            ["lesson_step_results.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_column("lessons", "text")
    op.drop_column("lessons", "timing")
    op.drop_column("lessons", "status")
    op.drop_column("lessons", "percentage")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "lessons",
        sa.Column("percentage", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "lessons", sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "lessons", sa.Column("timing", sa.INTEGER(), autoincrement=False, nullable=True)
    )
    op.add_column(
        "lessons", sa.Column("text", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.drop_table("lesson_step_timings")
    op.drop_table("lesson_step_texts")
    op.drop_table("lesson_step_results")
    op.drop_table("lesson_steps")
    op.drop_table("lesson_results")
    # ### end Alembic commands ###
