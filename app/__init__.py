from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
#app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
#
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES

jwt = JWTManager(app)

# enable CORS
cors = CORS()
#CORS(app, origins='http://localhost:8080', resources={r'/*': {'origins': '*'}}, supports_credentials=True)
CORS(app, resources={r'/*': {'origins': '*'}})#, supports_credentials=True)

#login = LoginManager(app)
#login.login_view = 'login'
db = SQLAlchemy(app)
ma = Marshmallow(app)
#cors.init_app(app, resources={r"*": {"origins": "*"}})
migrate = Migrate(app, db)

#Models import
from app.models.country import Country
from app.models.gender import Gender
from app.models.category import Category
from app.models.competitor import Competitor
from app.models.competition import Competition
from app.models.event import Event
from app.models.score import Score
from app.models.link_competition_category import LinkCompetitionCategory
from app.models.link_competition_competitor import LinkCompetitionCompetitor
from app.models.link_competition_gender import LinkCompetitionGender
from app.models.user import User

#Routes import
from app.routes import competitor
from app.routes import country
from app.routes import gender
from app.routes import competition
from app.routes import score
from app.routes import login

if __name__ == "__main__":
    app.run(host='0.0.0.0')
