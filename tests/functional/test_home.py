def test_home_page_get(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Vonnemdubliner" in response.data

def test_home_page_post(test_client):
    response = test_client.post('/')
    assert response.status_code == 405
