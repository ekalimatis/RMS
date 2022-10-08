from collections import defaultdict

from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import save_requirement_in_bd, make_requirements_list, get_plain_requirement_text


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/create_requirement/', methods=['GET'])
def create_requirement():
    requirement_form = RequirementForm()
    return render_template('create_requirement.html', form=requirement_form)


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
    save_requirement_in_bd(requirement_form)
    return redirect(url_for('requirements.create_requirement'))