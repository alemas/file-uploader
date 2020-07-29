import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTabWidget

app = QApplication(sys.argv)
window = QWidget()

class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Drive Uploader")
        self.setFixedSize(650, 400)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        self._createTabs()
        self.show()

    def _createTabs(self):
        self.tabs = QTabWidget()
        self.generalLayout.addWidget(self.tabs)

    def addTab(self, tab, name):
        self.tabs.addTab(tab, name)


        