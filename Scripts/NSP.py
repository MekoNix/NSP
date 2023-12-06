

def time_spent(func): # Функция для отчёта времени, после потребуеться для отчёта. TIMEIT НЕ РАБОТЕТ!
    start_time=time.time()
    func
    end_time=time.time()
    execution_time=end_time-start_time
    return execution_time
# не работает выводит 0.0 времени.

def cve_search(ver):# Поиск CVE по версии MongoDb на сайте. Если есть то функция вернёт True иначе False
    url=f"http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=mongodb+{ver}"
    response= requests.get(url)
    response.raise_for_status()
    target="CVE"

    pars=BeautifulSoup(response.text,'html.parser')
    found_text=pars.find(string=lambda text: target.lower() in text.lower() )
    if found_text:
        return True
    else:
        return False


def check_mongodb_ver(host,port): # Поиск версии MongoDB опрашивая сервер и проверка на CVE для этой версии
    try:
        target = MongoClient(host,port)
        server_info=target.server_info()
        print(f"MongoDB Server Version {server_info['version']}")
        cve_search(server_info['version'])
    except pymongo.errors.ConnectionFailure:
        print(f"{Fore.RED}[-] {Style.RESET_ALL}Cannot connect to MongoDB")
    finally:
        target.close()

def main_console():
    from tqdm import tqdm
    import os
    from colorama import Fore, Back, Style
    import requests
    import flask
    from fpdf import FPDF
    import nmap
    import pymongo
    from pymongo import MongoClient
    from bs4 import BeautifulSoup
    import time
    print("Starting CVE Search... ")
    timesp=time_spent(cve_search("1.5"))
    print(f"CVE Search compite. Total time {timesp} ")



