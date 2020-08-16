from functools import partial
from enum import Enum
from typing import List

from PyQt5.QtWidgets import QTableView, QDialog, QVBoxLayout, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QThread, pyqtSignal, QObject, Qt

import views.gdrive_table_model as gdrive_table_model
import file_handler

class GDriveTableController(QObject):

    did_change_path = pyqtSignal()

    def __init__(self, folder_id="root"):
        super().__init__()
        self._file_thread = None
        self.table_view = QTableView()
        self.files = []
        self._model = gdrive_table_model.GDriveTableModel()
        self.table_view.setModel(self._model)
        self._set_table_view_style()
        self._connect_table_view_signals()
        self._update_files(folder_id)
        self.path = [file_handler.get_gdrive_file(folder_id)]

    def _set_table_view_style(self):
        self.table_view.verticalHeader().hide()
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setShowGrid(False)
        self.table_view.setUpdatesEnabled(True)

        vertical_header = self.table_view.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(24)

        horizontal_header = self.table_view.horizontalHeader()
        horizontal_header.setHighlightSections(False)
        # horizontal_header.setSectionResizeMode()

    def _connect_table_view_signals(self):
        selectionModel = self.table_view.selectionModel()
        selectionModel.currentRowChanged.connect(self.did_select_row_index)

        self.table_view.doubleClicked.connect(self.did_double_click_row_index)

    def _update_files(self, folder_id):

        def did_get_files(files):
            self.files = files
            self._model.load_files(self.files)
            self.table_view.viewport().update()
            self._set_loading_mode(False)

        def error_occurred(error):
            print(error)

        if self._file_thread == None:
            self._file_thread = FileThread()
            self._file_thread.did_get_files.connect(did_get_files)
            self._file_thread.error_occurred.connect(error_occurred)

        self._file_thread.file_id = folder_id
        self._set_loading_mode(True)
        self._file_thread.run()

    def _set_loading_mode(self, is_loading):
        if is_loading:
            self.table_view.setEnabled(False)
        else :
            self.table_view.setEnabled(True)

    def did_double_click_row_index(self, index):
        row = index.row()
        file = self.files[row]
        if file.is_folder:
            self.path.append(file)
            self._update_files(str(file.id))
            self.table_view.clearSelection()
            self.did_change_path.emit()

    def did_select_row_index(self, index):
        row = index.row()
        # print("row changed to " + str(row))

    def go_back(self):
        if len(self.path) > 1:
            self.path.pop()
            self._update_files(str(self.path[-1].id))
            self.table_view.clearSelection()
            self.did_change_path.emit()
    
class FileThread(QThread):

    error_occurred = pyqtSignal(Exception)
    did_get_files = pyqtSignal(list)

    def run(self):
        try:
            files = file_handler.get_gdrive_file_children(self.file_id)
            self.did_get_files.emit(files)
        except Exception as error:
            print(error)
            self.error_occurred.emit(error)