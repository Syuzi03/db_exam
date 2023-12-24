"""Add new columns to Purchase model

Revision ID: 9e4ad39701d3
Revises: 17226cfce21a
Create Date: 2023-12-25 01:57:00.732265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4ad39701d3'
down_revision: Union[str, None] = '17226cfce21a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Purchase', sa.Column('new_column5', sa.String(length=50)))
    op.add_column('Purchase', sa.Column('new_column6', sa.Integer()))

def downgrade():
    op.drop_column('Purchase', 'new_column5')
    op.drop_column('Purchase', 'new_column6')

def upgrade():
    op.create_index('ix_purchase_new_column5', 'Purchase', ['new_column5'])
    op.create_index('ix_purchase_new_column6', 'Purchase', ['new_column6'])

def downgrade():
    op.drop_index('ix_purchase_new_column5', 'Purchase')
    op.drop_index('ix_purchase_new_column6', 'Purchase')