from flask import Blueprint, redirect, url_for, jsonify, flash, Response
from flask_login import current_user

from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import *
from rms.requirements.models import AcceptRequirement


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/get_requirement/<requirement_id>')
def get_requirement(requirement_id):
    requirement = get_last_requirement(requirement_id)
    accepted = False
    for req_accept in requirement.accepts:
        if req_accept.get_user() == current_user.id:
            accepted = True

    requirement_json = {
        'requirement_id': requirement.id,
        'requirement_node_id': requirement.requirement_id,
        'name': requirement.name,
        'description': requirement.description,
        'status_id': requirement.status_id,
        'tags': requirement.tags,
        'priority_id': requirement.priority_id,
        'type_id': requirement.type_id,
    }

    if accepted:
        requirement_json['is_accept'] = True
    else:
        requirement_json['is_accept'] = False

    return {'requirement': requirement_json}

@blueprint.route('/tree_data/<int:project_id>')
def get_tree_data(project_id):
    tree_list = make_requirements_list_with_parent_id(project_id)
    return jsonify({'data': tree_list})


@blueprint.route('/requirement_doc/<project_id>')
def get_requirement_doc(project_id):
    requirement_doc = get_plain_requirement_text(project_id)
    return jsonify({'requirement_doc': requirement_doc})

@blueprint.route('save', methods=['POST'])
def save_requirement():
    requirement_form = RequirementForm()
    save_requirement_in_bd(requirement_form)
    flash('Требование сохранено!')
    return  redirect(url_for('projects.view_project', project_id=requirement_form.project_id.data))

@blueprint.route('accept/<requirement_id>')
def accept(requirement_id):
    save_accept(requirement_id, current_user.id)
    return Response(status=200)
