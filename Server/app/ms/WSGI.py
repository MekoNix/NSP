import os
from Server.app.app import app  # импортируйте ваше Flask-приложение

def WSGI():
    if os.name == 'nt':  # Windows
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    else:  # Unix/Linux
        from gunicorn.app.base import BaseApplication

        class Application(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super(Application, self).__init__()

            def load_config(self):
                config = {key: value for key, value in self.options.items()
                          if key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': '0.0.0.0:8080',
            'workers': 4,
        }
        Application(app, options).run()
WSGI()