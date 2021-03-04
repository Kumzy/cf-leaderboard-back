"""Add competition start_date

Revision ID: 4d03d5de745e
Revises: 8dc67297f3a0
Create Date: 2021-03-01 18:28:04.755985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d03d5de745e'
down_revision = '8dc67297f3a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('competition', sa.Column('date_start', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('competition', 'date_start')
    # ### end Alembic commands ###