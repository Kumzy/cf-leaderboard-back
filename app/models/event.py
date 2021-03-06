from sqlalchemy.dialects.postgresql import UUID
from app import db, ma
from app.models.score import Score

class Event(db.Model):
    __tablename__ = 'event'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'))
    scores = db.relationship(Score, primaryjoin='Score.event_id==Event.id',
                             uselist=True, viewonly=True, lazy='dynamic')
    max_score_best = db.Column(db.Boolean, nullable=False, server_default=db.text('True'))
    #competition = db.relationship("Competition", primaryjoin="Competition.id==Event.competition_id",remote_side="Competition.id")

class EventSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Event

    id = ma.auto_field()
    name = ma.auto_field()
    created_on = ma.auto_field()
    scores = ma.Nested('ScoreSchema',many=True)
    #competition = ma.Nested('CompetitionSchema')