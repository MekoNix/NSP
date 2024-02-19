from Server.cli.commands import add_user
from Scripts.log import log_event
from datetime import *
from Server.cli.server_modules import generate_password, user_folder, add_to_json, if_user_exist
from Server.cli.crypto import *
from Server.app.ms.profiler import profiler
import os, platform


def get_birthday_file(filename, who_req):
    filename = find_path(f"{who_req}", ndir=1) + f"/{filename}"
    stat = os.stat(filename)
    if platform.system() == "Windows1":
        return datetime.datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        try:
            return datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError:
            return "123"


def make_user(username="", createby='console', AcccessLevel='user', pas=generate_password(12)):
    if not if_user_exist(username):
        user_folder(username)
    else:
        return 0
    try:
        date = datetime.datetime.now()
        user_data = {
            "User": username,
            "Pass": hash_password(pas),
            "AccessLevel": AcccessLevel,
            "CreatedBy": createby,
            "DateCreated": date.strftime("%d.%m.%Y")
        }
        users_data = user_data

        add_to_json(find_path(nroot=1) + '/Server/Users/db/users.json', users_data)
        log_event(f"Added user {username}, Created by: {createby}, AcccessLevel: {AcccessLevel}")
        pr = profiler()
        pr.create_file(str(username))
        return 1
    except Exception as e:
        log_event(f"Failed to add user {username}, An error occurred: {e}")
        raise e


def sign_up(username, password):
    return make_user(username=username, createby='Web server NSP', AcccessLevel='user', pas=password)
