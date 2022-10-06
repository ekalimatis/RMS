from collections import defaultdict


from flask import Blueprint, render_template, redirect, url_for, request, jsonify


from rms.requirements.forms import RequirementForm
from rms.requirements.requirements import save_requirement_in_bd
from rms.requirements.models import db, Project, RequirementTree


blueprint = Blueprint('requirements', __name__, url_prefix='/requirements')

@blueprint.route('/create_requirement/', methods=['GET', 'POST'])
def create_requirement():
    requirement_form = RequirementForm()
    projects = db.session.query(Project).all()
    project_list = []
    for project in projects:
        project_list.append((project.id, project.name))
    requirement_form.project.choices = project_list
    requirement_form.requirement.choices = []

    return render_template('create_requirement.html', form=requirement_form)


@blueprint.route('/project/<project>')
def get_requirement(project):
    nodes = db.session.query(RequirementTree).filter(RequirementTree.project_id == project).all()

    tree = {}
    requirement_list = [{'id': 0, 'name': ""}]

    for node in nodes:
        tree[node.id] = node

    for node in tree.values():
        requirement_chain = str(node.requirements)
        node_id = node.id

        while node.requirement_id:
            node = tree[node.requirement_id]
            requirement_chain = str(node.requirements) + ' -> ' + requirement_chain
        requirement_list.append({'id' : node_id, 'name': requirement_chain})

    return jsonify({'requirements': requirement_list})


@blueprint.route('save', methods=['POST'])
def save_requirement():
    requirement_form = RequirementForm()
    save_requirement_in_bd(requirement_form)
    return redirect(url_for('requirements.create_requirement'))