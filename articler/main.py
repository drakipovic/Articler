from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask.ext.httpauth import HTTPBasicAuth

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

api = Api(app, prefix='/api')