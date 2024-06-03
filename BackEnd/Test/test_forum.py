# all code are written with the help of Copilot. 
def test_post_get(client):
    response = client.get('/forum/post/get')
    data = response.get_json()
    assert response.status_code == 200
    
def test_post_getcontent(client):
    json_data = {
        "post_id": 1
    }
    response = client.post('/forum/post/getcontent', json=json_data)
    data = response.get_json()
    assert response.status_code == 200



def test_post_put(client):
    json_data = {
        "title": "test",
        "content": "test",
        "topic": "课程",
        "board": "学术",
    }
    response = client.post('/forum/post/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
    
def test_post_delete(client):
    json_data = {
        "post_id": 1000
    }
    response = client.post('/forum/post/delete', json=json_data)
    data = response.get_json()
    assert response.status_code != 200


 

def test_post_addview(client):
    json_data = {
        "post_id": 1
    }
    response = client.post('/forum/post/addview', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_reply_get(client):
    json_data = {
        "post_id": 1
    }
    response = client.post('/forum/reply/get', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_reply_put(client):
    response = client.get('/forum/post/get')
    data = response.get_json()
    last_post_id = data[-1]['post_id']
    
    json_data = {
        "post_id": last_post_id,
        "content": "test",
    }
    response = client.post('/forum/reply/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_reply_delete(client):
    json_data = {
        "reply_id": 1000
    }
    response = client.post('/forum/reply/delete', json=json_data)
    data = response.get_json()
    assert response.status_code != 200
    
def test_reply_delete_success(client):
    response = client.get('/forum/post/get')
    data = response.get_json()
    last_post_id = data[-1]['post_id']
    json_data = {
        "post_id": last_post_id
    }
    response = client.post('/forum/reply/get', json=json_data)
    data = response.get_json()
    last_reply_id = data[-1]['reply_id']
    
    json_data = {
        "reply_id": last_reply_id
    }
    response = client.post('/forum/reply/delete', json=json_data)
    data = response.get_json()
    assert response.status_code == 200
    
def test_post_delete_success(client):
    response = client.get('/forum/post/get')
    data = response.get_json()
    last_post_id = data[-1]['post_id']
    
    json_data = {
        "post_id": last_post_id
    }
    # print('fuuuuuuuuuuuuuuuuuuuufffffffffff')
    response = client.post('/forum/post/delete', json=json_data)
    data = response.get_json()
    # print(data)
    assert response.status_code == 200
    