from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api

from api import Users

app = Flask('articler', template_folder='templates', static_folder='static')

db = SQLAlchemy(app)

api = Api(app, prefix='/api')
api.add_resource(Users, '/users')