from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from models import User

app = Flask('articler', template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
app.config['SECRET_KEY'] = 'tajna'
#app.config['JWT_AUTH_URL_RULE'] = '/api/token'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

api = Api(app, prefix='/api')

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    return User.query.filter_by(id=payload['identity'])

jwt = JWT(app, authenticate, identity)