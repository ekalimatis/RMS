from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

from rms.projects.forms import ProjectForm
from rms.projects.projects import save_project_in_bd
from rms.projects.models import Project


blueprint = Blueprint('projects', __name__, url_prefix='/projects')

@blueprint.route('/create_project/', methods=['GET'])
def create_project():
    project_form = ProjectForm()
    return render_template('projects/create_project.html', form=project_form)

@blueprint.route('save', methods=['POST'])
def save_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        save_project_in_bd(project_form)
        return redirect(url_for('requirements.create_requirement'))
    else:
        return render_template('projects/create_project.html', form=project_form)



@blueprint.route('/index',methods=['GET'])
def list_projects():
    projects = Project.query.order_by(Project.created_date.desc()).all()
    return render_template('projects/index.html', project_list=projects)
