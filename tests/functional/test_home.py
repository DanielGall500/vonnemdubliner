def test_home_page_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Vonnemdubliner" in response.data

def test_home_page_post(client):
    response = client.post('/')
    assert response.status_code == 405
