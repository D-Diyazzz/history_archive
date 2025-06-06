"""empty message

Revision ID: e2cdcf7b3888
Revises: f4744c3583c6
Create Date: 2024-09-17 11:49:31.048795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2cdcf7b3888'
down_revision: Union[str, None] = 'f4744c3583c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document_links', 'sequence_number')
    op.drop_column('phono_document_links', 'sequence_number')
    op.drop_column('photo_document_links', 'sequence_number')
    op.drop_column('video_document_links', 'sequence_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('video_document_links', sa.Column('sequence_number', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('photo_document_links', sa.Column('sequence_number', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('phono_document_links', sa.Column('sequence_number', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('document_links', sa.Column('sequence_number', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
