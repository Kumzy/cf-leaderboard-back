"""Added order to event

Revision ID: 261bac5b2602
Revises: 1101741fb4c6
Create Date: 2021-03-14 10:52:32.927291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '261bac5b2602'
down_revision = '1101741fb4c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('order', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'order')
    # ### end Alembic commands ###