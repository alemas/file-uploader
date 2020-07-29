import os.path

from functools import partial
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

import views.upload_widget as upload_widget
import file_handler

class UploadController:
    
    def __init__(self):
        super().__init__()
        self.view = upload_widget.UploadWidget()
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
            try:
                for status_msg, progress in file_handler.upload(path):
                    self.view.lblStatus.setText(status_msg)
                    self.view.pbrStatus.setValue(progress)
            except Exception as error:
                errorMsg = QMessageBox(QMessageBox.Critical, "Error", "An Error Ocurred\n\n" + str(error), QMessageBox.Ok)
                errorMsg.exec()
                self.view.lblStatus.setText("")
        else:
            errorMsg = QMessageBox(QMessageBox.Warning, "Warning", "The chosen file or folder doesn't seem to exist", QMessageBox.Ok)
            errorMsg.exec()
        
        return