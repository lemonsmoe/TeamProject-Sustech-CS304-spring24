from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# import pymysql
from datetime import datetime
from sqlalchemy import text

app = Flask(__name__)
from flask_cors import CORS
CORS(app)
app_ctx = app.app_context()
app_ctx.push()
# app.config["SQLALCHEMY_DATABASE_URI"] = (
    # "mysql+pymysql://root:81991889@127.0.0.1:3306/seproject"
# )

fk_command = text("PRAGMA foreign_keys = ON;")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "./seproject.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jjjsks"

db = SQLAlchemy(app)  # 实例化的数据库


# 学生登录信息表
class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.String(16), nullable=False, unique=True, primary_key=True)  # 学号，唯一标识
    password = db.Column(db.String(64), nullable=False)  # 登录密码
    last_login_time = db.Column(db.DateTime, default=datetime.now)  # 上次登录时间
    
# 给选课系统使用的表，兴趣爱好等
class StudentInfo(db.Model):
    __tablename__ = "student_info"
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"), primary_key=True)  # 学号，唯一标识
    grade = db.Column(db.String(16), nullable=False)  # 年级
    major = db.Column(db.String(64), nullable=False)  # 专业
    hobbies = db.Column(db.String(256))  # 兴趣爱好，以字符串形式存储，可以是逗号分隔的多个兴趣爱好

# 日历功能需要的DDL表
class DDL(db.Model):
    __tablename__ = "ddl"
    ddl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"), nullable=True)
    course_id = db.Column(db.String(16), nullable=True)
    ddl_time = db.Column(db.DateTime, nullable=False)
    ddl_content = db.Column(db.String(256), nullable=False)
    ddl_status = db.Column(db.String(16), nullable=True)

### 辅导老师信息表 (tutors)
class Tutor(db.Model):
    __tablename__ = "tutors"
    tutor_id = db.Column(db.String(16), primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(128), nullable=False)

### 学生的预约信息表 (appointments)
class Appointment(db.Model):
    __tablename__ = "appointments"
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"), nullable=False)
    tutor_id = db.Column(db.String(16), db.ForeignKey("tutors.tutor_id"), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    help_needed = db.Column(db.String(256), nullable=False)

### 公开习题课信息表 (workshops)
class Workshop(db.Model):
    __tablename__ = "workshops"
    workshop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    tutor_id = db.Column(db.String(16), db.ForeignKey("tutors.tutor_id"), nullable=False)

# 初始化数据库表
def init_db():
    # db.drop_all()
    db.create_all()

# 初始化数据库信息
def init_student_data():
    # 初始化一些学生数据
    students = [
        {
            "student_id": "12111728",
            "password": "123456",
            "last_login_time": datetime.now()
        },
        {
            "student_id": "12111713",
            "password": "123456",
            "last_login_time": datetime.now()
        },
        {
            "student_id": "12110323",
            "password": "123456",
            "last_login_time": datetime.now()
         }
    ]

    # 将学生数据插入到数据库中
    for student_data in students:
        student = Student(**student_data)
        db.session.add(student)
    
    # 提交更改
    db.session.commit()
# 删除当前数据库所有表
def drop_all_tables():
    # 获取当前数据库引擎
    engine = db.engine

    # 创建一个数据库连接
    conn = engine.connect()

    # 开始事务
    trans = conn.begin()

    try:
        # 构造 SQL 指令，获取当前数据库中所有表的名称
        sql = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'seproject'")

        # 执行 SQL 查询
        result = conn.execute(sql)

        # 获取所有表的名称
        table_names = [row[0] for row in result]

        # 构造删除表的 SQL 指令，并执行
        for table_name in table_names:
            drop_sql = text(f"DROP TABLE IF EXISTS {table_name} CASCADE")
            conn.execute(drop_sql)

        # 提交事务
        trans.commit()
        print("所有表已成功删除")
    except Exception as e:
        # 发生异常时回滚事务
        trans.rollback()
        print("删除表时发生异常：", e)
    finally:
        # 关闭数据库连接
        conn.close()


if __name__ == '__main__':
    init_db()
    # 调用初始化函数，初始化学生数据
    # init_student_data()