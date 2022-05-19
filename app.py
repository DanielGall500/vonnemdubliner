from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

#Configuration settings including secret key
#Not committed to the repo
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

migrate = Migrate(app, db, render_as_batch=True)
CORS(app)

import resources
