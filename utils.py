from app import db
from resources import User
from werkzeug.security import generate_password_hash

def create_user(username,password,is_admin):
    pwhash = generate_password_hash(password)
    new_user = User(username=username,password=pwhash,admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
