from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class LinkCompetitionGender(db.Model):
    __tablename__ = 'link_competition_gender'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    gender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gender.id'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'))

class LinkCompetitionGenderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = LinkCompetitionGender

    id = ma.auto_field()
