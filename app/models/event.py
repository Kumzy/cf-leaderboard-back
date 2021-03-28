from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Event(db.Model):
    __tablename__ = 'event'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    competition_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competition.id'))
    # scores = db.relationship(Score, primaryjoin='Score.event_id==Event.id',
    #                          # uselist=True, viewonly=True, lazy='dynamic')
    max_score_best = db.Column(db.Boolean, nullable=False, server_default=db.text('True'))
    has_tiebreak = db.Column(db.Boolean, nullable=False, server_default=db.text('True'))
    time_cap = db.Column(db.Integer)
    is_amrap = db.Column(db.Boolean, nullable=False, server_default=db.text('False'))
    has_maxscore = db.Column(db.Boolean, nullable=False, server_default=db.text('True'))
    max_score = db.Column(db.Integer)
    order = db.Column(db.Integer)
    #competition = db.relationship("Competition", primaryjoin="Competition.id==Event.competition_id",remote_side="Competition.id")

class EventSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Event

    id = ma.auto_field()
    name = ma.auto_field()
    created_on = ma.auto_field()
    scores = ma.Nested('ScoreSchema',many=True)
    max_score_best = ma.auto_field()
    has_tiebreak = ma.auto_field()
    time_cap = ma.auto_field()
    is_amrap = ma.auto_field()
    max_score = ma.auto_field()
    order = ma.auto_field()
    #competition = ma.Nested('CompetitionSchema')