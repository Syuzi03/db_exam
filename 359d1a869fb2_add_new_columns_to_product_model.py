"""Add new columns to Product model

Revision ID: 359d1a869fb2
Revises: 
Create Date: 2023-12-24 02:58:08.339100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '359d1a869fb2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.add_column('Product', sa.Column('new_column1', sa.String(length=50)))
    op.add_column('Product', sa.Column('new_column2', sa.Integer()))

def downgrade():
    op.drop_column('Product', 'new_column1')
    op.drop_column('Product', 'new_column2')

def upgrade():
    op.create_index('ix_product_new_column1', 'Product', ['new_column1'])
    op.create_index('ix_product_new_column2', 'Product', ['new_column2'])

def downgrade():
    op.drop_index('ix_product_new_column1', 'Product')
    op.drop_index('ix_product_new_column2', 'Product')
