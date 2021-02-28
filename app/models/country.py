from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Country(db.Model):
    __tablename__ = 'country'
    __name_list__ = f'{__tablename__[:-1]}ies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, nullable=False)
    iso2 = db.Column(db.Text, nullable=False)
    iso3 = db.Column(db.Text, nullable=False)

class CountrySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Country

    id = ma.auto_field()
    name = ma.auto_field()
    iso2 = ma.auto_field()
    iso3 = ma.auto_field()