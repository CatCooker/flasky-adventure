# defines the Flask application
# includes a few tasks that help manage the application
import os
from app import create_app,db
from app.models import User,Garbage,GarbageType
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app,db)

@app.shell_context_processor  #防止每次使用数据库时都要import，节省时间
def make_shell_context():
    return dict(db=db,User=User,Garbage=Garbage,GarbageType=GarbageType)