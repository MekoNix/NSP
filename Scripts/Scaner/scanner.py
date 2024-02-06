
from Scripts.modules import *
from pymongo import MongoClient
from Server.app.ms.html_editor import HTMLPageModifier
from Scripts.Scaner.search_cve import *

class Scanner(HTMLPageModifier):
    def __init__(self,login,password,host,port,who_req,title,comment):
        self.login=login
        self.password=password
        self.host=host
        self.port=port
        self.who_req=who_req
        self.version="4.6.5"
        self.title=title
        self.comment=comment
        self.body_content = []
        self.background_color = "#343541"

    def get_mongodb_version(self):
        try:
            con_info=f"mongodb://{self.login}:{self.password}@{self.host}:{self.port}"
            client = MongoClient(con_info)
            build_info = client.admin.command('buildInfo')
            self.version=build_info['version']
        except Exception as e:

            return e
    def scan(self):
        data=prepare_data(self.version,self.who_req)
        self.report(data)

    def report(self,data):
        self.add_header(scan_host=self.host,created_by=self.who_req)
        self.add_text_block(f"Comment: {self.comment}",font_weight="bold")
        self.add_text_block("")
        for key, value in data.items():

            self.add_text_block(f"{key}",font_weight="bold")
            for text in value:
                self.add_text_block(f"{text}")
        self.save_to_file(filepath=find_path(str(self.who_req),ndir=1)+f"/{self.title}.html")




