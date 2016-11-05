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


@app.route('/users')
def get_users():
    return session['logged_in']


@app.route('/')
@app.route('/articles')
def articles():
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