"""Add link competition gender link table

Revision ID: edb4eb1fbb04
Revises: e745c8f6a08d
Create Date: 2021-03-06 17:17:41.991993

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'edb4eb1fbb04'
down_revision = 'e745c8f6a08d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link_competition_gender',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('gender_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('competition_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['competition_id'], ['competition.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['gender.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link_competition_gender')
    # ### end Alembic commands ###
