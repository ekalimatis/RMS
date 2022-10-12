from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from rms.db import db
from rms.user.models import User
from rms.user.forms import LoginForm, UserCreationForm
from rms.user.decorators import admin_required
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


@blueprint.route("/logout")
def logout():
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("user.login"))


@blueprint.route("/create")
@admin_required
def create():
    title = "Cоздание нового пользователя"
    create_form = UserCreationForm()
    return render_template("user/create.html",
                           page_title = title,
                           form = create_form)


@blueprint.route("/process-create", methods=['POST'])
@admin_required
def process_create():
    create_form = UserCreationForm()
    if create_form.validate_on_submit():
        new_user = User(username=create_form.username.data,
                        role=create_form.user_role.data)
        new_user.set_password(create_form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Создан пользователь {create_form.username.data}, c ролью {create_form.user_role.data}")
        return redirect(url_for('user.create'))
    else:
        for field, errors in create_form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(create_form, field).label.text,error
                ))
        return redirect(url_for('user.create'))