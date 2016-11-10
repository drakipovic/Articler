import json
from datetime import datetime

from flask import jsonify, request, session
from flask_restful import Resource
from flask_jwt import jwt_required

from models import User, Article
from main import auth


def check_user(user):
    if user.username != session['logged_in'].split(':')[0]:
        return {"error": "You don't have this kind of permission"}

    return True


class UserResource(Resource):
    
    def get(self, user_id):
        user = User.query.get(user_id)

        return jsonify(dict(user))
        

class Users(Resource):
    
    def get(self):
        users = User.query.all()
        
        users = [dict(user) for user in users]

        return jsonify({'users': users})
    
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        user = User(username, password)
        user.save()

        return jsonify({"success": True, "user": dict(user)})
    
    @auth.login_required
    def put(self):
        data = request.get_json()
        
        user = User.query.get(data["user_id"])
        resp = check_user(user)
        if resp != True:
            return jsonify(resp)
        
        user.username = data["username"]
        user.save()

        return jsonify({"success": True})
    
    @auth.login_required
    def delete(self):
        username = request.json.get('username')

        user = User.query.filter_by(username=username).first()
        resp = check_user(user)
        if resp != True:
            return jsonify(resp)

        user.delete()

        return jsonify({"success": True})


class Articles(Resource):

    def get(self):
        articles = Article.query.all()

        articles = [dict(article) for article in articles]

        return jsonify({"articles": articles})

    @auth.login_required
    def post(self):
        data = request.get_json()
        
        user = User.query.get(data["user_id"]) 
        article = Article(data["name"], data["text"], user)
        article.save()

        return jsonify({"success": True})


class ArticleResource(Resource):
    
    def get(self, article_id):
        article = Article.query.get(article_id)

        return jsonify({"article": dict(article)})

    @auth.login_required
    def put(self, article_id):
        data = request.get_json()
        
        article = Article.query.get(article_id)
        
        user = User.query.get(article.user_id)
        resp = check_user(user)
        if resp != True:
            return jsonify(resp)

        article.name = data["name"]
        article.text = data["text"]
        article.save()
        
        return jsonify({"article": dict(article)})
    
    @auth.login_required
    def delete(self, article_id):
        article = Article.query.get(article_id)

        user = User.query.get(article.user_id)
        resp = check_user(user)
        if resp != True:
            return jsonify(resp)
            
        article.delete()

        return jsonify({"success": True})


class UserArticles(Resource):

    def get(self, user_id):
        articles = Article.query.filter_by(user_id=user_id).all()

        articles = [dict(article) for article in articles]

        return jsonify({"articles": articles})
