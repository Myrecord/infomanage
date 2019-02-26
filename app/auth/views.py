# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template,redirect,url_for
from . import auth
from flask import request,flash
from ..models import User
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.status and request.blueprint != 'auth' and request.endpoint and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirm'))

@auth.route('/unconfirm')
def unconfirm():
    if current_user.status:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.html')


@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template('auth/page-login.html')

@auth.route('/login_data',methods=['GET','POST'])
def login_data():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            user = User.query.filter_by(username=username).first()
            if user is not None and user.verify_passwd(password):
                login_user(user)
                return redirect(url_for('main.index'))
            else:
                flash('Error:密码错误.')
        else:
            flash('Error:用户名不存在.')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register',methods=['GET','POST'])
def register():
    username = request.form.get('username')
    passwds = request.form.get('password')
    passwds_confirm = request.form.get('confirm_password')
    email = request.form.get('email')
    if passwds == passwds_confirm:
        if not User.query.filter_by(email=email).first():
            if not User.query.filter_by(username=username).first():
                if request.method == 'POST':
                    try:
                        new_user = User(username=request.form.get('username'),email=request.form.get('email'),password=request.form.get('confirm_password'))
                        db.session.add(new_user)
                        db.session.commit()
                        token = new_user.tokens()
                        login_user(new_user)
                        send_email(new_user.email, 'Confirm Your Account', 'auth/email/confirm', user=new_user,token=token)
                    except Exception as e:
                        db.session.rollback()
                    return  redirect(url_for('main.index'))
            else:
                flash('Error:用户名已被注册.')
        else:
            flash('Error: 邮箱已被注册.')
    else:
        flash('Error: 两次输入密码不相同.')
    return render_template('auth/page-register.html')

@auth.route('/confirm/<token>')    
@login_required
def confirm(token):
    if current_user.status:
        return redirect(url_for('main.index'))
    if current_user.loosen_tokens(token):
        db.session.commit()
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))
0
@auth.route('/confirm')
@login_required
def resend_confirm():
    tokens = current_user.tokens()
    send_email(current_user.email, 'Confirm Your Account','auth/email/confirm', user=current_user, token=tokens)  
    flash('认证邮件已从新发送.')
    return redirect(url_for('main.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def reset_request():
    return render_template('auth/page-forgat.html')


@auth.route('/reset_data',methods=['GET','POST'])
def reset_data():
    username = request.form.get('username')
    email = request.form.get('email')
    if User.query.filter_by(username=username).first():
        if User.query.filter_by(email=email).first():
            if request.method == 'POST':
                user = User.query.filter_by(username=username,email=email).first()
                send_email(user.email, 'Confirm Your Account','auth/email/reset_passwd', user=user, token=user.tokens())
                flash('重置密码邮件已发送至你的邮箱')
                return redirect(url_for('auth.login'))
        else:
            flash('Error:邮箱地址不存在.')
    else:
        flash('Error:用户名不存在.')
    return render_template('auth/page-forgat.html')

@auth.route('/reset_passwd/<token>',methods=['GET','POST'])
def reset_passwd(token):
    if request.method == 'POST':
        passwd = request.form.get('passwords')
        passwd_confirm = request.form.get('confirm_password')
        if passwd == passwd_confirm:
            if User.reset_passwd_tokens(token,passwd_confirm):
                db.session.commit()
                flash('密码已重置.')
                return redirect(url_for('auth.login'))
        else:
            flash('Error: 两次输入密码不一样')
    return render_template('auth/page-setpasswd.html')

