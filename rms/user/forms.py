from flask_wtf import FlaskForm
from wtforms import BooleanField,  StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


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
