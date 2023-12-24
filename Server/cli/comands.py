from Scripts.log import log_event
from Scripts.modules import *
import string
import random
from datetime import datetime
from Server.cli.crypto import *
from Server.cli.server_modules import *

from datetime import datetime
def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

date = datetime.now()
def add_user(createby='console',AcccessLevel='user'):
    username=input("Username: ")
    decrypt_and_save_json()
    pas=generate_password(12)
    print(f"User {username} with password {pas} created successfully")
    log_event(f"Added user {username}, Created by: {createby}, AcccessLevel: {AcccessLevel}")
    user_data = {
        "User": username,
        "Pass": pas,
        "AccessLevel": AcccessLevel,
        "CreatedBy": createby,
        "DateCreated": date.strftime("%d.%m.%Y")
    }
    users_data = user_data
    # Сохраняем данные в JSON-файл
    add_to_json(find_path(nroot=1)+'/Server/Users/db/users.json',users_data)
    encrypt_data()

def delete_user(username):
    print(f"Удаление пользователя: {username}")

def show_status():
    print("Показ текущего статуса сервера...")

def show_server_info():
    print("Предоставление информации о сервере...")

def show_active_connections():
    print("Отображение активных подключений к серверу...")

def list_users():
    print("Вывод списка всех пользователей...")

def exit_program():
    print("Выход из программы...")
    exit()
def show_help():
    help_text = """
    Server Utilities - Help Menu
    ============================
    Команды:
    --------
    adduser            - Добавляет нового пользователя. 
                         Использование: adduser [username]
    deluser            - Удаляет существующего пользователя.
                         Использование: deluser [username]
    status             - Показывает текущий статус сервера.
    serverinfo         - Предоставляет информацию о сервере, включая версию, время работы и т.д.
    activeconnection   - Отображает активные подключения к серверу.
    users              - Выводит список всех пользователей.
    exit               - Выходит из программы
        """
    print(help_text)
