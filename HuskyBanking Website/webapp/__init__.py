from flask import Flask
import os
from threading import Lock
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = "cDGGHimMBD5wOMuIpb9IkJ2BTystAjBy"
csrf = CSRFProtect(app)
csrf.init_app(app)



#Allows Cross Origin requests
# cors = CORS(app, supports_credentials=True, origins="http://127.0.0.1:3030") #https://flask-cors.readthedocs.io/en/latest/api.html

app.config["WTF_CSRF_ENABLED"] = True

#################################
## Constants used in all files ##
#################################

lab_4 = False #This boolean controls whether the Lab 4 vulnerabilites, or Lab 6 vulnerabilites are present
transferLock = Lock()

cwd = os.getcwd()
sep = os.sep

from webapp import routes