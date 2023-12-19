from Scripts.modules import *
from Scripts.log import *
from colorama import Fore,Back

import os
logoNSP=Fore.YELLOW+Back.BLACK+"""
    ███╗   ██╗███████╗██████╗ 
    ████╗  ██║██╔════╝██╔══██╗
    ██╔██╗ ██║███████╗██████╔╝
    ██║╚██╗██║╚════██║██╔═══╝ 
    ██║ ╚████║███████║██║     
    ╚═╝  ╚═══╝╚══════╝╚═╝     
    NoSQL Pentester for MongoDB """
host_value=""

def command_handler(com):
    if "exit" in com:
        log_event("Завершение программы","info",1)
        exit()
    if "help" in com:
        show_help()
    if "set-host" in com:
        global host_value
        host_value = input("Host: ")
        set_host(host_value)
        log_event(f"Хост установлен: {host_value}","info",1)
        port=input("Port:")
        set_port(port,host=host_value)
        log_event(f"Порт установлен: {port}",'info',npt=1)
    if "ver" in com:
        dv=display_version()
        print(f"Последняя версия проекта: {dv}")
        log_event(f"Проверена вресия проекта пользователем {dv}",'info',0)
    if "scan" in com:
        start_scan()
    if "clear" in com:
        cls()
        print(logoNSP)
    if 'LPS' in com:
        if not host_value == "":
            user=input("User: ")
            password=input("Password: ")
            LPS(password,user,host_value)
            log_event(f"JSON file update: Установлен user и pass для хоста. ",'info',npt=0)
            DB=input("DB (By default config): ")
            if DB=="":
                DB='config'
            write_to_json(f"DB:{DB}",host_value)
            log_event(f"JSON file update:DB to conn {DB} ", 'info', npt=0)
        else:
            print("Сначала надо установить хост")
    if 'credentials-set' in com:
        if not host_value == "":
            user=input("User: ")
            password=input("Password: ")
            LPS(password,user,host_value)
            log_event(f"JSON file update: Установлен user и pass для хоста. ",'info',npt=0)
        else:
            print("Сначала надо установить хост")


def main():
    cls()
    print(logoNSP)
    print("Введите help для помощи")
    while True:
        command_handler(input("Command: "))