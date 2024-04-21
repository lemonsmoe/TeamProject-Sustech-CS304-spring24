"""
这个类用来处理全校课表的数据
要实现这些功能：
1. 读取加密好的encrypted文件， 具体实现方法参考Tool/TableEncry.py
2. 从网上请求最新的课表数据 具体实现方法参考Tool/Tool_RequestJson.py
3. 将课表数据保存到encrypted文件中
"""
from Tool.Tool_RequestJson import get_Course_json, analyze_Course_json
class Asset:
    def __init__(self):
        pass