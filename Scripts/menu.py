
from colorama import Fore, Back,init
from Scripts.modules import cls
from Scripts.NSP import *

def menu_start(): # Вывод меню
    import time
    cls()
    logo=Fore.YELLOW+Back.BLACK+"""
    ███╗   ██╗███████╗██████╗ 
    ████╗  ██║██╔════╝██╔══██╗
    ██╔██╗ ██║███████╗██████╔╝
    ██║╚██╗██║╚════██║██╔═══╝ 
    ██║ ╚████║███████║██║     
    ╚═╝  ╚═══╝╚══════╝╚═╝     
    
    NoSQL Pentester for MongoDB                
    [1] Запустить сканирование в консоли 
    [2] Запустить веб-сервер
    """
    print(logo)
    while True:
        chose=int(input("Выберите параметр запуска: "))
        if chose == 1:
            log_event("-----------------------NEW LOG----------------------------",'info',npt=0)
            main()
            break
        elif chose==2:
            from Server.cli.console import mainserv
            cls()
            mainserv()
            break
        else:
            print("Не правильный параметр запуска")