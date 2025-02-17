from gui.gui import GUIMain
from decodejar.decodejar import DecodeJar

from FabricStructur.FabricStructur import FabricStructur
from parser.remapper.download_mapper import downloadMapping
from parser.parser.parser_mapper import ParserMapper
from parser.parser.log_mapper import map_log


from libs.Logger.logger import Logger
from libs.Config import Configuration

import dearpygui.dearpygui as dpg

import zipfile
import time
import os

class APP:
    def __init__(self):
        self.logger = Logger("APP", "./logger.log", GUIMain.set_text)
        self.gui = GUIMain(self.programm_start)

        self.parser = ParserMapper()
        self.config = Configuration()
        self.decoder_files = DecodeJar()

        self.__temp_path = "Temp/"

    def build(self):
        if not self.config.check_config():
            self.config.new_config({"java-path": "java.exe"})
            self.logger.error("Create new config")
            exit(1)

        self.gui.gui_builder()

    def create_missing_folders(self, path: str):
        # Разделяем путь на список каталогов
        folders = path.split(os.path.sep)

        # Проверяем каждый каталог в пути
        current_path = ''
        for folder in folders:
            current_path = os.path.join(current_path, folder)
            # Если текущий каталог не существует, создаем его
            if not os.path.exists(current_path):
                os.makedirs(current_path)

    def programm_start(self, jar: str, path: str):
        self.logger.info("Wow start programm wow")

        mod_path = self.__temp_path + jar.split("\\")[-1]
        mod_name = jar.split("\\")[-1].replace(".jar", "")
        
        self.logger.info("Decoding jar file....")
        te_ = time.time()
        if not os.path.isfile(mod_path):
            DecodeJar.decode_file(jar, self.__temp_path, self.config.load_config()['java-path'])
        self.logger.info(f"Decoding jar file end at {time.time() - te_}")


        config_fabric: dict = FabricStructur.get_info_mod(jar)

        minecraft_version = config_fabric['depends']['minecraft'].replace(">", "").replace("<", "").replace("*", "").replace("=", "").replace("~", "")
        path_mapper = f"./Temp/{minecraft_version}.tini"

        self.logger.info(f"Download mapper version: {minecraft_version}.tini")
        if not os.path.isfile(path_mapper):
            open( path_mapper, "w", encoding="utf-8" ).write(downloadMapping(minecraft_version))
        self.logger.info("Create Mapper")

        mapper = ParserMapper().parser(path_mapper)

        with zipfile.ZipFile(mod_path, 'r') as mod:
            path_to_dir = config_fabric['entrypoints']['main'][0].split(".")[0]

            all_entries = mod.namelist()

            # Фильтруем только файлы из нужной директории
            target_directory = f"{path_to_dir}/"
            files_in_directory: list[str] = [entry for entry in all_entries if entry.startswith(target_directory) and not entry.endswith('/')]
            # with zipfile.ZipFile(mod_path + f"/{path_to_dir}/", 'r') as mod_decode:
            n = len(files_in_directory)
            self.logger.info("Decoding Progress...")
            for d, zfile in enumerate(files_in_directory):

                time_st = time.time()

                funny_der = zfile.split("/")[:-1]
                self.create_missing_folders(f"{path}/{mod_name}/{ '/'.join(funny_der) }")

                data_text = mod.open(zfile, 'r').read().decode("utf-8")
                # self.logger.debug("funny " + data_text.replace("\n", ""))
                data = map_log(data_text, mapper)
                open(f"{path}/{mod_name}/{zfile}", "w", encoding="utf-8").write( data.replace("\n", "") )

                dpg.set_value("progress_bar", (d+1)/n)
                dpg.set_value("time_death", f"{d}/{n} {int( (n-d) * (time.time()-time_st)  )}s")

            dpg.hide_item("progress")
            dpg.enable_item("super_puper_button")
        
        
        self.logger.info("Decoding Progress Done :0")
        os.remove(mod_path)
            


if __name__ == "__main__":
    APP().build()