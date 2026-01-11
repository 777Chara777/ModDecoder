from gui.gui import GUIMain
from decodejar.decodejar import DecodeJar



from Structurs.FabricStructur import FabricStructur
from parser.remapper.download_mapper import downloadMapping
from parser.parser.parser_mapper import ParserMapper
from parser.parser.log_mapper import map_log


from libs.Logger.logger import Logger
from libs.Config import Configuration

import dearpygui.dearpygui as dpg

import argparse
import zipfile
import time
import sys
import os


class APP:
    __version__: str = "1.0.1"

    def __init__(self):
        self.logger = Logger("APP", "./logger.log", GUIMain.set_text)
        self.gui = GUIMain(self.program_start)

        self.parser = ParserMapper()
        self.config = Configuration()
        self.decoder_files = DecodeJar()

        # commands

    def set_level_logger(self, level: str):
        pass

    def generation_api(self, path: str):
        pass

    def cmd(self, commands: str):
        '''Command line arguments'''
        # -l debug > level
        # -g api > gen
        # -m path -> module
        pass

    def build(self):
        '''Builds the GUI'''
        if not self.config.check_config():
            self.config.new_config({"java-path": "java.exe"})
            self.logger.error("Create new config")
            exit(1)
        
        self.gui.gui_builder()

    def create_missing_folders(self, path: str):
        '''Creates missing folders'''
        os.makedirs(path, exist_ok=True)

    def program_start(self, jar: str, path: str):
        '''Starts the program'''
        self.logger.info("Starting the program")


    


if __name__ == "__main__":
    app = APP()
    app.cmd(sys.argv[:1])
    app.build()