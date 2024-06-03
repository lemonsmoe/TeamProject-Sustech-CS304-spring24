def test_get_students(client):
    response = client.get('/general/students')
    data = response.get_json()
    assert response.status_code == 200
    
def test_register(client):
    json_data = {
        "student_id": "test",
        "password": "test"
    }
    response = client.post('/general/register', json=json_data)
    data = response.get_json()
    assert response.status_code == 202
    
def test_login(client):
    json_data = {
        "student_id": "test",
        "password": "test"
    }
    response = client.post('/general/login', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_current_student(client):
    # 先登录
    json_data = {
        "student_id": "test",
        "password": "test"
    }
    response = client.post('/general/login', json=json_data)
    
    response = client.get('/general/current_student')
    data = response.get_json()
    assert response.status_code == 200
    
def test_logout(client):
    response = client.get('/general/logout')
    data = response.get_json()
    assert response.status_code == 200
    
