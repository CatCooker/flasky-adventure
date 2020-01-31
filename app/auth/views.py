from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from ..models import User
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('pred.cam_or_file')
            return redirect(next)
        flash('邮箱或密码错误')
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user() # a function to remove and reset the user session
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET','POST'])
def register():
    reg_url = 'auth.register'
    if request.method == 'GET':
        return render_template('auth/register.html')
    if request.method == 'POST':
        new_user = User()
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        db_user = User.query.filter_by(username=username).first()
        db_email = User.query.filter_by(email=email).first()
        if db_user is not None:
            flash("用户名已存在！")
            return redirect(url_for(reg_url))
        if db_email is not None:
            flash("邮箱已被注册")
            return redirect(url_for(reg_url))
        if password != confirm_password:
            flash('两次密码输入不匹配')
            return redirect(url_for(reg_url))
        new_user.username = username
        new_user.email = email
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

