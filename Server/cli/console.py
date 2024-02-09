import time

from Scripts.modules import *
from threading import Thread
from Server.app.app import NSP,create_db
from Server.app.ms.WSGI import WSGI
from colorama import *
from Server.cli.server_modules import *
from Server.cli.commands import logo
from Server.app.ms.Update_CVE import *

def ch():
    global User

    print(logo)
    print("Updating CVE base")
    Update_CVE_Base()
    print("Creating DB")
    create_db()
    print("Starting app")
    initialize_application()
    cls()
    print(logo)
    print("")
    print("Server started at localhost:8080")
    user = "Admin"
    user_changed = False

    while True:
        if user_changed:
            print(f"Logged in as {user}")
            user_changed = False

        command_input = input(f"{user}@localhost: ")
        command, *args = command_input.split()
        user, user_changed = command_handler(command, user, *args)






def mainserv():
    main_thread = Thread(target=ch)
    main_thread.start()
    time.sleep(2)
    WSGI(NSP)
    log_event("Server started at localhost:8080", npt=1)


if __name__ == '__main__':
    mainserv()