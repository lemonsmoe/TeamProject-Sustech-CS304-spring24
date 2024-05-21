from models_wholeProject import app, db, Student, StudentInfo
from routes_temptest import *
from routes_general import *
from routes_courserc import *
from routes_calender import *
from routes_tutorial import *

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=5050)