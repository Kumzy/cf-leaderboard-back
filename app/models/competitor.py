from sqlalchemy.dialects.postgresql import UUID, JSONB
from app import db, ma
from app.models.gender import GenderSchema
from app.models.country import CountrySchema
from sqlalchemy.ext.hybrid import hybrid_property

class Competitor(db.Model):
    __tablename__ = 'competitor'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True)
    active = db.Column(db.Boolean)
    avatar = db.Column(JSONB)
    height = db.Column(db.Integer)
    birthday_date = db.Column(db.Date)
    weight = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    gender_id = db.Column(UUID(as_uuid=True), db.ForeignKey('gender.id'))
    gender = db.relationship("Gender", primaryjoin="Gender.id==Competitor.gender_id",
                                     remote_side="Gender.id")
    nationality_id = db.Column(UUID(as_uuid=True), db.ForeignKey('country.id'))
    nationality = db.relationship("Country", primaryjoin="Country.id==Competitor.nationality_id",
                             remote_side="Country.id")

    # Retrieve the last price from the API
    @hybrid_property
    def longname(self):
        return self.firstname + ' ' + self.lastname

class CompetitorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competitor
        include_fk = True
        load_instance = True

    id = ma.auto_field()
    firstname = ma.auto_field()
    lastname = ma.auto_field()
    avatar = ma.auto_field()
    email = ma.auto_field()
    active = ma.auto_field()
    height = ma.auto_field()
    weight = ma.auto_field()
    birthday_date = ma.auto_field()
    created_on = ma.auto_field()
    gender = ma.Nested(GenderSchema)
    nationality = ma.Nested(CountrySchema)
    longname = ma.String()