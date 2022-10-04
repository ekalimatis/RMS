from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

from rms.db import db
from rms.requirements.models import RequirementStatuses, RequirementPriority, RequirementTypes


class RequirementForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.status.choices = db.session.query(RequirementStatuses).all()
        self.priorty_id.choices = db.session.query(RequirementPriority).all()
        self.type_id.choices = db.session.query(RequirementTypes).all()

    name = StringField('Требование', validators=[DataRequired()],
                       render_kw={"class": "form-control"})
    description = TextAreaField('Описание', validators=[DataRequired()],
          render_kw={"class": "form-control"})
    created_date = DateTimeField('Дата создания:', validators=[DataRequired()],
                       render_kw={"class": "form-control", 'disabled':'True',
                                  "style": "width:200px"}, default=datetime.now())
    update_date = DateTimeField('Дата обновления:', validators=[DataRequired()],
                       render_kw={"class": "form-control", "disabled": "True",
                                  "style": "width:200px", "style": "width:200px"})
    tags = StringField('Тэги', validators=[DataRequired()],
                       render_kw={"class": "form-control"})

    priorty_id = SelectField('Важность', validators=[DataRequired()], render_kw={"class": "form-control"},
                             choices=['Критично', 'Важно', 'Незначительно',])

    type_id = SelectField('Тип', validators=[DataRequired()], render_kw={"class": "form-control"},
                          choices=['Бизнес требование', 'Пользовательское требование','Функциональное требование',
                                     'Нефункциональное требование'])

    status = SelectField('Статус', validators=[DataRequired()], render_kw={"class": "form-control"})

    release = StringField('Релиз', validators=[DataRequired()], render_kw={"class": "form-control"})

    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-primary"})