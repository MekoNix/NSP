from Server.cli.crypto import *
from Scripts.log import log_event
from flask import session, redirect, url_for, request
from functools import wraps

# БЛОК МОДУЛЕЙ ДЛЯ МОДУЛЕЙ
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
