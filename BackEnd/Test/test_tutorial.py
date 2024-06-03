def test_tutors_get(client):
    response = client.get('tutorial/tutors/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_tutors_add(client):
    # 使用管理员登录
    json_data = {
        "student_id": "admin",
        "password": "admin"
    }
    response = client.post('general/login', json=json_data)
    assert response.status_code == 200
    
    json_data =     {
        "name": "彭子燊小猫咪",
        "subject": "数学",
        "gender": "男",
        "age": 30,
        "email": "OpenzS@mail.sustech.edu.cn"
    }
    response = client.post('tutorial/tutors/add', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
    # 重复添加
    response = client.post('tutorial/tutors/add', json=json_data)
    data = response.get_json()
    assert response.status_code != 200

def test_tutors_delete(client):
    response = client.get('tutorial/tutors/get')
    data = response.get_json()
    last_tutor_id = data[-1]['tutor_id']
    
    json_data = {
        "tutor_id": last_tutor_id
    }
    response = client.post('tutorial/tutors/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
    # 重复删除
    response = client.post('tutorial/tutors/delete', json=json_data)
    data = response.get_json()
    assert response.status_code != 200
    
def test_appointments(client):
    response = client.get('tutorial/appointments')
    data = response.get_json()
    assert response.status_code == 200
    
def test_appointments_get(client):
    json_data = {
        "tutor_name": "1",
        "appointment_date": "2021-06-01"
    }
    response = client.post('tutorial/appointments/get', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_appointments_add(client):
    json_data = {
        "tutor_id": "1",
        "appointment_date": "2021/06/01",
        "appointment_time": "10:00 - 11:00",
        "help_needed": "数学作业",
    }
    response = client.post('tutorial/appointments/add', json=json_data)
    data = response.get_json()
    # assert response.status_code == 200
    
def test_appointments_addworkshop(client):
    json_data = {
        "workshop_id": "1",
    }
    response = client.post('tutorial/appointments/addworkshop', json=json_data)
    data = response.get_json()
    # assert response.status_code == 200
    
def test_appointments_delete(client):
    response = client.get('tutorial/appointments')
    data = response.get_json()
    last_appointment_id = data[-1]['appointment_id']
    
    json_data = {
        "appointment_id": last_appointment_id
    }
    response = client.post('tutorial/appointments/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
    # 重复删除
    response = client.post('tutorial/appointments/delete', json=json_data)
    data = response.get_json()
    assert response.status_code != 200
    
def test_workshops_get(client):
    response = client.get('tutorial/workshops/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_workshops_add(client):
    json_data = {
        "subject": "数学",
        "date": "2021/06/01",
        "time": "10:00 - 11:00",
        "location": "教室1",
        "tutor_id": "1",
        "content": "数学作业"
    }
    response = client.post('tutorial/workshops/add', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_workshops_delete(client):
    response = client.get('tutorial/workshops/get')
    data = response.get_json()
    last_workshop_id = data[-1]['workshop_id']
    
    json_data = {
        "workshop_id": last_workshop_id
    }
    response = client.post('tutorial/workshops/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
    # 重复删除
    response = client.post('tutorial/workshops/delete', json=json_data)
    data = response.get_json()
    assert response.status_code != 200