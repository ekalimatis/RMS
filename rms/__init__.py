from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from rms.db import db
from rms.user.models import User
from rms.requirements.models import Requirement
from rms.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db,  compare_server_default=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'

    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
