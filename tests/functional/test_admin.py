from flask import session

def test_access_session_auth(test_client):
    """
    GIVEN a valid username and password
    WHEN logging in to admin account
    THEN ensure the log in is successful
    """
    test_client.post("/auth/admin", data={
    "username": "admin",
    "password": "test",
    })
    assert int(session["_user_id"]) == 1

def test_access_session_unauth(test_client):
    """
    GIVEN an invalid username and password
    WHEN logging in to admin account
    THEN ensure the log in is NOT successful
    """
    response = test_client.post("/auth/admin", data={
    "username": "invalid",
    "password": "invalid",
    })
    assert b"Could not verify" in response.data
