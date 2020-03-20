# stores the configuration settings
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a string'  # wtf 渲染form时需要使用
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MODEL_PATH = "app/static/model/shufflenet_50_1_lr0.003_k10.pth"
    SUPPORT_IMG = ['bmp','jpg','png','jpeg']
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'default':DevelopmentConfig
}
