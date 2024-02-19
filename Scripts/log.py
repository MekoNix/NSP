import logging
import os
from datetime import datetime
from Scripts.modules import find_path

cur_date = datetime.now()
form_date = cur_date.strftime("%d.%m.%Y")
name = find_path(nroot=1) + f'/logs/{form_date}.log'
logging.basicConfig(filename=name, format="%(levelname)s: %(asctime)s: %(message)s", level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")


def log_event(event, level="info",
              npt=0):  # event- событие которое нужно логировать, level - уровень события, npt - нужен ли print события
    if npt == 1:
        print(event)
    if level == "info":
        logging.info(event)
    else:
        logging.warning(event)
