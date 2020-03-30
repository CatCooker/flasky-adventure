from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_bluprint
    app.register_blueprint(auth_bluprint,url_prefix='/auth')
    from .predict import pred as pred_bluprint
    app.register_blueprint(pred_bluprint,url_prefix='/pred')
    from .result import result as result_bluprint
    app.register_blueprint(result_bluprint,url_prefix='/result')
    from .model import model_info as model_bluprint
    app.register_blueprint(model_bluprint, url_prefix='/model')

    return app
