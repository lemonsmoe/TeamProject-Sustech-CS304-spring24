def test_review_getbrief(client):
    response = client.get('evaluation/review/getbrief')
    data = response.get_json()
    assert response.status_code == 200
    
def test_review_getall(client):
    response = client.get('evaluation/review/getall/CS307')
    data = response.get_json()
    assert response.status_code == 200
    
def test_review_stats(client):
    response = client.get('evaluation/review/stats/CS307')
    data = response.get_json()
    assert response.status_code == 200
    
def test_course(client):
    response = client.get('evaluation/course/CS307')
    data = response.get_json()
    assert response.status_code == 200
    
    response = client.get('evaluation/course/CS000')
    data = response.get_json()
    
def test_courses_brief(client):
    response = client.get('evaluation/courses/brief')
    data = response.get_json()
    assert response.status_code == 200
    
def test_review_put(client):
    json_data =     {
        "course_id": "CS307",
        "rating": 3,
        "difficulty": "简单",
        "homework": "少",
        "grading": "低",
        "harvest": "多",
        "comment": "这门课很好"
    }
    response = client.post('evaluation/review/put', json=json_data)
    data = response.get_json()
    assert response.status_code == 200