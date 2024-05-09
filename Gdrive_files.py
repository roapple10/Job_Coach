from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
import io
import json
import os

# Specify the path to your credentials file
credentials_file_path = 'backend/cred/cred.json'

# Load the JSON credentials from the specified file
with open(credentials_file_path, 'r') as file:
    credz = json.load(file)

# Initialize the Google Drive service with the loaded credentials
credentials = service_account.Credentials.from_service_account_info(credz)
drive_service = build('drive', 'v3', credentials=credentials)

# Specify the folder ID of the Google Drive folder
folder_id = '1OG_JxejOOcXnOSjd4o3Yh5ogGRWjdfVt'

# Query to get the files in the specified folder
query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed=false"
response = drive_service.files().list(q=query, fields='files(id, name)').execute()
files = response.get('files', [])

# Download each file
for file in files:
    file_id = file['id']
    file_name = file['name']
    request = drive_service.files().get_media(fileId=file_id)
    data_directory ='data/'
    download_file_path = os.path.join(data_directory, file_name)  # This will use the same name as in Google Drive
    fh = io.FileIO(download_file_path, 'wb')

    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download of {file_name} {int(status.progress() * 100)}% complete.")

    fh.close()
    print(f"Download of {file_name} complete.")
