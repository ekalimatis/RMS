from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

from rms.projects.forms import ProjectForm
from rms.projects.projects import save_project_in_bd


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