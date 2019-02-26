from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
import flask_whooshalchemyplus 
from flask_apscheduler import APScheduler
from flask_sockets import Sockets

mail = Mail()
db = SQLAlchemy()
scheduler = APScheduler()
sockets = Sockets()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    flask_whooshalchemyplus.init_app(app) 
    login_manager.init_app(app)
    sockets.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app

