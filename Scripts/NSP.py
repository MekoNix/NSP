from Scripts.modules import server_ping
from Scripts.log import *
from colorama import Fore
def main(host):
    host=str(host)
    if not server_ping(host):
        print(Fore.Red+"Не возможно соединиься с сервером")
        log_event("Не возможно соединиься с сервером","Warning")
