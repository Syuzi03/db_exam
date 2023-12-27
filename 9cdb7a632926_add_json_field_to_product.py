"""add_json_field_to_product

Revision ID: 9cdb7a632926
Revises: 
Create Date: 2023-12-27 02:05:12.746732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cdb7a632926'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Product', sa.Column('json_data', sa.JSON))

def downgrade():
    op.drop_column('Product', 'json_data')