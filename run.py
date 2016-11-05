import os

import articler.views
from articler.main import app, api
from articler.database import db
from articler.models import User, Article
from articler.api import Users

api.add_resource(Users, '/users')

db.init_app(app)
if not os.path.exists('articler/dev.db'):
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0', debug=True)