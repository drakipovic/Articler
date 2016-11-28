from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.restful_swagger_2 import Api
from flask.ext.httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

from models import User


app = Flask('articler', template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
app.config['SECRET_KEY'] = 'tajna'

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.check_password(password):
        return False

    return True

api = Api(app, api_version='1', api_spec_url='/api/docs', description='API endpoints documentation')
CORS(app)

handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)