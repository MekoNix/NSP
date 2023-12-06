# Установка модулей с прогресс баром чтобы было не скучно и красиво.
import os
import time
from Scripts.menu import *


def modules_install():
    try:
        from tqdm import tqdm
        import colorama
        import requests
        import flask
        from fpdf import FPDF
        import nmap
        import pymongo
        from bs4 import BeautifulSoup
    except ModuleNotFoundError:
        # В README написать как обновить pip "python.exe -m pip install --upgrade pip"
        listm = ["tqdm", 'colorama', 'requests', 'flask', 'fpdf', 'python-nmap', 'pymongo', 'bs4']
        print("Модули не установленны,начниаем установку...")
        time.sleep(0.5)
        bar = tqdm(listm, desc="Установка модуля", unit="bit", colour='cyan')
        for md in bar:
            os.system(f"pip install {md} --quiet")
            bar.set_description(desc=f"Установка {md}")
        if menu_start() == 1:
            from Scripts.NSP import *
            exit()
        else:
            from Server.server import *
            exit()


modules_install()
