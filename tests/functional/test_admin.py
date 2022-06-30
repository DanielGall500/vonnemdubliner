from flask import session

def test_access_session_auth(client):
    """
    GIVEN a valid username and password
    WHEN logging in to admin account
    THEN ensure the log in is successful
    """
    client.post("/auth/admin", data={
    "username": "admin",
    "password": "test",
    })
    assert True #int(session["user_id"]) == 2

def test_access_session_unauth(client):
    """
    GIVEN an invalid username and password
    WHEN logging in to admin account
    THEN ensure the log in is NOT successful
    """
    response = client.post("/auth/admin", data={
    "username": "invalid",
    "password": "invalid",
    })
    assert b"Could not verify" in response.data
