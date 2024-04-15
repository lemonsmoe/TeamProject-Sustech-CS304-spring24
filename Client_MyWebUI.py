import threading
import time
from flask import Flask, request, jsonify, render_template
from Client_scheduleCourse import Client_Schedule
import sys
import os


if getattr(sys, 'frozen', False):
    # The application is frozen (i.e., it is running in a bundled PyInstaller environment)
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
else:
    # The application is not frozen
    template_folder = './WebUI/templates'
    static_folder = './WebUI/static'

app = Flask(__name__, static_url_path='', static_folder=static_folder, template_folder=template_folder)
from flask_cors import CORS

CORS(app)  # 启用跨域支持，允许所有源

def print_info():
    print()
    print('-' * 50)
    print('请在浏览器中打开 http://127.0.0.1:5000 查看网页')
    print('在网页中输入必要信息后，点击确认按钮，即可开始选课')
    print('-' * 50)

@app.route('/')
def home():
    return render_template('UI.html')

@app.route('/timetable', methods=['GET'])
def timetable():
    return render_template('timetable.html')

@app.route('/get_scheme', methods=['post'])
def get_scheme():
    return jsonify(scheduler.get_schdule_scheme_info())

@app.route('/submit_data', methods=['POST'])
def handle_submission():
    data = request.get_json()
    # 逻辑处理数据和调用选课程序
    # 将data['keywords']列表中的空字符串去掉
    data['keywords'] = list(filter(lambda x: x != '', data['keywords']))
    data['keywords'] = list(filter(lambda x: x != '-', data['keywords']))
    data['badwords'] = list(filter(lambda x: x != '', data['badwords']))
    # print(data)
    # 单独开一个线程运行选课程序
    # def run_schedule():
    global scheduler
    scheduler = Client_Schedule(data=data)
    print_info()


    # threading.Thread(target=run_schedule).start()
    if scheduler is None:
        response = {'status': 'fail'}
        return jsonify(response)
    else:
        print(scheduler.get_selected_course_info())
        response = {'status': 'success',
        "solution_count": len(scheduler.schedule_scheme),
        "info": scheduler.get_selected_course_info(),
        "schedule_scheme": scheduler.get_schdule_scheme_info()}
        return jsonify(response)

@app.route('/build_excel', methods=['POST'])
def build_excel():
    print('正在生成Excel文件')

    # thread = threading.Thread(target=run_print_dot)
    # thread.start()
    scheduler.schedule2excel()
    response = {'status': 'success'}
    # 销毁线程
    # thread.join()
    return jsonify(response)

@app.route('/api', methods=['POST'])
def dispatch():
    # 获取发来的json数据
    data = request.get_json()
    method = data['method']
    
    print(data)
    return jsonify(data)

if __name__ == '__main__':
    print_info()

    app.run(debug=False,port=1314)


# {'password': 'my father is YHT', 'student_name': '', 'keywords': ['系统', '视觉'], 'badwords': [''], 'excluded_time': {'点': []}}