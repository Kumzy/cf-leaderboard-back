from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Category(db.Model):
    __tablename__ = 'category'
    __name_list__ = f'{__tablename__[:-1]}ies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))

class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Category

    id = ma.auto_field()
    name = ma.auto_field()
    created_on = ma.auto_field()