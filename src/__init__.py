import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_misaka import Misaka


app = Flask(__name__)
md = Misaka(smartypants=True)
md.init_app(app)
Bootstrap(app)

app.config['SECRET_KEY'] = 'supersecretkey'

########### Database Config #########

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:cisco123@127.0.0.1/conclave'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

############ Login Config ############

login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'


from src.core.views import core
from src.users.views import users
from src.conclave.views import conclave

app.register_blueprint(core, url_prefix='')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(conclave, url_prefix='/conclave')
