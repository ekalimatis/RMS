from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from rms.db import db
from rms.projects.models import Project


class ProjectForm(FlaskForm):
    name = StringField('Проект', validators=[DataRequired(), Length(max=240)], render_kw={"class": "form-control"})

    description = StringField('Описание', validators=[DataRequired()],render_kw={"class": "form-control"})

    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-primary"})
