import re

import pandas as pd
from bs4 import BeautifulSoup
import os, sys

from Tool.Tool_EncrytExcel import pwd_xlsx
from Tool.TempTool.Key_Info import excel_password


def parse_html(file_path="./HTML/2024春课表.html") -> list:
    """
    解析网页，返回课程信息
    :param file_path:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        htmls = f.readlines()
    # 获取网页中的每一栏课程信息
    pattern_str = r'<tr class="ivu-table-row">(.*?)</tr>'
    pattern = re.compile(pattern_str, re.DOTALL)
    result = pattern.findall(''.join(htmls))
    print(f'共有{len(result)}门课程')

    # 解析每一栏课程信息，保存到 data 中
    course_data = []
    for html in result:
        soup = BeautifulSoup(html, 'html.parser')
        # 找到所有的 td 标签
        td_tags = soup.find_all('td')
        # 提取每个 td 标签内的文本内容
        content_list = ['\n'.join(td.stripped_strings) for td in td_tags]
        course_data.append(content_list)
        # print('-' * 20)

    return course_data



def build_excel(course_data: list, file_path, headers=None):
    """
    将课程信息保存到 Excel 文件中
    :param course_data:
    :param file_path:
    :return:
    """
    if headers is None:
        headers = ['教学班', '培养类型', '课程代码', '课程名称', '课程性质', '课程类别', '授课语言', '学分', '学时',
               '上课信息',
               '面向对象', '限制对象', '本科生容量/已选', '研究生容量/已选', '开课院系']
    df = pd.DataFrame(course_data, columns=headers)
    df.to_excel(file_path, index=False)

    # 获取两个文件的绝对路径
    old_filename = os.path.abspath(file_path)
    new_filename = os.path.abspath(file_path)
    pwd_str = excel_password
    print('加密中……')
    pwd_xlsx(old_filename, new_filename, pwd_str)


def main():
    course_data = parse_html()
    build_excel(course_data)


if __name__ == '__main__':
    # 重定向到文件
    sys.stdout = open('../Log/output.txt', 'w')
    main()
