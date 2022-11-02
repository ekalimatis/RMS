from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, Response
from flask_login import current_user, login_required

from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import *
from rms.requirements.models import AcceptRequirement
from rms.user.decorators import admin_required
from rms.projects.models import Project
from rms.projects.views import view_project


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/get_requirement/<requirement_id>')
def get_requirement(requirement_id):
    requirement = get_last_requirement(requirement_id)
    accepted = False
    for accept in requirement.accepts:
        if accept.get_user() == current_user.id:
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

@blueprint.route('/requirement_list/<project_id>')
def get_requirements_list(project_id):
    requirement_list = make_requirements_list(project_id)
    return jsonify({'requirements': requirement_list})


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
    return redirect(url_for('projects.view_project', project_id=requirement_form.project_id.data))

@blueprint.route('accept/<requirement_id>')
def accept(requirement_id):
    save_accept(requirement_id, current_user.id)

    requirement = load_requirement(requirement_id)
    accept_rool = get_accept_rool(requirement.type_id)
    accepts_user = get_accept_users(requirement_id)

    if accept_rool == accepts_user:
        db.session.query(Requirement).filter(Requirement.id == requirement_id).update({"approve": True})
        db.session.commit()
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