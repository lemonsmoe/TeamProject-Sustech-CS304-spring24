from flask import jsonify, request, session
from datetime import datetime
from models_wholeProject import app, db, Student

@app.route("/index")
@app.route("/hello")
def hello_world():
    return "hello world"

@app.route("/")
def hello_pzs():
    return "Openzishen!!!!!!!!!!"
