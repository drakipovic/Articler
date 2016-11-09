from flask import jsonify, request, render_template, session, redirect, url_for, g

from main import app
from models import User


@app.route('/api/current_user')
def get_current_user():
    username = session.get('logged_in', None)
    if username:
        user = User.query.filter_by(username = username).first()
        return jsonify(dict(user))
    
    return jsonify({"error": "no user"})


@app.route('/user/<int:user_id>/articles')
def user_articles(user_id=None):
    return render_template('user_articles.html')


@app.route('/users')
def get_users():
    return render_template('users.html')


@app.route('/article/<int:article_id>')
def get_article(article_id=None):
    return render_template('article.html')
    

@app.route('/')
@app.route('/articles')
def get_articles():
    return render_template('articles.html')


@app.route('/api/login', methods=['POST'])
def do_login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['logged_in'] = username
        return jsonify({"success": True, "username": username})
    
    else:
        return jsonify({"error": "Bad credentials"})

    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('get_articles'))