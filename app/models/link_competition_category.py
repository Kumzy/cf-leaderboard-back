from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class LinkCompetitionCategory(db.Model):
    __tablename__ = 'link_competition_category'
    __name_list__ = f'{__tablename__[:-1]}ies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'))

class LinkCompetitionCategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = LinkCompetitionCategory

    id = ma.auto_field()
