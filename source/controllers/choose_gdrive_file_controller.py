from functools import partial

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog

import views.choose_gdrive_file_widget as choose_gdrive_file_widget
import controllers.gdrive_table_controller as gdrive_table_controller
import file_handler

class ChooseGDriveFileController(QObject):

    did_select_file = pyqtSignal(file_handler.File, str)
    did_cancel = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._table_controller = gdrive_table_controller.GDriveTableController()
        self.view = choose_gdrive_file_widget.ChooseGDriveFileWidget(self._table_controller.table_view)

        self._connect_signals()

        self._update_led_file_path()

    def _connect_signals(self):
        self.view.btnBack.clicked.connect(self._table_controller.go_back)
        self.view.btnSelect.clicked.connect(self._did_press_select_button)
        self.view.btnCancel.clicked.connect(self._did_press_cancel_button)
        # self.view.lblInfo
        self._table_controller.did_change_path.connect(partial(self._update_led_file_path))

    def _get_current_path_str(self):
        file_path = ""
        for file in self._table_controller.path:
            file_path = file_path + file.name + "/"
        file_path = file_path[:-1]
        return file_path

    def _update_led_file_path(self):
        file_path = self._get_current_path_str()
        self.view.ledFilePath.setText(file_path)

    def _did_press_select_button(self):
        selected_file = self._table_controller.path[-1]
        file_path = self._get_current_path_str()
        self.did_select_file.emit(selected_file, file_path)
        if self.view.parentWidget() and type(self.view.parentWidget()) == QDialog:
            self.view.parentWidget().accept()
    
    def _did_press_cancel_button(self):
        if self.view.parentWidget() and type(self.view.parentWidget()) == QDialog:
            self.view.parentWidget().reject()
    
