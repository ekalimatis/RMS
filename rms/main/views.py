from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import config, current_user

blueprint = Blueprint('main', __name__, url_prefix='')

@blueprint.route('/', methods=['GET'])
def main_page():
    if current_user.is_authenticated:
        return redirect(url_for('projects.list_projects'))
    return redirect(url_for('user.login'))