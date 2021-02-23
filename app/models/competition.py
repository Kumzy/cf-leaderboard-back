from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Competition(db.Model):
    __tablename__ = 'competition'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))

class CompetitionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competition

    id = ma.auto_field()
    name = ma.auto_field()
    created_on = ma.auto_field()