import importlib.util
import os


class Mod:
    def __init__(self, host, login, pas, port, who_req):
        self.host = host
        self.login = login
        self.pas = pas
        self.port = port
        self.who_req = who_req

    def load_module(self, module_name, path):
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def survey_modules(self, ):
        # Определяем абсолютный путь к директории скрипта
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Строим путь к папке modules
        data = {}

        # Проверяем, существует ли папка modules

        for filename in os.listdir(script_dir):
            if filename.endswith('.py') and filename != "loader.py":
                path = os.path.join(script_dir, filename)
                module_name = filename[:-3]  # Удаляем расширение .py
                module = self.load_module(module_name, path)

                if hasattr(module, 'get_text') and callable(module.get_text):
                    text_output = module.get_text(self.host, self.login, self.pas, self.port, self.who_req)
                    # Разделяем вывод на отдельные строки
                    separated_output = text_output.strip().split('\n')
                    # Сохраняем список строк вместо одной длинной строки
                    data[module_name] = separated_output

        return data
