import copy
import os
import time

import numpy as np

from Class.Class_Course import Course
from Tool.Tool_Plan2Excel import write_schedule_scheme_to_excel
from Tool.Tool_EncrytExcel import read_encrypt_excel
from Tool.TempTool.Key_Info import excel_password


class Scheduler:
    used_time: np.ndarray
    name: str
    course_keywords: list  # 课程关键词,用来查询excel表格
    concrete_course: dict  # key: 课程关键词，value: Course对象列表
    schedule_scheme: list  # 排课方案，每个元素是一个Course列表，代表一种排课方案

    exclude_time: dict  # 排除的时间段

    def __init__(self, name, course_keywords, bad_keywords, student_type='本', excel_path="./Excel/ClassTable.xlsx"):

        self.name = name
        self.course_keywords = course_keywords
        self.bad_keywords = bad_keywords
        self.student_type = student_type
        self.used_time = np.zeros((14, 6), dtype=np.int8)

        self.excel_path = excel_path
        self.find_course()

        self.schedule_scheme = []

    def schedule_class(self, excluded_time: dict = {}) -> int:
        """
        开始排课
        要求如下，每个关键词的课程都必须有一个课程被排上，所有课不能有冲突

        :return:
        返回排课方案的数量
        """
        self.exclude_time = excluded_time

        # 检查是否每个关键词都有课程，打印出所有没有课程的关键词
        useless_keywords = []
        for keyword in self.course_keywords:
            if len(self.concrete_course[keyword]) == 0:
                print(f'关键词{keyword}没有课程')
                useless_keywords.append(keyword)
        if len(useless_keywords) > 0:
            return []

        # 将需要排除的时间段在used_time中标记为1
        for key in excluded_time:
            if '点' in key:
                hours = excluded_time[key]
                for weekday, period in hours:
                    self.used_time[weekday - 1, period - 1] = 1
                    self.used_time[weekday + 6, period - 1] = 1
            elif '星期' in key:
                weekdays = excluded_time[key]
                for weekday in weekdays:
                    self.used_time[weekday - 1] = 1
                    self.used_time[weekday + 6] = 1
            elif '节' in key:
                periods = excluded_time[key]
                for period in periods:
                    self.used_time[:, period - 1] = 1

        temp_concrete_course = self.concrete_course
        # 将直接冲突的课程排除掉
        to_remove = []
        for keyword in temp_concrete_course:
            for course in temp_concrete_course[keyword]:
                if self.is_conflict(course) or len(course.time) == 0:
                    to_remove.append(course)
                    print(course)
            for course in to_remove:
                temp_concrete_course[keyword].remove(course)
            to_remove = []
        # self.print_concrete_course()
        # self.concrete_course, temp_concrete_course = temp_concrete_course, self.concrete_course

        start = time.time()
        # 递归排课
        # 先将关键词按照他们的课程数量排序，数量少的排前面，这样可以减少递归次数
        # self.course_keywords.sort(key=lambda x: len(self.concrete_course[x]))
        print(f'\n正在用力排课中，请稍等......')
        self.existing_thread = False
        self.schedule_scheme = self.recursive_schedule_class()
        # self.concrete_course, temp_concrete_course = temp_concrete_course, self.concrete_course
        # self.print_concrete_course()
        # self.iterate_schedule_class()
        self.existing_thread = False
        print(f'共找到{len(self.schedule_scheme)}种排课方案, 总耗时：{time.time() - start}秒')
        # 打印排课方案
        # self.print_schedule_scheme()
        return len(self.schedule_scheme)

    def iterate_schedule_class(self):
        """
        TODO:
        迭代排课
        判定方法是将所有课程的np_time相加，如果有大于1的元素，则说明有冲突
        :return:
        """

        # 单独开一个线程，每隔五秒观测一下self.schedule_scheme的长度
        def print_result_len():
            start = time.time()
            while True and self.existing_thread:
                if time.time() - start > 5:
                    print(f'过了{time.time() - start}秒，已找到{len(self.schedule_scheme)}种排课方案')
                time.sleep(5)

        if not self.existing_thread:
            self.existing_thread = True
            import threading
            t = threading.Thread(target=print_result_len)
            t.start()

        choose_index = [0] * len(self.course_keywords)
        course_list = []
        while True:
            self.used_time = np.zeros((14, 6), dtype=np.int8)
            for index, keyword in enumerate(self.course_keywords):
                course = self.concrete_course[keyword][choose_index[index]]
                course_list.append(course)
                self.used_time += course.np_time
            if np.any(self.used_time > 1):
                course_list = []
                choose_index[0] += 1
                for i in range(len(choose_index)):
                    if choose_index[i] == len(self.concrete_course[self.course_keywords[i]]):
                        choose_index[i] = 0
                        choose_index[i + 1] += 1
                    else:
                        break
                if choose_index[-1] == len(self.concrete_course[self.course_keywords[-1]]):
                    break
            else:
                self.schedule_scheme.append(copy.copy(course_list))
                course_list = []
                choose_index[0] += 1
                for i in range(len(choose_index)):
                    if choose_index[i] == len(self.concrete_course[self.course_keywords[i]]):
                        choose_index[i] = 0
                        choose_index[i + 1] += 1
                    else:
                        break
                if choose_index[-1] == len(self.concrete_course[self.course_keywords[-1]]):
                    break

    def schedule2excel(self):
        """
        将排课方案写入Excel
        :return:
        """
        time_date = time.strftime("%Y-%m-%d", time.localtime())+'_'+self.name
        time_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        # 判断Output文件夹是否存在，不存在则创建
        if not os.path.exists('./Output'):
            os.mkdir('./Output')
        # 如果对应日期的文件夹不存在，则创建
        if not os.path.exists(f'./Output/{time_date}'):
            os.mkdir(f'./Output/{time_date}')

        output_excel_path = f"./Output/{time_date}/{self.name}.{len(self.schedule_scheme)}.{time_str}.xlsx"
        if len(self.schedule_scheme) == 0:
            print("没有找到排课方案")
            return
        start = time.time()
        write_schedule_scheme_to_excel(self, output_excel_path)
        print(f'写入Excel耗时：{time.time() - start}秒')

    def print_schedule_scheme(self):
        """
        打印排课方案
        :return:
        """
        if len(self.schedule_scheme) == 0:
            print("没有找到排课方案")
            return
        for index, scheme in enumerate(self.schedule_scheme):
            print(f'方案{index + 1}')
            for course in scheme:
                print(course)

    def recursive_schedule_class(self, index=0, course_list=[]):
        """
        递归排课
        :param index:
        :param course_list:
        :return:
        """

        if index == len(self.course_keywords):
            return [copy.copy(course_list)]
        else:
            result = []

            # 单独开一个线程，每隔五秒观测一下result的长度
            # def print_result_len():
            #     start = time.time()
            #     while True and self.existing_thread:
            #         if time.time() - start > 5:
            #             print(f'过了{int(time.time() - start)}秒, 正在持续用力......')
            #         time.sleep(5)
            #
            # if not self.existing_thread:
            #     self.existing_thread = True
            #     t = threading.Thread(target=print_result_len)
            #     t.start()

            for course in self.concrete_course[self.course_keywords[index]]:
                if len(course.time) == 0:
                    continue
                if self.add_course(course):
                    course_list.append(course)
                    result += self.recursive_schedule_class(index + 1, course_list)
                    self.remove_course(course)
                    course_list.remove(course)
            return result

    def add_course(self, course: Course):
        """
        添加课程,如果发现冲突，返回False
        :param course:
        :return:
        """
        if self.is_conflict(course):
            return False
        else:
            self.used_time += course.np_time
            return True

    def remove_course(self, course: Course):
        """
        移除课程
        :param course:
        :return:
        """
        self.used_time -= course.np_time

    def is_conflict(self, course: Course):
        """
        判断是否冲突
        :param course:
        :return:
        """
        return np.any(self.used_time & course.np_time)

    def find_course(self):
        start = time.time()
        self.concrete_course = {}
        try:
            # df = pd.read_excel(self.excel_path)
            df = read_encrypt_excel(self.excel_path, excel_password)
        except FileNotFoundError:
            print(f'没有找到{self.excel_path}文件，请检查文件路径是否正确')
            return
        for keyword in self.course_keywords:
            self.concrete_course[keyword] = []
            relevant_rows = df[df.iloc[:, 2].str.contains(keyword) | df.iloc[:, 0].str.contains(keyword) | df.iloc[:, 3].str.contains(keyword)]
            for index, row in relevant_rows.iterrows():
                if any([(badword in row.iloc[0] or badword in row.iloc[2]) for badword in
                        self.bad_keywords]):  # 课程名称中包含不想上的课程
                    continue
                if row.iloc[1] not in self.student_type:  # 本科生或者研究生
                    continue
                if not isinstance(row["上课信息"], str):  # 上课信息为空的课程直接跳过
                    print(f'教学班：{row["教学班"]} 上课信息：{row["上课信息"]}')
                    continue
                course = Course(row)
                self.concrete_course[keyword].append(course)

            # 排除掉总课程，就是每被分组的课，这些课只有大课的时间，没有实验课的时间，所以不需要。他们的特征是，他们的教学班字符串会全部出现在其他课程的教学班字符串中。例如：计算机程序设计基础-01班-双语，计算机程序设计基础-01班-双语-2组
            for course in self.concrete_course[keyword]:
                for other_course in self.concrete_course[keyword]:
                    if course.name in other_course.name and course.name != other_course.name:
                        self.concrete_course[keyword].remove(course)
                        break
        self.print_concrete_course()
        print(f'\n查找课程耗时：{time.time() - start}秒')

    def print_concrete_course(self):
        for keyword in self.concrete_course:
            print(f'\n关键词：{keyword}')
            for course in self.concrete_course[keyword]:
                # print(course)
                all_info = course.all_info
                print(all_info['教学班'], '    ',all_info['课程名称'])
            print(f'共{len(self.concrete_course[keyword])}门课程')

    def get_concrete_course_info(self) -> dict:
        course_info = {}
        for keyword in self.concrete_course:
            course_info[keyword] = []
            for course in self.concrete_course[keyword]:
                all_info = course.all_info
                course_info[keyword].append(all_info['教学班'])

        return course_info

    def get_selected_course_info(self) -> dict:
        course_info = {}
        for keyword in self.concrete_course:
            course_info[keyword] = []
            for course in self.concrete_course[keyword]:
                # 判断course是否在排课方案中
                if any([course in c for c in self.schedule_scheme]):
                    all_info = course.all_info['教学班']
                    code = course.all_info['课程代码']
                    course_info[keyword].append(f'{code} {all_info} {course.time}')

        return course_info

    def get_schdule_scheme_info(self) -> dict:
        course_info = {}
        for index, scheme in enumerate(self.schedule_scheme):
            course_info[index] = []
            for course in scheme:
                all_info = course.all_info
                course_info[index].append({
                    "教学班": all_info['教学班'],
                    "上课时间": course.time,
                    "学分": all_info['学分']
                })

        return course_info