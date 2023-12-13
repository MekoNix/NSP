import logging
from datetime import datetime
import os
logpy_dir=os.path.dirname(os.path.abspath(__file__)) #Определяем папку с файлом log.py
start_dir=os.path.dirname(logpy_dir)#Определяем папку с проектом
logging.basicConfig(filename=start_dir+'/logs/NSP_log.log', format="%(levelname)s: %(asctime)s: %(message)s",level=logging.INFO,datefmt="%Y-%m-%d %H:%M:%S")
def log_event(event,level):
    if level == "info":
        logging.info(event)
    else:
        logging.warning(event)