from sqlalchemy.dialects.postgresql import UUID
from app import db, ma
from app.models.event import Event
from app.models.category import Category
from app.models.competitor import Competitor
from app.models.gender import Gender
from app.models.team import Team
from app.models.link_competition_category import LinkCompetitionCategory
from app.models.link_competition_competitor import LinkCompetitionCompetitor
from app.models.link_competition_gender import LinkCompetitionGender

class Competition(db.Model):
    __tablename__ = 'competition'
    __name_list__ = f'{__tablename__}s'

    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text('gen_random_uuid()'))
    name = db.Column(db.Text, unique=True)
    date_start = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime(timezone=True),server_default=db.text('now()'))
    events = db.relationship(Event, primaryjoin='Event.competition_id==Competition.id',
                               order_by="asc(Event.order)",
                               uselist=True, viewonly=True, lazy='dynamic')
    categories = db.relationship(Category, secondary='link_competition_category', uselist=True, viewonly=True)
    competitors = db.relationship(Competitor, secondary='link_competition_competitor', uselist=True, viewonly=True)
    teams = db.relationship(Team, primaryjoin='Team.competition_id==Competition.id',
                               uselist=True, viewonly=True, lazy='dynamic')
    genders = db.relationship(Gender, secondary='link_competition_gender', uselist=True, viewonly=True)

class CompetitionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Competition
        include_fk = True
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    date_start = ma.auto_field()
    active = ma.auto_field()
    created_on = ma.auto_field()
    events = ma.Nested('EventSchema',many=True)
    categories = ma.Nested('CategorySchema', many=True)
    competitors = ma.Nested('CompetitorSchema', many=True)
    genders = ma.Nested('GenderSchema', many=True)
    teams = ma.Nested('TeamSchema', many=True)