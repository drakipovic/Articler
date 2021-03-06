from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from main import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(1000))

    articles = db.relationship('Article', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password_hash = self._set_password(password)

    def __iter__(self):
        yield 'id', str(self.id)
        yield 'username', self.username

    def _set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    __tablename__ = 'articles'

    article_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime())
    text = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, text, user):
        self.timestamp = datetime.utcnow()
        self.text = text
        self.user_id = user.id
        self.name = name

    def __iter__(self):
        yield 'id', self.article_id
        yield 'name', self.name
        yield 'text', self.text
        yield 'user_id', self.user_id
        yield 'date', datetime.strftime(self.timestamp, "%m/%d/%Y")
        yield 'username', User.query.get(self.user_id).username
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()