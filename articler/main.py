import os
from datetime import timedelta
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.ext.restful_swagger_2 import Api
from flask.ext.httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy


app = Flask('articler', template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if os.environ.get('TEST') else 'sqlite:///dev.db' 
app.config['SECRET_KEY'] = 'tajna'

db = SQLAlchemy(app)

auth = HTTPBasicAuth()



api = Api(app, api_version='1', api_spec_url='/api/docs', description='API endpoints documentation')
CORS(app)

handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)