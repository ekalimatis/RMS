from datetime import datetime
from operator import itemgetter

from sqlalchemy import func
from sqlalchemy_mptt import tree_manager

from rms import db
from rms.requirements.models import RequirementTree, Requirement, AcceptRequirementRool, AcceptRequirement
from rms.requirements.forms import RequirementForm


def load_requirement(requirement_id:int) -> Requirement:
    requirement = db.session.get(Requirement, requirement_id)
    return requirement

def get_last_requirement(node_id):
    requirement = db.session.query(Requirement).filter(Requirement.requirement_id == node_id).order_by(
        Requirement.created_date.desc()).first()
    return requirement

def upgrade_requirement(requirement_form):
    current_version = db.session.query(func.max(Requirement.version)).filter(
        Requirement.requirement_id == requirement_form.requirement_node_id.data).one()[0]

    requirement_value = {
        'name': requirement_form.name.data,
        'description': requirement_form.description.data,
        'status_id': requirement_form.status.data,
        'tags': requirement_form.tags.data,
        'priority_id': requirement_form.priority.data,
        'type_id': requirement_form.type.data,
        'update_date': datetime.utcnow(),
        'requirement_id': requirement_form.requirement_node_id.data,
        'version':  current_version + 1,
    }
    requirement = Requirement(**requirement_value)
    db.session.add(requirement)
    db.session.commit()

def create_new_requirement(requirement_form):
    requirement_value = {
        'name': requirement_form.name.data,
        'description': requirement_form.description.data,
        'status_id': requirement_form.status.data,
        'tags': requirement_form.tags.data,
        'priority_id': requirement_form.priority.data,
        'type_id': requirement_form.type.data,
        'update_date': datetime.utcnow(),
        'created_date': datetime.utcnow(),
        'version': 1,
    }
    tree_manager.register_events(remove=True)
    node = RequirementTree(
        parent_id=requirement_form.requirement_node_id.data,
        project_id=requirement_form.project_id.data,
        left=0,
        right=0
    )
    requirement = Requirement(**requirement_value)
    node.requirements.append(requirement)
    db.session.add(node)
    db.session.commit()
    tree_manager.register_events()

def save_requirement_in_bd(form:RequirementForm):
    if form.requirement_id.data:
        upgrade_requirement(form)
    else:
        create_new_requirement(form)


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


def make_requirements_list_with_parent_id(project_id: int) -> list:

    tree_node_list = db.session.query(RequirementTree).filter(RequirementTree.project_id == project_id).all()

    tree_node_dict = {}
    for node in tree_node_list:
        tree_node_dict[node.id] = node

    requirement_list = []
    for node in tree_node_dict.values():
        requirement_chain = node.get_last_requirement().name
        node_id = node.id
        if node.parent_id:
            parent_id = str(node.parent_id)
        else:
            parent_id = "#"
        requirement_list.append({'id': str(node_id), 'parent': parent_id, 'text': requirement_chain})

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
        requirement = db.session.query(Requirement).filter(Requirement.requirement_id == node[1].id).order_by(Requirement.created_date.desc()).first()
        indent = '&nbsp;' * len(str(node[0]).replace('0',''))
        text += f"{indent}{'.'.join(str(node[0]).replace('0',''))} {requirement.name}<br>{indent}{indent}{requirement.description}<br>"

    return  text

def save_accept(requirement_id:int, user_id:int) -> None:
    accept_requirement = AcceptRequirement(requirement_id, user_id)
    db.session.add(accept_requirement)
    db.session.commit()

def get_accept_rool(requirement_type:int) -> list:
    roles = db.session.query(AcceptRequirementRool.accept_role).filter(AcceptRequirementRool.requirement_type == requirement_type).all()
    roles = set([role[0] for role in roles])
    return roles

def get_accept_users(requirement_id:int) -> list:
    accepts = db.session.query(AcceptRequirement).filter(AcceptRequirement.requirement_id == requirement_id).all()
    accept_users = set([accept.user.role.value for accept in accepts])
    return accept_users