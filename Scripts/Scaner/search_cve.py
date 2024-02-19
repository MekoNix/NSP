import json
import re
from packaging import version
from Scripts.modules import find_path
from Server.app.ms.profiler import profiler


def load_data_from_json(file_path):
    """Загружает данные из JSON файла."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def find_affected_cves(data, target_version):
    affected_cves = []
    # Обновленный шаблон для поиска информации о версиях
    version_pattern = re.compile(r'(\d+\.\d+\.\d+) (affects|and prior versions)')

    try:
        target_ver = version.parse(target_version)
    except version.InvalidVersion:
        print(f"Invalid target version: {target_version}")
        return affected_cves

    for cve, versions_info in data.items():
        for version_info in versions_info:
            match = version_pattern.search(version_info)
            if match:
                base_version, relation = match.groups()
                try:
                    base_ver = version.parse(base_version)
                    # Если уязвимость относится к версии равной или более новой, чем целевая версия,
                    # и указано, что она влияет на предыдущие версии, добавляем CVE в список
                    if target_ver <= base_ver and relation == 'and prior versions':
                        affected_cves.append(cve)
                        break
                    elif relation == 'affects' and target_ver == base_ver:
                        # Если уязвимость явно указывает на целевую версию
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
    file_path = find_path("cve.json")
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


def score_analys(who_req, score):
    p = profiler(find_path(f"{who_req}", ndir=1))
    if score > 7.0:
        p.plus_value(key="red", amount=1)
    if 7.0 < score > 4.0:
        p.plus_value(key="yellow", amount=1)
    else:
        p.plus_value(key="green", amount=1)


def prepare_data(version, who_req):
    data = {}
    p = profiler(find_path(f"{who_req}", ndir=1))
    p.plus_value(key="Total_scan", amount=1)

    if scan_db_for_CVE(version) == []:
        data = "CVE NOT FOUND"
        return data
    for cve in scan_db_for_CVE(version):
        score_analys(who_req, get_cve_score(cve))
        score = f"Score: {get_cve_score(cve)} "
        link = f"More info: https://nvd.nist.gov/vuln/detail/{cve}"
        data[cve] = [score, link]

    return data
