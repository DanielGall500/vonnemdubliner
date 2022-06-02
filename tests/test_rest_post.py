import pytest
from app import create_app
from flask import session

@pytest.fixture()
def app():
    app = create_app()
    app.config_update({
    "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_access_session(client):
    with client:
        client.post("/auth/admin", data={
        "username": "admin",
        "password": "test",
        })
        print(session)
        assert session["user.id"] == 1
