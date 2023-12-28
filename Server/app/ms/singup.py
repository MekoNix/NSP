from Server.cli.comands import add_user
from Scripts.log import log_event
from datetime import datetime
from Server.cli.server_modules import generate_password,userfolder,add_to_json
from Server.cli.crypto import *


def makeuser(username="",createby='console',AcccessLevel='user',pas=generate_password(12)):
    decrypt_and_save_json()
    log_event(f"Added user {username}, Created by: {createby}, AcccessLevel: {AcccessLevel}")
    userfolder(username)
    date = datetime.now()
    user_data = {
        "User": username,
        "Pass": hash_password(pas),
        "AccessLevel": AcccessLevel,
        "CreatedBy": createby,
        "DateCreated": date.strftime("%d.%m.%Y")
    }
    users_data = user_data
    # Сохраняем данные в JSON-файл
    add_to_json(find_path(nroot=1) + '/Server/Users/db/users.json', users_data)
    encrypt_data()
def sing_up(username,password):
        makeuser(username=username,pas=password,createby='Web server app',AcccessLevel='user')