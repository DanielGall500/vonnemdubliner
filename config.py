import os
import re

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY", "development_key")
SQlALCHEMY_TRACK_MODIFICATIONS = False
