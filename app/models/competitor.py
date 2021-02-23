from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Competitor(db.Model):
    __tablename__ = 'competitor'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True)
    active = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))

class CompetitorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competitor

    id = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    email = ma.auto_field()
    active = ma.auto_field()
    created_on = ma.auto_field()