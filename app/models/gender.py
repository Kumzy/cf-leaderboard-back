from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Gender(db.Model):
    __tablename__ = 'gender'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True, nullable=False)

class GenderSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Gender

    id = ma.auto_field()
    name = ma.auto_field()