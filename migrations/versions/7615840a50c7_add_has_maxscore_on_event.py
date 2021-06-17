"""Add has_maxscore on event

Revision ID: 7615840a50c7
Revises: 261bac5b2602
Create Date: 2021-03-28 18:59:39.625788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7615840a50c7'
down_revision = '261bac5b2602'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('has_maxscore', sa.Boolean(), server_default=sa.text('True'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'has_maxscore')
    # ### end Alembic commands ###