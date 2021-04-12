from enum import Enum

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor, QIcon

class FileHeader(Enum):
    Name = "Name"
    Size = "Size"
    DateModified = "Date Modified"
    Shared = "Shared"

class GDriveTableModel(QAbstractTableModel):
    def __init__(self, files=[]):
        super().__init__()
        self._headers = None
        self.load_files(files)  
    
    def load_files(self, files, headers=[FileHeader.Name, FileHeader.DateModified, FileHeader.Size]):
        self.data = []
        self._files = files
        self._headers = self._headers if self._headers else headers
        for file_index in range(len(files)):
            file = files[file_index]
            self.data.append([])
            for header_index in range(len(headers)):
                header = headers[header_index]
                if header == FileHeader.Name:
                    self.data[file_index].append(file.name)
                elif header == FileHeader.DateModified:
                    self.data[file_index].append(file.get_formatted_date_modified())
                elif header == FileHeader.Size:
                    self.data[file_index].append(file.get_formatted_size())
                elif header == FileHeader.Shared:
                    self.data[file_index].append(False)

    def refresh(self):
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0)-1, self.columnCount(0)-1))
        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft + Qt.AlignVCenter
        elif role == Qt.DecorationRole:
            if column == 0:
                return QIcon('img/folder.png') if self._files[row].is_folder else QIcon('img/file.png')
            else:
                return None
        elif role == Qt.DisplayRole:
            return self.data[row][column]

    
    def headerData(self, section, orientation, role):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft + Qt.AlignVCenter
        elif role == Qt.DisplayRole:
            return self._headers[section].value
    
    def rowCount(self, index):
        return len(self.data)

    def columnCount(self, index):
        return len(self._headers)