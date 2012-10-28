"""Created the Datapoints table.

Revision ID: 27ba4bd69d9f
Revises: 42c51594aec
Create Date: 2012-10-28 07:05:47.470124

"""

# revision identifiers, used by Alembic.
revision = '27ba4bd69d9f'
down_revision = '42c51594aec'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('datapoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Unicode(), nullable=False),
    sa.Column('line', sa.Unicode(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('is_demo', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column(u'checkins', u'line',
               existing_type=sa.VARCHAR(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'checkins', u'line',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_table('datapoints')
    ### end Alembic commands ###