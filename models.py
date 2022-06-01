from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    subtitle = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, index=True)
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Post {}>'.format(self.title)
