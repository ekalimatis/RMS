from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from rms.db import db
from rms.users.models import User
from rms.users.forms import LoginForm

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('user/login.html',
                           page_title=title,
                           form=login_form)

