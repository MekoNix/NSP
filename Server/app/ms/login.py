from Server.cli.crypto import summ_hash, load_key
from Scripts.log import log_event
from flask import session, redirect, url_for, request
from flask_login import UserMixin
from functools import wraps


# БЛОК МОДУЛЕЙ ДЛЯ МОДУЛЕЙ

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        self.id = username


# Декартор проверки пользователя


def login_web(username, password):
    if summ_hash(password, username):
        return User(username)
    else:
        return None
