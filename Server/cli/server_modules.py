import os

from Scripts.log import log_event
from Scripts.modules import *
import string
import random
from datetime import datetime
from Server.cli.crypto import *
from Server.app.server import run_server
import threading
from colorama import Fore,Back









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

def find_password_for_user(filename=find_path("users.json"),username="admin"):
    with open(filename, 'r') as file:
        data = json.load(file)

    for item in data:
        if item.get("User") == username:
            return item.get("Pass")

    return "Пользователь не найден"
def ifuserexist(username):
    decrypt_and_save_json()
    filename=find_path("users.json")

    with open(filename, 'r') as file:
        data = json.load(file)

    for item in data:
        if item.get("User") == username:
            encrypt_data()
            print("User exist, select another name")
            return "User exist, select another name"
    encrypt_data()
    return 1
def userfolder(username):
    os.mkdir(find_path("profiles", ndir=1) + f"/{username}")
    pathofuser = find_path("profiles", ndir=1) + f"/{username}"
    log_event(f"Add folder for {username} in {pathofuser}")
def create_users_file():
    # Генерируем пароль для первого пользователя
    password = generate_password()
    date=datetime.datetime.today()
    # Данные первого пользователя
    first_user_data = {
        "User": "admin",
        "Pass": hash_password(password),
        "AccessLevel": "admin",
        "CreatedBy": "console",
        "DateCreated": date.strftime("%d.%m.%Y")
    }
    userfolder("admin")
    # Создаем список пользователей и добавляем первого пользователя
    users_data = [first_user_data]
    # Сохраняем данные в JSON-файл
    with open(find_path(nroot=1)+'/Server/Users/db/users.json', 'w') as file:
        json.dump(users_data, file, indent=4)
    encrypt_data(find_path(nroot=1)+'/Server/Users/db/users.json')
    return password  # Возвращаем пароль для дальнейшего использования

# Предположим, это функция, вызываемая при запуске вашего приложения
def initialize_application():
    if  not find_path("enc"):
        initial_password = create_users_file()
        print(f"To login please use the admin account with {initial_password} in password. Or create new user")
        print(" PLEASE REMEMBER PASS YOU WILL NOT BE ABLE TO CHANGE YOUR PASSWORD")
    else:
        pass
def command_handler(command, *args):
    from Server.cli.comands import add_user,delete_user,show_help,show_status,show_server_info,show_active_connections,list_users,exit_program,clear
    commands = {
        "adduser": add_user,
        "deluser": delete_user,
        "status": show_status,
        "serverinfo": show_server_info,
        "activeconnection": show_active_connections,
        "user_list": list_users,
        "exit": exit_program,
        'help': show_help,
        'clear': clear
    }

    if command in commands:
        commands[command](*args)
    else:
        print(f"Неизвестная команда: {command}. Напишите help для справки")


