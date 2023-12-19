from Scripts.log import *
from Scripts.modules import *
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

def db_ver(host):

    host = pars_json("Host",host)
    port = int(pars_json("Port",host))
    username=pars_json("User",host)
    password=pars_json("Password",host)
    authSource=pars_json("authSource",host)

    mongo_client = MongoClient(host=host, port=port,username=username,password=password,authSource=authSource)

    server_info = mongo_client.server_info()

    print(f"Версия MongoDB: {server_info['version']}")
    return server_info['version']

def pars_ver():
    url="https://www.mongodb.com/alerts"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        cve_elements = soup.find_all('strong')  # Ищем все теги <strong>

        for cve_element in cve_elements:
            cve = cve_element.text.strip()

            # Ищем следующий элемент <p> с нужным классом
            versions_block = cve_element.find_next('p', class_='m-t-0 m-b-10')

            if versions_block:
                # Извлекаем текст из всех тегов <span> внутри блока версий
                versions_list = [span.text.strip() for span in versions_block.find_all('span')]

                # Вывод списка
                if versions_list:
                    print(f'CVE: {cve}')
                    for version in versions_list:
                        print(f'  - {version}')
            else:
                print(f'Для CVE {cve} не найден блок с версиями.')
    else:
        print(f'Ошибка при получении страницы. Код статуса: {response.status_code}')