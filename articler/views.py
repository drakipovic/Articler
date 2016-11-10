from flask import jsonify, request, render_template, session, redirect, url_for, g

from main import app
from models import User


@app.route('/api/current_user')
def get_current_user():
    username_and_password = session.get('logged_in', None)
    if username_and_password:
        username = username_and_password.split(':')[0]
        password = username_and_password.split(':')[1]
        user = User.query.filter_by(username = username).first()
        user_dict = dict(user)
        user_dict["password"] = password
        return jsonify(user_dict)
    
    return jsonify({"error": "no user"})


@app.route('/user/<int:user_id>/articles')
def user_articles(user_id=None):
    path = "/user/" + str(user_id) + "/articles"
    browser = request.user_agent.browser
    app.logger.info(path + "   " + browser)
    return render_template('user_articles.html')


@app.route('/users')
def get_users():
    path = "/users/"
    browser = request.user_agent.browser
    app.logger.info(path + "   " + browser)
    return render_template('users.html')


@app.route('/article/<int:article_id>')
def get_article(article_id=None):
    path = "/article/" + str(article_id)
    browser = request.user_agent.browser
    app.logger.info(path + "   " + browser)
    return render_template('article.html')
    

@app.route('/')
@app.route('/articles')
def get_articles():
    path = "/articles"
    browser = request.user_agent.browser
    app.logger.info(path + "   " + browser)
    return render_template('articles.html')


@app.route('/api/login', methods=['POST'])
def do_login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['logged_in'] = username + ':' + password
        return jsonify({"success": True, "username": username})
    
    else:
        return jsonify({"error": "Bad credentials"})

    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)

    return redirect(url_for('get_articles'))