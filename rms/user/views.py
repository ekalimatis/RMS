from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from rms.db import db
from rms.user.models import User
from rms.user.forms import LoginForm

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/index')
def index():
    #page_title = 'Пользовательский контент'
    return render_template("user/index.html")


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html',
                           page_title=title,
                           form=login_form)


@blueprint.route("/process-login", methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("вы успешно вошли")
            return redirect(url_for('user.index'))
    flash("Неправильный логин или пароль")
    return redirect(url_for('user.login'))


@blueprint.route("/unauthorized")
def unauthorized():
    return render_template('user/unauthorized.html')


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("user.login"))