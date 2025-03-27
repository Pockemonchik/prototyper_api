"""empty message

Revision ID: 1131c7a10cb4
Revises: 9e6d0ea78eba
Create Date: 2025-03-27 13:42:00.516546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1131c7a10cb4'
down_revision: Union[str, None] = '9e6d0ea78eba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('lesson_results')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lesson_results',
    sa.Column('percentage', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('lesson_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], name='lesson_results_lesson_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='lesson_results_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='lesson_results_pkey')
    )
    # ### end Alembic commands ###
