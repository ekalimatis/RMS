from datetime import datetime

from rms import db
from rms.requirements.models import RequirementTree, Requirement
from rms.requirements.forms import RequirementForm


def save_requirement_in_bd(form):

    node = RequirementTree(
        parent_id = form.requirement.data,
        project_id = form.project.data
    )

    requirement = Requirement(
        name = form.name.data,
        description = form.description.data,
        created_date = datetime.utcnow(),
        update_date = datetime.utcnow(),
        status_id = form.status.data,
        tags = form.tags.data,
        priority_id = form.priority.data,
        type_id = form.type.data
    )

    node.requirements.append(requirement)

    db.session.add(node)
    db.session.commit()

def make_requirements_list(project_id:int) -> list:
    """Преобразуем спосик нод дерева требований в список требований вида:
    Корневое требование 0 -> Требование 1
    Корневое требование 0 -> Требование 1 -> Требование 2
    Корневое требование 0 -> Требование 1 -> Требование 3
    Корневое требование 0 -> Требование 1 -> Требование 3 - > Требование 4"""

    tree_node_list = db.session.query(RequirementTree).filter(RequirementTree.project_id == project_id).all()

    tree_node_dict = {}
    for node in tree_node_list:
        tree_node_dict[node.id] = node

    requirement_list = [{'id': 0, 'name': "Выберите родительское требование"}]
    for node in tree_node_dict.values():
        requirement_chain = str(node.requirements)
        node_id = node.id

        while node.parent_id:
            node = tree_node_dict[node.parent_id]
            requirement_chain = str(node.requirements) + ' -> ' + requirement_chain
        requirement_list.append({'id': node_id, 'name': requirement_chain})

    return requirement_list
