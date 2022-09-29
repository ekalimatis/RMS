import os
from dotenv import load_dotenv


load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'rms.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv("SECRET_KEY")