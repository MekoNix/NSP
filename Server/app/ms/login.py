from Server.cli.crypto import *
from Scripts.log import log_event
from flask import session, redirect, url_for, request
from functools import wraps

# БЛОК МОДУЛЕЙ ДЛЯ МОДУЛЕЙ
def find_password_for_user(filename="",username="admin"):
    filename=find_path("users.json")
    with open(filename, 'r') as file:
        data = json.load(file)
    for item in data:
        if item.get("User") == username:
            return item.get("Pass")

# Декартор проверки пользователя


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function




def login_web(username,password):
    if summ_hash(password,username):
        return 1
    else:
        return 0
#test
#123
