import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Auth import Auth

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file', 
          'https://www.googleapis.com/auth/drive.metadata']

def main():
  authorizer = Auth(SCOPES, os.path.join(os.path.abspath('.'), './credentials'), os.path.join(os.path.abspath('.'), './pickled_creds'))
  service = authorizer.authorize()
  
  # Call the Drive v3 API
  results = service.files().list(fields="nextPageToken, files(id, name)").execute()
  
  items = results.get('files', [])

  if not items:
      print('No files found.')
  else:
      print('Files:')
      for item in items:
          print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
  main()