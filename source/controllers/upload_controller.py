import os.path

from functools import partial
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import views.upload_widget as upload_widget
import file_handler

class UploadController:
    
    def __init__(self):
        super().__init__()
        self.view = upload_widget.UploadWidget()
        self.thread = None
        self._connectSignals()

        self.view.cbxCompress.setChecked(True)
        self.view.cbxCompress.setEnabled(False)
        self.view.cbxReplace.setEnabled(False)

        self.view.btnCancel.setEnabled(False)

    def _connectSignals(self):
        self.view.btnFilePath.clicked.connect(partial(self._chooseFilePath))
        self.view.btnFolderPath.clicked.connect(partial(self._chooseFolderPath))
        self.view.btnDrivePath.clicked.connect(partial(self._chooseDrivePath))
        self.view.btnUpload.clicked.connect(partial(self._uploadFile))

    def _chooseFilePath(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setWindowTitle("Choose File")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self.view.ledFilePath.setText(path)
        return

    def _chooseFolderPath(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setWindowTitle("Choose Folder")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self.view.ledFilePath.setText(path)
        return

    def _chooseDrivePath(self):
        # self.view.ledDrivePath.setText("/")
        return
    
    def _uploadFile(self):
        path = self.view.ledFilePath.text()
        if os.path.exists(path):
            self.view.lblStatus.setText("Preparing...")
            self.view.pbrStatus.setValue(0)
            self._set_gui_upload_mode(True)

            def thread_has_finished():
                self._set_gui_upload_mode(False)

            def handle_thread_error( error):
                self.app.display_error_message(error)   

            self.thread = self.thread if self.thread else UploadThread()
            self.thread.path = path
            self.thread.status_update.connect(self.view.lblStatus.setText)
            self.thread.progress_update.connect(self.view.pbrStatus.setValue)
            self.thread.error_occurred.connect(partial(handle_thread_error))
            self.thread.upload_finished.connect(partial(thread_has_finished))
            self.thread.start()

        else:
            warnMsg = QMessageBox(QMessageBox.Warning, "Warning", "The local file or folder path is invalid.", QMessageBox.Ok)
            warnMsg.exec()
        return

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
    upload_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            for status_msg, progress in file_handler.upload(self.path):
                self.progress_update.emit(progress)
                self.status_update.emit(status_msg)
        except Exception as error:
            self.error_occurred.emit(error)
            self.status_update.emit("An error occurred. The upload had to be interrupted\n\n" + str(error))

        self.upload_finished.emit()
        self.progress_update.disconnect()
        self.status_update.disconnect()
        self.error_occurred.disconnect()
        self.upload_finished.disconnect()
    

