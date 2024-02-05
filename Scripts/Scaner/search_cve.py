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

