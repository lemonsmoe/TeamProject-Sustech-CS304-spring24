from models_wholeProject import app
from routes_temptest import *
from routes_general import app_general
from routes_courserc import app_courserc
from routes_forum import app_forum
from routes_tutorial import app_tutorial
from routes_calender import app_calender
from routes_evaluation import app_evaluation

app.register_blueprint(app_general)
app.register_blueprint(app_courserc)
app.register_blueprint(app_forum)
app.register_blueprint(app_tutorial)
app.register_blueprint(app_calender)
app.register_blueprint(app_evaluation)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=5050)