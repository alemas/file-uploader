import sys
import locale

from googleapiclient.discovery import build
from PyQt5.QtWidgets import QApplication

import credentials
# import file_handler
# import user_data_manager
import controllers.app_controller as app_controller

locale.setlocale(locale.LC_ALL, '') 

def main():
    q_application = QApplication(sys.argv)
    app = app_controller.AppController()
    sys.exit(q_application.exec())

    # file_handler.upload('data/really_big.zip')
    # list_files()
    # file_handler.get_gdrive_file('1jMcQBk1P9s5zST2u10iWg7DWQI39cZi_')
    # for file in file_handler.get_gdrive_file_children("'root'"):
    #     print(str(file.is_folder))

def list_files():
    creds = credentials.get()
    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, parents, mimeType)", q="'root' in parents").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) {2} {3}'.format(item['name'], item['id'], item['parents'], item['mimeType']))

if __name__ == '__main__':
    main()