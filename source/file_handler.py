import os.path
import requests
import json
import sys

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
# from googleapiclient.errors import HttpError
from requests.exceptions import HTTPError

import credentials

drive = build('drive', 'v3', credentials=credentials.get())
chunk_size = 1024*1024*5

ACCESS_TOKEN = credentials.get().token
API_KEY = None

with open('api_key.txt') as file:
    API_KEY = file.read()

# def get_local_file(path):
#     if os.path.exists(path):
#         with open(path, "r") as file:
#             return file
#     return None

def upload(path):
    if os.path.exists(path):
        yield ("Starting Upload...", 0)
        file_metadata = {"name": os.path.basename(path)}
        resumable_url = None
        file_size = os.path.getsize(path)

        # Sends the initial POST to start the upload
        try:
            headers = __get_initial_request_headers(file_metadata, str(file_size))
            response = requests.post('https://www.googleapis.com/upload/drive/v3/files',
            params={'uploadType':'resumable', 'key':API_KEY},
            headers=headers,
            data=json.dumps(file_metadata))

            # print(response.request.path_url)
            # print(response.request.headers)
            # print(response.request.body)
            # print(response.headers)

            resumable_url = response.headers['Location']

        except HTTPError as error:
            print(f'HTTP error occurred while starting the file upload: {http_err}')
            raise

        # Starts the upload
        try:
            file = open(path, "rb")
            offset = 0
            for data in __read_file_chunks(file):
                yield ("Uploading '" + file_metadata['name'] + "'...", offset)
                data_size = sys.getsizeof(data)
                headers = __get_resumable_upload_headers(
                    str(data_size),
                    "bytes " + str(offset) + "-" + str(offset+data_size-1-17) + "/" + str(file_size))
                response = requests.put(resumable_url,
                headers=headers,
                data=data)

                print(response)
                
                offset += chunk_size
        except HTTPError as error:
            print(f'HTTP error occurred while uploading file: {http_err}')
            raise
        yield ("Uploaded '" + file_metadata['name'] + "' succesfully!", 100)
    else:
        print("Couldn't find the specified file")
    return

def update(path, id):
    return

def __get_initial_request_headers(body, file_size):
    headers = {
        "Authorization":"Bearer " + ACCESS_TOKEN,
        "X-Upload-Content-Type": "application/octet-stream",
        "X-Upload-Content-Length": file_size,
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Length": str(sys.getsizeof(body))
    }
    return headers

def __get_resumable_upload_headers(size, range):
    headers = {
        "Content-Length": size,
        "Content-Range": range
    }
    return headers

def __read_file_chunks(file):
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        yield chunk