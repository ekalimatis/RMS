from sqlalchemy_mptt.mixins import BaseNestedSets


from rms import db
from rms.requirements.enums import Requirement_status


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime())

    def __repr__(self):
        return self.name


class Requirement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240))
    requirement = db.Column(db.Text())
    created_date = db.Column(db.DateTime())
    update_date = db.Column(db.DateTime())
    approve = db.Column(db.Boolean())
    verify_id = db.Column(db.Integer())
    status = db.Column(db.Enum(Requirement_status))
    author_id = db.Column(db.Integer())
    tags = db.Column(db.String())
    parent_id = db.Column(db.Integer())
    project_id = db.Column(db.Integer())
    test_id = db.Column(db.Integer())
    task_id = db.Column(db.Integer())
    priorty_id = db.Column(db.Integer())
    history_log = db.Column(db.Integer())
    version = db.Column(db.String(20))
    type_id = db.Column(db.Integer())
    release = db.Column(db.String(20))

    def __repr__(self):
        return self.name


class requirement_tree(db.Model, BaseNestedSets):
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer())
    requirement_id = db.Column(db.Integer())

    def __repr__(self):
        return f'{self.project_id} - {self.requirement_id}'