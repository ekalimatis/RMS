from flask import Flask
from flask_migrate import Migrate
from rms.db import db
from rms.users.models import User


def create_app():
        app = Flask(__name__)
        app.config.from_pyfile('config.py')
        db.init_app(app)
        migrate = Migrate(app,db)
        #TODO delete route
        @app.route('/')
        def index():
                return 'Hello world'

        return app