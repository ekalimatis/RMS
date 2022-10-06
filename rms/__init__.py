from flask import Flask
from flask_migrate import Migrate


from rms.db import db
from rms.requirements.views import blueprint as requirements_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db,  compare_server_default=True)
    app.register_blueprint(requirements_blueprint)

    return app
