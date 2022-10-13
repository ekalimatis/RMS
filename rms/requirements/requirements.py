from datetime import datetime
from operator import itemgetter

from sqlalchemy import func

from rms import db
from rms.requirements.models import RequirementTree, Requirement
from rms.requirements.forms import RequirementForm


def load_requirement(requirement_id):
    print(requirement_id)
    requirement = db.session.query(Requirement).filter(Requirement.id == requirement_id).one()
    return requirement

def get_last_requirement(node_id):
    requirement = db.session.query(Requirement).filter(Requirement.requirement_node_id == node_id).order_by(
        Requirement.created_date.desc()).first()
    return requirement

def save_requirement_in_bd(form):

    requirement_value = {
        'name': form.name.data,
        'description': form.description.data,
        'status_id': form.status.data,
        'tags': form.tags.data,
        'priority_id': form.priority.data,
        'type_id': form.type.data,
        'update_date': datetime.utcnow(),
    }

    if form.id.data:
        #Обновление
        requirement_value['version'], requirement_value['requirement_node_id'] = db.session.query(
            Requirement.version, Requirement.requirement_node_id).filter(Requirement.id == form.id.data).one()
        requirement_value['version'] += 1
        # for key, value in requirement_value.items():
        #     setattr(requirement,key,value)
        requirement = Requirement(**requirement_value)
        db.session.add(requirement)

    else:
        #Новое
        requirement_value['created_date'] = datetime.utcnow()
        requirement_value['version'] = 1

        node = RequirementTree(
                parent_id=form.requirement_id.data,
                project_id=form.project_id.data
            )

        requirement = Requirement(**requirement_value)
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

    requirement_list = []
    for node in tree_node_dict.values():
        requirement = get_last_requirement(node.id)
        requirement_chain = requirement.name
        requirement_id = requirement.id

        while node.parent_id:
            node = tree_node_dict[node.parent_id]
            requirement = get_last_requirement(node.id)
            requirement_chain = requirement.name + ' -> ' + requirement_chain
        requirement_list.append({'id': requirement_id, 'name': requirement_chain})

    return requirement_list

def get_plain_requirement_text(project_id:int) -> str:

    max_requirement_level = db.session.query(func.max(RequirementTree.level)).filter(
        RequirementTree.project_id == project_id).one()[0]

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
        requirement = db.session.query(Requirement).filter(Requirement.requirement_node_id == node[1].id).order_by(Requirement.created_date.desc()).first()
        indent = '&nbsp;' * len(str(node[0]).replace('0',''))
        text += f"{indent}{'.'.join(str(node[0]).replace('0',''))} {requirement.name}<br>{indent}{indent}{requirement.description}<br>"

    return  text