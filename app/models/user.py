from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class User(db.Model):
    __tablename__ = 'user'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True)
    active = db.Column(db.Boolean)
    password_hash = db.Column(db.Text, nullable=False)

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    email = ma.auto_field()
    active = ma.auto_field()