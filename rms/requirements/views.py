from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, Response
from flask_login import current_user, login_required

from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import *
from rms.requirements.models import AcceptRequirement


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/get_last_requirement/<node_id>')
def get_last_requirement(node_id):
    requirement = load_last_requirement(node_id)
    return {'requirement': make_json_requirement(requirement)}

@blueprint.route('/get_requirement/<requirement_id>')
def get_requirement(requirement_id):
    requirement = load_requirement(requirement_id)
    return {'requirement': make_json_requirement(requirement)}

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
    id = save_requirement_in_bd(requirement_form)
    flash('Требование сохранено!')
    return redirect(url_for('projects.view_project', project_id=requirement_form.project_id.data, id=requirement_form.project_id.data))

@blueprint.route('accept/<requirement_id>')
def accept(requirement_id):
    save_accept(requirement_id, current_user.id)
    return Response(status=200)

@blueprint.route('/<int:requirement_id>')
def view_requirement(requirement_id:int):
    requirement = Requirement.query.filter(Requirement.id == requirement_id).first()
    return render_template('requirements/req_page.html', requirement=requirement)

@blueprint.route('/versions/<int:requirement_id>')
def view_versions(requirement_id:int):
    requirement = Requirement.query.filter(Requirement.id == requirement_id).first()
    versions = Requirement.query.filter(Requirement.requirement_id == requirement.requirement_id).all()
    return render_template('requirements/version_history.html', versions=versions)

@blueprint.route('/history/<int:requirement_node_id>')
def get_history(requirement_node_id:int):
    versions = Requirement.query.filter(Requirement.requirement_id == requirement_node_id).order_by(Requirement.created_date.desc()).all()
    history_log = []
    for requirement in versions:
        history_log.append(make_json_requirement(requirement))
    return render_template('requirements/history.html', versions=history_log)