"""Removed table link_team_competition

Revision ID: 7a3246e50bcd
Revises: 77e078c295df
Create Date: 2021-06-06 15:15:16.056782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7a3246e50bcd'
down_revision = '77e078c295df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link_competition_team')
    op.add_column('team', sa.Column('competition_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'team', 'competition', ['competition_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'team', type_='foreignkey')
    op.drop_column('team', 'competition_id')
    op.create_table('link_competition_team',
    sa.Column('id', postgresql.UUID(), server_default=sa.text('gen_random_uuid()'), autoincrement=False, nullable=False),
    sa.Column('team_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('competition_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['competition_id'], ['competition.id'], name='link_competition_team_competition_id_fkey'),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], name='link_competition_team_team_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='link_competition_team_pkey')
    )
    # ### end Alembic commands ###
