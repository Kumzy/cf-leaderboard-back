from sqlalchemy.dialects.postgresql import UUID
from app import db, ma

class Score(db.Model):
    __tablename__ = 'score'
    __name_list__ = f'{__tablename__}s'

    __table_args__ = (
        db.UniqueConstraint('competitor_id', 'event_id'),
    )

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    result = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey('event.id'))
    # event = db.relationship("Event", primaryjoin="Event.id==Score.event_id",
    #                               remote_side="Event.id")
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('category.id'))
    category = db.relationship("Category", primaryjoin="Category.id==Score.category_id",
                            remote_side="Category.id")
    competitor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('competitor.id'))
    competitor = db.relationship("Competitor", primaryjoin="Competitor.id==Score.competitor_id",
                            remote_side="Competitor.id")


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