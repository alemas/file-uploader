import os.path

from googleapiclient.discovery import build
from googleapiclient.http.MediaFileUpload import MediaFileUpload

import credentials

drive = build('drive', 'v3', credentials=credentials.get())

def get_local_file(path):
    if os.path.exists(path):
        with open(path, "r") as file:
            return file
    return None

def upload(path):
    if os.path.exists(path):
        file_metadata = {"name": os.path.basename(path)}
        response = drive.files().create(body=file_metadata, media_body=path).execute()
        if response:
            print('Uploaded ' + path + ' succesfully')
    else:
        print("Couldn't find the specified file")
    return

def update(path, id):
    return
