from flask import jsonify, request, session
from flask import Flask, render_template_string
from datetime import datetime
from models_wholeProject import app, db, Student
import os
import importlib.util

@app.route("/index")
@app.route("/hello")
def hello_world():
    return "hello world"


def get_routes_info():
    routes_info = []
    current_directory = os.path.dirname(os.path.abspath(__file__))

    for filename in os.listdir(current_directory):
        if filename.startswith('routes') and filename.endswith('.py'):
            module_name = filename[:-3]  # 去掉 ".py" 后缀
            file_path = os.path.join(current_directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'app'):
                for rule in module.app.url_map.iter_rules():
                    routes_info.append({
                        'rule': rule.rule,
                        'endpoint': rule.endpoint,
                        'methods': list(rule.methods),
                    })

    return routes_info


@app.route("/")
def index():
    # routes_info = get_routes_info()
    # html = """
    # <!doctype html>
    # <html lang="en">
    #   <head>
    #     <meta charset="utf-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    #     <title>Routes Information</title>
    #   </head>
    #   <body>
    #     <h1>Routes Information</h1>
    #     <table border="1">
    #       <tr>
    #         <th>Rule</th>
    #         <th>Endpoint</th>
    #         <th>Methods</th>
    #       </tr>
    #       {% for route in routes_info %}
    #       <tr>
    #         <td>{{ route.rule }}</td>
    #         <td>{{ route.endpoint }}</td>
    #         <td>{{ route.methods }}</td>
    #       </tr>
    #       {% endfor %}
    #     </table>
    #   </body>
    # </html>
    # """
    # return render_template_string(html, routes_info=routes_info)
# def hello_pzs():

    # 扫描当前路径下带有routes_前缀的文件
    routes = [i for i in os.listdir() if i.startswith("routes_")]
    # 返回所有文件文本内容
    html_text = "瞎几把写的东西"
    for route in routes:
        with open(route, "r", encoding='utf-8') as f:
            contents = f.readlines()
            html_text += "<br>" + '<br><br>'.join(contents) + "<br>"
    return html_text

    
    return "这是Open籽肾的软工后端，请直接打开文件查阅相关API"
