from sqlalchemy.dialects.postgresql import UUID, JSONB
from app import db, ma
from app.models.competitor import Competitor
from app.models.link_team_competitor import LinkTeamCompetitor

class Team(db.Model):
    __tablename__ = 'team'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'), nullable=False)
    competitors = db.relationship(Competitor, secondary='link_team_competitor', uselist=True, viewonly=True)

class TeamSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Team
        include_fk = True
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    competitors = ma.Nested('CompetitorSchema', many=True)