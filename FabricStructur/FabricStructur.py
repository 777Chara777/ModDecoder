import json
import zipfile

class FabricStructur:
    @staticmethod
    def get_info_mod(path: str) -> dict:
        with zipfile.ZipFile(path, 'r') as mod:
                with mod.open("fabric.mod.json", 'r') as fabric_config:
                    return json.loads(fabric_config.read())