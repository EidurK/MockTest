import json

class Settings:
    def __init__(self, settings_path):
        self.read_file(settings_path)

    def read_file(self, settings_path):
        with open(settings_path, 'r') as f:
            self.setting = json.load(f)

    def get(self, name):
        return self.setting.get(name)

    def set(self, name, value):
        self.setting[name] = value



