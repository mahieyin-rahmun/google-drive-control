import json
import os
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth, SCOPES

def get_folder_id_by_name(get_id_only=False):
	# get authorization if not authorized
	authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
	service = authorizer.authorize()

	folder_name = input("Please enter the folder name to search for: ")

	response = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
										spaces='drive',
										fields='nextPageToken, files(id, name)').execute()

	items = response.get('files', [])

	if not items:
		print('No files found.')
		return None
	else:
		item = items[0]
		if get_id_only:
			folder_id = f"'{item['id']}'"
			return folder_id
		else:
			return item

if __name__ == "__main__":
  	get_folder_id_by_name()