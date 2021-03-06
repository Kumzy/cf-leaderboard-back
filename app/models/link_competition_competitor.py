from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class LinkCompetitionCompetitor(db.Model):
    __tablename__ = 'link_competition_competitor'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    competitor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competitor.id'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'))

class LinkCompetitionCompetitorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LinkCompetitionCompetitor

    id = ma.auto_field()