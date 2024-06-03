def test_submit_data(client):
    json_data = {'password': 'my father is YHT', 'student_name': '', 'keywords': ['系统', '组成'], 'badwords': [''], 'excluded_time': {'点': []}}
    response = client.post('courserc/submit_data', json=json_data)
    data = response.get_json()
    assert response.status_code == 200

def test_submit_data_2(client):
    json_data = {'password': 'my father is YHT', 'student_name': '', 'keywords': ['系统', '组成', '多媒体'], 'badwords': [''], 'excluded_time': {'点': [[1, 1], [2, 1], [3, 1]]}}
    response = client.post('courserc/submit_data', json=json_data)
    data = response.get_json()
    assert response.status_code == 200

def test_star_get(client):
    response = client.get('courserc/star/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_star_put(client):
    json_data = {'schedule': [{'上课时间': [[2, 3, 4, True, True]], '学分': '2.0', '教学班': '医学影像系统实验-01班-双语'}, {'上课时间': [[1, 2, 2, True, True], [1, 3, 3, True, True]], '学分': '3.0', '教学班': '计算机组成原理-01班-英文-4组'}]}
    response = client.post('courserc/star/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_star_put_2(client):
    json_data = {'schedule': [{'上课时间': [[2, 3, 4, True, True]], '学分': '2.0', '教学班': '医学影像系统实验-01班-双语'}, {'上课时间': [[1, 2, 2, True, True], [1, 3, 3, True, True]], '学分': '3.0', '教学班': '计算机组成原理-01班-英文-4组'}]}
    response = client.post('courserc/star/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 202
    
def test_star_delete_1(client):
    json_data = {'schedule': {'上课时间': [[2, 3, 4, True, True]], '学分': '2.0', '教学班': '医学影像系统实验-01班-双语'}}
    response = client.post('courserc/star/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    assert data['msg'] == '删除成功'
    
def test_star_delete_2(client):
    json_data = {'schedule': [{'上课时间': [[2, 3, 4, True, True]], '学分': '2.0', '教学班': '医学影像系统实验-01班-双语'}, {'上课时间': [[1, 2, 2, True, True], [1, 3, 3, True, True]], '学分': '3.0', '教学班': '计算机组成原理-01班-英文-4组'}]}
    response = client.post('courserc/star/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
