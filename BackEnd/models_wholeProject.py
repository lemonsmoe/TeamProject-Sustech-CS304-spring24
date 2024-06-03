from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# import pymysql
from datetime import datetime
from sqlalchemy import text
# from flask_session import Session
app = Flask(__name__)
from sqlalchemy import UniqueConstraint


# from flasgger import Swagger
# swagger = Swagger(app)

from flask_cors import CORS
CORS(app, supports_credentials=True)
from flasgger import Swagger
Swagger(app)

app_ctx = app.app_context()
app_ctx.push()
fk_command = text("PRAGMA foreign_keys = ON;")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "./openzishen.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jjjsks"

db = SQLAlchemy(app)  # 实例化的数据库

# 学生登录信息表
class Student(db.Model):
    __tablename__ = "student"
    nickname = db.Column(db.String(64))  # 昵称
    student_id = db.Column(db.String(16), unique=True, primary_key=True)  # 学号，唯一标识
    password = db.Column(db.String(64))  # 登录密码
    last_login_time = db.Column(db.DateTime, default=datetime.now)  # 上次登录时间
    
# 给选课系统使用的表，
class Student_Star(db.Model):
    __tablename__ = "student_star"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))  # 学号，唯一标识
    schedule = db.Column(db.Text)  # 课程表
    __table_args__ = (UniqueConstraint('student_id', 'schedule', name='_student_schedule_uc'),)
    
# 学生订阅课程表
class Student_Subscribe(db.Model):
    __tablename__ = "student_subscribe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))  # 学号，唯一标识
    course_id = db.Column(db.String(16))  # 课程号
    __table_args__ = (UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),)

# 日历功能需要的DDL表
class Student_DDL(db.Model):
    __tablename__ = "student_ddl"
    ddl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))
    # course_ddl_id = db.Column(db.String(16))
    ddl_time = db.Column(db.DateTime)
    ddl_title = db.Column(db.String(256))
    ddl_content = db.Column(db.String(256))
    ddl_status = db.Column(db.String(16), default="未完成")
    
class Course_DDL(db.Model):
    __tablename__ = "course_ddl"
    ddl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.String(16))
    ddl_time = db.Column(db.DateTime)
    ddl_title = db.Column(db.String(256))
    ddl_content = db.Column(db.String(256))
    
class Student_Course_finished(db.Model):
    __tablename__ = "student_course_finished"
    finish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))
    course_ddl_id = db.Column(db.String(16), db.ForeignKey("course_ddl.ddl_id"))
    __table_args__ = (UniqueConstraint('student_id', 'course_ddl_id', name='_student_course_ddl_uc'),)

### 辅导老师信息表 (tutors)
class Tutor(db.Model):
    __tablename__ = "tutors"
    tutor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    subject = db.Column(db.String(64))
    gender = db.Column(db.String(8))
    age = db.Column(db.Integer)
    email = db.Column(db.String(128))
    __table_args__ = (UniqueConstraint('name', 'subject', name='_name_subject_uc'),)

## 学生的预约信息表 (appointments)
class Appointment(db.Model):
    __tablename__ = "appointments"
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))
    tutor_id = db.Column(db.Integer, db.ForeignKey("tutors.tutor_id"))
    workshop_id = db.Column(db.Integer, db.ForeignKey("workshops.workshop_id"))
    appointment_time_start = db.Column(db.DateTime)
    appointment_time_end = db.Column(db.DateTime)
    help_needed = db.Column(db.String(256))
    used = db.Column(db.Boolean, default=True)
    # 要求两列必须
    __table_args__ = (UniqueConstraint('student_id', 'appointment_time_start', name='_student_appointment_time_uc'),)
    

### 公开习题课信息表 (workshops)
class Workshop(db.Model):
    __tablename__ = "workshops"
    workshop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    location = db.Column(db.String(128))
    subject = db.Column(db.String(64))
    tutor_id = db.Column(db.String(16), db.ForeignKey("tutors.tutor_id"))
    content = db.Column(db.Text)

# 论坛模块
## 帖子表：帖子id，发帖人id，发帖时间，帖子标题，帖子内容，查看数，回复数，最后更新时间，主题，板块
class Post(db.Model):
    __tablename__ = "posts"
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))
    
    title = db.Column(db.String(128))
    # content = db.Column(db.Text)
    topic = db.Column(db.String(64))
    board = db.Column(db.String(64))
    
    view_count = db.Column(db.Integer, default=0)
    # reply_count = db.Column(db.Integer, default=0)
    
    created_time = db.Column(db.DateTime)
    last_updated_time = db.Column(db.DateTime)
    
    used = db.Column(db.Boolean, default=True)

## 帖子内容表：
class PostContent(db.Model):
    __tablename__ = "post_content"
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), primary_key=True)
    content = db.Column(db.Text)

## 回复表：
class Reply(db.Model):
    __tablename__ = "replies"
    reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))  # 回复用户的ID，假设有一个 users 表存储用户信息
    content = db.Column(db.Text)
    created_time = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=True)

    # 兮兄，你别急，要创建表的时候联系我
    

## 课程评价表：
class CourseReview(db.Model):
    __tablename__ = "course_review"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"))
    course_id = db.Column(db.String(100))
    rating = db.Column(db.Float)
    difficulty = db.Column(db.String(50))
    homework = db.Column(db.String(50))
    grading = db.Column(db.String(50))
    harvest = db.Column(db.String(50))
    comment = db.Column(db.Text)
    created_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_time = db.Column(db.DateTime, default=datetime.utcnow)

# class CourseReviewStats(db.Model):
#     __tablename__ = "course_review_stats"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     course_id = db.Column(db.String(100), nullable=False, unique=True)
#     easy_count = db.Column(db.Integer, default=0)
#     medium_count = db.Column(db.Integer, default=0)
#     hard_count = db.Column(db.Integer, default=0)
#     homework_less = db.Column(db.Integer, default=0)
#     homework_medium = db.Column(db.Integer, default=0)
#     homework_more = db.Column(db.Integer, default=0)
#     grading_low = db.Column(db.Integer, default=0)
#     grading_medium = db.Column(db.Integer, default=0)
#     grading_high = db.Column(db.Integer, default=0)
#     harvest_low = db.Column(db.Integer, default=0)
#     harvest_medium = db.Column(db.Integer, default=0)
#     harvest_high = db.Column(db.Integer, default=0)

