from Scripts.log import *
from Scripts.modules import *
from pymongo import MongoClient


def credentials_check(host):
    host = pars_json("Host", host)
    port = int(pars_json("Port", host))
    username = pars_json("User", host)
    password = pars_json("Password", host)
    authSource = pars_json("authSource", host)
    try:
        MongoClient(host=host, port=port, username=username, password=password, authSource=authSource)
    except Exception as e:
        log_event("Неверный пароль или пользователь. Пожалуйста, проверьте правильность введенных данных и повторите попытку.",'Warning',npt=1)


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

def found_CVE_by_ver(ver):
    found=[]
    cve=find_path("cve.json")
    with open(cve, 'r') as file:
        cve_data = json.load(file)
    for cve, versions in cve_data.items():
        if ver in versions:
            found.append(cve)
    return found