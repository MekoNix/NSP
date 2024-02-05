import requests
from bs4 import BeautifulSoup
import json
import re
from Scripts.modules import find_path

def parse_cve_versions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, что запрос выполнен успешно
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ищем все блоки данных о уязвимостях
        vulnerability_blocks = soup.find_all('div', class_='fl-column fl-justify-between fl-1')

        cve_versions = {}
        # Регулярное выражение для поиска версий
        version_regex = re.compile(r'\d+(\.\d+)+')

        for block in vulnerability_blocks:
            # Находим элемент с информацией о CVE
            cve_element = block.find('div', class_='AlertsCardGrid__Eyebrow-sc-8sd2rs-2 najyN fnt-14')
            # Находим элемент с оценкой уязвимости
            score_element = block.find('div', class_='AlertsCardGrid__ScoreBox-sc-8sd2rs-4')
            if cve_element and score_element:
                cve_text = cve_element.get_text().strip()
                # Извлекаем значение оценки из элементов <small> и <b>
                score_value = score_element.find('small').find('b').get_text().strip()

                # Ищем блоки с версиями, следующие за блоком с CVE
                versions = ["Score: " + score_value]  # Добавляем оценку уязвимости в список версий
                version_elements = block.find_all('span')  # Получаем все span, предполагая, что они содержат версии
                for version_element in version_elements:
                    version_text = version_element.get_text().strip()
                    if version_regex.search(version_text):  # Если строка соответствует формату версии
                        versions.append(version_text)  # Добавляем текст версии в список

                if versions:
                    cve_versions[cve_text] = versions

        return json.dumps(cve_versions, indent=2)
    except requests.RequestException as e:
        return json.dumps({"error": str(e)}, indent=2)

def Update_CVE_Base():
    url = 'https://www.mongodb.com/alerts'
    cve_data_json = parse_cve_versions(url)

    file_path = find_path("static", ndir=1) + "/cve.json"
    with open(file_path, 'w') as file:
        file.write(cve_data_json)

    print('Data has been updated')

Update_CVE_Base()