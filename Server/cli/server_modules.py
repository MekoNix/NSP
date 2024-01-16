import os
import ctypes
from Scripts.log import log_event
from Scripts.modules import *
import string
import random
from datetime import datetime
from Server.cli.crypto import hash_password,summ_hash
import threading
from colorama import Fore,Back
import shutil
import os
import stat




def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def add_to_json(filename, new_user):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла.")
        return

    users.append(new_user)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def parse_json_users():

    filename=find_path("users.json")
    # Чтение данных из файла
    with open(filename, 'r') as file:
        data = json.load(file)

    # Извлечение данных пользователей и дат создания
    user_dates = [(item['User'], item['DateCreated']) for item in data]

    return user_dates

def remove_user_from_json(username,file=find_path(nroot=1)+'/Server/Users/db/users.json'):
    try:
        with open(file, 'r') as file:
            users = json.load(file)
            data=[item for item in users if item.get("User")!= username]
            file=find_path(nroot=1)+'/Server/Users/db/users.json'
            with open(file, 'w') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        users = []
    except json.JSONDecodeError:
        print("Ошибка чтения JSON файла.")
        return
def delete_file(username):
    folder = find_path("profiles", ndir=1) + f"/{username}"
    os.chmod(folder, stat.S_IWRITE)
    shutil.rmtree(folder)
def find_password_for_user(filename="",username="admin"):
    filename=find_path("users.json")
    with open(filename, 'r') as file:
        data = json.load(file)
    for item in data:
        if item.get("User") == username:
            return item.get("Pass")

    return "Пользователь не найден"
def if_user_exist(username):
    path=find_path(nroot=1)+'/Server/Users/profiles'
    if os.path.exists(path+f"/{username}"):

        return 1
    else:
        return 0
def user_folder(username):
    os.mkdir(find_path("profiles", ndir=1) + f"/{username}")
    pathofuser = find_path("profiles", ndir=1) + f"/{username}"
    log_event(f"Add folder for {username} in {pathofuser}")
def create_users_file():
    # Генерируем пароль для первого пользователя
    password = generate_password()
    date=datetime.today()
    # Данные первого пользователя
    first_user_data = {
        "User": "admin",
        "Pass": hash_password(password),
        "AccessLevel": "admin",
        "CreatedBy": "console",
        "DateCreated": date.strftime("%d.%m.%Y")
    }
    user_folder("admin")
    # Создаем список пользователей и добавляем первого пользователя
    users_data = [first_user_data]
    # Сохраняем данные в JSON-файл
    with open(find_path(nroot=1)+'/Server/Users/db/users.json', 'w') as file:
        json.dump(users_data, file, indent=4)
    return password  # Возвращаем пароль для дальнейшего использования


def initialize_application():
    if  not find_path("users.json"):
        initial_password = create_users_file()
        print(f"To login please use the admin account with {initial_password} in password. Or create new user")
        print(" PLEASE REMEMBER PASS YOU WILL NOT BE ABLE TO CHANGE YOUR PASSWORD")
    else:
            pass
def command_handler(command, user, *args):
    from Server.cli.commands import add_user, delete_user, show_help, show_status, show_server_info, show_active_connections, list_users, exit_program, clear, login

    commands = {
        "adduser": add_user,
        "deluser": delete_user,
        "status": show_status,
        "serverinfo": show_server_info,
        "activeconnection": show_active_connections,
        "user_list": list_users,
        "exit": exit_program,
        'help': show_help,
        'clear': clear,
        'login': login
    }

    if command in commands:
        if command == 'login':
            return login(), True  # Возвращает нового пользователя и флаг смены пользователя
        else:
            commands[command](*args)
    else:
        print(f"Команда {command} не найдена, напишите help")

    return user, False
