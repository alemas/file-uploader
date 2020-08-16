from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTableView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class ChooseGDriveFileWidget(QWidget):

    def __init__(self, tableView=QTableView()):
        super(QWidget, self).__init__()
        self._createGUI(tableView)

    def _createGUI(self, tableView):

        self.lblInfo = QLabel("")
        
        self.ledFilePath = QLineEdit()
        self.ledFilePath.setFixedHeight(24)
        self.ledFilePath.setReadOnly(True)

        self.btnBack = QPushButton()
        self.btnBack.setIcon(QIcon('img/up_arrow.png'))
        self.btnBack.setFixedSize(30, 26)
        self.btnCancel = QPushButton("Cancel")
        self.btnCancel.setFixedWidth(90)
        self.btnSelect = QPushButton("Select")
        self.btnSelect.setFixedWidth(90)

        self.tableView = tableView

        layout = QVBoxLayout()

        firstLayout = QHBoxLayout()
        firstLayout.addWidget(self.btnBack)
        firstLayout.addWidget(self.ledFilePath)

        layout.addLayout(firstLayout)

        layout.addWidget(self.tableView)

        secondLayout = QHBoxLayout()

        secondLayout.addWidget(self.btnSelect)
        secondLayout.addWidget(self.btnCancel)
        secondLayout.setAlignment(Qt.AlignRight)
        layout.addLayout(secondLayout)

        layout.addWidget(self.lblInfo)

        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)