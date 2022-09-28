from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
        return 'Hello world'



def create_app():
        app = Flask(__name__)
        app.config.from_pyfile('config.py')
        return app