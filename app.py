from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():
    #Config settings include secret key
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from models import db

    migrate = Migrate(app, db, render_as_batch=True)
    db.init_app(app)

    CORS(app)

    from views.auth import auth
    from views.base import base
    app.register_blueprint(auth)
    app.register_blueprint(base)

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

    return app
