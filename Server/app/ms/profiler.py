import json
import datetime
from Scripts.modules import find_path

class profiler():
    def __init__(self, filename=None):
        self.filename = filename
        if filename:
            self.data=self.load_data()
        else:
            current_time = datetime.datetime.now()
            self.data = {
                "Creation_date": current_time.date().isoformat(),
                "Last_scan": current_time.isoformat(),
                "Total_scan": 0,
                "red": 0,
                "yellow": 0,
                "green": 0
            }

    def load_data(self):
        try:
            with open(self.filename+"/pf.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename+"/pf.json", 'w') as file:
            json.dump(self.data, file, indent=4)

    def update(self, key, new_value):
        self.data["Last_scan"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if key in self.data:
            self.data[key] = new_value
        else:
            for sub_key, sub_value in self.data.items():
                if isinstance(sub_value, dict):
                    if self.update_value_in_dict(sub_value, key, new_value):
                        break
        self.save_data()

    def plus_value(self,key, amount=1):
        self.load_data()
        if key in self.data:
            self.data[key] += amount
        else:
            print("Key not found: %s" % key)
        self.save_data()

    def create_file(self, username):
        self.filename = find_path(f"{username}",ndir=1)
        self.save_data()