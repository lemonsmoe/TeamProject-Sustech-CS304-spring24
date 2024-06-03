# all code are written with the help of Copilot. 
from flask import jsonify, request, session, Blueprint
from datetime import datetime
import json
from CourseRec.Client_scheduleCourse import Client_Schedule
from models_wholeProject import app, db, fk_command, Student, Student_Star
import concurrent.futures
import multiprocessing
app_courserc = Blueprint('app_courserc', __name__, url_prefix='/courserc')

def task(data):
        return Client_Schedule(data=data)

@app_courserc.route('/submit_data', methods=['POST'])
def handle_submission():
    """
    根据前端传来的数据，调用选课程序，返回选课结果
    ---
    tags:
      - Course Schedule
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            password:
              type: string
              description: 用户的密码
            student_name:
              type: string
              description: 学生姓名
            keywords:
              type: array
              items:
                type: string
              description: 关键词列表，用于选课筛选
            badwords:
              type: array
              items:
                type: string
              description: 禁用词列表，用于排除不想选的课
            excluded_time:
              type: object
              properties:
                点:
                  type: array
                  items:
                    type: array
                    items:
                      type: integer
                  description: 排除的时间段
    responses:
      200:
        description: 返回选课结果
        schema:
          type: object
          properties:
            status:
              type: string
              description: 操作状态（成功或失败）
            solution_count:
              type: integer
              description: 可行方案的数量
            info:
              type: array
              items:
                type: string
              description: 选中的课程信息
            schedule_scheme:
              type: array
              items:
                type: string
              description: 课程安排方案
    """
    data = request.get_json()
    print(data)
    # 逻辑处理数据和调用选课程序
    # 将data['keywords']列表中的空字符串去掉
    data['keywords'] = list(filter(lambda x: x != '', data['keywords']))
    data['keywords'] = list(filter(lambda x: x != '-', data['keywords']))
    data['badwords'] = list(filter(lambda x: x != '', data['badwords']))
    global scheduler
    scheduler = Client_Schedule(data=data)
    # with multiprocessing.Pool(1) as pool:
    #     result = pool.apply_async(task, (data,))

    #     try:
    #         scheduler = result.get(timeout=15)
    #     except multiprocessing.TimeoutError:
    #         print("Task timed out")
    #         response = {'status': 'fail', "msg": '彭小僧猪脑过载了啦，你这张表很可能有过万种课程组合，我实在是算不过来啦'}
    #         pool.terminate()  # Terminate the process
    #         return jsonify(response)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(task, data)
        try:
            scheduler = future.result(timeout=15)
        except concurrent.futures.TimeoutError:
            print("Task timed out")
            response = {'status': 'fail', "msg": '彭小僧猪脑过载了啦，你这张表很可能有过万种课程组合，我实在是算不过来啦'}
            return jsonify(response)
    # print_info()


    # threading.Thread(target=run_schedule).start()
    if scheduler is None:
        response = {'status': 'fail', "msg": '彭小僧找不到符合条件的课程安排方案，请重新设置条件捏'}
        return jsonify(response)
    else:
        print(scheduler.get_selected_course_info())
        response = {'status': 'success',
        "solution_count": len(scheduler.schedule_scheme),
        "info": scheduler.get_selected_course_info(),
        "schedule_scheme": scheduler.get_schdule_scheme_info()}
        return jsonify(response)
    
@app_courserc.route('/star/put', methods=['POST'])
def star():
    """
    收藏一个课程安排方案
    ---
    tags:
      - Course Schedule
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            schedule:
              type: object
              description: 你要收藏的课程安排方案（一个JSON对象）
    responses:
      200:
        description: 收藏成功
        schema:
          type: object
          properties:
            msg:
              type: string
              example: 收藏成功
      202:
        description: 收藏失败
        schema:
          type: object
          properties:
            msg:
              type: string
              example: 收藏失败
    """
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    print(req_data)
    schedule = req_data.get("schedule")
    if schedule is None:
        return jsonify(msg="收藏失败"), 202
    
    schedule = json.dumps(schedule)
    student_star = Student_Star(student_id=student_id, schedule=schedule)
    try:
        db.session.execute(fk_command)
        db.session.add(student_star)
        db.session.commit()
        return jsonify(msg="收藏成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="收藏失败"), 202
    
@app_courserc.route('/star/get', methods=['GET'])
def get_star():
    """
    获取用户收藏的课程安排方案
    ---
    tags:
      - Course Schedule
    responses:
      200:
        description: 获取成功
        schema:
          type: array
          items:
            type: object
          example:
            - {"schedule": {"星期一": [[1, 2], [3, 4]]}}
            - {"schedule": {"星期二": [[5, 6], [7, 8]]}}
      202:
        description: 获取失败
        schema:
          type: object
          properties:
            msg:
              type: string
              example: 获取失败
    """
    try:
        student_id = session.get("student_id", 'admin')
        student_star = Student_Star.query.filter_by(student_id=student_id).all()
        data = [json.loads(i.schedule) for i in student_star]
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify(msg="获取失败"), 202
    
@app_courserc.route('/star/delete', methods=['POST'])
def delete_star():
    """
    删除用户收藏的课程安排方案
    ---
    tags:
      - Course Schedule
    parameters:
        - name: body
          in: body
          required: true
          schema:
                type: object
                properties:
                    schedule:
                        type: object
                        description: 你要删除的课程安排方案（一个JSON对象）
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
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    schedule = req_data.get("schedule")
    if schedule is None:
        return jsonify(msg="删除失败"), 202
    
    schedule = json.dumps(schedule)
    student_star = Student_Star.query.filter_by(student_id=student_id, schedule=schedule).first()
    if student_star is None:
        return jsonify(msg="删除失败"), 202
    try:
        db.session.delete(student_star)
        db.session.commit()
        return jsonify(msg="删除成功"), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(msg="删除失败"), 202