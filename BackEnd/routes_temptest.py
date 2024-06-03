from flask import jsonify, request, session
from flask import Flask, render_template_string
from datetime import datetime
from models_wholeProject import app, db, Student
import os
import importlib.util

def connect_db(db_type='sqlite'):
    """
    连接数据库
    :param db_type: 数据库类型
    :return:
    """
    
    if db_type == 'sqlite':
        print("sqlite")
        import sqlite3
        con = sqlite3.connect('./instance/course.sqlite')
        cur = con.cursor()
    else:
        print("不支持的数据库类型")
        return
    
    return con, cur


@app.route("/hello")
def hello_world():
    return jsonify({'message': 'Hello, World!'})

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

@app.route('/')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        route_info = {
            'endpoint': rule.endpoint,
            'methods': methods,
            'url': rule.rule
        }
        routes.append(route_info)
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Routes</title>
    </head>
    <body>
        <h1>All Routes</h1>
        <table border="1">
            <tr>
                <th>Endpoint</th>
                <th>Methods</th>
                <th>URL</th>
            </tr>
            {% for route in routes %}
            <tr>
                <td>{{ route.endpoint }}</td>
                <td>{{ route.methods }}</td>
                <td>{{ route.url }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    
    return render_template_string(template, routes=routes)