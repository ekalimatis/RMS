import datetime

from sqlalchemy_mptt.mixins import BaseNestedSets
from sqlalchemy.sql import text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

from rms import db
from rms.user.models import User


class RequirementTree(db.Model, BaseNestedSets):
    __tablename__ = 'requirement_tree'
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    requirements = relationship("Requirement", backref="requirement_tree")
    created_date = db.Column(db.DateTime(), nullable=False, server_default=db.text('(now() at time zone \'utc0\')'))

    def __repr__(self):
        return f'{self.project_id} - {self.id}'

class Requirement(db.Model):
    __tablename__ = 'requirement'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime(), nullable=False, server_default=db.text('(now() at time zone \'utc0\')'))
    update_date = db.Column(db.DateTime(), nullable=False, onupdate=datetime.datetime.utcnow())
    approve = db.Column(db.Boolean())
    verify_id = db.Column(db.Integer())
    status_id = db.Column(db.Integer(), db.ForeignKey('requirement_statuses.id'))
    author_id = db.Column(db.Integer())
    tags = db.Column(db.String())
    requirement_node_id = db.Column(db.Integer(), db.ForeignKey('requirement_tree.id'))
    project_id = db.Column(db.Integer(), db.ForeignKey('project.id'))
    test_id = db.Column(db.Integer())
    task_id = db.Column(db.Integer())
    priority_id = db.Column(db.Integer(), db.ForeignKey('requirement_priority.id'))
    history_log = db.Column(db.Integer())
    version = db.Column(db.Integer())
    type_id = db.Column(db.Integer(), db.ForeignKey('requirement_types.id'))
    release = db.Column(db.String(20))
    priority = relationship('RequirementPriority', backref='requirements')
    status = relationship('RequirementStatuses', backref='requirements')
    type = relationship('RequirementTypes', backref='requirements')

    def __repr__(self):
        return self.name

class RequirementStatuses(db.Model):
    __tablename__ = 'requirement_statuses'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.status

class RequirementPriority(db.Model):
    __tablename__ = 'requirement_priority'
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.priority

class RequirementTypes(db.Model):
    __tablename__ = 'requirement_types'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.type

class AcceptRequirement(db.Model):
    __tablename__ = 'accept_requirement'
    id = db.Column(db.Integer, primary_key=True)
    requirement_id = db.Column(db.Integer(), db.ForeignKey('requirement.id'), nullable=False)
    accept_user = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    requirement = relationship("Requirement", backref="accepts")
    user = relationship("User", backref="accept_requirements")
    __table_args__ = (
        UniqueConstraint("requirement_id", "accept_user"),
    )

    def __init__(self, requirement_id, user_id):
        self.requirement_id = requirement_id
        self.accept_user = user_id



