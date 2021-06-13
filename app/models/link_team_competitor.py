from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class LinkTeamCompetitor(db.Model):
    __tablename__ = 'link_team_competitor'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    competitor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competitor.id'))
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('team.id'))

class LinkTeamCompetitorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LinkTeamCompetitor

    id = ma.auto_field()