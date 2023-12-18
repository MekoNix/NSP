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

def command_handler(com):
    if "exit" in com:
        log_event("Завершение программы","info",1)
        exit()
    if "help" in com:
        show_help()
    if "set-host" in com:
        host_value = com.replace("set-host", "").strip()
        set_host(host_value)
        log_event(f"Хост установлен: {host_value}","info",1)
    if "ver" in com:
        dv=display_version()
        print(f"Последняя версия проекта: {dv}")
        log_event(f"Проверена вресия проекта пользователем {dv}",'info',0)
    if "scan" in com:
        start_scan()
    if "clear" in com:
        cls()
        print(logoNSP)



def main():
    cls()
    print(logoNSP)
    print("Введите help для помощи")
    while True:
        command_handler(input("Command: "))