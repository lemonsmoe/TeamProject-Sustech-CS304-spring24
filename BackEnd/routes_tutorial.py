# all code are written with the help of Copilot. 
from flask import jsonify, request, session, Blueprint
from datetime import datetime, timedelta
from models_wholeProject import db, Tutor, Appointment, Workshop,fk_command
from sqlalchemy import inspect

app_tutorial = Blueprint('app_tutorial', __name__, url_prefix='/tutorial')

@app_tutorial.route('/tutors/get', methods=['GET'])
def get_tutors():
    """
    获取导师列表
    ---
    tags:
      - Tutorial
    responses:
      200:
        description: 返回导师列表
        schema:
          type: array
          items:
            type: object
            properties:
              age:
                type: integer
                description: 导师年龄
                example: 18
              email:
                type: string
                description: 导师邮箱
                example: "12110323@mail.sustech.edu.cn"
              gender:
                type: string
                description: 导师性别
                example: "母"
              name:
                type: string
                description: 导师姓名
                example: "Openzishen"
              subject:
                type: string
                description: 导师擅长科目
                example: "钢管舞"
              tutor_id:
                type: integer
                description: 导师ID
                example: 1
      default:
        description: 未知错误
        schema:
          type: object
          properties:
            msg:
              type: string
              description: 错误信息
              example: "未知错误"
    """
    print(f'current student_id: {session.get("student_id", None)}')
    tutors = Tutor.query.all()
    data = [dict((c, getattr(tutor, c)) for c in inspect(tutor).mapper.column_attrs.keys()) for tutor in tutors]
    return jsonify(data)


@app_tutorial.route('/tutors/add', methods=['POST'])
def add_tutor():
    """
    添加导师信息
    ex:
    {
        "name": "张三",
        "subject": "数学",
        "gender": "男",
        "age": 30,
        "email": "12110316@mail.sustech.edu.cn"
    }
    ---
    tags:
        - Tutorial
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 导师姓名
              example: "张三"
            subject:
              type: string
              description: 导师擅长科目
              example: "数学"
            gender:
              type: string
              description: 导师性别
              example: "男"
            age:
              type: integer
              description: 导师年龄
              example: 30
            email:
              type: string
              description: 导师邮箱
              example: "12110316@mail.sustech.edu.cn"
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
    """
    # 检查是不是管理员
    if session.get("student_id", "admin") != "admin":
        return jsonify(msg="没有权限"), 202
    req_data = request.get_json()
    # 判断是否已经存在
    tutor = Tutor.query.filter_by(email=req_data.get("email")).first()
    if tutor is not None:
        return jsonify(msg="该邮箱已经注册过"), 202
    tutor = Tutor(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(tutor)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败", error=str(e)), 202

@app_tutorial.route('/tutors/delete', methods=['POST'])
def delete_tutor():
    """
    ex:
    {
        "tutor_id": 1
    }
    """
    req_data = request.get_json()
    tutor_id = req_data.get("tutor_id")
    tutor = Tutor.query.get(tutor_id)
    if tutor is None:
        return jsonify(msg="tutor_id 不存在"), 202
    try:
        db.session.delete(tutor)
        db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202

@app_tutorial.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    data = [dict((c, getattr(appointment, c)) for c in inspect(appointment).mapper.column_attrs.keys()) for appointment in appointments]
    return jsonify(data)

@app_tutorial.route('/appointments/get', methods=['POST'])
def get_appointment():
    """
获取预约信息
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: false
    schema:
      type: object
      properties:
        tutor_name:
          type: string
          description: 老师姓名（可选）
        appointment_date:
          type: string
          format: date
          description: 预约日期（可选，格式：YYYY-MM-DD）
responses:
  200:
    description: 成功获取预约信息
    schema:
      type: array
      items:
        type: object
        properties:
          appointment_id:
            type: integer
            description: 预约ID
          tutor_id:
            type: string
            description: 教师ID
          tutor_name:
            type: string
            description: 教师姓名
          appointment_time_start:
            type: string
            description: 预约开始时间（格式：YYYY-MM-DD HH:MM）
          appointment_time_end:
            type: string
            description: 预约结束时间（格式：YYYY-MM-DD HH:MM）
          type:
            type: string
            description: 预约类型（"习题课" 或 "1对1辅导"）
  404:
    description: 未找到预约信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 未找到预约信息
"""

    # print(session)
    student_id = session.get("student_id", "admin")
    appointments = Appointment.query.filter_by(student_id=student_id, used=1).all()
    data = [dict((c, getattr(appointment, c)) for c in inspect(appointment).mapper.column_attrs.keys()) for appointment in appointments]
    # 获取老师的名字
    for workshop in data:
      try:
        workshop["tutor_name"] = Tutor.query.get(workshop["tutor_id"]).name
      except:
        workshop["tutor_name"] = "彭小僧猫娘妹妹啾咪"
    # 根据tutor_id是否为空给每个appointment添加一个type字段
    data = [dict(appointment, type="习题课" if appointment["workshop_id"] is not None else "1对1辅导") for appointment in data]
    
    
    req_data = request.get_json()
    print(req_data)
    if req_data.get('tutor_name') and appointments:
        data = [appointment for appointment in data if req_data.get('tutor_name').lower() in appointment["tutor_name"].lower()]
        
    if req_data.get('appointment_date') and appointments:
        appointment_date = req_data.get("appointment_date").split('T')[0]
        appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d")
        appointment_date = appointment_date + timedelta(hours=25)
        # print(appointment_date.date())
        data = [appointment for appointment in data if appointment_date.date() == appointment["appointment_time_start"].date()]
        
    # 剔除已过期的预约
    data = [appointment for appointment in data if appointment["appointment_time_start"] > datetime.now()]
    
    return jsonify(data)
    

@app_tutorial.route('/appointments/add', methods=['POST'])
def add_appointment():
    """
添加一个预约课程
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        tutor_id:
          type: string
          description: 教师ID
        appointment_date:
          type: string
          format: date
          description: 预约日期（格式：YYYY-MM-DD）
        appointment_time:
          type: string
          description: 预约时间段（格式：“HH:MM - HH:MM”）
        help_needed:
          type: string
          description: 需要帮助的内容
responses:
  200:
    description: 添加成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 添加成功
  202:
    description: 添加失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 添加失败
"""

    req_data = request.get_json()
    # 过滤掉不需要的数据
    need_keys = ["tutor_id", "appointment_date", "appointment_time", "help_needed"]
    req_data = {k: v for k, v in req_data.items() if k in need_keys}
    
    print('fuck', req_data)
    try:
        appointment_date = req_data.pop("appointment_date")
        appointment_date = appointment_date.split('T')[0]
        appointment_time = req_data.pop("appointment_time")
        req_data["appointment_time_start"] = datetime.strptime(f"{appointment_date} {appointment_time.split(' - ')[0]}", "%Y/%m/%d %H:%M")
        req_data["appointment_time_end"] = datetime.strptime(f"{appointment_date} {appointment_time.split(' - ')[1]}", "%Y/%m/%d %H:%M")
        
        
        if not req_data.get("student_id"):
            req_data["student_id"] = session.get("student_id", "admin")
        appointment = Appointment(**req_data)
    
        db.session.execute(fk_command)
        db.session.add(appointment)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败", error=str(e)), 202

@app_tutorial.route('/appointments/addworkshop', methods=['POST'])
def add_workshop_appointment():
    """
添加研讨会预约
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        workshop_id:
          type: integer
          description: 研讨会ID
          example: 1
responses:
  200:
    description: 预约成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 预约成功
  202:
    description: 预约失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 预约失败
"""

    req_data = request.get_json()
    workshop_id = req_data.get("workshop_id")
    workshop = Workshop.query.get(workshop_id)
    if workshop is None:
        return jsonify(msg="workshop_id 不存在"), 202
    try:
        appointment = Appointment(
            tutor_id=workshop.tutor_id,
            workshop_id=workshop_id,
            appointment_time_start=workshop.time_start,
            appointment_time_end=workshop.time_end,
            student_id=session.get("student_id", "admin"),
            help_needed=workshop.subject
        )
        db.session.execute(fk_command)
        db.session.add(appointment)
        db.session.commit()
        return jsonify(msg="预约成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="预约失败"), 202
    
@app_tutorial.route('/appointments/delete', methods=['POST'])
def delete_appointment():
    """
删除预约
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        appointment_id:
          type: integer
          description: 预约ID
          example: 1
responses:
  200:
    description: 删除成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除成功
  202:
    description: 删除失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除失败
"""

    req_data = request.get_json()
    appointment_id = req_data.get("appointment_id")
    appointment = Appointment.query.get(appointment_id)
    if appointment is None:
        return jsonify(msg="appointment_id 不存在"), 202
    try:
        db.session.delete(appointment)
        db.session.commit()
        # appointment.used = False
        # db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202

@app_tutorial.route('/workshops/add', methods=['POST'])
def add_workshop():
    """
添加研讨会
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        date:
          type: string
          format: date
          description: 研讨会日期（格式：YYYY-MM-DD）
        time:
          type: string
          description: 研讨会时间段（格式：“HH:MM - HH:MM”）
        location:
          type: string
          description: 研讨会地点
        subject:
          type: string
          description: 研讨会主题
        tutor_id:
          type: string
          description: 教师ID
        content:
          type: string
          description: 研讨会内容
responses:
  200:
    description: 添加成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 添加成功
  202:
    description: 添加失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 添加失败
"""

    # 检查是不是管理员
    if session.get("student_id", "admin") != "admin":
        return jsonify(msg="没有权限"), 202
    req_data = request.get_json()
    # 过滤掉不需要的数据
    need_keys = ["date", "time", "location", "subject", "tutor_id", "content"]
    req_data = {k: v for k, v in req_data.items() if k in need_keys}
    
    date = req_data.pop("date")
    time = req_data.pop("time")
    date = date.split('T')[0]
    req_data["time_start"] = datetime.strptime(f"{date} {time.split(' - ')[0]}", "%Y/%m/%d %H:%M")
    req_data["time_end"] = datetime.strptime(f"{date} {time.split(' - ')[1]}", "%Y/%m/%d %H:%M")
    
    workshop = Workshop(**req_data)
    try:
        db.session.execute(fk_command)
        db.session.add(workshop)
        db.session.commit()
        return jsonify(msg="添加成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="添加失败", error=str(e)), 202

@app_tutorial.route('/workshops/get', methods=['GET'])
def get_workshops():
    """
获取所有研讨会信息
---
tags:
  - Tutorial
responses:
  200:
    description: 成功获取研讨会信息
    schema:
      type: array
      items:
        type: object
        properties:
          date:
            type: string
            format: date
            description: 研讨会日期（格式：YYYY-MM-DD）
          time_start:
            type: string
            description: 研讨会开始时间（格式：HH:MM）
          time_end:
            type: string
            description: 研讨会结束时间（格式：HH:MM）
          location:
            type: string
            description: 研讨会地点
          subject:
            type: string
            description: 研讨会主题
          tutor_id:
            type: string
            description: 教师ID
          tutor_name:
            type: string
            description: 教师姓名
  404:
    description: 未找到研讨会信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 未找到研讨会信息
"""

    workshops = Workshop.query.all()
    data = [dict((c, getattr(workshop, c)) for c in inspect(workshop).mapper.column_attrs.keys()) for workshop in workshops]
    # 获取老师的名字
    for workshop in data:
      try:
        workshop["tutor_name"] = Tutor.query.get(workshop["tutor_id"]).name
      except:
        workshop["tutor_name"] = "彭小僧猫娘妹妹啾咪"
    # 修改时间格式
    for workshop in data:
        workshop["time_start"] = workshop["time_start"].strftime("%Y-%m-%d %H:%M")
        workshop["time_end"] = workshop["time_end"].strftime("%H:%M")
    return jsonify(data)

@app_tutorial.route('/workshops/delete', methods=['POST'])
def delete_workshop():
    """
删除研讨会
---
tags:
  - Tutorial
parameters:
  - name: body
    in: body
    required: true
    schema:
      type: object
      properties:
        workshop_id:
          type: integer
          description: 研讨会ID
          example: 1
responses:
  200:
    description: 删除成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除成功
  202:
    description: 删除失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 删除失败
"""

    req_data = request.get_json()
    workshop_id = req_data.get("workshop_id")
    workshop = Workshop.query.get(workshop_id)
    if workshop is None:
        return jsonify(msg="workshop_id 不存在"), 202
    try:
        db.session.delete(workshop)
        db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202