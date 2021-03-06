import json
import os
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth, SCOPES
from search_folder import get_folder_id_by_name


def get_child_folders():
	"""
		This is a function that takes the name of the folder as input, and then finds the subfolders under that folder
	"""
	authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
	service = authorizer.authorize()

	folder_id = get_folder_id_by_name(get_id_only=True)
 
	if folder_id:
		print(folder_id)
						
		child_folders = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and {folder_id} in parents", 
														fields='nextPageToken, files(id, name)').execute()

		pprint(child_folders)
		return child_folders

	return None

if __name__ == "__main__":
	get_child_folders()