import requests
import json
import enum
import os

from Tool.Tool_NewCookie import get_new_Cookie
from bs4 import BeautifulSoup

semester_dict = {'秋季学期': '1', '春季学期': '2', '夏季学期': '3'}
# 创建一个枚举类，用于表示学期
class Semester(enum.Enum):
    Autumn = '1'
    Spring = '2'
    Summer = '3'

def get_Course_json(year: int, sem: Semester):
    """
    获取课程信息的json文件
    :param year: 学年
    :param sem:  学期
    :return:
    """

    if not os.path.exists('CourseData'):
        os.mkdir('CourseData')

    try:
        with open('../CourseData/cookies.json', 'r', encoding='utf-8') as f:
            cookies = json.load(f)
            COOKIE_list = [f'{key}={value}' for key, value in cookies.items()]
            COOKIE = '; '.join(COOKIE_list)
    except FileNotFoundError:
        print("未找到cookies.json文件，正在重新获取cookies")
        get_new_Cookie()
        return get_Course_json(year, sem)



    a_year = 0
    b_year = 0
    if sem == Semester.Autumn:
        a_year = year
        b_year = year + 1
    elif sem == Semester.Spring or sem == Semester.Summer:
        a_year = year - 1
        b_year = year
    else:
        print("学期输入错误")
        return

    url = "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": COOKIE,
        "Origin": "https://tis.sustech.edu.cn",
        "Referer": "https://tis.sustech.edu.cn/Xsxktz/queryRwxxcxList/3",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-gpc": "1",
    }

    data = {
        "p_chapylx": "",
        "ordertext_0": "",
        "p_xn": f"{a_year}-{b_year}",
        "p_xq": f"{sem.value}",
        "p_xnxq": f"{a_year}-{b_year}{sem.value}",
        "p_gjz": "",
        "p_xiaoqu": "",
        "p_kkyx": "",
        "p_rwlx": "",
        "p_kclb": "",
        "p_kcxz": "",
        "p_chaxungjz": "",
        "p_chaxunxiaoqu": "",
        "p_chaxunkkyx": "",
        "p_chaxunnj": "",
        "p_chaxunglyx": "",
        "p_chaxunzy": "",
        "p_chaxunxdm": "",
        "p_chaxunpylx": "3",
        "mxpylx": "3",
        "p_id": "",
        "p_sfhltsxx": "0",
        "file": "",
        "pageNum": "1",
        "pageSize": "2000",
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Check if the request was successful

        # 将返回的json数据写入文件
        with open(f'CourseData/{year}{sem.name}.json', 'w', encoding='utf-8') as f:
            f.write(response.text)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        get_new_Cookie()
        return get_Course_json(year, sem)

def parse_kcxx(kcxx: str) -> str:
    soup = BeautifulSoup(kcxx, 'html.parser')
    return '\n'.join(soup.stripped_strings)

def analyze_Course_json(year: int, sem: Semester) -> (list, list):
    """
    解析课程信息的json文件
    :param year:
    :param sem:
    :return:
    """
    with open(f'CourseData/{year}{sem.name}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    course_rows = data['rwList']['list']
    print(f'共有{len(course_rows)}门课程')
    all_info = []
    for course in course_rows:
        name = course['rwmc'] # 教学班
        pylx = '本' if course['pylx'] == '1' else '研' if course['pylx'] == '2' else '其他'
        kcdm = course['kcdm'] # 课程代码
        kcmc = course['kcmc'] # 课程名称
        kcxzmc = course['kcxzmc'] # 课程性质
        kclbmc = course['kclbmc'] # 课程类别
        skyymc = course['skyymc'] # 授课语言
        xf = course['xf'] # 学分
        zxs = course['zxs'] # 学时
        kcxx = course['kcxx'] # 上课信息

        kcxx = parse_kcxx(kcxx)

        mxdx = course['mxdx'] # 面向对象
        xzdx = None # 限制对象
        bksrl_yx = f"{course['bksrl']}/{course['bksyxrs']}" # 本科生容量/已选
        yjsrl_yx = f"{course['yjsrl']}/{course['yjsyxrs']}" # 研究生容量/已选
        kkyxmc = course['kkyxmc'] # 开课院系

        all_info.append([name, pylx, kcdm, kcmc, kcxzmc, kclbmc, skyymc, xf, zxs, kcxx, mxdx, xzdx, bksrl_yx, yjsrl_yx, kkyxmc])

        total_number = course['zrl'] # 课程容量人数
        b_total_number = course['bksrl'] # 本科生容量人数
        y_total_number = course['yjsrl'] # 研究生容量人数
        yx_number = course['yxzrs'] # 有效总人数
        b_yx_number = course['bksyxrs'] # 本科生有效人数
        y_yx_number = course['yjsyxrs'] # 研究生有效人数
        nans_yx_number = course['nansyxrs']
        nvs_yx_number = course['nvsyxrs']
        girl_rate = int(nvs_yx_number) / int(yx_number) if int(yx_number) != 0 else 0

        all_info[-1].append(girl_rate)
        # print(f'课程名称：{name} 培养类型：{pylx} 总人数：{total_number} 有效总人数：{yx_number} 男生有效人数：{nans_yx_number} 女生有效人数：{nvs_yx_number} 女生比例：{girl_rate}')
    #     all_info.append([name, yx_number, nvs_yx_number, girl_rate])
    #
    # all_info.sort(key=lambda x: x[3], reverse=True)
    # # print(all_info)
    # for course in [x for x in all_info if float(x[3]) > 0.5 and int(x[1]) >= 15]:
    #     print(f'课程名称：{course[0]} 有效总人数：{course[1]} 女生有效人数：{course[2]} 女生比例：{course[3]}')
    headers = ['教学班', '培养类型', '课程代码', '课程名称', '课程性质', '课程类别', '授课语言', '学分', '学时', '上课信息', '面向对象', '限制对象', '本科生容量/已选', '研究生容量/已选', '开课院系', '女生比例']
    return all_info, headers

def main():
    # route, jsessionid = '02a1344e82a4379f520dd2ee82590745', '55CC801A27B6A78E7AC14F83D568E6D'
    # COOKIE = f"route={route}; JSESSIONID={jsessionid}"


    # if not get_Course_json(2024, Semester.Spring):
    #     print("获取课程信息失败")
    #     return main()
    # else:
    #     print("获取课程信息成功")
    #     return
    analyze_Course_json(2024, Semester.Spring)
    # print(Semester.Autumn.value)

if __name__ == '__main__':
    main()