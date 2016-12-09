import os
import base64

import json
import pytest
from flask import session
from flask_sqlalchemy import SQLAlchemy


os.environ['TEST'] = '1'
from articler.main import app, api, db
from articler.models import User, Article
from articler.api import Users, Articles, UserArticles, ArticleResource


api.add_resource(Users, '/api/users')
api.add_resource(Articles, '/api/articles')
api.add_resource(UserArticles, '/api/user/<int:user_id>/articles')
api.add_resource(ArticleResource, '/api/article/<int:article_id>')

if not os.path.exists('articler/test.db'):
    db.create_all()
else:
    db.drop_all()
    db.create_all()

app = app.test_client()

headers = {'Content-Type': 'application/json'}


def request(method, url, auth=None, **kwargs):
    headers = kwargs.get('headers', {})
    if auth:
        headers['Authorization'] = 'Basic ' + base64.b64encode(auth[0] + ':' + auth[1])

    kwargs['headers'] = headers

    return app.open(url, method=method, **kwargs)


def register_user(username, password):
    return request('POST', '/api/users', data=json.dumps({'username': username, 'password': password}), headers=headers)


def test_users_api_get_req_returns_all_users():
    user_1 = User('user_1', 'pass_1')
    user_1.save()

    response = request('GET', 'api/users')

    assert 'user_1' in response.data
    user_1.delete()


def test_users_api_post_req_returns_success():
    response = register_user('test_1', 'pass_1')

    assert 'success' in response.data
    assert 'test_1' in response.data

    user = User.query.filter_by(username='test_1').first()
    assert user != None

    user.delete()


def test_users_api_put_req_with_logged_user_updates_user():
    response = register_user('test_1', 'pass_1')

    response = request('PUT', '/api/users', data=json.dumps({'user_id': 1, 'username': 'updated', 'username_test': 'test_1'}), auth=['test_1', 'pass_1'], headers=headers)

    assert 'success' in response.data
    
    user = User.query.filter_by(username='updated').first()
    assert user != None

    user.delete()


def test_users_api_put_req_with_anonymous_user_fails():
    response = request('PUT', '/api/users', data=json.dumps({'user_id': 1, 'username': 'updated', 'username_test': 'test'}), auth=['test_1', 'pass_1'], headers=headers)

    assert 'Unauthorized Access' in response.data


def test_users_api_delete_req_with_logged_user_deletes_user():
    response = register_user('test_1', 'pass_1')

    response = request('DELETE', '/api/users', data=json.dumps({'username': 'test_1'}), auth=['test_1', 'pass_1'], headers=headers)

    assert 'success' in response.data

    user = User.query.filter_by(username='test_1').first()
    assert user == None


def test_users_api_delete_req_with_anonymous_user_fails():
    response = request('DELETE', '/api/users', data=json.dumps({'username': 'test_1'}), auth=['test_1', 'pass_1'], headers=headers)

    assert 'Unauthorized Access' in response.data


def test_articles_api_get_req_returns_all_articles():
    user = User('test', 'pass')
    user.save()
    
    article = Article('lorem', 'lorem ipsum', user)
    article.save()

    response = request('GET', '/api/articles')

    assert 'lorem ipsum' in response.data
    article.delete()
    user.delete()


def test_articles_api_post_req_returns_success():
    response = register_user('test_1', 'pass_1')
    
    response = request('POST', '/api/articles', data=json.dumps({'username': 'test_1', 'name': 'name_1', 'text': 'text_1'}), auth=['test_1', 'pass_1'], headers=headers)

    assert 'success' in response.data

    article = Article.query.filter_by(name='name_1').first()
    assert article.name == 'name_1'

    article.delete()

    user = User.query.filter_by(username='test_1').first()
    user.delete()    


def test_article_api_get_request_returns_article():
    user = User('test', 'pass')
    user.save()
    
    article = Article('lorem', 'lorem ipsum', user)
    article.save()

    response = request('GET', '/api/article/1')
    assert 'lorem ipsum' in response.data

    article.delete()
    user.delete()


def test_article_api_put_request_with_logged_user_updates_article():
    user = User('test', 'pass')
    user.save()
    
    article = Article('lorem', 'lorem ipsum', user)
    article.save()

    response = request('PUT', '/api/article/1', data=json.dumps({'username': 'test', 'name': 'loremm', 'text': 'lorem ipsum'}), auth=['test', 'pass'], headers=headers)

    assert 'loremm' in response.data

    user.delete()
    article.delete()


def test_article_api_put_req_with_anonymous_user_fails_to_update():
    response = request('PUT', '/api/article/1', data=json.dumps({'name': 'loremm'}), auth=['testtt', 'passs'], headers=headers)

    assert 'Unauthorized Access' in response.data


def test_article_api_delete_req_with_logged_user_deletes_article():
    user = User('test', 'pass')
    user.save()
    
    article = Article('lorem', 'lorem ipsum', user)
    article.save()

    response = request('DELETE', '/api/article/1', data=json.dumps({'username': 'test'}), auth=['test', 'pass'], headers=headers)

    assert 'success' in response.data

    user.delete()
    article.delete()


def test_user_articles_get_request_returns_articles_from_given_user():
    user_1 = User('test', 'pass')
    user_1.save()
    
    user_2 = User('user', 'pass')
    user_2.save()

    article_1 = Article('lorem', 'lorem ipsum', user_1)
    article_1.save()

    article_2 = Article('loremm', 'loremm ipsumm', user_2)
    article_2.save()

    response = request('GET', '/api/user/1/articles')

    assert 'lorem ipsum' in response.data
    assert 'loremm ipsumm' not in response.data

    user_1.delete()
    user_2.delete()
    article_1.delete()
    article_2.delete()