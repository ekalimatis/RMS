from datetime import datetime


from rms.requirements.models import db, RequirementTree, Requirement
from rms.requirements.forms import RequirementForm


def save_requirement_in_bd(form):

    node = RequirementTree(parent_id=form.requirement.data,
                           project_id=form.project.data)

    requirement = Requirement(name=form.name.data,
                              description=form.description.data,
                              created_date=datetime.utcnow(),
                              update_date=datetime.utcnow(),
                              status_id=form.status.data,
                              tags=form.tags.data,
                              priority_id=form.priority.data,
                              type_id=form.type.data)

    node.requirements.append(requirement)

    db.session.add(node)
    db.session.commit()
