import sys

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QCheckBox
from PyQt5 import QtCore

class FileDialog(QFileDialog):
    def __init__(self, parent=None):
        super(FileDialog, self).__init__()
        self.setOption(self.DontUseNativeDialog, True)
        self._startUI()

    def _startUI(self):
        checkbox = QCheckBox("Select Folder")
        checkbox.stateChanged.connect(self.toggleFilesFolders)
        self.layout().addWidget(checkbox)

    def toggleFilesFolders(self, state):
        if state == QtCore.Qt.Checked:
            self.setFileMode(self.Directory)
        else:
            self.setFileMode(self.ExistingFile)