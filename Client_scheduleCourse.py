import json
import time

from Class.Class_Scheduler import Scheduler
from Tool.Tool_ClientAu import handle_authorization

student_name = "hqc"
keywords = ["软件工程", "计算机操作系统", "创新实践II-01班", "人工智能", "计算机网络"]
student_type = ["本", "研"][0]

import sys
import os

if getattr(sys, 'frozen', False):
    # The application is frozen (i.e., it is running in a bundled PyInstaller environment)
    excel_folder = os.path.join(sys._MEIPASS, 'CourseData')
else:
    # The application is not frozen
    excel_folder = './CourseData/'


def Client_Schedule(input_path='Input/input.json', data: dict = None):
    # 打开Input文件夹下的input.json文件，读取学生姓名、关键词、学生类型
    if data is None:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    # 判断是否有权限使用本程序
    if not handle_authorization(data['password']):
        return


    student_name = data['student_name']
    keywords = data['keywords']
    badwords = data['badwords']
    student_type = data.get('student_type', '本')
    excluded_time = data['excluded_time']

    excel_path = data.get('excel_path', os.path.join(excel_folder, '2024Spring.xlsx'))

    if len(keywords) == 0:
        print("选课关键词不能为空")
        return

    scheduler = Scheduler(student_name, keywords, badwords, student_type, excel_path=excel_path)

    # 开始计算排课方案
    scheduler.schedule_class(excluded_time=excluded_time)

    return scheduler


if __name__ == '__main__':

    try:
        Client_Schedule()
    except Exception as e:
        print(e)
        print("程序出错了，怪我咯")

    time.sleep(60)
