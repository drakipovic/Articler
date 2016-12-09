import json
from datetime import datetime

from flask import jsonify, request, session
from flask.ext.restful_swagger_2 import swagger, Resource
from flask_jwt import jwt_required

from models import User, Article
from main import auth


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.check_password(password):
        return False

    return True


def check_user(user, username=None):
    if username and user.username == username: return True
    if user.username != session['logged_in'].split(':')[0]:
        return {"error": "You don't have this kind of permission"}

    return True



class Users(Resource):
    
    @swagger.doc({
        'tags': ['user'],
        'description': 'Returns users list',
        'responses': {
            '200': {
                'description': 'Users',
            }
        }
    })
    def get(self):
        """Returns a list of all users"""
        users = User.query.all()
        
        users = [dict(user) for user in users]

        return jsonify({'users': users})
    
    @swagger.doc({
        'tags': ['user'],
        'description': 'Creates an user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'User',
            }
        },
      
    })
    def post(self):
        """Creates a new user"""
        username = request.json.get('username')
        password = request.json.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username taken"})
        
        user = User(username, password)
        user.save()

        return jsonify({"success": True, "user": dict(user)})
    
    @swagger.doc({
        'tags': ['user'],
        'description': 'Updates an user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'Success',
            }
        },
      
    })
    @auth.login_required
    def put(self):
        """Updating user"""
        data = request.get_json()
        
        user = User.query.get(data["user_id"])
        resp = check_user(user, data.get('username_test'))
        if resp != True:
            return jsonify(resp)
        
        user.username = data["username"]
        user.save()

        return jsonify({"success": True})

    @swagger.doc({
        'tags': ['user'],
        'description': 'Updates an user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'Success',
            }
        },
      
    })
    @auth.login_required
    def delete(self):
        """Deletes user"""
        username = request.json.get('username')

        user = User.query.filter_by(username=username).first()
        resp = check_user(user, username)
        if resp != True:
            return jsonify(resp)

        user.delete()

        return jsonify({"success": True})


class Articles(Resource):

    @swagger.doc({
        'tags': ['articles'],
        'description': 'Returns a list of articles',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'Articles',
            }
        },
      
    })
    def get(self):
        """Returns list of articles"""
        articles = Article.query.all()

        articles = [dict(article) for article in articles]

        return jsonify({"articles": articles})
    
    @swagger.doc({
        'tags': ['articles'],
        'description': 'Creates a new article',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'Articles',
            }
        },
      
    })
    @auth.login_required
    def post(self):
        """Creates a new article"""        
        data = request.get_json()

        username = data["username"]
        user = User.query.filter_by(username=username).first()
        article = Article(data["name"], data["text"], user)
        article.save()

        return jsonify({"success": True})


class ArticleResource(Resource):
    
    @swagger.doc({
        'tags': ['articles'],
        'description': 'Gets the article with id',
        'produces':[
            'application/json'
        ],
        'parameters':[{
            'name': 'article_id',
            'in': 'path',
            'type': 'integer',
        }],
        'responses': {
            '200': {
                'description': 'Articles',
            }
        },
      
    })
    def get(self, article_id):
        """Gets the article with article_id"""
        article = Article.query.get(article_id)

        return jsonify({"article": dict(article)})
    
    @swagger.doc({
        'tags': ['articles'],
        'description': 'Updates the article with id',
        'produces':[
            'application/json'
        ],
        'parameters':[{
            'name': 'article_id',
            'in': 'path',
            'type': 'integer',
        }],
        'responses': {
            '200': {
                'description': 'Articles',
            }
        },
      
    })
    @auth.login_required
    def put(self, article_id):
        """Updated article with article_id"""
        data = request.get_json()
        
        article = Article.query.get(article_id)
        
        user = User.query.get(article.user_id)
        resp = check_user(user, data.get('username'))
        if resp != True:
            return jsonify(resp)

        article.name = data["name"]
        article.text = data["text"]
        article.save()
        
        return jsonify({"article": dict(article)})
    
    @swagger.doc({
        'tags': ['articles'],
        'description': 'Delets the article with id',
        'produces':[
            'application/json'
        ],
        'parameters':[{
            'name': 'article_id',
            'in': 'path',
            'type': 'integer',
        }],
        'responses': {
            '200': {
                'description': 'Articles',
            }
        },
      
    })
    @auth.login_required
    def delete(self, article_id):
        """Delets the article with article_id"""
        data = request.get_json()

        article = Article.query.get(article_id)

        user = User.query.get(article.user_id)
        resp = check_user(user, data.get('username'))
        if resp != True:
            return jsonify(resp)
            
        article.delete()

        return jsonify({"success": True})


class UserArticles(Resource):

    @swagger.doc({
        'tags': ['user articles'],
        'description': 'Get the articles of a user with user_id',
        'produces':[
            'application/json'
        ],
        'parameters':[{
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
        }],
        'responses': {
            '200': {
                'description': 'User Articles',
            }
        },
      
    })
    def get(self, user_id):
        """Articles belonging to user with user_id"""
        articles = Article.query.filter_by(user_id=user_id).all()

        articles = [dict(article) for article in articles]

        return jsonify({"articles": articles})