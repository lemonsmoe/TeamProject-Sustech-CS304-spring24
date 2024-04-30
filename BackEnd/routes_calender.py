from flask import jsonify, request, session
from datetime import datetime
from models_wholeProject import app, db, DDL

@app.route('/calender', methods=['GET'])
def get_calender():
    ddls = DDL.query.all()
    data = []
    for ddl in ddls:
        data.append({
            "ddl_id": ddl.ddl_id,
            "ddl_time": ddl.ddl_time,
            "ddl_content": ddl.ddl_content,
            "ddl_status": ddl.ddl_status or "未完成"
        })
    return jsonify(data)

@app.route('/calender/<student_id>', methods=['GET'])
def get_student_calender(student_id):
    ddls = DDL.query.filter_by(student_id=student_id).all()
    data = []
    for ddl in ddls:
        data.append({
            "ddl_id": ddl.ddl_id,
            "ddl_time": ddl.ddl_time,
            "ddl_content": ddl.ddl_content,
            "ddl_status": ddl.ddl_status or "未完成"
        })
    return jsonify(data)

@app.route('/calender/add', methods=['POST'])
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
    student_id = req_data.get("student_id")
    course_id = req_data.get("course_id", None)
    ddl_time = req_data.get("ddl_time", None)
    ddl_content = req_data.get("ddl_content")
    # student_id 和 course_id 只需要一个即可
    if student_id is None and course_id is None:
        return jsonify(code=400, msg="参数不完整")
    # 如果都有， 返回错误
    if student_id is not None and course_id is not None:
        return jsonify(code=400, msg="不能同时指定 student_id 和 course_id")
    
    ddl_time = datetime.strptime(ddl_time, "%Y-%m-%d %H:%M:%S")
    ddl = DDL(student_id=student_id, course_id=course_id, ddl_time=ddl_time, ddl_content=ddl_content)
    try:
        db.session.add(ddl)
        db.session.commit()
        return jsonify(code=200, msg="添加成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加失败")
        
@app.route('/calender/update', methods=['POST'])
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
        return jsonify(code=400, msg="ddl_id 不存在")
    ddl.ddl_status = ddl_status
    try:
        db.session.commit()
        return jsonify(code=200, msg="更新成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="更新失败")