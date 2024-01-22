from Scripts.log import *
from Scripts.modules import *
from pymongo import MongoClient
from Server.cli.report import *

def find_cve_by_version_in_file(version, file_path):
        CVEs=[]
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        for cve, versions in json_data.items():
            if version in versions:
                CVEs.append(cve)
        return cve_preforme(CVEs)

def cve_preforme(CVE_List):
    if not CVE_List:
        print("Gecnjq")
    cve_data={cve: f" More info: https://nvd.nist.gov/vuln/detail/{cve}" for cve in CVE_List}
    return cve_data
def get_mongodb_version(host,port,login,password):
    try:
        con_info=f"mongodb://{login}:{password}@{host}:{port}"
        client = MongoClient(con_info)
        build_info = client.admin.command('buildInfo')
        return build_info['version']
    except Exception as e:
        log_event(e, 'WARNING', npt=1)
        return e

def Light_Scanner(host,port,login,password):
    try:
        MongoDB_Version=str(get_mongodb_version(host,port,login,password))
        Found_CVE=pars_json(MongoDB_Version,find_path("cve"))
    except Exception as e:
        log_event(e,'WARNING',npt=1)
        return e
#print(get_mongodb_version(host="127.0.0.0",port="27017"))


def wsgi_test(host,user):
    create_pdf_report(host=host, key_value_pairs=find_cve_by_version_in_file("4.4.1", find_path("cve.json")),user=user) #ВНИМАНИЕ ПОМЕНЯТЬ ВЕРСИЮ НА get_mongodb_version
