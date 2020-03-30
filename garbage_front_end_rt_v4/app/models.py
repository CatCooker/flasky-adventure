from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %r>' % self.username


"""
------垃圾类别------
分为四类 0 1 2 3
0是可回收垃圾 1是厨余垃圾 2是有害垃圾 3是其他垃圾
"""


class GarbageType(db.Model):
    __tablename__="garbagetype"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, unique=True)
    _class = db.Column(db.String(64),unique=True)
    def __repr__(self):
        return '<class %r>' % self._class
    garbages = db.relationship('Garbage', backref='gtype')


class Garbage(db.Model):
    __tablename__ = 'garbages'
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(64),unique=True,index=True)
    type_id = db.Column(db.Integer, db.ForeignKey('garbagetype.id'))