import os.path
from functools import partial

from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import views.upload_widget as upload_widget
import controllers.choose_gdrive_file_controller as choose_gdrive_file_controller
import file_handler
import user_data_manager

class UploadController:

    _user_data_manager = user_data_manager.UserDataManager()
    
    def __init__(self):
        super().__init__()
        self.view = upload_widget.UploadWidget()
        self.thread = None
        self._connect_signals()
        self._set_gui_upload_mode(False)
        self._set_gdrive_and_local_paths()

    def _connect_signals(self):
        self.view.btnFilePath.clicked.connect(partial(self._choose_file_path))
        self.view.btnFolderPath.clicked.connect(partial(self._choose_folder_path))
        self.view.btnDrivePath.clicked.connect(partial(self._choose_drive_path))
        self.view.btnUpload.clicked.connect(partial(self._upload_file))
        self.view.btnCancel.clicked.connect(partial(self._cancel_upload))

    def _set_gdrive_and_local_paths(self):
        local_path = self._user_data_manager.get_last_upload_local_path()
        gdrive_path = self._user_data_manager.get_last_upload_gdrive_path()
        self._gdrive_upload_file = self._user_data_manager.get_last_upload_gdrive_file()

        if not local_path:
            local_path = ""

        if not gdrive_path or not self._gdrive_upload_file:
            self._gdrive_upload_file = file_handler.get_gdrive_file("root")
            gdrive_path = self._gdrive_upload_file.name

        self.view.ledFilePath.setText(local_path)
        self.view.ledDrivePath.setText(gdrive_path)

    def _choose_file_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setWindowTitle("Choose File")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self.view.ledFilePath.setText(path)
        return

    def _choose_folder_path(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setWindowTitle("Choose Folder")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self.view.ledFilePath.setText(path)
        return

    def _choose_drive_path(self):
        gdrive_controller = choose_gdrive_file_controller.ChooseGDriveFileController()

        def did_select_gdrive_path(file, path):
            if path:
                self.view.ledDrivePath.setText(path)
            if file:
                self._gdrive_upload_file = file

        gdrive_controller.did_select_file.connect(did_select_gdrive_path)
        self._gdrive_dialog = QDialog()
        layout = QVBoxLayout()
        layout.addWidget(gdrive_controller.view)
        self._gdrive_dialog.setLayout(layout)
        self._gdrive_dialog.setFixedWidth(600)
        self._gdrive_dialog.setWindowTitle("Select Google Drive Path")
        self._gdrive_dialog.exec()

        return
    
    def _upload_file(self):
        path = self.view.ledFilePath.text()
        if os.path.exists(path):
            self.view.lblStatus.setText("Preparing...")
            self.view.pbrStatus.setValue(0)
            self._set_gui_upload_mode(True)

            self._user_data_manager.set_last_upload_local_path(path)
            self._user_data_manager.set_last_upload_gdrive_path(self.view.ledDrivePath.text())
            self._user_data_manager.set_last_upload_gdrive_file(self._gdrive_upload_file)

            if not self.thread:
                def thread_has_finished():
                    self._set_gui_upload_mode(False)

                self.thread = UploadThread()
                self.thread.status_update.connect(self.view.lblStatus.setText)
                self.thread.progress_update.connect(self.view.pbrStatus.setValue)
                self.thread.error_occurred.connect(partial(self.app.show_error_message))
                self.thread.finished.connect(partial(thread_has_finished))

            self.thread.path = path
            self.thread.upload_parents_id = [self._gdrive_upload_file.id]
            self.thread.should_zip = os.path.isdir(path)
            self.thread.start()

        else:
            warnMsg = QMessageBox(QMessageBox.Warning, "Warning", "The local file or folder path is invalid.", QMessageBox.Ok)
            warnMsg.exec()
        return

    def _cancel_upload(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop = True
            self.view.btnCancel.setEnabled(False)
            self.view.lblStatus.setText("Canceling the upload...")

    def _set_gui_upload_mode(self, upload_mode):
        self.view.ledFilePath.setEnabled(not upload_mode)
        self.view.ledDrivePath.setEnabled(not upload_mode)
        self.view.btnFilePath.setEnabled(not upload_mode)
        self.view.btnFolderPath.setEnabled(not upload_mode)
        self.view.btnDrivePath.setEnabled(not upload_mode)
        self.view.btnCancel.setEnabled(upload_mode)
        self.view.btnUpload.setEnabled(not upload_mode)

class UploadThread(QThread):

    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    error_occurred = pyqtSignal(Exception)
    upload_parents_id = None
    should_zip = False
    stop = False

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            if self.should_zip:
                self.path = file_handler.zip_file(self.path)
            for status_msg, progress in file_handler.upload(self.path, self.upload_parents_id):
                self.progress_update.emit(progress)
                self.status_update.emit(status_msg)
                if self.stop:
                    self.status_update.emit("The upload was canceled")
                    self.progress_update.emit(0)
                    self.stop = False
                    break
            if self.should_zip:
                file_handler.clear_temporary_files()
        except Exception as error:
            self.error_occurred.emit(error)
            self.status_update.emit("An error occurred. The upload was interrupted")
    

