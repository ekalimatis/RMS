import sys

from getpass import getpass

from rms import create_app
from rms.db import db
from rms.user.models import User
from rms.user.enums import Roles

app = create_app()

with app.app_context():
    username = input("Введите имя:")

    if User.query.filter(User.username == username).count():
        print("Уже есть такой пользователь")
        sys.exit(1)

    password1 = getpass('Введите пароль: ')
    password2 = getpass('Введите пароль: ')

    if password1 != password2:
        print("Пароли не совпадают.")
        sys.exit(1)

    new_user = User(username=username, role=Roles.ADMIN)
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан пользователь с id {new_user.id} и ролью {Roles.ADMIN.value}")