# all code are written with the help of Copilot. 
from flask import jsonify, request, session, Blueprint
from datetime import datetime
from models_wholeProject import app, db, Student_DDL, Course_DDL, Student_Course_finished, fk_command, Student_Subscribe
from tool import connect_db
from sqlalchemy import inspect, text
app_calender = Blueprint('app_calender', __name__, url_prefix='/calender')

@app_calender.route('/', methods=['GET'])
def get_calender():
    ddls = Student_DDL.query.all()
    data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in ddls]
    return jsonify(data)

@app_calender.route('/getallevent', methods=['GET'])
def get_calender_byid():
    """
    获取个人的所有DDL和订阅课程的DDL
    ---
    tags:
      - Calender
    responses:
      200:
        description: 返回个人的所有DDL和订阅课程的DDL
        schema:
          type: object
          additionalProperties:
            type: object
            properties:
              display:
                type: array
                items:
                  type: array
                  items:
                    type: string
                  description: DDL标题和状态
                description: 显示的DDL列表
              meta:
                type: string
                description: 完成的DDL数与总DDL数的比值
        examples:
          application/json:
            {
              "2024-05-01": {
                "display": [
                  ["喜欢pzs被你发现", "未完成"]
                ],
                "meta": "0/1"
              },
              "2024-05-02": {
                "display": [
                  ["你干嘛呀", "未完成"]
                ],
                "meta": "0/1"
              }
            }
    """
    student_id = session.get("student_id", 'admin')
    student_ddls = Student_DDL.query.filter_by(student_id=student_id).all()
    subscribe_courses = Student_Subscribe.query.filter_by(student_id=student_id).all()
    course_ddls = Course_DDL.query.filter(Course_DDL.course_id.in_([i.course_id for i in subscribe_courses])).all()
    all_ddls = student_ddls + course_ddls
    # 返回示例
    """
    {
        '2021-06-01': {
            'display': [('ddl_title1', 'ddl_status1'), ('ddl_title2', 'ddl_status2'), ...],
            'meta': 2/10
        }
        '2021-06-02': {
            'display': [('ddl_title1', 'ddl_status1'), ('ddl_title2', 'ddl_status2'), ...],
            'meta': 2/10
            }
    }
    """
    data = {}
    for ddl in all_ddls:
        ddl_time = ddl.ddl_time.strftime("%Y-%m-%d")
        if ddl_time not in data:
            data[ddl_time] = {"display": [], "meta": 0}
        # elif len(data[ddl_time]['display']) >= 3:
        #     continue

        # 如果是course_ddl，需要判断是否完成
        if isinstance(ddl, Course_DDL):
            ddl_status = "未完成"
            if Student_Course_finished.query.filter_by(student_id=student_id, course_ddl_id=ddl.ddl_id).first():
                ddl_status = "完成"
        else:
            ddl_status = ddl.ddl_status
        data[ddl_time]['display'].append((ddl.ddl_title, ddl_status))
        if ddl_status == "完成":
            data[ddl_time]['meta'] += 1
            
    for k, v in data.items():
        data[k]['meta'] = f"{v['meta']}/{len(v['display'])}"
        
    return jsonify(data)
    
@app_calender.route('/get_byday', methods=['POST'])
def get_calender_byday():
    """
    获取指定日期的所有DDL
    ex:
    {
        "ddl_time": "2021-06-01"
    }
    ---
    tags:
      - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            ddl_time:
              type: string
              description: 日期（格式：YYYY-MM-DD）
              example: "2021-06-01"
    responses:
      200:
        description: 返回指定日期的所有DDL
        schema:
          type: array
          items:
            type: object
            properties:
              ddl_id:
                type: integer
                description: DDL的ID
              ddl_title:
                type: string
                description: DDL的标题
              ddl_time:
                type: string
                description: DDL的时间
              ddl_status:
                type: string
                description: DDL的状态（完成或未完成）
              course_id:
                type: integer
                description: 课程ID，如果是个人DDL则为空
              ddl_type:
                type: string
                description: DDL类型（课程或个人）
        examples:
          application/json:
            [
              {
                "ddl_id": 1,
                "ddl_title": "喜欢pzs被你发现",
                "ddl_time": "2021-06-01 10:00:00",
                "ddl_status": "未完成",
                "course_id": null,
                "ddl_type": "personal"
              },
              {
                "ddl_id": 2,
                "ddl_title": "你干嘛呀",
                "ddl_time": "2021-06-01 14:00:00",
                "ddl_status": "完成",
                "course_id": 101,
                "ddl_type": "course"
              }
            ]
    """
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    print(req_data)
    ddl_time = req_data.get("ddl_time")
    # 使用like查询
    student_ddls = Student_DDL.query.filter(Student_DDL.ddl_time.like(f"{ddl_time}%"), Student_DDL.student_id == student_id).all()
    subscribe_courses = Student_Subscribe.query.filter_by(student_id=student_id).all()
    course_ddls = Course_DDL.query.filter(Course_DDL.ddl_time.like(f"{ddl_time}%"), Course_DDL.course_id.in_([i.course_id for i in subscribe_courses])).all()
    all_ddls = student_ddls + course_ddls
    data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in all_ddls]
    # 加一个ddl_type字段，根据是否有course_id来判断
    data = [{"ddl_type": ddl.get("course_id") if ddl.get("course_id") else "personal", **ddl} for ddl in data]
    # 给course_ddl加一个ddl_status字段
    for ddl in data:
        if ddl.get("course_id"):
            ddl["ddl_status"] = "未完成"
            if Student_Course_finished.query.filter_by(student_id=student_id, course_ddl_id=ddl["ddl_id"]).first():
                ddl["ddl_status"] = "完成"
    return jsonify(data)

@app_calender.route('/student_ddl/get', methods=['GET'])
def get_ddl():
    student_id = session.get("student_id", 'admin')
    if student_id is None:
        return jsonify(msg="未登录"), 202
    else:
        ddls = Student_DDL.query.filter_by(student_id=student_id).all()
        data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in ddls]
        return jsonify(data)
        
@app_calender.route('/course_ddl/get', methods=['GET'])
def get_course_ddl():
    ddls = Course_DDL.query.all()
    data = [dict((c, getattr(ddl, c)) for c in inspect(ddl).mapper.column_attrs.keys()) for ddl in ddls]
    return jsonify(data)

@app_calender.route('/course/get', methods=['POST'])
def get_course():
    """
    根据课程ID、课程名称和课程教师获取课程信息, 用于订阅
    ex:
    {
        "course_id": "CS1",
        "course_name": "组成原理",
        "course_teacher": "刘"
    }
    ---
    tags:
        - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            course_id:
              type: string
              description: 课程ID
              example: "CS1"
            course_name:
              type: string
              description: 课程名称
              example: "组成原理"
            course_teacher:
              type: string
              description: 课程教师
              example: "刘"
    responses:
      200:
        description: 返回课程信息列表
        schema:
          type: array
          items:
            type: object
            properties:
              course_id:
                type: string
                description: 课程ID
              course_name:
                type: string
                description: 课程名称
      202:
        description: 获取失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "获取失败"
            error:
              type: string
              description: 错误详情
    """
    try:
        req_data = request.get_json()
        print(req_data)
        
        sql = """
            select col2, col0,col9 from course2024spring;
        """
        # 用like查询
        sql = f"""
            select col2, col3,col9 from course2024spring where col2 like '%{req_data.get("course_id")}%' and col3 like '%{req_data.get("course_name")}%' and col9 like '%{req_data.get("course_teacher")}%';
        """
        # sql = text(sql)
        # result = db.session.execute(sql)
        con, cur = connect_db()
        cur.execute(sql)
        result = cur.fetchall()
        data = []
        # print(result)
        for row in result:
            # print(row)
            course = {
                "course_id": row[0],
                "course_name": row[1]
            }
            if course not in data:
                data.append(course)
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify(msg="获取失败", error=str(e)), 202

@app_calender.route('/student_ddl/add', methods=['POST'])
def add_ddl():
    """
    添加学生DDL
    ex:
    {
        "ddl_time": "2021-06-01 00:00:00",
        "ddl_title": "实验报告",
        "ddl_content": "完成实验报告"
    }
    ---
    tags:
        - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            ddl_time:
              type: string
              description: DDL的时间（格式：YYYY-MM-DD HH:MM:SS）
              example: "2021-06-01 00:00:00"
            ddl_title:
              type: string
              description: DDL的标题
              example: "实验报告"
            ddl_content:
              type: string
              description: DDL的内容
              example: "完成实验报告"
    responses:
      200:
        description: 添加成功
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 成功信息
              example: "添加成功"
      202:
        description: 添加失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "添加失败"
            error:
              type: string
              description: 错误详情
    """
    try:
        req_data = request.get_json()
        print(req_data)
        req_data["ddl_time"] = datetime.strptime(req_data["ddl_time"], "%Y-%m-%d %H:%M:%S")
        student_id = session.get("student_id", 'admin')
        ddl = Student_DDL(**req_data, student_id=student_id)
    
        db.session.add(ddl)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败", error=str(e)), 202
    
@app_calender.route('/course_ddl/add', methods=['POST'])
def add_course_ddl():
    """
    添加课程DDL
    ex:
    {
        "ddl_time": "2021-06-01 00:00:00",
        "ddl_title": "实验报告",
        "ddl_content": "完成实验报告",
        "course_id": "CS101"
    }
    ---
    tags:
        - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            ddl_time:
              type: string
              description: DDL的时间（格式：YYYY-MM-DD HH:MM）
              example: "2021-06-01 00:00:00"
            ddl_title:
              type: string
              description: DDL的标题
              example: "实验报告"
            ddl_content:
              type: string
              description: DDL的内容
              example: "完成实验报告"
            course_id:
              type: string
              description: 课程ID
              example: "CS101"
    responses:
      200:
        description: 添加成功
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 成功信息
              example: "添加成功"
      202:
        description: 添加失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "添加失败"
            error:
              type: string
              description: 错误详情
    """
    try:
        req_data = request.get_json()
        req_data["ddl_time"] = datetime.strptime(req_data["ddl_time"], "%Y-%m-%d %H:%M")
        ddl = Course_DDL(**req_data)
    
        db.session.add(ddl)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败", error=str(e)), 202
        
@app_calender.route('/update', methods=['POST'])
def update_ddl():
    """
    ex:
    {
        "course_id": "CS101",
        "ddl_content": "123",
        "ddl_id": 7,
        "ddl_status": "完成",
        "ddl_time": "Sat, 18 May 2024 00:00:00 GMT",
        "ddl_title": "去酒店开房3",
        "ddl_type": "CS101"
    }
    or
    {
        "ddl_content": "完成实验报告",
        "ddl_id": 1,
        "ddl_status": "未完成",
        "ddl_time": "Sat, 18 May 2024 00:00:00 GMT",
        "ddl_title": "滋生甘我",
        "ddl_type": "personal",
        "student_id": "admin"
    }
    """
    req_data = request.get_json()
    student_id = session.get("student_id", 'admin')
    print(req_data)
    if req_data.get('course_id'):
        try:
            db.session.execute(fk_command)
            # print('fuckkkkkk')
            if req_data.get("ddl_status") == "完成":
                student_course_finished = Student_Course_finished(student_id=student_id, course_ddl_id=req_data.get("ddl_id"))
                db.session.add(student_course_finished)
            else:
                student_course_finished = Student_Course_finished.query.filter_by(student_id=student_id, course_ddl_id=req_data.get("ddl_id")).first()
                if student_course_finished:
                    db.session.delete(student_course_finished)
            db.session.commit()
            return jsonify(msg="更新成功"), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(msg="更新失败"), 202
    ddl_id = req_data.get("ddl_id")
    ddl_status = req_data.get("ddl_status")
    ddl = Student_DDL.query.get(ddl_id)
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
    
@app_calender.route('/student_ddl/delete', methods=['POST'])
def delete_ddl():
    
    req_data = request.get_json()
    print(req_data)
    if req_data.get('course_id'):
        return jsonify(msg="请退课以删除！！！"), 202
    ddl_id = req_data.get("ddl_id")
    ddl = Student_DDL.query.get(ddl_id)
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
    
@app_calender.route('/course_ddl/delete', methods=['POST'])
def delete_course_ddl():
    """
    ex:
    {
        "ddl_id": 1
    }
    """
    pass

@app_calender.route('/subscribe/put', methods=['POST'])
def subscribe():
    """
    订阅课程
    ex:
    {
        "course_id": "CS101"
    }
    ---
    tags:
      - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            course_id:
              type: string
              description: 课程ID
              example: "CS101"
    responses:
      200:
        description: 订阅成功
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 成功信息
              example: "订阅成功"
      202:
        description: 订阅失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "订阅失败"
    """
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    course_id = req_data.get("course_id")
    if course_id is None:
        return jsonify(msg="订阅失败"), 202
    student_subscribe = Student_Subscribe(student_id=student_id, course_id=course_id)
    try:
        db.session.execute(fk_command)
        db.session.add(student_subscribe)
        db.session.commit()
        return jsonify(msg="订阅成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="订阅失败"), 202
    
@app_calender.route('/subscribe/get', methods=['GET'])
def get_subscribe():
    """
    获取订阅课程列表
    ---
    tags:
      - Calender
    responses:
      200:
        description: 返回订阅课程列表
        schema:
          type: array
          items:
            type: string
        examples:
          application/json:
            [
              "CS101",
              "CS102"
            ]
      202:
        description: 获取失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "获取失败"
    """
    
    try:
        student_id = session.get("student_id", 'admin')
        student_subscribe = Student_Subscribe.query.filter_by(student_id=student_id).all()
        data = [i.course_id for i in student_subscribe]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify(msg="获取失败"), 202
    
@app_calender.route('/subscribe/delete', methods=['POST'])
def delete_subscribe():
    """
    取消订阅课程
    ex:
    {
        "course_id": "CS101"
    }
    ---
    tags:
        - Calender
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            course_id:
              type: string
              description: 课程ID
              example: "CS101"
    responses:
      200:
        description: 删除成功
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 成功信息
              example: "删除成功"
      202:
        description: 删除失败
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "删除失败"
    """
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    course_id = req_data.get("course_id")
    if course_id is None:
        return jsonify(msg="删除失败"), 202
    student_subscribe = Student_Subscribe.query.filter_by(student_id=student_id, course_id=course_id).first()
    if student_subscribe is None:
        return jsonify(msg="删除失败"), 202
    try:
        db.session.delete(student_subscribe)
        db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202