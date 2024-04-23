from flask import jsonify, request, session
from datetime import datetime

from CourseRec.Client_scheduleCourse import Client_Schedule
from assistant_models import app, db, Student

@app.route('/courserc/submit_data', methods=['POST'])
def handle_submission():
    data = request.get_json()
    print(data)
    # 逻辑处理数据和调用选课程序
    # 将data['keywords']列表中的空字符串去掉
    data['keywords'] = list(filter(lambda x: x != '', data['keywords']))
    data['keywords'] = list(filter(lambda x: x != '-', data['keywords']))
    data['badwords'] = list(filter(lambda x: x != '', data['badwords']))
    global scheduler
    scheduler = Client_Schedule(data=data)
    # print_info()


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