import os.path
import json

from Tool.Tool_NewCourseInfo import parse_html, build_excel
from Tool.Tool_RequestJson import get_Course_json, Semester, analyze_Course_json
from Tool.Tool_DataBase import insert_excel_data
def main():
    # with open('Input/input.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #     year = int(data['year'])
    #     sem = Semester[data['sem']]
    for year in range(2024, 2025):
        for sem in Semester:
            print(f"正在处理{year}年{sem.name}课程信息")
            get_Course_json(year, sem)
            course_data, headers = analyze_Course_json(year, sem)
            # os.remove(f'CourseData/{year}{sem.name}.json')
            build_excel(course_data, f"CourseData/{year}{sem.name}.xlsx", headers=headers)
            print(f'正在将{year}年{sem.name}课程信息插入数据库')
            insert_excel_data(f"CourseData/{year}{sem.name}.xlsx")

if __name__ == '__main__':
    main()