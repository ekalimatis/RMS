from datetime import datetime
from operator import itemgetter

from sqlalchemy import func

from rms.requirements.models import db, RequirementTree, Requirement
from rms.requirements.forms import RequirementForm


def save_requirement_in_bd(form):

    node = RequirementTree(
        parent_id=form.requirement.data,
        project_id=form.project.data
    )

    requirement = Requirement(
        name=form.name.data,
        description=form.description.data,
        created_date=datetime.utcnow(),
        update_date=datetime.utcnow(),
        status_id=form.status.data,
        tags=form.tags.data,
        priority_id=form.priority.data,
        type_id=form.type.data
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

def get_plain_requirement_text(project_id:int) -> str:

    max_requirement_level = db.session.query(func.max(RequirementTree.level)).filter(
        RequirementTree.project_id == project_id).one()[0]
    print(max_requirement_level )

    requirement_nodes_list = db.session.query(RequirementTree).filter(
        RequirementTree.project_id == project_id).order_by(RequirementTree.level).order_by(RequirementTree.created_date).all()

    requirement_list = []
    requirement_dict = {}

    for node in requirement_nodes_list:
        node_index = 10 ** (max_requirement_level - node.level)
        if node.parent_id in requirement_dict:
            requirement_dict[node.parent_id][2] += 1
            node_index = requirement_dict[node.parent_id][2] * node_index + requirement_dict[node.parent_id][0]
        requirement_dict[node.id] = [node_index, node, 0]
        requirement_list.append((node_index, node,))

    requirement_list.sort(key=itemgetter(0))

    text = ''
    for node in requirement_list:
        requirement = db.session.query(Requirement).filter(Requirement.requirement_id == node[1].id).order_by(Requirement.created_date.desc()).one()
        indent = '&nbsp;' * len(str(node[0]).replace('0',''))
        text += f"{indent}{'.'.join(str(node[0]).replace('0',''))} {requirement.name}<br>{indent}{indent}{requirement.description}<br>"

    return  text