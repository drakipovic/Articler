import os

import articler.views
from articler.main import app, api
from articler.database import db
from articler.models import User, Article
from articler.api import Users, Articles,  UserArticles, ArticleResource


api.add_resource(Users, '/api/users')
api.add_resource(Articles, '/api/articles')
api.add_resource(UserArticles, '/api/user/<int:user_id>/articles')
api.add_resource(ArticleResource, '/api/article/<int:article_id>')


app.run(host='0.0.0.0', debug=True)