from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import current_user

from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import *
from rms.requirements.models import AcceptRequirement
from rms.user.decorators import admin_required


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/create_requirement/', methods=['GET'])
@admin_required
def create_requirement():
    requirement_form = RequirementForm()
    return render_template('create_requirement.html', form=requirement_form)

@blueprint.route('/get_requirement/<requirement_id>')
def get_requirement(requirement_id):
    requirement = load_requirement(requirement_id)
    accepted = False
    for accept in requirement.accepts:
        if accept.get_user() == current_user.get_id():
            accepted = True

    requirement_json = {
        'id': requirement.id,
        'name': requirement.name,
        'description': requirement.description,
        'status_id': requirement.status_id,
        'tags': requirement.tags,
        'priority_id': requirement.priority_id,
        'type_id': requirement.type_id,
    }

    if accepted:
        requirement_json['accept_but'] = True
    else:
        requirement_json['accept_but'] = False

    return {'requirement': requirement_json}

@blueprint.route('/requirement_list/<project_id>')
def get_requirements_list(project_id):
    requirement_list = make_requirements_list(project_id)
    return jsonify({'requirements': requirement_list})

@blueprint.route('/requirement_doc/<project_id>')
def get_requirement_doc(project_id):
    requirement_doc = get_plain_requirement_text(project_id)
    return jsonify({'requirement_doc': requirement_doc})

@blueprint.route('save', methods=['POST'])
def save_requirement():
    requirement_form = RequirementForm()
    if requirement_form.project_id.data == '0':
        flash('Выберите проект!')
    else:
        save_requirement_in_bd(requirement_form)
        flash('Требование сохранено!')

    return render_template('create_requirement.html', form=requirement_form)

@blueprint.route('accept/<requirement_id>')
def accept(requirement_id):
    accept_rool = set(['user', 'admin']) #нужно где-то хранить правила
    accept_requirement = AcceptRequirement(requirement_id, current_user.get_id())
    db.session.add(accept_requirement)
    db.session.commit()

    accepts = db.session.query(AcceptRequirement).filter(AcceptRequirement.requirement_id == requirement_id).all()
    accept_users = []
    for accept in accepts:
        accept_users.append(accept.user.role.value)
    accept_users = set(accept_users)
    if accept_rool == accept_users:
        db.session.query(Requirement).filter(Requirement.id == requirement_id).update({"approve": True})
        db.session.commit()

    return 'status=200'
