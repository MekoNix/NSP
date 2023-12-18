# Установка модулей с прогресс баром чтобы было не скучно и красиво.
import os
import time


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
    log_event("Проверка nmap", level="info", npt=1)
    nmapc()
    log_event("Проверка интернета", "info", 1)
    internet_con()


# ----------------------------------------------------------------------------------------------------------------------
# БЛОК УСТАНОВОК
# =======================================================================================================================
def modules_install():  # Установка моуделй. tqdm уже должен быть установлен
    from tqdm import tqdm
    from Scripts.log import log_event
    listm = ["tqdm", 'colorama', 'requests', 'flask', 'fpdf', 'python-nmap', 'pymongo', 'bs4']
    log_event("Модули не установленны,начниаем установку", "info", npt=1)
    time.sleep(0.5)
    bar = tqdm(listm, desc="Установка модуля", unit="bit")
    for md in bar:
        log_event(f"Установка модуля: {md}", "info", 0)
        os.system(f"pip install {md} --quiet")
        bar.set_description(desc=f"Установка {md}")


# =======================================================================================================================
# БЛОК МОДУЛЕЙ


def first_start():  # Первый запуск программы. Установка компонентов и модулей
    from Scripts.log import log_event
    log_event("Программа запушена в первые, начинаем настройку...", 'info', npt=1)
    log_event("Установка обновления pip", "info", 0)
    os.system("python.exe -m pip install --upgrade pip --quiet")
    log_event("Установка модуля tqdm ", "info", 0)
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


def write_info_file(line, host):
    logpy_dir = os.path.dirname(os.path.abspath(__file__))  # Определяем папку с файлом log.py
    start_dir = os.path.dirname(logpy_dir)  # Определяем папку с проектом
    log_dir = os.path.join(start_dir+ '\logs')
    log_file_path = os.path.join(log_dir, f"{host}.txt")
    with open(log_file_path, 'a') as f:
        f.write(f'{line}\n')

def show_help():
    command_descriptions = {
        'exit': 'Завершает программу',
        'help': 'Отображает справку по командам',
        'set-host': 'Устанавливает хост для сканирования',
        'ver': 'Отображает версию программы',
        'scan': 'Запускает сканирование',
        'clear': 'Очищает экран консоли'
    }
    print("Справка по командам:")
    for command, description in command_descriptions.items():
        print(f"/{command}: {description}")

def display_version():
    import requests
    url="https://api.github.com/repos/MekoNix/NSP/releases/lasted"
    response=requests.get(url)
    release_info = response.json()
    latest_version = release_info.get("tag_name")
    return latest_version

def set_host(host):
    from Scripts.log import log_event
    from colorama import Fore
    host=str(host)
    #if not server_ping(host):
        #print(Fore.Red+"Не возможно соединиься с сервером")
        #log_event("Не возможно соединиься с сервером","Warning")
    write_info_file(f"Host target: {host}",host)
# =======================================================================================================================
def main():  # Главаная программма для запуска NSP и его других частей.
    from colorama import Fore, Back, init
    from Scripts.menu import menu_start
    init(convert=True)
    print(Fore.YELLOW + Back.BLACK)
    menu_start()
