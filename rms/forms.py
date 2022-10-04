from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


#
# with app.app_context():
#     def get_list_of_status():
#         return db.session.query(RequirementTree).filter(RequirementTree.id == 19)


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