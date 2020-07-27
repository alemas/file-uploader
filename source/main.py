import sys

from googleapiclient.discovery import build
from PyQt5.QtWidgets import QApplication

import credentials
import file_handler
import views.main_window as main_window
import upload_controller

def main():
    app = QApplication(sys.argv)
    view = main_window.MainWindow()
    view.show()
    upload_controller.UploadController(view=view)

    sys.exit(app.exec())

    # file_handler.upload('data/really_big.zip')

def list_files():
    creds = credentials.get()
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()