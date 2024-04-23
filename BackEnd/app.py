from assistant_models import app, db, Student, StudentInfo
from routes import *
from general_routes import *
from courserc_routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=5050)
