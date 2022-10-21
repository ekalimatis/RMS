from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from rms.db import db
from rms.user.models import User
from rms.user.views import blueprint as user_blueprint
from rms.requirements.views import blueprint as requirements_blueprint
from rms.projects.views import blueprint as projects_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db,  compare_server_default=True, compare_type=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(requirements_blueprint)
    app.register_blueprint(projects_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
