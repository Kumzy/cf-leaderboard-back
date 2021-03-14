"""Add max_score to event

Revision ID: 1101741fb4c6
Revises: 6406b7c8b95b
Create Date: 2021-03-13 13:55:56.054639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1101741fb4c6'
down_revision = '6406b7c8b95b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('max_score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'max_score')
    # ### end Alembic commands ###
