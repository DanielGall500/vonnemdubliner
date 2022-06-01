from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import MetaData

app = Flask(__name__)

#Configuration settings including secret key
#Not committed to the repo
app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

migrate = Migrate(app, db, render_as_batch=True)
CORS(app)

#Handle the login functionality
login_manager = LoginManager()
login_manager.login_view = "auth.admin"
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_first_request
def create_tables():
    db.create_all()
