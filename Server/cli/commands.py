from Server.cli.server_modules import *
from colorama import Fore, Back
from datetime import *
from Server.app.ms.killer import *
from Server.app.ms.profiler import profiler

logo = Fore.YELLOW + Back.BLACK + """
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


def add_user(createby='console', AcccessLevel='user', pas=generate_password(12)):
    username = input("User: ")
    while if_user_exist(username) == 1:
        print("User exist, change name")
        username = input("User: ")
    print(f"User {username} with password {pas} created successfully")
    log_event(f"Added user {username}, Created by: {createby}, AcccessLevel: {AcccessLevel}")
    user_folder(username)
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
    pr = profiler()
    pr.create_file(str(username))


def clear():
    cls()
    print(logo)


def delete_user():
    try:
        uname = input("User: ")
        while if_user_exist(uname) != 1:
            print("User not exists check name")
            uname = input("User: ")

        pas = input("Password: ")
        while summ_hash(pas, uname) == 0:
            print("Не верный пароль")
            pas = input("Password: ")
        remove_user_from_json(uname)
        delete_file(uname)
        print(f"User {uname} deleted successfully")
        log_event(f"Deleted user {uname}")

    except Exception as e:

        log_event(f"delete user failed with error: {e}", '')
        print(f"Ошибка команды попробуйте снова: {e}")


def list_users():
    for user, time in parse_json_users():
        print(f"User: {user} Creation date: {time} ")


def login():
    auth = False
    while auth != True:
        User = input("Login as: ")
        if if_user_exist(User):
            pas = input(f"Password for {User}: ")
            if summ_hash(pas, User) == 1:
                auth = True
                return User
            else:
                print("Wrong Password")
        else:
            print("User not exist")


def exit_program():
    print("Выход из программы...")
    pid = os.getpid()
    kill_process(pid)


def show_help():
    help_text = Fore.WHITE + """
    Server Utilities - Help Menu
    ============================
    Команды:
    --------
    adduser            - Добавляет нового пользователя. 
    deluser            - Удаляет существующего пользователя.
    user_list          - Выводит список всех пользователей.
    exit               - Выходит из программы
        """ + Fore.YELLOW
    print(help_text)
