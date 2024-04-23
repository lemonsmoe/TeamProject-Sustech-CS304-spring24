from flask import jsonify, request, session
from datetime import datetime
from assistant_models import app, db, Student

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    data = []
    for student in students:
        data.append({
            "student_id": student.student_id,
            "password": student.password,
            "last_login_time": student.last_login_time
        })
    return jsonify(data)

@app.route('/general/register', methods=['POST'])
def register_student():
    req_data = request.get_json()
    student_id = req_data.get("student_id")
    password = req_data.get("password")
    if not all([student_id, password]):
        return jsonify(code=400, msg="参数不完整")
    student = Student(student_id=student_id, password=password)
    try:
        db.session.add(student)
        db.session.commit()
        return jsonify(code=200, msg="注册成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="注册失败")
    
@app.route('/general/login', methods=['POST'])
def login_student():
    req_data = request.get_json()
    student_id = req_data.get("student_id")
    password = req_data.get("password")
    if not all([student_id, password]):
        return jsonify(code=400, msg="参数不完整")
    student = Student.query.get(student_id)
    if student is None or password != student.password:
        return jsonify(code=400, msg="账号或密码错误")
    session["student_id"] = student_id
    student.last_login_time = datetime.now()
    db.session.commit()
    return jsonify(code=200, msg="登录成功")

@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify(code=400, msg="学生不存在")
    data = {
        "student_id": student.student_id,
        "password": student.password,
        "last_login_time": student.last_login_time
    }
    return jsonify(data)
