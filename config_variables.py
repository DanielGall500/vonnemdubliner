import os
import re

"""
Heroku config variables are used to set up the database uri and secret key.
However, when debugging these need to be set in the environment varaibles on the system.
"""

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY", "development_key")
SQlALCHEMY_TRACK_MODIFICATIONS = False
