# Установка модулей с прогресс баром чтобы было не скучно и красиво.
import os
import time


def cls(): # Модуль отчистки командной строки
    from platform import platform
    if 'Windows' in str(platform()):
        os.system("cls")
    else:
        os.system("clear")


# БЛОК ПРОВЕРОК
# ----------------------------------------------------------------------------------------------------------------------

def first_start_check(): # Проверка на папку logs если программа уже запускалась logs будет существовать, если нет то программа создаст её и начнёт загрузку компонентов
    if not os.path.exists("logs"):
        os.mkdir("logs")
        first_start()
    else:
        main()


def nmapc():# Проверка установлен ли Nmap. Сслыка на документацию и как поставить nmap: https:nmap-install.com
    a = os.popen('nmap').read()
    if "Options" in a:
        time.sleep(4)
        pass
    else:
        exit("Nmap не установлен, проверьте что nmap установлен. Проверьте документацию для установки")


def internet_con(): #Проверка на интернет соединение.
    import socket
    import time
    try:
        socket.create_connection(('www.google.com',80),timeout=5)
        time.sleep(5)
        pass
    except OSError:
        exit("Интернет соединение отсутствует. Проверьте подключение")

def server_ping(host):
    answer=os.popen(f"ping {host}").read()
    if "TTL" in answer:
        return 1
    else:
        return 0

def cominst():# Проверка компонентов
    from tqdm import tqdm
    pb = tqdm(total=2, desc="Проверка nmap ")
    pb.update(1)
    nmapc()
    pb.set_description("Проверка интернета")
    internet_con()
    pb.update(2)

# ----------------------------------------------------------------------------------------------------------------------
#БЛОК УСТАНОВОК
#=======================================================================================================================
def modules_install(): # Установка моуделй. tqdm уже должен быть установлен
    from tqdm import tqdm
    from log import log_event
    listm = ["tqdm", 'colorama', 'requests', 'flask', 'fpdf', 'python-nmap', 'pymongo', 'bs4']
    log_event("Модули не установленны,начниаем установку","info")
    print("Модули не установленны,начниаем установку...")
    time.sleep(0.5)
    bar = tqdm(listm, desc="Установка модуля", unit="bit")
    for md in bar:
        log_event(f"Установка модуля: {md}","info")
        os.system(f"pip install {md} --quiet")
        bar.set_description(desc=f"Установка {md}")


#=======================================================================================================================
# БЛОК МОДУЛЕЙ


def first_start(): # Первый запуск программы. Установка компонентов и модулей
    from log import log_event
    log_event("Программа запушена в первые, начинаем настройку...",'info')
    print("Программа запушена в первые, начинаем настройку...")
    log_event("Установка обновления pip","info")
    os.system("python.exe -m pip install --upgrade pip --quiet")
    log_event("Установка модуля tqdm ", "info")
    os.system("pip install tqdm --quiet")
    from colorama import Fore,Back
    print(Back.BLACK+Fore.YELLOW)
    cominst()
    print(Fore.GREEN+"Установка компонентов завершена"+Fore.YELLOW)
    time.sleep(3)
    cls()
    modules_install()
    print(Fore.GREEN+"Установка модулей завершена"+Fore.YELLOW)
    main()



#=======================================================================================================================
def main(): # Главаная программма для запуска NSP и его других частей.
    from colorama import Fore, Back,init
    from Scripts.menu import menu_start
    init(convert=True)
    print(Fore.YELLOW + Back.BLACK)
    menu_start()

