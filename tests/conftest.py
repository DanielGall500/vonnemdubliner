from vonnemdubliner.models import Blogpost
from datetime import datetime
from app import create_app
import pytest

@pytest.fixture()
def new_post():
    curr_time = datetime.now()
    post = Blogpost(title="test-title", subtitle="test-subtitle", \
    slug="test-slug", author="test-author", \
    content="test-content", date_posted=curr_time)
    return post

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
    "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
