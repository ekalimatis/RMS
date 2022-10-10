from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from rms.db import db
from rms.requirements.models import RequirementStatuses, RequirementPriority, RequirementTypes
from rms.projects.models import Project


class RequirementForm(FlaskForm):

    name = StringField('Требование', validators=[DataRequired()],
                       render_kw={"class": "form-control"})

    description = TextAreaField('Описание', validators=[DataRequired()],
          render_kw={"class": "form-control"})

    tags = StringField('Тэги', render_kw={"class": "form-control"})

    priority = SelectField('Важность', render_kw={"class": "form-control"})

    type = SelectField('Тип', render_kw={"class": "form-control"})

    status = SelectField('Статус', render_kw={"class": "form-control"})

    release = StringField('Релиз', render_kw={"class": "form-control"})

    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-primary"})

    requirement = SelectField('Родительское требование', render_kw={"class": "form-control"}, id='requirement')

    project = SelectField('Проект', render_kw={"class": "form-control"}, id='project')

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)

        projects = db.session.query(Project).all()
        project_list = [(0, 'Выберите проект')]
        for project in projects:
            project_list.append((project.id, project.name))

        self.status.choices = [(item.id, item.status) for item in db.session.query(RequirementStatuses).all()]
        self.priority.choices = [(item.id, item.priority) for item in db.session.query(RequirementPriority).all()]
        self.type.choices = [(item.id, item.type) for item in db.session.query(RequirementTypes).all()]
        self.project.choices = project_list
        self.requirement.choices = [(0, 'Выберите родительское требование')]
