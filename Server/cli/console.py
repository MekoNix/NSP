from Scripts.modules import *
import threading
from Server.app.server import *
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

def mainserv():
    cls()
    print(logo)
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    print()
    log_event("Server start in http://localhost:5000",'info',npt=1)
    initialize_application()

    while True:
        command_handler(input("Command: "))
if __name__ == '__main__':
    mainserv()