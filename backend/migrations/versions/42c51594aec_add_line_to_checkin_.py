"""add line to Checkin model

Revision ID: 42c51594aec
Revises: 36c1b1d3c9a4
Create Date: 2012-10-28 03:59:59.870135

"""

# revision identifiers, used by Alembic.
revision = '42c51594aec'
down_revision = '36c1b1d3c9a4'

from alembic import op
from sqlalchemy import *

def upgrade():
    op.add_column('checkins', Column('line', Unicode))

def downgrade():
    op.drop_column('checkins', 'line')
