import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout

app = QApplication(sys.argv)
window = QWidget()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Drive Uploader")
        self.setFixedSize(800, 600)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createUploadGui()

    def _createUploadGui(self):
        
        lblFilePath = QLabel("File/Folder to Upload:")
        lblDrivePath = QLabel("Google Drive Path:")

        ledFilePath = QLineEdit()
        ledDrivePath = QLineEdit()
        # ledFilePath.setAlignment(Qt.AlignLeft)
        ledDrivePath.setReadOnly(True)
        ledDrivePath.setText("/")

        btnFilePath = QPushButton("Choose Path")
        btnDrivePath = QPushButton("Choose Path")
        btnUpload = QPushButton("Upload")

        layout = QGridLayout()

        # File/Folder Upload
        layout.addWidget(lblFilePath, 0, 0)
        layout.addWidget(ledFilePath, 0, 1, 1, 4)
        layout.addWidget(btnFilePath, 0, 5)

        # Drive Path
        layout.addWidget(lblDrivePath, 1, 0)
        layout.addWidget(ledDrivePath, 1, 1, 1, 4)
        layout.addWidget(btnDrivePath, 1, 5)

        #Upload Button
        layout.addWidget(btnUpload, 2, 0)

        self.generalLayout.addLayout(layout)

        return