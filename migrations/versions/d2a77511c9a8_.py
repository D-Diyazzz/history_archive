"""empty message

Revision ID: d2a77511c9a8
Revises: 72803faa1739
Create Date: 2024-11-05 23:35:55.141702

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2a77511c9a8'
down_revision: Union[str, None] = '72803faa1739'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection_comment',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('collection_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['collection_id'], ['collection.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_collection_comment_id'), 'collection_comment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_collection_comment_id'), table_name='collection_comment')
    op.drop_table('collection_comment')
    # ### end Alembic commands ###
