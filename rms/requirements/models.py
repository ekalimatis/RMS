import datetime

from sqlalchemy_mptt.mixins import BaseNestedSets
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship


from rms import db
from rms.requirements.enums import Requirement_status


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime(), nullable=False, server_default=text('(now() at time zone \'utc0\')'))
    requirement_tree_node = relationship("RequirementTree", backref="project")

    def __repr__(self):
        return self.name

class RequirementTree(db.Model, BaseNestedSets):
    __tablename__ = 'requirement_tree'
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    requirement_id = db.Column(db.Integer())
    requirements = relationship("Requirement", backref="requirement_tree")

    def __repr__(self):
        return f'{self.project_id} - {self.requirement_id}'

class Requirement(db.Model):
    __tablename__ = 'requirement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime(), nullable=False, server_default=db.text('(now() at time zone \'utc0\')'))
    update_date = db.Column(db.DateTime(), nullable=False, onupdate=datetime.datetime.utcnow())
    approve = db.Column(db.Boolean())
    verify_id = db.Column(db.Integer())
    status = db.Column(db.Enum(Requirement_status))
    author_id = db.Column(db.Integer())
    tags = db.Column(db.String())
    parent_id = db.Column(db.Integer(), db.ForeignKey('requirement_tree.id'))
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    test_id = db.Column(db.Integer())
    task_id = db.Column(db.Integer())
    priorty_id = db.Column(db.Integer())
    history_log = db.Column(db.Integer())
    version = db.Column(db.String(20))
    type_id = db.Column(db.Integer())
    release = db.Column(db.String(20))

    def __repr__(self):
        return self.name

