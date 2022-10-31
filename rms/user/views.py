from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

from rms.db import db
from rms.user.models import User
from rms.user.enums import Roles
from rms.requirements.models import AcceptRequirement, Requirement
from rms.user.forms import LoginForm, UserCreationForm, UserChangePasswordForm
from rms.user.decorators import admin_required
from rms.helpers.form_helpers import flash_form_errors
blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/index')
def index():
    return redirect(url_for('projects.list_projects'))


@blueprint.route('/profile', methods=['GET'])
@login_required
def get_profile():
    current_user_id = current_user.id
    #reqs_ids_to_accept = AcceptRequirement.query(AcceptRequirement.requirement_id)\
    #    .filter(AcceptRequirement.accept_user == current_user_id).all()
    #reqs_to_accept = Requirement.query.filter(Requirement.id in reqs_ids_to_accept)
    change_psw_form = UserChangePasswordForm()
    return render_template('user/profile.html', form=change_psw_form)


@blueprint.route("/process-password-change", methods=['POST'])
@login_required
def process_password_change():
    change_psw_form = UserChangePasswordForm()
    #user = User.query.filter(User.id == current_user.id).first()
    if change_psw_form.validate_on_submit():
        current_user.set_password(change_psw_form.password.data)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('user.get_profile'))
    else:
        flash_form_errors(change_psw_form)
        return redirect(url_for('user.get_profile'))




@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('projects.list_projects'))
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
            return redirect(url_for('projects.list_projects'))
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
    create_form = UserCreationForm(user_role=Roles.user)
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


