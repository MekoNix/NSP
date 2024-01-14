import time

from Scripts.modules import *
from threading import Thread
from Server.app.app import NSP,create_db
from Server.app.ms.WSGI import WSGI
from colorama import *
from Server.cli.server_modules import *

logo=Fore.YELLOW + Back.BLACK + """
    ███╗   ██╗███████╗██████╗ 
    ████╗  ██║██╔════╝██╔══██╗
    ██╔██╗ ██║███████╗██████╔╝
    ██║╚██╗██║╚════██║██╔═══╝ 
    ██║ ╚████║███████║██║     
    ╚═╝  ╚═══╝╚══════╝╚═╝  
    Server utilities
    
"""
def ch():
    print(logo)
    create_db()
    initialize_application()
    while True:
        command_handler(input("Command: "))

def start_flask():
    WSGI(NSP)


def mainserv():
    server_thread = Thread(target=start_flask)
    server_thread.start()
    time.sleep(2)

    main_thread = Thread(target=ch)
    main_thread.start()
    log_event("Server started at localhost:8080", npt=1)


if __name__ == '__main__':
    mainserv()