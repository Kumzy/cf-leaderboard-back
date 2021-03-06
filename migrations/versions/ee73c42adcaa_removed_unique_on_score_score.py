"""Removed unique on score.score

Revision ID: ee73c42adcaa
Revises: aa87c6e976d5
Create Date: 2021-03-03 18:31:46.447569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee73c42adcaa'
down_revision = 'aa87c6e976d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('score_score_key', 'score', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('score_score_key', 'score', ['score'])
    # ### end Alembic commands ###
