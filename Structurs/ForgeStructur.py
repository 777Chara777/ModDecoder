import json
import zipfile

from .BaseStructur import BaseStructur

class ForgeStructur(BaseStructur):

    @staticmethod
    def get_info_mod(path: str) -> dict:
        ...