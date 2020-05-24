import os

from flask import Flask


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists


from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_mail import Mail

app = Flask(__name__)


app.config['SECRET_KEY'] = 'ba2f9e93b64d1bee714e83cc8a3e2636'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



# create database
db = SQLAlchemy(app)



bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# restrictred access to account - only for valid users not for guyest
login_manager.login_view = 'login_func'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)

from flaskapp import route_s
