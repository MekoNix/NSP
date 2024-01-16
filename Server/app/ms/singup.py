from Server.cli.commands import add_user
from Scripts.log import log_event
from datetime import datetime
from Server.cli.server_modules import generate_password,user_folder,add_to_json,if_user_exist
from Server.cli.crypto import *


def make_user(username="",createby='console',AcccessLevel='user',pas=generate_password(12)):
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
        return 1
    except Exception as e:
        log_event(f"Failed to add user {username}, An error occurred: {e}")
        raise e
def sign_up(username,password):
        return make_user(username=username, createby='Web server NSP', AcccessLevel='user', pas=password)
