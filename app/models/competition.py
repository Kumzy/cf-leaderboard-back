from sqlalchemy.dialects.postgresql import UUID
from app import db, ma
from app.models.event import Event

class Competition(db.Model):
    __tablename__ = 'competition'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    date_start = db.Column(db.Date)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    events = db.relationship(Event, primaryjoin='Event.competition_id==Competition.id',
                               uselist=True, viewonly=True, lazy='dynamic')


class CompetitionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competition
        include_fk = True
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    date_start = ma.auto_field()
    created_on = ma.auto_field()
    events = ma.Nested('EventSchema',many=True)