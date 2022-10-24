from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from rms.requirements.models import *
from rms.user.models import User
from rms.projects.models import Project


def init_admin(app, db):
    admin = Admin(app)
    admin.add_view(ModelView(Requirement, db.session))
    admin.add_view(ModelView(RequirementTree, db.session))
    admin.add_view(ModelView(RequirementStatuses, db.session))
    admin.add_view(ModelView(RequirementTypes, db.session))
    admin.add_view(ModelView(RequirementPriority, db.session))
    admin.add_view(ModelView(AcceptRequirement, db.session))

    admin.add_view(ModelView(User, db.session, endpoint='user_tbl'))

    admin.add_view(ModelView(Project, db.session))


