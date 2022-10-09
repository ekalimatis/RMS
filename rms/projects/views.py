from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

from rms.projects.forms import ProjectForm


blueprint = Blueprint('projects', __name__, url_prefix='/projects')

@blueprint.route('/create_project/', methods=['GET'])
def create_project():
    project_form = ProjectForm()
    return render_template('create_project.html', form=project_form)