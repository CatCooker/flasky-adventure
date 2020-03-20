from flask import render_template,session,redirect,url_for
from . import main #main 是一个bluePrint

@main.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
