from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt

class UploadWidget(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self._createUploadGUI()

    def _createUploadGUI(self):
        
        lblFilePath = QLabel("Local Drive path:")
        lblDrivePath = QLabel("Google Drive Path:")
        lblStatus = QLabel("")

        self.lblStatus = lblStatus

        ledFilePath = QLineEdit()
        ledDrivePath = QLineEdit()
        ledDrivePath.setReadOnly(True)

        self.ledFilePath = ledFilePath
        self.ledDrivePath = ledDrivePath

        btnFilePath = QPushButton("Choose File")
        btnFolderPath = QPushButton("Choose Folder")
        btnDrivePath = QPushButton("Choose Path")
        btnUpload = QPushButton("Upload")
        btnCancel = QPushButton("Cancel")

        self.btnFilePath = btnFilePath
        self.btnFolderPath = btnFolderPath
        self.btnDrivePath = btnDrivePath
        self.btnUpload = btnUpload
        self.btnCancel = btnCancel

        grpSettings = QGroupBox("Upload Options")
        settingsLayout = QVBoxLayout()

        cbxCompress = QCheckBox("Compress to .zip")
        cbxReplace = QCheckBox("Replace existing files")

        self.cbxCompress = cbxCompress
        self.cbxReplace = cbxReplace

        settingsLayout.addWidget(cbxCompress)
        settingsLayout.addWidget(cbxReplace)
        grpSettings.setLayout(settingsLayout)

        pbrStatus = QProgressBar()

        self.pbrStatus = pbrStatus

        layout = QGridLayout()

        # File/Folder Path
        layout.addWidget(lblFilePath, 0, 0)
        layout.addWidget(ledFilePath, 0, 1, 1, 4)
        layout.addWidget(btnFilePath, 0, 5)
        layout.addWidget(btnFolderPath, 0, 6)

        # Drive Path
        layout.addWidget(lblDrivePath, 1, 0)
        layout.addWidget(ledDrivePath, 1, 1, 1, 4)
        layout.addWidget(btnDrivePath, 1, 5, 1, 2)

        # Checkboxes
        layout.addWidget(grpSettings, 2, 0, 1, 7)
        grpSettings.setFixedHeight(20 + settingsLayout.count()*30) 

        # Upload Button & Cancel Button
        layout.addWidget(btnUpload, 3, 0)
        layout.addWidget(btnCancel, 3, 1)

        # Progress Bar
        layout.addWidget(pbrStatus, 4, 0, 1, 7)

        # Status Label
        layout.addWidget(lblStatus, 5, 0, 1, 7, Qt.AlignTop)

        self.setLayout(layout)

