# all code are written with the help of Copilot. 
def test_get_calender(client):
    response = client.get('/calender/')
    data = response.get_json()
    assert response.status_code == 200
    
def test_get_allevents(client):
    response = client.get('/calender/getallevent')
    data = response.get_json()
    assert response.status_code == 200
    
def test_get_byday(client):
    json_data =     {
        "ddl_time": "2021-06-01"
    }
    response = client.post('/calender/get_byday', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_student_ddl_get(client):
    response = client.get('/calender/student_ddl/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_course_ddl_get(client):
    response = client.get('/calender/course_ddl/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_course_get(client):
    json_data =     {'course_id': 'cs', 'course_name': '', 'course_teacher': ''}
    response = client.post('/calender/course/get', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_student_ddl_add(client):
    json_data =         {
        "ddl_time": "2021-06-01 00:00:00",
        "ddl_title": "实验报告",
        "ddl_content": "完成实验报告"
    }
    response = client.post('/calender/student_ddl/add', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_course_ddl_add(client):
    json_data =       {
        "ddl_time": "2021-06-01 00:00:00",
        "ddl_title": "实验报告",
        "ddl_content": "完成实验报告",
        "course_id": "CS101"
    }
    response = client.post('/calender/course_ddl/add', json=json_data)
    data = response.get_json()
    assert response.status_code != 100
    
def test_student_ddl_delete(client):
    json_data =     {
        "ddl_id": 10000000
    }
    response = client.post('/calender/student_ddl/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_course_ddl_delete(client):
    json_data =     {
        "ddl_id": 10000000
    }
    response = client.post('/calender/course_ddl/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_subscribe_get(client):
    response = client.get('/calender/subscribe/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_subscribe_put(client):
    json_data =        {
        "course_id": "CS301"
    }
    response = client.post('/calender/subscribe/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_subscribe_delete(client):
    json_data =     {
        "course_id": "CS301"
    }
    response = client.post('/calender/subscribe/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200