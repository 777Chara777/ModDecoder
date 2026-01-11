import json
import os

class Configuration:
    def __init__(self, derictory: str = "./config.json"):
        self.derictory = derictory

    def check_config(self) -> bool:
        return os.path.isfile(self.derictory)

    def new_config(self, data: dict):
        self.update_config(data)

    def update_config(self, data):
        with open(self.derictory, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_config(self):
        with open(self.derictory, encoding="utf-8") as config_file:
            data = json.load(config_file)
        return data



