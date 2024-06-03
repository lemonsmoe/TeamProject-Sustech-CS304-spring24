def test_hello_world(client):
    response = client.get('/hello')
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Hello, World!'
    