
from colorama import Fore, Back,init
from Scripts.modules import cls
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
        return 1
    else:
        return 2
