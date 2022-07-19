import os
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "development_key")
SQlALCHEMY_TRACK_MODIFICATIONS = False
