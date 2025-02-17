import os
import dearpygui.dearpygui as dpg

# from multiprocessing import Process
# from threading import Thread

from libs.Logger.logger import Logger
from libs.StoppableThread import StoppableThread
from FabricStructur.FabricStructur import FabricStructur

class GUIMain:
    set_text = "Decoder"
    def __init__(self, programm_start):
        self.logger = Logger("GUI")
        self.thread = None
        self.__programm_start = programm_start

    def button_ok(self):
        self.logger.debug("Prees button ok")
        if not os.path.isfile(dpg.get_value("path")) or dpg.get_value("path") == "":
            self.logger.warm("File not found at this path")
            return
        if not os.path.isdir(dpg.get_value("path2")) or dpg.get_value("path2") == "":
            self.logger.warm("File not found at this dir")
            return

        self.update_mod_info(dpg.get_value("path"))

        dpg.show_item("progress")
        dpg.disable_item("super_puper_button")
        # create and start
        # self.__programm_start(dpg.get_value("path"), dpg.get_value("path2"), self.is_stop_thread)
        self.thread = StoppableThread(target=self.__programm_start, args=(dpg.get_value("path"), dpg.get_value("path2"),))
        self.thread.start()

    def button_cancel(self):
        self.logger.debug("Prees button Cancel")
        dpg.hide_item("progress")
        dpg.set_value("progress_bar", 0)
        dpg.set_value("time_death", "0/0 0s")
        dpg.enable_item("super_puper_button")
        if self.thread is not None and self.thread.is_alive():
            self.thread.stop()
            # self.is_stop_thread = True

    @staticmethod
    def set_text(text:str):
        pass
        # if dpg.does_item_exist("out_put_text"):
        #     if len(text) // 50 >= 1:
        #         for num in range(len(text) // 50):
        #             num += 1
        #             text = text[:num*50] + "\n" + text[num*50:]

        #     if len(dpg.get_value("out_put_text")) != 0:
        #         msg = dpg.get_value("out_put_text") + f"\n{text}"
        #     else: msg = text
            
        #     dpg.set_value("out_put_text", msg)

    def _callback(self, sender, app_data, user_data):
        if os.path.isfile(app_data["file_path_name"]):
            dpg.set_value("path", app_data["file_path_name"])

            self.update_mod_info(app_data["file_path_name"])
    def _callback2(self, sender, app_data):
        dpg.set_value("path2", app_data['file_path_name'])

    def _center_item(self, item_id, parent_id):
        # Получаем размеры родительского окна
        parent_width = dpg.get_item_width(parent_id)
        parent_height = dpg.get_item_height(parent_id)

        # Получаем размеры элемента
        item_width = dpg.get_item_width(item_id)
        item_height = dpg.get_item_height(item_id)
        # print(item_width, item_height)

        # Вычисляем позицию для размещения элемента по центру
        center_x = (parent_width - item_width) // 2
        center_y = (parent_height - item_height) // 2

        # Устанавливаем позицию элемента
        dpg.set_item_pos(item_id, [center_x, center_y])

    def _degub(self):
        # debug
        dpg.show_item_registry()
        # dpg.show_metrics()
        dpg.show_style_editor()

    def update_mod_info(self, path:str):
        data_fabric_config = FabricStructur.get_info_mod(path)
        dpg.set_value("info", f"Name: {data_fabric_config[ 'name' ]}\nVersion: {data_fabric_config[ 'version' ]}\nMinecraftV: {data_fabric_config[ 'depends' ][ 'minecraft' ]}")
    
    def gui_builder(self):
        dpg.create_context()

        self.logger.debug("Create GUI")
          
        # dialog windows
        with dpg.file_dialog( directory_selector=False, show=False, callback=self._callback, id="file_dialog_id", width=700, height=400 ):
            dpg.add_file_extension(".jar", custom_text="[Java]", color=(0,255,0))
        dpg.add_file_dialog( directory_selector=True, show=False, callback=self._callback2, tag="dir_dialog_id", width=700, height=400 )

        
        with dpg.window(label="Decoder", width=800, height=600) as main_manu_window:
            with dpg.child_window(height=300, width=400, border=False) as dadadan:
                dpg.add_text("java file")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(tag="path", width=250)
                    dpg.add_button(label="Select", callback=lambda : dpg.show_item("file_dialog_id"), width=-1)

                dpg.add_text("output derectory")
                with dpg.group(horizontal=True):
                    dpg.add_input_text(tag="path2", width=250)
                    dpg.add_button(label="Select", callback=lambda : dpg.show_item("dir_dialog_id"), width=-1)

                with dpg.child_window(border=True, height=100, width=400):
                    with dpg.group():
                        with dpg.group(horizontal=True, indent=38):
                            dpg.add_button(label="Ok", callback=self.button_ok, width=150, tag="super_puper_button")
                            dpg.add_button(label="Cancel", callback=lambda: dpg.destroy_context(), width=150)
                        dpg.add_text(tag="info", show_label=True)

        with dpg.window(label="Progress", width=300, height=100, show=False, tag="progress", no_close=True):
            with dpg.group(horizontal=True):
                dpg.add_progress_bar(tag="progress_bar", width=180, label="0/0 0s")
                dpg.add_text(tag="time_death", default_value="0/0 0s")
            dpg.add_button(label="Cancel", callback=self.button_cancel, width=-1)

        self._center_item(dadadan, main_manu_window)

        dpg.create_viewport(title="Decoder", width=800, height=600, decorated=True)
        dpg.set_viewport_resizable(False)

        dpg.setup_dearpygui()
        dpg.show_viewport()

        # Аааа disable
        dpg.set_primary_window(window=main_manu_window, value=True)

        dpg.start_dearpygui()
        dpg.destroy_context()

