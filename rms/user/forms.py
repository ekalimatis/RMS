from flask_wtf import FlaskForm
from wtforms import BooleanField,  StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo

from rms.user.enums import Roles


class LoginForm(FlaskForm):
    """ Simple user login form 'modelled' after in-course presentations
    """
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    remember_me = BooleanField('Запомнить меня',
                               default=True,
                               render_kw={"class": "form-check-input"})


class UserCreationForm(FlaskForm):
    """
    Form to create a user by admin
    """
    username = StringField('Имя пользователя',
                               validators=[DataRequired()],
                               render_kw={"class": "form-control"})

    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})

    user_role = SelectField('Роль',
                            render_kw={"class": "form-control"})

    submit = SubmitField('Отправить!', render_kw={"class": "btn btn-primary"})

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.user_role.choices = [(choice, choice.name) for choice in Roles]


class UserChangePasswordForm(FlaskForm):
    password = PasswordField('Пароль',
                         validators=[DataRequired()],
                         render_kw={"class": "form-control"})
    password1 = PasswordField('Повторите пароль',
                             validators=[DataRequired(),EqualTo('password')],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Сменить пароль', render_kw={"class": "btn btn-primary"})



