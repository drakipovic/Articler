import os

import articler.views
from articler.main import app, api
from articler.database import db
from articler.models import User, Article
from articler.api import Users, Articles,  UserArticles, ArticleResource, UserResource

api.add_resource(Users, '/users')
api.add_resource(Articles, '/articles')
api.add_resource(UserArticles, '/user/<int:user_id>/articles')
api.add_resource(ArticleResource, '/article/<int:article_id>')
api.add_resource(UserResource, '/user/<int:user_id>')

db.init_app(app)
if not os.path.exists('articler/dev.db'):
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0', debug=True)