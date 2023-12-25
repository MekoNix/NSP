# Установка модулей с прогресс баром чтобы было не скучно и красиво.
import os
import time
import json


def cls():  # Модуль отчистки командной строки
    from platform import platform
    if 'Windows' in str(platform()):
        os.system("cls")
    else:
        os.system("clear")


# БЛОК ПРОВЕРОК
# ----------------------------------------------------------------------------------------------------------------------

def first_start_check():  # Проверка на папку logs если программа уже запускалась logs будет существовать, если нет то программа создаст её и начнёт загрузку компонентов
    if not os.path.exists("logs"):
        os.mkdir("logs")
        first_start()
    else:
        main()


def nmapc():  # Проверка установлен ли Nmap. Сслыка на документацию и как поставить nmap: https:nmap-install.com
    a = os.popen('nmap').read()
    if "Options" in a:
        pass
    else:
        exit("Nmap не установлен. Проверьте документацию для установки")


def internet_con():  # Проверка на интернет соединение.
    import socket
    try:
        socket.create_connection(('www.google.com', 80), timeout=5)
        pass
    except OSError:
        exit("Интернет соединение отсутствует. Проверьте подключение")


def server_ping(host):
    answer = os.popen(f"ping {host}").read()
    if "TTL" in answer:
        return 1
    else:
        return 0


def cominst():  # Проверка компонентов
    from Scripts.log import log_event
    log_event("Проверка nmap",npt=1)
    nmapc()
    log_event("Проверка интернета",npt=1)
    internet_con()


# ----------------------------------------------------------------------------------------------------------------------
# БЛОК УСТАНОВОК
# =======================================================================================================================
def modules_install():  # Установка моуделй. tqdm уже должен быть установлен
    from tqdm import tqdm
    from Scripts.log import log_event
    listm = ["tqdm", 'colorama', 'requests', 'flask', 'fpdf', 'python-nmap', 'pymongo', 'bs4','reportlab','bcrypt','cryptography']
    log_event("Модули не установленны,начниаем установку", npt=1)
    time.sleep(0.5)
    bar = tqdm(listm, desc="Установка модуля", unit="bit")
    for md in bar:
        log_event(f"Установка модуля: {md}", )
        os.system(f"pip install {md} --quiet")
        bar.set_description(desc=f"Установка {md}")


# =======================================================================================================================
# БЛОК МОДУЛЕЙ

def disclaimer():
    from Scripts.log import log_event
    l1984="n"
    text="""NSP - это утилита с открытым исходным кодом, предназначен для легального использования в рамках тестирования безопасности.
Все введенные пользователем данные, включая IP-адреса и учетные записи, строго хранятся локально на компьютере пользователя 
и не передаются разработчикам или третьим лицам.
            """
    print(text)
    while l1984 !="y":
        l1984=input("Согласится? y[да] n[нет]: ")
        if l1984 == "n":
            exit()
    log_event("Пользователь согласился")

def first_start():  # Первый запуск программы. Установка компонентов и модулей
    from Scripts.log import log_event
    disclaimer()
    log_event("Программа запушена в первые, начинаем настройку...", npt=1)
    log_event("Установка обновления pip")
    os.system("python.exe -m pip install --upgrade pip --quiet")
    log_event("Установка модуля tqdm " )
    os.system("pip install tqdm --quiet")
    from colorama import Fore, Back
    print(Back.BLACK + Fore.YELLOW)
    cominst()
    print(Fore.GREEN + "Проверка компонентов завершена" + Fore.YELLOW)
    time.sleep(3)
    cls()
    modules_install()
    print(Fore.GREEN + "Установка модулей завершена" + Fore.YELLOW)
    time.sleep(2)
    main()





def show_help():
    command_descriptions = {
        'exit': 'Завершает программу',
        'help': 'Отображает справку по командам',
        'set-host': 'Устанавливает хост для сканирования',
        'ver': 'Отображает версию программы',
        'scan': 'Запускает сканирование',
        'clear': 'Очищает экран консоли',
        'credentials-set': 'Устанавливает логин и пароль для доступа к серверу.',
        'LPS': 'Тоже самое что и credentials-set'


    }
    print("Справка по командам:")
    for command, description in command_descriptions.items():
        print(f"/{command}: {description}")



def display_version():
    import requests
    url="https://api.github.com/repos/MekoNix/NSP/releases/latest"
    response=requests.get(url)
    release_info = response.json()
    latest_version = release_info.get("name")
    return latest_version

def set_host(host):
    from Scripts.log import log_event
    from colorama import Fore
    host=str(host)
    if not server_ping(host):
        print(Fore.Red+"Не возможно соединиься с сервером")
        log_event("Не возможно соединиься с сервером","Warning")
    write_to_json(f"Host:{host}",host)

def set_port(port,host):
    from Scripts.log import log_event
    port=str(port)
    write_to_json(f"Port:{port}",host)
    log_event(f"Порт установлен: {port}", )

import os

def find_path(file='', nroot=0, ndir=0):
    """
    Поиск файла или папки в проекте.
    Если нужен только корень проекта, установите nroot=1.
    Для поиска папки установите ndir=1 и укажите название папки в 'file'.
    """
    py_dir = os.path.dirname(os.path.abspath(__file__))  # Определяем директорию файла
    root = os.path.dirname(py_dir)  # Определяем корневую директорию проекта

    if ndir:
        # Поиск директории
        for root_folder, subfolders, _ in os.walk(root):
            if file in subfolders:
                return os.path.join(root_folder, file)
        return None  # Возвращаем None, если директория не найдена

    elif nroot:
        return root
    else:
        # Поиск файла
        for root_folder, _, files in os.walk(root):
            if file in files:
                return os.path.join(root_folder, file)
        return None  # Возвращаем None, если файл не найден



def write_to_json(line,host):
    key, value = map(str.strip, line.split(':', 1))
    dic={key:value}
    try:
        with open(get_json_path(host), 'r') as f:
            # Загружаем существующие данные из файла
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не существует или не может быть декодирован, создаем новый пустой словарь
        data = {}
    data.update(dic)
    with open(get_json_path(host),'w') as f:
        f.write("") # Чистим файл, а то идёт наслоение, да кастыль но работает.
    with open(get_json_path(host),'a') as f:
        json.dump(data,f,indent=4)

def get_json_path(host):
    from Scripts.log import log_event
    log_file_path=find_path(nroot=1)
    log_file_path+=f"/logs/{host}.json"
    try:
        # Пытаемся открыть файл в режиме создания ('x')
        with open(log_file_path, 'x'):
            pass  # Если файл не существует, то он будет создан и оставлен пустым
            log_event(f"Json file for {host} created")
    except FileExistsError:
        # Если файл уже существует, то ничего не делаем
        pass

    return log_file_path


def pars_json(whattopas,file):
    with open(get_json_path(file)) as f:
        json_data=json.load(f)
    value=json_data.get(whattopas)
    return value


def LPS(pas,user,host):
    write_to_json(f"User:{user}",host)
    write_to_json(f"Password:{pas}",host)

# =======================================================================================================================
def main():  # Главаная программма для запуска NSP и его других частей.
    from colorama import Fore, Back, init
    from Scripts.menu import menu_start
    init(convert=True)
    print(Fore.YELLOW + Back.BLACK)
    menu_start()
