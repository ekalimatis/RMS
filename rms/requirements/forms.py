from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired

from rms.db import db
from rms.requirements.models import RequirementStatuses, RequirementPriority, RequirementTypes


class RequirementForm(FlaskForm):

    name = StringField('Требование', validators=[DataRequired()],
                       render_kw={"class": "form-control"})

    description = TextAreaField('Описание', validators=[DataRequired()],
          render_kw={"class": "form-control"})

    created_date = DateTimeField('Дата создания:', validators=[DataRequired()],
                       render_kw={"class": "form-control", 'disabled':'True',
                                  "style": "width:200px"}, default=datetime.now())

    update_date = DateTimeField('Дата обновления:', validators=[DataRequired()],
                       render_kw={"class": "form-control", "disabled": "True",
                                  "style": "width:200px", "style": "width:200px"},
                                default=datetime.now())
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

        self.status.choices = [(item.id, item.status) for item in db.session.query(RequirementStatuses).all()]
        self.priority.choices = [(item.id, item.priority) for item in db.session.query(RequirementPriority).all()]
        self.type.choices = [(item.id, item.type) for item in db.session.query(RequirementTypes).all()]
        self.project.choices = [(0, 'Выберите проект')]
        self.requirement.choices = [(0, 'Выберите родительское требование')]
