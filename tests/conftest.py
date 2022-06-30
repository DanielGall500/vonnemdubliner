from vonnemdubliner.models import Blogpost
from sqlalchemy import create_engine, MetaData
from vonnemdubliner.models import db
from datetime import datetime
from app import create_app
import logging
import pytest
import os

@pytest.fixture()
def new_post():
    curr_time = datetime.now()
    post = Blogpost(
        title="test-title", subtitle="test-subtitle", \
        slug="test-slug", author="test-author", \
        content="test-content", date_posted=curr_time
    )
    return post

def setup_test_config(_app):
    _app.config.update({
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite://"
    })
    _app.testing = True

@pytest.fixture()
def app():
    _app = create_app()
    _app.logger.setLevel(logging.CRITICAL)

    setup_test_config(_app)

    ctx = _app.test_request_context()
    ctx.push()
    db.create_all()
    yield _app
    ctx.pop()

@pytest.fixture()
def client(app):
    yield app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
