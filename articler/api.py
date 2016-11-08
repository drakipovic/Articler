import json

from flask import jsonify, request
from flask_restful import Resource
from flask_jwt import jwt_required

from models import User, Article


class Users(Resource):
    #decorators = [jwt_required()]

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

    def delete(self):
        username = request.json.get('username')

        user = User.query.filter_by(username=username).first()
        user.delete()

        return jsonify({"success": True})


class Articles(Resource):

    def get(self):
        articles = Article.query.all()

        articles = [dict(article) for article in articles]

        return jsonify({"articles": articles})
    
    def post(self):
        data = request.get_json()
        
        user = User.query.get(data["user_id"]) 
        article = Article(data["name"], data["text"], user)
        article.save()

        return jsonify({"success": True})


    def put(self):
        pass

    def delete(self):
        pass


class ArticleResource(Resource):
    pass


class UserArticle(Resource):
    pass


class UserArticles(Resource):
    pass
