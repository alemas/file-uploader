import os.path

from functools import partial
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import file_handler

class UploadController:
    
    def __init__(self, view):
        super().__init__()
        self._view = view
        self._connectSignals()

        self._view.cbxCompress.setChecked(True)
        self._view.cbxCompress.setEnabled(False)
        self._view.cbxReplace.setEnabled(False)

        self._view.btnCancel.setEnabled(False)

    def _connectSignals(self):
        self._view.btnFilePath.clicked.connect(partial(self._chooseFilePath))
        self._view.btnFolderPath.clicked.connect(partial(self._chooseFolderPath))
        self._view.btnDrivePath.clicked.connect(partial(self._chooseDrivePath))
        self._view.btnUpload.clicked.connect(partial(self._uploadFile))

    def _chooseFilePath(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setWindowTitle("Choose File")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self._view.ledFilePath.setText(path)
        return

    def _chooseFolderPath(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setWindowTitle("Choose Folder")
        path = None
        if dialog.exec():
            path = dialog.selectedFiles()[0]
        if path:
            self._view.ledFilePath.setText(path)
        return

    def _chooseDrivePath(self):
        # self._view.ledDrivePath.setText("/")
        return
    
    def _uploadFile(self):
        path = self._view.ledFilePath.text()
        if os.path.exists(path):
            self._view.lblStatus.setText("Preparing...")
            self._view.pbrStatus.setValue(0)
            try:
                for status_msg, progress in file_handler.upload(path):
                    self._view.lblStatus.setText(status_msg)
                    self._view.pbrStatus.setValue(progress)
            except Exception as error:
                errorMsg = QMessageBox(QMessageBox.Critical, "Error", "An Error Ocurred\n\n" + str(error), QMessageBox.Ok)
                errorMsg.exec()
                self._view.lblStatus.setText("")
        else:
            errorMsg = QMessageBox(QMessageBox.Warning, "Warning", "The chosen file or folder doesn't seem to exist", QMessageBox.Ok)
            errorMsg.exec()
        
        return