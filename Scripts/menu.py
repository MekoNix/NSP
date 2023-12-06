

def menu_start():
    from colorama import Fore
    logo=Fore.RED+"""
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
    if int(input("Выберите параметр запуска: ")) == 1:
        return 1
    else:
        return 2
