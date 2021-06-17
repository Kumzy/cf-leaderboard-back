from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Score(db.Model):
    __tablename__ = 'score'
    __name_list__ = f'{__tablename__}s'

    __table_args__ = (
        db.UniqueConstraint('competitor_id', 'event_id'),
        db.UniqueConstraint('team_id', 'event_id')
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    result = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey('event.id'))
    event = db.relationship("Event", primaryjoin="Event.id==Score.event_id",
                                  remote_side="Event.id", lazy='subquery')
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))
    category = db.relationship("Category", primaryjoin="Category.id==Score.category_id",
                            remote_side="Category.id", lazy='subquery')
    competitor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competitor.id'))
    competitor = db.relationship("Competitor", primaryjoin="Competitor.id==Score.competitor_id",
                            remote_side="Competitor.id", lazy='subquery' )
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('team.id'))
    team = db.relationship("Team", primaryjoin="Team.id==Score.team_id",
                                 remote_side="Team.id", lazy='subquery')
    tiebreak = db.Column(db.Integer)
    time = db.Column(db.Integer)

    def generateScoreNotParticipated(self, last_score: int):
        self.point = last_score + 1

class ScoreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Score
        include_fk = True
        load_instance = True

    id = ma.auto_field()
    result = ma.auto_field()
    created_on = ma.auto_field()
    event = ma.Nested('EventSchema')
    category = ma.Nested('CategorySchema')
    competitor = ma.Nested('CompetitorSchema')
    team = ma.Nested('TeamSchema')
    tiebreak = ma.auto_field()
    time = ma.auto_field()