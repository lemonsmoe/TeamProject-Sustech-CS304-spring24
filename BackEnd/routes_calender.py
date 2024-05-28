from flask import jsonify, request, session, Blueprint
from datetime import datetime
from models_wholeProject import app, db, DDL
from sqlalchemy import inspect

app_calender = Blueprint('app_calender', __name__, url_prefix='/calender')

@app_calender.route('/', methods=['GET'])
def get_calender():
    ddls = DDL.query.all()
    data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in ddls]
    return jsonify(data)

@app_calender.route('/<student_id>', methods=['GET'])
def get_student_calender(student_id):
    ddls = DDL.query.filter_by(student_id=student_id).all()
    data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in ddls]
    return jsonify(data)

@app_calender.route('/get', methods=['GET'])
def get_ddl():
    student_id = session.get("student_id", None)
    if student_id is None:
        return jsonify(msg="未登录"), 202
    else:
        personal_ddls = DDL.query.filter_by(student_id=student_id).all()
        # 将表中course_id列不为空的行取出到all_ddls
        all_ddls = DDL.query.filter(DDL.course_id != None).all()
        # 将personal_ddls和all_ddls合并
        all_ddls.extend(personal_ddls)
        data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in all_ddls]
        return jsonify(data)
        

@app_calender.route('/add', methods=['POST'])
def add_ddl():
    """
    ex:
    {
        "student_id": "12111728",
        "ddl_time": "2021-06-01 00:00:00",
        "ddl_content": "完成实验报告"
    }
    """
    req_data = request.get_json()
    student_id = req_data.get("student_id", None)
    course_id = req_data.get("course_id", None)
    ddl_time = req_data.get("ddl_time", None)
    ddl_content = req_data.get("ddl_content")
    # student_id 和 course_id 只需要一个即可
    if student_id is None and course_id is None:
        return jsonify(msg="参数不完整"), 202
    # 如果都有， 返回错误
    if student_id is not None and course_id is not None:
        return jsonify(msg="不能同时指定 student_id 和 course_id"), 202
    
    ddl_time = datetime.strptime(ddl_time, "%Y-%m-%d %H:%M:%S")
    ddl = DDL(student_id=student_id, course_id=course_id, ddl_time=ddl_time, ddl_content=ddl_content)
    try:
        db.session.add(ddl)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败"), 202
        
@app_calender.route('/update', methods=['POST'])
def update_ddl():
    """
    ex:
    {
        "ddl_id": 1,
        "ddl_status": "已完成"
    }
    """
    req_data = request.get_json()
    ddl_id = req_data.get("ddl_id")
    ddl_status = req_data.get("ddl_status")
    ddl = DDL.query.get(ddl_id)
    if ddl is None:
        return jsonify(msg="ddl_id 不存在"), 202
    ddl.ddl_status = ddl_status
    try:
        db.session.commit()
        return jsonify(msg="更新成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="更新失败"), 202
    
@app_calender.route('/delete', methods=['POST'])
def delete_ddl():
    """
    ex:
    {
        "ddl_id": 1
    }
    """
    req_data = request.get_json()
    ddl_id = req_data.get("ddl_id")
    ddl = DDL.query.get(ddl_id)
    if ddl is None:
        return jsonify(msg="ddl_id 不存在"), 202
    try:
        db.session.delete(ddl)
        db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202