import re
import numpy as np

def remove_chinese(text):
    chinese_pattern = re.compile('[\u4e00-\u9fa5]')
    return re.sub(chinese_pattern, '', text)

def chinese_num_to_int(text):
    chinese_num = ['一', '二', '三', '四', '五', '六', '日']
    for i in range(len(chinese_num)):
        text = text.replace(chinese_num[i], str(i+1))
    return text

odd_week_str = ['1-', '3', '5', '7', '9', '11', '13', '15', '单', '1周', '2-16周']
even_week_str = ['2', '4', '6', '8', '10', '12', '14', '16', '双']
time_pattern = re.compile(r'(\d+(?:-\d+)?(?:,\d+(?:-\d+)?)?(?:单周|双周|周)?),星期(一|二|三|四|五|六|日)第(\d+)-(\d+)节')

class Course:
    name: str
    time: list # [[day, start, end, odd, even], ...]
    np_time: np.array #
    all_info: dict

    def __init__(self, course_row):
        """
        name: 课程名称
        time_info: 上课信息 
        eg: 刘南钦
            上课信息:
            1-16周,星期六第5-7节 商学院102
            选课要求:辅修课程
            
        通过正则表达式解析上课信息，得到上课时间
        """
        self.all_info = course_row
        self.name = course_row["教学班"]
        self.parse_time_info(course_row["上课信息"])
        self.generate_np_time()
        
    def parse_time_info(self, time_info):
        """
        解析上课信息，使用正则表达式，得到上课时间编码
        :param time_info:
        :return:
        """
        # print(time_info)
        matches = time_pattern.findall(time_info)
        all_time = {}
        for match in matches:
            time = ','.join(match[-3:])
            week = match[0]
            if time in all_time:
                all_time[time].append(week)
            else:
                all_time[time] = [week]
        
        
        time_json = all_time
        self.time = []
        for key in time_json:
            odd = False
            even = False
            for week in time_json[key]:
                if any(s in week for s in odd_week_str):
                    odd = True
                if any(s in week for s in even_week_str):
                    even = True
                    
            time_encode = chinese_num_to_int(key).split(',')
            time_encode += [odd, even]
            time_encode = [int(i) if type(i) == str else i for i in time_encode]
            time_encode[1] = (time_encode[1] + 1) // 2
            time_encode[2] = (time_encode[2] + 1) // 2
            self.time.append(time_encode)

    def generate_np_time(self):
        """
        生成 numpy 时间矩阵, 用于计算冲突
        大小是： 14 * 5 前7天代表单周，后7天代表双周，5代表一天5节课 1-2是第一节课，3-4是第二节课，以此类推
        :return:
        """
        self.np_time = np.zeros((14, 6), dtype=np.int8)
        # print(f'课程名称：{self.name}')
        for time in self.time:
            # print(time)
            day = int(time[0]) - 1
            start = int(time[1]) - 1
            end = int(time[2]) - 1
            odd = time[3]
            even = time[4]
            # print(f'课程名称：{self.name}，星期{day+1}，第{start+1}-{end+1}节，单周：{odd}，双周：{even}')
            for i in range(start, end+1):
                if odd:
                    self.np_time[day][i] = 1
                if even:
                    self.np_time[day+7][i] = 1

            
    def __str__(self):
        return self.name + ' ' + str(self.time)
            