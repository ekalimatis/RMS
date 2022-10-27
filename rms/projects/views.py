from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, abort

from rms.projects.forms import ProjectForm
from rms.projects.projects import save_project_in_bd
from rms.helpers.form_helpers import flash_form_errors
from rms.user.decorators import admin_required

from rms.projects.models import Project, RequirementTree
from rms.requirements.requirements import make_requirements_list
from rms.requirements.forms import RequirementForm
from rms import db

blueprint = Blueprint('projects', __name__, url_prefix='/projects')

@blueprint.route('/create_project_page/', methods=['GET'])
@login_required
def create_project_page():
    project_form = ProjectForm()
    return render_template('projects/create_project.html', form=project_form)

@blueprint.route('save', methods=['POST'])
def save_project():
    project_form = ProjectForm()
    save_project_in_bd(project_form)
    if project_form.validate_on_submit():
        save_project_in_bd(project_form)
        return redirect(url_for('projects.list_projects'))
    else:
        flash_form_errors(project_form)
        return render_template('projects/create_project.html', form=project_form)


@blueprint.route('/<int:project_id>', methods=['GET'])
def view_project(project_id: int):
    requirement_form = RequirementForm()
    project = db.session.get(Project, project_id)
    req_list = make_requirements_list(project_id)
    requirement_form.project_id.data = project_id
    if not project:
        abort(404)
    return render_template('create_requirement.html',
                           form=requirement_form,
                           project_id=project.id,
                           req_tree=req_list,
                           page_text=f'ПРОЕКТ({project.id}) - {project.name}: {project.description}')


@blueprint.route('/index', methods=['GET'])
@login_required
def list_projects():
    projects = Project.query.order_by(Project.created_date.desc()).all()
    return render_template('projects/index.html', project_list=projects)