
from Server.cli.server_modules import *
from colorama import Fore,Back
from datetime import datetime


logo=Fore.YELLOW + Back.BLACK + """
    ███╗   ██╗███████╗██████╗ 
    ████╗  ██║██╔════╝██╔══██╗
    ██╔██╗ ██║███████╗██████╔╝
    ██║╚██╗██║╚════██║██╔═══╝ 
    ██║ ╚████║███████║██║     
    ╚═╝  ╚═══╝╚══════╝╚═╝  
    Server utilities
"""
def generate_password(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

date = datetime.now()
def add_user(createby='console',AcccessLevel='user',pas=generate_password(12)):
    username = input("User: ")
    while ifuserexist(username) == 1:
        print("User exist, change name")
        username=input("User: ")
    decrypt_and_save_json()# Сломался decrypt надо починить, я поменял file_path нужно придумать как его вводить так чтобы не было проблем( он воодиться до создания фалйлов)
    print(f"User {username} with password {pas} created successfully")
    log_event(f"Added user {username}, Created by: {createby}, AcccessLevel: {AcccessLevel}")
    userfolder(username)
    user_data = {
        "User": username,
        "Pass": hash_password(pas),
        "AccessLevel": AcccessLevel,
        "CreatedBy": createby,
        "DateCreated": date.strftime("%d.%m.%Y")
    }
    users_data = user_data
    # Сохраняем данные в JSON-файл
    add_to_json(find_path(nroot=1)+'/Server/Users/db/users.json',users_data)
    encrypt_data()

def clear():
    cls()
    print(logo)

def delete_user():
    try:
        uname = input("User: ")
        while ifuserexist(uname) != 1:
            print("User not exists check name")
            uname = input("User: ")
        decrypt_and_save_json()
        pas=input("Password: ")
        while summ_hash(pas,uname) == 0:
            print("Не верный пароль")
            pas = input("Password: ")
        remove_user_from_json(uname)
        delete_file(uname)
        print(f"User {uname} deleted successfully")
        log_event(f"Deleted user {uname}")
        encrypt_data()
    except Exception as e:
        encrypt_data()
        log_event(f"delete user failed with error: {e}",'')
        print(f"Ошибка команды попробуйте снова: {e}")
def show_status():
    print("Показ текущего статуса сервера...")

def show_server_info():
    print("Предоставление информации о сервере...")

def show_active_connections():
    print("Отображение активных подключений к серверу...")

def list_users():
    decrypt_and_save_json()
    for user,time in parse_json_users():
        print(f"User: {user} Creation date: {time} ")
    encrypt_data()

def exit_program():
    print("Выход из программы...")
    exit()
def show_help():
    help_text = Fore.WHITE+"""
    Server Utilities - Help Menu
    ============================
    Команды:
    --------
    adduser            - Добавляет нового пользователя. 
    deluser            - Удаляет существующего пользователя.
    status             - Показывает текущий статус сервера.
    serverinfo         - Предоставляет информацию о сервере, включая версию, время работы и т.д.
    activeconnection   - Отображает активные подключения к серверу.
    user_list          - Выводит список всех пользователей.
    exit               - Выходит из программы
        """+Fore.YELLOW
    print(help_text)