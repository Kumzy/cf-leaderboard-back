from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
import config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_object(Config)


# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
# app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'


# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
#
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False

app.config['JWT_SECRET_KEY'] = 'ksIm5iZiI6MTU4ODYwODAwOSwianRpIjoiOWE'
#app.config['JWT_SECRET_KEY'] = os.urandom(24)


# jwt = JWTManager(app)

# enable CORS
cors = CORS()
CORS(app, origins='http://localhost:8080', resources={r'/*': {'origins': '*'}}, supports_credentials=True)

#login = LoginManager(app)
#login.login_view = 'login'
db = SQLAlchemy(app)
ma = Marshmallow(app)
#cors.init_app(app, resources={r"*": {"origins": "*"}})
migrate = Migrate(app, db)

#Routes import
from app.routes import competitor
from app.routes import country
from app.routes import gender

#Models import
from app.models.country import Country
from app.models.gender import Gender
from app.models.category import Category
from app.models.competitor import Competitor
from app.models.competition import Competition
from app.models.event import Event


