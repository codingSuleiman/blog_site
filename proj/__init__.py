from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session 

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
Session(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
app.app_context().push()

from proj import routes
