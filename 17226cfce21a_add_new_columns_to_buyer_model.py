"""Add new columns to Buyer model

Revision ID: 17226cfce21a
Revises: 359d1a869fb2
Create Date: 2023-12-25 01:49:21.127264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17226cfce21a'
down_revision: Union[str, None] = '359d1a869fb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Buyer', sa.Column('new_column3', sa.String(length=50)))
    op.add_column('Buyer', sa.Column('new_column4', sa.Integer()))

def downgrade():
    op.drop_column('Buyer', 'new_column3')
    op.drop_column('Buyer', 'new_column4')


def upgrade():
    op.create_index('ix_buyer_new_column3', 'Buyer', ['new_column3'])
    op.create_index('ix_buyer_new_column4', 'Buyer', ['new_column4'])

def downgrade():
    op.drop_index('ix_buyer_new_column3', 'Buyer')
    op.drop_index('ix_buyer_new_column4', 'Buyer')

