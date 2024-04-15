'''
pyinstaller --onefile --name=CourseUR --workpath=./Builds --distpath=./Builds --icon=./Builds/img/yz1.ico --add-data "dist;CourseData" --add-data "WebUI/templates;templates" --add-data "WebUI/static;static" .\Client_MyWebUI.py
'''

# 你可以使用Python的`subprocess`模块来执行shell命令。下面是一个简单的脚本，它将把你的PyInstaller命令执行起来：
#
# ```python
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

# 运行命令
subprocess.run(" ".join(pyinstaller_command), shell=True)
# ```
#
# 请注意，在Windows中，默认的shell分隔符是`;`，在Unix-like系统（Linux和macOS）中，则是`:`。 这段代码会自动根据你的操作系统选择正确的分隔符。
#
# 在上面的脚本中，资源目录参数是作为一个列表来拎出来的，你可以很容易地修改它并追加新的资源文件夹对。然后这些资源目录参数会被添加到生成的PyInstaller命令行中。
#
# 请确保将这个脚本保存在与你的`Client_MyWebUI.py`文件相同的目录中，并且运行这个脚本的Python环境中已经安装了PyInstaller。
#
# 运行这个脚本将会创建一个单文件的可执行程序，并将其放在`./Builds`目录下。如果你打算经常执行这个过程，将它写成Python脚本会更方便快捷。

