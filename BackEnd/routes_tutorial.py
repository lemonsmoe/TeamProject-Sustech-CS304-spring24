from flask import jsonify, request, session
from datetime import datetime
from models_wholeProject import app, db, Tutor, Appointment, Workshop,fk_command
from sqlalchemy import inspect

@app.route('/tutorial/tutors', methods=['GET'])
def get_tutors():
    tutors = Tutor.query.all()
    data = [dict((c, getattr(tutor, c)) for c in inspect(tutor).mapper.column_attrs.keys()) for tutor in tutors]
    return jsonify(data)

@app.route('/tutorial/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    data = [dict((c, getattr(appointment, c)) for c in inspect(appointment).mapper.column_attrs.keys()) for appointment in appointments]
    return jsonify(data)

@app.route('/tutorial/appointments/<student_id>', methods=['GET'])
def get_student_appointments(student_id):
    appointments = Appointment.query.filter_by(student_id=student_id).all()
    data = [dict((c, getattr(appointment, c)) for c in inspect(appointment).mapper.column_attrs.keys()) for appointment in appointments]
    return jsonify(data)

@app.route('/tutorial/workshops', methods=['GET'])
def get_workshops():
    workshops = Workshop.query.all()
    data = [dict((c, getattr(workshop, c)) for c in inspect(workshop).mapper.column_attrs.keys()) for workshop in workshops]
    return jsonify(data)

@app.route('/tutorial/appointments/add', methods=['POST'])
def add_appointment():
    """
    ex:
    {
        "student_id": "12111728",
        "tutor_id": "1001",
        "appointment_time": "2021-06-01 00:00:00",
        "help_needed": "需要帮助"
    }
    """
    req_data = request.get_json()
    req_data["appointment_time"] = datetime.strptime(req_data["appointment_time"], "%Y-%m-%d %H:%M:%S")
    appointment = Appointment(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(appointment)
        db.session.commit()
        return jsonify(code=200, msg="添加成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加失败", error=str(e))

@app.route('/tutorial/tutors/add', methods=['POST'])
def add_tutor():
    """
    ex:
    {
        "tutor_id": "1001",
        "name": "张三",
        "subject": "数学",
        "gender": "男",
        "age": 30,
        "email": "12110316@mail.sustech.edu.cn"
    }
    """
    req_data = request.get_json()
    tutor = Tutor(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(tutor)
        db.session.commit()
        return jsonify(code=200, msg="添加成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加失败", error=str(e))

@app.route('/tutorial/workshops/add', methods=['POST'])
def add_workshop():
    """
    ex:
    {
        "time": "2021-06-01 00:00:00",
        "location": "A101",
        "subject": "数学",
        "tutor_id": "1001"
    }
    """
    req_data = request.get_json()
    req_data["time"] = datetime.strptime(req_data["time"], "%Y-%m-%d %H:%M:%S")
    workshop = Workshop(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(workshop)
        db.session.commit()
        return jsonify(code=200, msg="添加成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加失败", error=str(e))












# @app.route('/calender/<student_id>', methods=['GET'])
# def get_student_calender(student_id):
#     ddls = DDL.query.filter_by(student_id=student_id).all()
#     data = []
#     for ddl in ddls:
#         data.append({
#             "ddl_id": ddl.ddl_id,
#             "ddl_time": ddl.ddl_time,
#             "ddl_content": ddl.ddl_content,
#             "ddl_status": ddl.ddl_status or "未完成"
#         })
#     return jsonify(data)

# @app.route('/calender/add', methods=['POST'])
# def add_ddl():
#     """
#     ex:
#     {
#         "student_id": "12111728",
#         "ddl_time": "2021-06-01 00:00:00",
#         "ddl_content": "完成实验报告"
#     }
#     """
#     req_data = request.get_json()
#     student_id = req_data.get("student_id")
#     course_id = req_data.get("course_id", None)
#     ddl_time = req_data.get("ddl_time", None)
#     ddl_content = req_data.get("ddl_content")
#     # student_id 和 course_id 只需要一个即可
#     if student_id is None and course_id is None:
#         return jsonify(code=400, msg="参数不完整")
#     # 如果都有， 返回错误
#     if student_id is not None and course_id is not None:
#         return jsonify(code=400, msg="不能同时指定 student_id 和 course_id")
    
#     ddl_time = datetime.strptime(ddl_time, "%Y-%m-%d %H:%M:%S")
#     ddl = DDL(student_id=student_id, course_id=course_id, ddl_time=ddl_time, ddl_content=ddl_content)
#     try:
#         db.session.add(ddl)
#         db.session.commit()
#         return jsonify(code=200, msg="添加成功")
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return jsonify(code=400, msg="添加失败")
        
# @app.route('/calender/update', methods=['POST'])
# def update_ddl():
#     """
#     ex:
#     {
#         "ddl_id": 1,
#         "ddl_status": "已完成"
#     }
#     """
#     req_data = request.get_json()
#     ddl_id = req_data.get("ddl_id")
#     ddl_status = req_data.get("ddl_status")
#     ddl = DDL.query.get(ddl_id)
#     if ddl is None:
#         return jsonify(code=400, msg="ddl_id 不存在")
#     ddl.ddl_status = ddl_status
#     try:
#         db.session.commit()
#         return jsonify(code=200, msg="更新成功")
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return jsonify(code=400, msg="更新失败")
    
# @app.route('/calender/delete', methods=['POST'])
# def delete_ddl():
#     """
#     ex:
#     {
#         "ddl_id": 1
#     }
#     """
#     req_data = request.get_json()
#     ddl_id = req_data.get("ddl_id")
#     ddl = DDL.query.get(ddl_id)
#     if ddl is None:
#         return jsonify(code=400, msg="ddl_id 不存在")
#     try:
#         db.session.delete(ddl)
#         db.session.commit()
#         return jsonify(code=200, msg="删除成功")
#     except Exception as e:
#         print(e)
#         db.session.rollback()
#         return jsonify(code=400, msg="删除失败")