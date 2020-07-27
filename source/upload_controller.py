from functools import partial
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog

class UploadController:
    
    def __init__(self, view):
        super().__init__()
        self._view = view
        self._connectSignals()

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
        return