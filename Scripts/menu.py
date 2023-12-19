
from colorama import Fore, Back,init
from Scripts.modules import cls
from Scripts.NSP import *

def menu_start(): # Вывод меню с эффектом печатающей машинки
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
    for i in range(len(logo)):
        time.sleep(0.001)
        print(logo[i], end='', flush=True)

    if int(input("Выберите параметр запуска: ")) == 1:
        log_event("-----------------------NEW LOG----------------------------",'info',npt=0)
        return main()
    else:
        return 2
