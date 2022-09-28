from rms import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10))

    def __repr__(self):
        return f'<User id {self.id}, {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
