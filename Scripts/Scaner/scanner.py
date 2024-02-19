from Scripts.modules import *
from pymongo import MongoClient
from Server.app.ms.html_editor import HTMLPageModifier
from Scripts.Scaner.search_cve import *
from Scripts.Scaner.modules.loader import Mod


class Scanner(HTMLPageModifier, Mod):
    def __init__(self, login, password, host, port, who_req, title, comment):
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.who_req = who_req
        self.version = self.get_mongodb_version()
        self.title = title
        self.comment = comment
        self.body_content = []
        self.background_color = "#343541"

    def get_mongodb_version(self):
        try:
            if self.password == "":
                client = MongoClient(self.host, int(self.port))
                build_info = client.admin.command('buildInfo')
                version = build_info['version']
                return version
            else:
                con_info = f"mongodb://{self.login}:{self.password}@{self.host}:{self.port}"
                client = MongoClient(con_info)
                build_info = client.admin.command('buildInfo')
                version = build_info['version']
                return version
        except Exception as e:

            return e

    def scan(self):
        mod = Mod(host=self.host, login=self.login, port=self.port, pas=self.password, who_req=self.who_req)
        data = prepare_data(self.version, self.who_req)
        data_from_mod = mod.survey_modules()

        self.report(data, data_from_mod)

    def report(self, data, data_from_mod):
        self.add_header(scan_host=self.host, created_by=self.who_req)
        self.add_text_block(f"Comment: {self.comment}", font_weight="bold")
        self.add_text_block("")
        self.add_large_center_text("CVE BASE SEARCH")
        if data == "CVE NOT FOUND":
            self.add_large_center_text("УЯЗВИМОСТИ НЕ НАЙДЕНЫ!", text_color="#00FF00")
        else:
            for key, value in data.items():
                self.add_text_block(f"{key}", font_weight="bold")
                for text in value:
                    self.add_text_block(f"{text}")
        for mod, texts in data_from_mod.items():
            self.add_large_center_text(text=f"Data from module: {mod}")
            if isinstance(texts, list):
                for text in texts:
                    self.add_text_block(text=text)
            else:
                self.add_text_block(text=str(texts))
        self.save_to_file(filepath=find_path(str(self.who_req), ndir=1) + f"/{self.title}.html")
