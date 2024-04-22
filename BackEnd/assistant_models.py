from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# import pymysql

from datetime import datetime


app = Flask(__name__)
from flask_cors import CORS
CORS(app)
app_ctx = app.app_context()
app_ctx.push()
# app.config["SQLALCHEMY_DATABASE_URI"] = (
    # "mysql+pymysql://root:81991889@127.0.0.1:3306/seproject"
# )

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "./seproject.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jjjsks"

db = SQLAlchemy(app)  # 实例化的数据库

from sqlalchemy import text


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


from datetime import datetime

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.String(16), nullable=False, unique=True, primary_key=True)  # 学号，唯一标识
    password = db.Column(db.String(64), nullable=False)  # 登录密码
    last_login_time = db.Column(db.DateTime, default=datetime.now)  # 上次登录时间
    
class StudentInfo(db.Model):
    __tablename__ = "student_info"
    student_id = db.Column(db.String(16), db.ForeignKey("student.student_id"), primary_key=True)  # 学号，唯一标识
    grade = db.Column(db.String(16), nullable=False)  # 年级
    major = db.Column(db.String(64), nullable=False)  # 专业
    hobbies = db.Column(db.String(256))  # 兴趣爱好，以字符串形式存储，可以是逗号分隔的多个兴趣爱好



# 初始化数据库表
def init_db():
    # db.drop_all()
    db.create_all()


from datetime import datetime

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



if __name__ == '__main__':
    init_db()
    # 调用初始化函数，初始化学生数据
    init_student_data()