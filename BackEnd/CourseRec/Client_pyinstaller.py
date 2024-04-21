'''
pyinstaller --onefile --name=CourseUR --workpath=./Builds --distpath=./Builds --icon=./Builds/img/yz1.ico --add-data "dist;CourseData" --add-data "WebUI/templates;templates" --add-data "WebUI/static;static" .\Client_MyWebUI.py
'''


import subprocess
import sys

# 资源目录参数
resources = [
    ("WebUI/templates", "templates"),
    ("WebUI/static", "static"),
]

# 将资源转换成PyInstaller所需要的格式
add_data = []
separator = ";" if sys.platform == "win32" else ":"
for source, target in resources:
    add_data.append(f"--add-data {source}{separator}{target}")

program_name = "ScheduleCourse"
icon_name = "yz1.ico"
python_file_name = "Client_MyWebUI.py"

# 构造PyInstaller命令
pyinstaller_command = [
    "pyinstaller",
    "--onefile",
    f"--name={program_name}",
    "--workpath=./Builds",
    "--distpath=./Builds",
    f"--icon=./Builds/img/{icon_name}",
] + add_data + [
    f"{python_file_name}"
]

subprocess.run(" ".join(pyinstaller_command), shell=True)