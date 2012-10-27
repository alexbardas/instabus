"""create checkins table

Revision ID: 36c1b1d3c9a4
Revises: None
Create Date: 2012-10-27 22:35:32.169630

"""

# revision identifiers, used by Alembic.
revision = '36c1b1d3c9a4'
down_revision = None

from alembic import op
from sqlalchemy import *
from geoalchemy import *

def upgrade():
    op.create_table(
        'checkins',
        Column('id', Integer, primary_key=True),
        Column('type', Unicode(3), nullable=False),
        Column('created', DateTime),
        Column('longitude', Float),
        Column('latitude', Float),
        # XXX(daniel) Had trouble getting this working with alembic and sqlalchemy-migrate (migrations)
        # GeometryColumn('location', Point(2)),
    )

def downgrade():
    op.drop_table('checkins')
