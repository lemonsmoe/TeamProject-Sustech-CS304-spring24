from flask import jsonify, request, session, Blueprint
from datetime import datetime
from models_wholeProject import db, Student, fk_command
from sqlalchemy import inspect

app_general = Blueprint('app_general', __name__, url_prefix='/general')

@app_general.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    data = [dict((c, getattr(student, c)) for c in inspect(student).mapper.column_attrs.keys()) for student in students]
    return jsonify(data)

@app_general.route('/register', methods=['POST'])
def register_student():
    """
        {
            "student_id": "12111728",
            "password": "123456"
        }
    """
    req_data = request.get_json()
    student = Student(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(student)
        db.session.commit()
        return jsonify(msg="注册成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="注册失败", error=str(e)), 202

@app_general.route('/login', methods=['POST'])
def login_student():
    # print(request.cookies)
    # print(request.headers)
    print(session)
    req_data = request.get_json()
    student_id = req_data.get("student_id")
    password = req_data.get("password")
    if not student_id or not password:
        return jsonify(msg="登录信息不完整"), 202
    student = Student.query.get(student_id)
    if student is None:
        return jsonify(msg="该账号不存在，请注册"), 202
    elif password != student.password:
        return jsonify(msg="密码错误"), 202
    session["student_id"] = student_id
    student.last_login_time = datetime.now()
    db.session.commit()
    response = jsonify({"msg": "登录成功"}), 200
    return response

@app_general.route('/logout', methods=['GET'])
def logout_student():
    session.pop("student_id", None)
    return jsonify(msg="登出成功"), 200

@app_general.route('/current_student', methods=['GET'])
def get_current_student():
    student_id = session.get("student_id")
    if student_id is None:
        return jsonify(msg="未登录",student_id="丢雷楼某赶紧去登录"), 202
    else:
        return jsonify(student_id=student_id), 200
    student = Student.query.get(student_id)
    data = [dict((c, getattr(student, c)) for c in inspect(student).mapper.column_attrs.keys())]
    return jsonify(data), 200

@app_general.route('/update_student', methods=['POST'])
def update_student():
    req_data = request.get_json()
    student_id = req_data.get("student_id")
    student = Student.query.get(student_id)
    if student is None:
        return jsonify(msg="学生不存在"), 202
    for key, value in req_data.items():
        setattr(student, key, value)
    try:
        db.session.commit()
        return jsonify(msg="更新成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="更新失败", error=str(e)), 202

@app_general.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify(msg="学生不存在"), 202
    data = [dict((c, getattr(student, c)) for c in inspect(student).mapper.column_attrs.keys())]
    return jsonify(data)
