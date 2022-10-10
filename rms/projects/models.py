from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

from rms import db
from rms.requirements.models import RequirementTree

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text())
    created_date = db.Column(db.DateTime(), nullable=False, server_default=text('(now() at time zone \'utc0\')'))
    requirement_tree_nodes = relationship("RequirementTree", backref="project")

    def __repr__(self):
        return self.name