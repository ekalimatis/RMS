from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, HiddenField, BooleanField
from wtforms.validators import DataRequired

from rms.db import db
from rms.requirements.models import RequirementStatuses, RequirementPriority, RequirementTypes


class RequirementForm(FlaskForm):

    requirement_id = HiddenField()
    requirement_node_id = HiddenField()
    project_id = HiddenField()

    name = StringField('Требование', validators=[DataRequired()],
                       render_kw={"class": "form-control"})

    description = TextAreaField('Описание', validators=[DataRequired()],
          render_kw={"class": "form-control", 'style': 'height: 300px'})

    tags = StringField('Тэги', render_kw={"class": "form-control"})

    priority = SelectField('Важность', render_kw={"class": "form-control"})

    type = SelectField('Тип', render_kw={"class": "form-control"})

    status = SelectField('Статус', render_kw={"class": "form-control", "disabled":""})

    release = BooleanField('Релиз')

    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-primary"})

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.status.choices = [(item.id, item.status) for item in db.session.query(RequirementStatuses).all()]
        self.priority.choices = [(item.id, item.priority) for item in db.session.query(RequirementPriority).all()]
        self.type.choices = [(item.id, item.type) for item in db.session.query(RequirementTypes).all()]
