from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required

from rms.db import db
from rms.users.models import User
from rms.requirements.models import Requirement
from rms.forms import RequirementForm
from rms.requirements.models import Project, db, Requirement, RequirementTree


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db,  compare_server_default=True)

    @app.route('/create_requirement')
    def create_requirement():
        requirement_form = RequirementForm()
        list_of_projects=db.session.query(Project).all()
        requirement_form.status.__setattr__('choices', list_of_projects)
        return render_template('create_requirement.html', form = requirement_form)

    return app
