from sqlalchemy.orm import backref
from flask import request, jsonify, make_response
from functools import wraps
import jwt
from app import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.Integer)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

#Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        #Pass JWT token in the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({"Message":"A valid token is missing."}), 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify({"Message": "Invalid Token"}), 401)
        return f(current_user, *args, **kwargs)
    return decorator
