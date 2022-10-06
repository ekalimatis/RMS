from rms.requirements.models import RequirementTree, Requirement
from rms.requirements.forms import RequirementForm


def save_requirement_in_bd(form):

    node = RequirementTree(parent_id=form.requirement.data,
                           project_id=form.project.data)

    requirement = Requirement(name=form.name.data,
                              description=form.description.data,
                              created_date=form.created_date.data,
                              update_date=form.update_date.data,
                              status_id=form.status.data,
                              tags=form.tags.data,
                              priority_id=form.priority.data,
                              type_id=form.type.data)

    node.requirements.append(requirement)

    db.session.add(node)
    db.session.commit()
