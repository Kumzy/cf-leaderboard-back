"""Add unique constraint on score competitor/event

Revision ID: 5b53db86c280
Revises: d97af6673303
Create Date: 2021-03-04 22:28:02.307275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b53db86c280'
down_revision = 'd97af6673303'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'score', ['competitor_id', 'event_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'score', type_='unique')
    # ### end Alembic commands ###
