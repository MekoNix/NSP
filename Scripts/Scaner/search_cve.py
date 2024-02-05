import json
import re
from packaging import version
from Scripts.modules import find_path
def load_data_from_json(file_path):
    """Загружает данные из JSON файла."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

import json
import re
from packaging import version

def find_affected_cves(data, target_version):
    affected_cves = []
    version_pattern = re.compile(r'(\d+\.\d+)(\.\d+)? (\w+ versions prior to (\d+\.\d+\.\d+)|and prior versions)')

    try:
        target_ver = version.parse(target_version)
    except version.InvalidVersion:
        print(f"Invalid target version: {target_version}")
        return affected_cves

    for cve, versions_info in data.items():
        for version_info in versions_info:
            if 'and prior versions' in version_info:
                base_version = version_info.split(' ')[0]
                try:
                    if target_ver <= version.parse(base_version):
                        affected_cves.append(cve)
                        break
                except version.InvalidVersion:
                    continue  # Пропускаем невалидные версии

            match = version_pattern.search(version_info)
            if match:
                _, _, _, version_to_compare = match.groups()
                try:
                    if version_to_compare and target_ver < version.parse(version_to_compare):
                        affected_cves.append(cve)
                        break
                except version.InvalidVersion:
                    continue  # Пропускаем невалидные версии

    return affected_cves


def scan_db_for_CVE(version):


    data = load_data_from_json(find_path("cve.json"))

    # Пример использования
    target_version = str(version)
    affected_cves = find_affected_cves(data, target_version)
    return affected_cves

def get_cve_score(cve_id):
    file_path=find_path("cve.json")
    with open(file_path, 'r') as file:
        data = json.load(file)
    cve_data = data.get(cve_id)
    if cve_data:
        score_text = cve_data[0]  # Например, "Score: 5.0"
        try:
            score_value = float(score_text.split(": ")[1])
            return score_value
        except (ValueError, IndexError):
            return None
    else:
        return None

def prepare_data(version):
    data = {}
    # Предполагаем, что scan_db_for_CVE(version) возвращает список идентификаторов CVE
    for cve in scan_db_for_CVE(version):
        # Предполагаем, что get_cve_score(cve) возвращает строку с оценкой уязвимости для данного CVE
        score = f"Score: {get_cve_score(cve)} "
        # Создаем строку с ссылкой на дополнительную информацию
        link = f"More info: https://nvd.nist.gov/vuln/detail/{cve}"
        # Обновляем словарь data, добавляя информацию о CVE
        data[cve] = [score, link]

    return data