from flask import jsonify, request, Blueprint, session
from datetime import datetime
from models_wholeProject import db, fk_command, CourseReview
from tool import connect_db
from sqlalchemy import inspect, text

app_evaluation = Blueprint('app_evaluation', __name__, url_prefix='/evaluation')

@app_evaluation.route('/review/put', methods=['POST'])
def put_course_review():
    """
发布课程评价
---
tags:
  - Evaluation
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
        rating:
          type: integer
          description: 评分（1-5）
        difficulty:
          type: string
          description: 课程难度
        homework:
          type: string
          description: 课程作业量
        grading:
          type: string
          description: 评分方式
        harvest:
          type: string
          description: 学到的内容
        comment:
          type: string
          description: 评论内容
responses:
  200:
    description: 评价发布成功
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 评价发布成功
  202:
    description: 评价发布失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 评价发布失败
"""

    focus_keys = ["course_id", "rating", "difficulty", "homework", "grading", "harvest", "comment"]
    
    student_id = session.get("student_id", 'admin')
    req_data = request.get_json()
    req_data = {k: req_data[k] for k in focus_keys}
    
    req_data["created_time"] = datetime.now()
    req_data["last_updated_time"] = datetime.now()

    course_review = CourseReview(**req_data, student_id=student_id)
    try:
        db.session.execute(fk_command)
        db.session.add(course_review)
        db.session.commit()
        return jsonify(msg="评价发布成功")
    except Exception as e:
        db.session.rollback()
        return jsonify(msg="发布失败", error=str(e)), 202

@app_evaluation.route('/review/getbrief', methods=['GET'])
def get_course_review_brief():
    """
获取课程评价摘要信息
---
tags:
  - Evaluation
responses:
  200:
    description: 成功获取课程评价摘要信息
    schema:
      type: array
      items:
        type: object
        properties:
          course_id:
            type: string
            description: 课程ID
          avg_rating:
            type: number
            description: 平均评分
          review_count:
            type: integer
            description: 评价数量
  404:
    description: 未找到课程评价摘要信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 未找到课程评价摘要信息
"""

    # 根据course_id分组，计算平均分、评价数量
    sql = text("SELECT course_id, ROUND(AVG(rating), 3) AS avg_rating, COUNT(*) AS review_count FROM course_review GROUP BY course_id")
    course_reviews = db.session.execute(sql).fetchall()
    data = [dict(course_id=course_review.course_id, avg_rating=course_review.avg_rating, review_count=course_review.review_count) for course_review in course_reviews]
    
    return jsonify(data)

@app_evaluation.route('/review/getall/<string:course_id>', methods=['GET'])
def get_course_reviews_by_id(course_id):
    """
按课程ID获取所有评价
---
tags:
  - Evaluation
parameters:
  - name: course_id
    in: path
    required: true
    type: string
    description: 课程ID
responses:
  200:
    description: 成功获取所有评价
    schema:
      type: array
      items:
        type: object
        properties:
          course_id:
            type: string
            description: 课程ID
          student_id:
            type: string
            description: 学生ID
          rating:
            type: integer
            description: 评分
          difficulty:
            type: string
            description: 课程难度
          homework:
            type: string
            description: 课程作业量
          grading:
            type: string
            description: 评分方式
          harvest:
            type: string
            description: 学到的内容
          comment:
            type: string
            description: 评论内容
          created_time:
            type: string
            description: 创建时间
          last_updated_time:
            type: string
            description: 最后更新时间
  404:
    description: 没有找到该课程的评价
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 没有找到该课程的评价
"""

    try:
        course_reviews = CourseReview.query.filter_by(course_id=course_id).all()
        data = [dict((c, getattr(course_review, c)) for c in inspect(course_review).mapper.column_attrs.keys()) for course_review in course_reviews]
        return jsonify(data)
    except Exception as e:
        return jsonify(msg="没有找到该课程的评价"), 202
    
@app_evaluation.route('/review/stats/<string:course_id>', methods=['GET'])
def get_course_review_stats(course_id):
    """
获取课程评价统计信息
---
tags:
  - Evaluation
parameters:
  - name: course_id
    in: path
    required: true
    type: string
    description: 课程ID
responses:
  200:
    description: 成功获取课程评价统计信息
    schema:
      type: object
      properties:
        difficulty:
          type: object
          properties:
            简单:
              type: integer
              description: 评价该课程为简单的数量
            普通:
              type: integer
              description: 评价该课程为普通的数量
            较难:
              type: integer
              description: 评价该课程为较难的数量
        homework:
          type: object
          properties:
            少:
              type: integer
              description: 评价该课程作业量少的数量
            适中:
              type: integer
              description: 评价该课程作业量适中的数量
            多:
              type: integer
              description: 评价该课程作业量多的数量
        grading:
          type: object
          properties:
            低:
              type: integer
              description: 评价该课程评分方式为低的数量
            中:
              type: integer
              description: 评价该课程评分方式为中的数量
            高:
              type: integer
              description: 评价该课程评分方式为高的数量
        harvest:
          type: object
          properties:
            少:
              type: integer
              description: 评价该课程学到内容少的数量
            中:
              type: integer
              description: 评价该课程学到内容中等的数量
            多:
              type: integer
              description: 评价该课程学到内容多的数量
  404:
    description: 获取课程评价统计信息失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 获取课程评价统计信息失败
"""

    try:
        course_reviews = CourseReview.query.filter_by(course_id=course_id).all()

        # 初始化统计信息
        stats = {
            "difficulty": {"简单": 0, "普通": 0, "较难": 0},
            "homework": {"少": 0, "适中": 0, "多": 0},
            "grading": {"低": 0, "中": 0, "高": 0},
            "harvest": {"少": 0, "中": 0, "多": 0},
        }

        for review in course_reviews:
            stats["difficulty"][review.difficulty] += 1
            stats["homework"][review.homework] += 1
            stats["grading"][review.grading] += 1
            stats["harvest"][review.harvest] += 1

        return jsonify(stats)
    except Exception as e:
        return jsonify(msg="获取课程评价统计信息失败", error=str(e)), 202    
 
@app_evaluation.route('/course/<string:course_id>', methods=['GET'])
def get_course_info_by_id(course_id):
    """
按课程ID获取课程信息
---
tags:
  - Evaluation
parameters:
  - name: course_id
    in: path
    required: true
    type: string
    description: 课程ID
responses:
  200:
    description: 成功获取课程信息
    schema:
      type: object
      properties:
        course_name:
          type: string
          description: 课程名称
        course_id:
          type: string
          description: 课程ID
        course_type:
          type: string
          description: 课程类型
        credit:
          type: number
          description: 学分
        college:
          type: string
          description: 开课学院
  404:
    description: 没有找到该课程的信息
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 没有找到该课程的信息
"""

    try:
        con, cur = connect_db()
        sql = f"SELECT * FROM course2024spring WHERE col2='{course_id}'"
        cur.execute(sql)
        course_info = cur.fetchall()[0]
        cur.close()
        con.close()
        data = {
            "course_name": course_info[3],
            "course_id": course_info[1],
            "course_type": course_info[4]+course_info[5],
            "credit": course_info[7],
            "college": course_info[-2],
        }
        return jsonify(data)
    except Exception as e:
        return jsonify(msg="没有找到该课程的信息"), 202

@app_evaluation.route('/courses/brief', methods=['GET'])
def get_all_courses_brief():
    """
获取所有课程简介信息
---
tags:
  - Evaluation
responses:
  200:
    description: 成功获取所有课程简介信息
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
          course_type:
            type: string
            description: 课程类型
          credit:
            type: number
            description: 学分
          college:
            type: string
            description: 开课学院
          avg_rating:
            type: number
            description: 平均评分
          review_count:
            type: integer
            description: 评价数量
  404:
    description: 获取课程简介信息失败
    schema:
      type: object
      properties:
        msg:
          type: string
          example: 获取课程简介信息失败
"""

    try:
        con, cur = connect_db()
        sql = "SELECT col2 as course_id, col3 as course_name, col5 as course_type, col8 as credit, col14 as college FROM course2024spring"
        cur.execute(sql)
        courses = cur.fetchall()
        cur.close()
        con.close()

        # 去重并添加评分信息
        unique_courses = {}
        for course in courses:
            course_id = course[0]
            if course_id not in unique_courses:
                unique_courses[course_id] = {
                    "course_id": course[0],
                    "course_name": course[1],
                    "course_type": course[2],
                    "credit": course[3],
                    "college": course[4],
                    "avg_rating": 0,
                    "review_count": 0
                }

        # 转换为列表并取前10条
        data = list(unique_courses.values())[:10]

        return jsonify(data)
    except Exception as e:
        return jsonify(msg="获取课程简介信息失败", error=str(e)), 202

