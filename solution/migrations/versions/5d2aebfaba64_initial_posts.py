"""initial posts

Revision ID: 5d2aebfaba64
Revises: d2ce850bcdbe
Create Date: 2024-03-04 19:22:46.590394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d2aebfaba64'
down_revision: Union[str, None] = 'd2ce850bcdbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("createdAt", sa.DateTime(), nullable=False),
        sa.Column("content", sa.String(1000), nullable=False),
        sa.Column("tags", sa.ARRAY(sa.String(20)), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_user_id_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_posts')),
        sa.UniqueConstraint('id', name=op.f('uq_posts_id'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("fk_posts_user_id_users"), "posts")
    op.drop_table('posts')
    # ### end Alembic commands ###
