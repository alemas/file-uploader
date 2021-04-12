import os.path
import requests
import json
import sys
import zipfile
import datetime
import sys

from pathlib import Path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests.exceptions import HTTPError

import credentials
import utils

# drive = build('drive', 'v3', credentials=credentials.get())
chunk_size = 1024*1024*20

DEBUG = True
ACCESS_TOKEN = credentials.get().token
API_KEY = None

with open('api_key.txt') as file:
    API_KEY = file.read()

class File:

    def __init__(self, id, name, is_folder=False, date_modified=None, size=0):
        super().__init__()
        self.id = id
        self.name = name
        self._date_modified = date_modified
        self.is_folder = is_folder
        self.size = size

    def get_formatted_date_modified(self):
        if self._date_modified:
            return self._date_modified.strftime("%x %X")
        return ""

    def get_formatted_size(self):
        return utils.format_file_size(self.size)

    def description(self):
        return "id = " + str(self.id) + "\nname = " + str(self.name) + "\ndate_modified = " + self.get_formatted_date_modified() + "\nis_folder = " + str(self.is_folder) + "\nsize = " + str(self.size)

def get_user_home_path():
    return str(Path.home())

def get_gdrive_file(id):
    creds = credentials.get()
    service = build('drive', 'v3', credentials=creds)
    # id = "'" + id + "'"
    result = service.files().get(fileId=id).execute()

    print(result)

    is_folder = result['mimeType'] == 'application/vnd.google-apps.folder'
    size = int(result['size']) if 'size' in result else 0
    date_modified = datetime.datetime.strptime(result['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ') if 'modifiedTime' in result else None
    return File(id=result['id'], name=result['name'], is_folder=is_folder, date_modified=date_modified, size=size)
    

def get_gdrive_file_children(id):
    creds = credentials.get()
    service = build('drive', 'v3', credentials=creds)
    
    page_token = None
    first_time = True
    files = []
    id = "'" + id + "'"
    while page_token or first_time:
        result = service.files().list(
            pageSize=100, 
            fields="nextPageToken, files(id, name, mimeType, size, trashed, modifiedTime)", 
            pageToken=page_token,
            q=id + " in parents"
        ).execute()

        page_token = result.get('nextPageToken')
        for item in result.get('files', []):
            if not item["trashed"]:
                is_folder = item['mimeType'] == 'application/vnd.google-apps.folder'
                size = int(item['size']) if 'size' in item else 0
                date_modified = datetime.datetime.strptime(item['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                files.append(File(id=item['id'], name=item['name'], is_folder=is_folder, date_modified=date_modified, size=size))
        
        first_time = False

    return files

def create_gdrive_folder(name, parents=None):
    creds = credentials.get()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    if parents:
        file_metadata['parents'] = parents

    file = service.files().create(body=file_metadata, fields="id")
    return File(id=file['id'], name=name, is_folder=true)

def zip_file(path):
    folder_name = os.path.basename(path)
    dest = "tmp/" + folder_name + ".zip"
    zipped = zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        files_zipped = 0
        for file in files:
            full_path = os.path.join(root, file)
            yield(dest, f"Zipping '{folder_name}'. Adding file '{file}' ({utils.format_file_size(os.path.getsize(full_path))})", int(files_zipped*100/len(files)))
            zipped.write(full_path, os.path.relpath(full_path, Path(root).parent))
            files_zipped += 1
    zipped.close()

def clear_temporary_files():
    for root, dirs, files in os.walk("./tmp"):
        for file in files:
            os.remove(os.path.join(root, file))
            print("removed " + file + " from 'tmp' folder")

def upload(path, parents=None):
    if os.path.exists(path):
        yield ("Starting Upload...", 0)
        file_metadata = {"name": os.path.basename(path)}
        if parents:
            file_metadata['parents'] = parents
        resumable_url = None
        file_size = os.path.getsize(path)

        # Sends the initial POST to start the upload
        print("\n===============>Sending initial POST")
        try:
            headers = _get_initial_request_headers(file_metadata, str(file_size))
            response = requests.post('https://www.googleapis.com/upload/drive/v3/files',
            params={'uploadType':'resumable', 'key':API_KEY},
            headers=headers,
            data=json.dumps(file_metadata))
            if DEBUG:
                print(f'Response:\nHEADERS\n{response.headers}\nBODY:\n{response.text}')
            resumable_url = response.headers['Location']

        except HTTPError as error:
            print(f'HTTP error occurred while starting the file upload: {error}')
            raise
        except Exception as error:
            print(f'An error occurred while starting the file upload: {error}')
            raise   

        # Starts the upload
        print("\n===============>Starting Upload")
        try:
            file = open(path, "rb")
            offset = 0
            for data in _read_file_chunks(file):
                yield ("Uploading " + file_metadata['name'] + "...", int(offset*100/file_size))
                data_size = sys.getsizeof(data)
                packet_offset = 17 if _get_os() == 'win32' else 33
                headers = _get_resumable_upload_headers(
                    str(data_size),
                    "bytes " + str(offset) + "-" + str(offset+data_size-1-packet_offset) + "/" + str(file_size))
                response = requests.put(resumable_url,
                headers=headers,
                data=data)
                
                if DEBUG:
                    print(f'Response:\nHEADERS\n{response.headers}\nBODY:\n{response.text}')
                print(response)
                
                offset += chunk_size

            file.close()
            yield (file_metadata['name'] + " succesfully uploaded!", 100)

        except HTTPError as error:
            file.close()
            print(f'HTTP error occurred while uploading the file: {error}')
            raise
        except Exception as error:
            file.close()
            print(f'An error occurred while uploading the file: {error}')
            raise
    else:
        print("Couldn't find the specified file")

def update(path, id):
    return

def _get_initial_request_headers(body, file_size):
    headers = {
        "Authorization":"Bearer " + ACCESS_TOKEN,
        "X-Upload-Content-Type": "application/octet-stream",
        "X-Upload-Content-Length": file_size,
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Length": str(sys.getsizeof(body))
    }
    return headers

def _get_resumable_upload_headers(size, range):
    headers = {
        "Content-Length": size,
        "Content-Range": range
    }
    return headers

def _read_file_chunks(file):
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield chunk

# Common values are 'win32', 'linux' and 'darwin' (MacOS)
def _get_os():
    return sys.platform