from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, abort

from rms.projects.forms import ProjectForm
from rms.projects.projects import save_project_in_bd
from rms.helpers.form_helpers import flash_form_errors
from rms.projects.models import Project, RequirementTree
from rms.requirements.requirements import make_requirements_list

blueprint = Blueprint('projects', __name__, url_prefix='/projects')

@blueprint.route('/create_project_page/', methods=['GET'])
def create_project_page():
    project_form = ProjectForm()
    return render_template('projects/create_project.html', form=project_form)

@blueprint.route('save', methods=['POST'])
def save_project():
    project_form = ProjectForm()
    save_project_in_bd(project_form)
    if project_form.validate_on_submit():
        save_project_in_bd(project_form)
        return redirect(url_for('requirements.create_requirement'))
    else:
        flash_form_errors(project_form)
        return render_template('projects/create_project.html', form=project_form)


@blueprint.route('/<int:project_id>', methods=['GET'])
def view_project(project_id: int):
    project = Project.query.filter(Project.id == project_id).first()
    #requirement_tree_nodes = RequirementTree.query.filter(RequirementTree.project_id == project_id).all()
    req_list = make_requirements_list(project_id)
    #print(req_list)
    if not project:
        abort(404)
    return render_template("projects/project_card.html", project=project, req_tree=req_list)



@blueprint.route('/index', methods=['GET'])
def list_projects():
    projects = Project.query.order_by(Project.created_date.desc()).all()
    return render_template('projects/index.html', project_list=projects)
