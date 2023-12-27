"""add_json_field_to_purchase

Revision ID: 68e5adfb3155
Revises: 12e79f1d7c5b
Create Date: 2023-12-27 02:10:25.740701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68e5adfb3155'
down_revision: Union[str, None] = '12e79f1d7c5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Purchase', sa.Column('json_data', sa.JSON))

def downgrade():
    op.drop_column('Purchase', 'json_data')
