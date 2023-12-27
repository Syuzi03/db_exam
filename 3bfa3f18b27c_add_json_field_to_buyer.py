"""add_json_field_to_buyer

Revision ID: 3bfa3f18b27c
Revises: 68e5adfb3155
Create Date: 2023-12-27 02:13:21.007230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3bfa3f18b27c'
down_revision: Union[str, None] = '68e5adfb3155'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Buyer', sa.Column('json_data', sa.JSON))

def downgrade():
    op.drop_column('Buyer', 'json_data')