import json
from ..objects import Settings
import os

class SettingsService:
    def __init__(self, ROOT_DIR, settings_path="data/settings.json"):
        self.ROOT_DIR = ROOT_DIR 
        self.SETTINGS_PATH = os.path.join(self.ROOT_DIR, settings_path)
        self.settings = Settings.Settings(self.SETTINGS_PATH)

    def get(self):
        return json.dumps(self.settings)

