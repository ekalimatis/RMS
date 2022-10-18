from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, abort

from rms.projects.forms import ProjectForm
from rms.projects.projects import save_project_in_bd
from rms.projects.models import Project, RequirementTree
from rms.requirements.requirements import make_requirements_list

blueprint = Blueprint('projects', __name__, url_prefix='/projects')

@blueprint.route('/create_project/', methods=['GET'])
def create_project():
    project_form = ProjectForm()
    return render_template('create_project.html', form=project_form)

@blueprint.route('save', methods=['POST'])
def save_project():
    project_form = ProjectForm()
    save_project_in_bd(project_form)
    return redirect(url_for('requirements.create_requirement'))


@blueprint.route('/<int:project_id>', methods=['GET'])
def view_project(project_id: int):
    project = Project.query.filter(Project.id == project_id).first()
    #requirement_tree_nodes = RequirementTree.query.filter(RequirementTree.project_id == project_id).all()
    req_list = make_requirements_list(project_id)
    print(req_list)
    if not project:
        abort(404)
    return render_template("project_card.html", project=project, req_tree=req_list)